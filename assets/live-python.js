/* Editor Python interactivo: ejecución en Web Worker con Pyodide (WebAssembly).
 * No transmite código a ningún servidor: Pyodide se descarga de CDN para ejecutar localmente.
 */
(() => {
'use strict';
const CDNPATH = 'https://cdn.jsdelivr.net/pyodide/v0.29.2/full/';
const LOAD_TIMEOUT = 90000;
const EXEC_TIMEOUT = 20000;
const WORKER_SOURCE = `
let runtime;
self.onmessage = async (event) => {
  const { id, code } = event.data || {};
  if (!id) return;
  const messages = [];
  try {
    if (!runtime) {
      importScripts('${CDNPATH}pyodide.js');
      runtime = await loadPyodide({ indexURL:'${CDNPATH}' });
    }
    self.postMessage({ id, stage:'ready' });
    runtime.setStdout({ batched: (line) => messages.push(line) });
    runtime.setStderr({ batched: (line) => messages.push(line) });
    const result = await runtime.runPythonAsync(code);
    if (result !== undefined && result !== null && String(result) !== 'None') {
      messages.push(String(result));
    }
    if (result && typeof result.destroy === 'function') result.destroy();
    self.postMessage({ id, output:messages.join('\\n'), ok:true });
  } catch (error) {
    self.postMessage({ id, output:messages.join('\\n'), error: String(error), ok:false });
  }
};
`;
let runner=null;
let pending=null;
let requestId=0;
function stopRunner() {
  if (runner) runner.terminate();
  runner=null;
  if (pending) {
    clearTimeout(pending.timeout);
    pending.reject(Error('La ejecución se detuvo o superó el tiempo permitido. Reiniciamos el intérprete.'));
    pending=null;
  }
}
function ensureRunner() {
  if (runner) return runner;
  const url=URL.createObjectURL(new Blob([WORKER_SOURCE], {type:'text/javascript'}));
  try { runner=new Worker(url); } finally { URL.revokeObjectURL(url); }
  runner.onmessage = (event) => {
    if (!pending || pending.id !== event.data.id) return;
    if (event.data.stage === 'ready') {
      clearTimeout(pending.timeout);
      pending.timeout=setTimeout(stopRunner,EXEC_TIMEOUT);
      return;
    }
    const {resolve,timeout}=pending;
    clearTimeout(timeout);pending=null;
    resolve(event.data);
  };
  runner.onerror = () => stopRunner();
  runner.onmessageerror = () => stopRunner();
  return runner;
}
function execute(code) {
  if (pending) return Promise.reject(Error('Ya hay una celda ejecutándose.'));
  return new Promise((resolve,reject) => {
    try {
      const worker=ensureRunner();
      const id=++requestId;
      pending={id,resolve,reject,timeout:setTimeout(stopRunner,LOAD_TIMEOUT)};
      worker.postMessage({id,code});
    } catch (error) {pending=null;reject(error);}
  });
}
// Motor compartido con «Mis cuadernos» (cuadernos.html).
window.SICPython={execute,stop:stopRunner};
function h(tag,attrs={},txt='') {
  const node=document.createElement(tag);
  for(const [key,value] of Object.entries(attrs)) node.setAttribute(key,value);
  if(txt) node.textContent=txt;
  return node;
}
const lesson = (location.pathname.split('/').pop() || 'clase') ;
const cells = [...document.querySelectorAll('.code-box')];
let count=0;
for (let i=0;i<cells.length;i++) {
  const box=cells[i];
  const originalCode=box.querySelector('.highlight pre');
  if (!originalCode) continue;
  count++;
  const original=originalCode.textContent.replace(/\n$/, '');
  const key='sic:pyodide:v1:'+lesson+':'+i;
  const hidden=box.querySelector('.highlight');
  if(hidden) hidden.style.display='none';
  const editor=h('textarea',{'class':'py-live-editor','aria-label':'Código Python editable, celda '+(i+1),'spellcheck':'false','autocomplete':'off','autocorrect':'off','autocapitalize':'off'});
  editor.value=localStorageSafeRead(key) ?? original;
  editor.rows=Math.min(Math.max(editor.value.split('\n').length+1,3),12);
  const actions=h('div',{'class':'py-live-actions'});
  const run=h('button',{'type':'button','class':'py-live-btn run'},'▶ Ejecutar');
  const reset=h('button',{'type':'button','class':'py-live-btn'},'↺ Restaurar');
  const shortcut=h('span',{'class':'py-live-shortcut'},'Ctrl/Cmd + Enter');
  actions.append(run,reset,shortcut);
  box.append(editor,actions);
  const output=h('div',{'class':'py-live-result','role':'status','aria-live':'polite'});
  output.hidden=true;
  const outputHead=h('div',{'class':'py-live-result-head'},'SALIDA REAL');
  const outputText=h('pre');
  output.append(outputHead,outputText);
  box.insertAdjacentElement('afterend',output);
  const expected=box.parentElement.querySelector('.output-box');
  if(expected) {
    const details=h('details',{'class':'py-live-reference'});
    details.append(h('summary',{},'Comparar con la salida esperada'));
    details.append(expected);
    output.insertAdjacentElement('afterend',details);
  }
  function autoSave() { try{localStorage.setItem(key,editor.value)}catch(_){ /* privacidad o file:// */ } }
  editor.addEventListener('input',autoSave);
  editor.addEventListener('keydown',e=>{
    if(e.key==='Tab') {
      e.preventDefault();
      const start=editor.selectionStart,end=editor.selectionEnd;
      editor.setRangeText('    ',start,end,'end');autoSave();
    }
    if(e.key==='Enter' && (e.ctrlKey || e.metaKey)) {e.preventDefault();run.click();}
  });
  reset.addEventListener('click',()=>{
    editor.value=original;
    autoSave();
    output.hidden=true;
    output.classList.remove('has-error');
    editor.focus();
  });
  run.addEventListener('click',async()=>{
    run.disabled=true;
    run.textContent='⌛ Ejecutando…';
    output.hidden=false;
    output.classList.remove('has-error');
    outputHead.textContent='SALIDA REAL · ejecutando Python';
    outputText.textContent='La primera ejecución necesita descargar el intérprete Python. Puede tardar un poco y requiere Internet.';
    try{
      const r=await execute(editor.value);
      output.classList.toggle('has-error', !r.ok);
      outputHead.textContent=r.ok?'SALIDA REAL':'ERROR DE PYTHON';
      outputText.textContent=r.ok?(r.output||'(El programa terminó sin imprimir nada)'):[r.output,r.error].filter(Boolean).join('\n');
    } catch(e){
      output.classList.add('has-error');
      outputHead.textContent='NO SE PUDO EJECUTAR';
      outputText.textContent=e.message+'\nVerifica tu conexión a Internet e inténtalo de nuevo.';
    } finally {
      run.disabled=false;
      run.textContent='▶ Ejecutar';
    }
  });
}
function localStorageSafeRead(key){try{return localStorage.getItem(key)}catch(_){return null}}
// Permite detener bucles bloqueados reiniciando el intérprete.
const topNav = document.querySelector('nav.top .nav-right');
if(topNav && count){
  const btn=h('button',{'type':'button','class':'nav-btn','title':'Detener un programa de Python bloqueado'},'■ Detener Python');
  btn.addEventListener('click',stopRunner);
  topNav.prepend(btn);
  // Abre un cuaderno nuevo ligado a esta clase y al tema de la diapositiva actual.
  const nb=h('button',{'type':'button','class':'nav-btn','title':'Abrir un cuaderno nuevo para practicar este tema'},'＋ Cuaderno');
  nb.addEventListener('click',()=>{
    const active=document.querySelector('.slide.active');
    const tema=(active?.querySelector('h2,h1')?.textContent || '').trim();
    const params=new URLSearchParams({nuevo:'1',clase:lesson.replace(/\.html$/,'')});
    if(tema) params.set('tema',tema.slice(0,120));
    window.open('cuadernos.html?'+params.toString(),'_blank','noopener');
  });
  topNav.prepend(nb);
}
})();
