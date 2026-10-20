/* «Mis cuadernos»: cuadernos en diapositivas (notas + código + salida) organizados en carpetas.
 * Guarda en Supabase cuando hay sesión iniciada; si no, en el navegador (localStorage).
 * Python se ejecuta con el motor de live-python.js (window.SICPython).
 */
(() => {
'use strict';
const $ = (id) => document.getElementById(id);
const uid = () => (crypto.randomUUID ? crypto.randomUUID() : 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
  const r = Math.random() * 16 | 0; return (c === 'x' ? r : (r & 3 | 8)).toString(16);
}));
const now = () => new Date().toISOString();
// Cada clase vive en la carpeta «Semana N / Clase N». Al agregar clases nuevas, añádelas aquí.
const CLASES = {
  clase_1: { nombre: 'Clase 1', semana: 'Semana 1' },
  clase_2: { nombre: 'Clase 2', semana: 'Semana 1' }
};
const nombreClase = (c) => CLASES[c]?.nombre || c.replace(/_/g, ' ').replace(/^./, m => m.toUpperCase());

function safeGet(key) { try { return localStorage.getItem(key); } catch (_) { return null; } }
function safeSet(key, value) { try { localStorage.setItem(key, value); } catch (_) { /* privado o lleno */ } }
function h(tag, attrs = {}, txt = '') {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  if (txt) node.textContent = txt;
  return node;
}
function nuevaDiapositiva(titulo = '') {
  return { id: uid(), titulo, notas: '', codigo: '', salida: null, ok: true };
}

// ---------- Almacenamiento en el navegador ----------
const LOCAL_KEY = 'sic:cuadernos:v1';
const localStore = {
  nombre: 'local',
  read() {
    try {
      const d = JSON.parse(localStorage.getItem(LOCAL_KEY));
      if (d && Array.isArray(d.carpetas) && Array.isArray(d.cuadernos)) return d;
    } catch (_) { /* vacío o ilegible */ }
    return { carpetas: [], cuadernos: [] };
  },
  write(d) {
    try { localStorage.setItem(LOCAL_KEY, JSON.stringify(d)); }
    catch (_) { throw new Error('el navegador no permite guardar (modo privado o almacenamiento lleno)'); }
  },
  async listFolders() { return this.read().carpetas; },
  async listNotebooks() { return this.read().cuadernos.map(({ diapositivas, ...meta }) => meta); },
  async getNotebook(id) { return structuredClone(this.read().cuadernos.find(c => c.id === id) || null); },
  async saveFolder(f) {
    const d = this.read(); const i = d.carpetas.findIndex(x => x.id === f.id);
    if (i < 0) d.carpetas.push(f); else d.carpetas[i] = f;
    this.write(d);
  },
  async deleteFolder(id) {
    const d = this.read(); const borrar = new Set([id]);
    for (let changed = true; changed;) {
      changed = false;
      for (const c of d.carpetas) if (c.parent_id && borrar.has(c.parent_id) && !borrar.has(c.id)) { borrar.add(c.id); changed = true; }
    }
    d.carpetas = d.carpetas.filter(c => !borrar.has(c.id));
    d.cuadernos.forEach(n => { if (borrar.has(n.carpeta_id)) n.carpeta_id = null; });
    this.write(d);
  },
  async saveNotebook(nb) {
    const d = this.read(); const i = d.cuadernos.findIndex(x => x.id === nb.id);
    if (i < 0) d.cuadernos.push(structuredClone(nb)); else d.cuadernos[i] = structuredClone(nb);
    this.write(d);
  },
  async deleteNotebook(id) { const d = this.read(); d.cuadernos = d.cuadernos.filter(c => c.id !== id); this.write(d); },
  count() { const d = this.read(); return d.carpetas.length + d.cuadernos.length; },
  clear() { try { localStorage.removeItem(LOCAL_KEY); } catch (_) { /* nada que borrar */ } }
};

// ---------- Almacenamiento en Supabase ----------
function supabaseStore(client) {
  const ok = ({ data, error }) => { if (error) throw new Error(error.message); return data; };
  return {
    nombre: 'nube',
    async listFolders() { return ok(await client.from('carpetas').select('id,parent_id,nombre,creado').order('nombre')); },
    async listNotebooks() { return ok(await client.from('cuadernos').select('id,carpeta_id,titulo,clase,creado,actualizado').order('actualizado', { ascending: false })); },
    async getNotebook(id) { return ok(await client.from('cuadernos').select('id,carpeta_id,titulo,clase,diapositivas,creado,actualizado').eq('id', id).maybeSingle()); },
    async saveFolder(f) { ok(await client.from('carpetas').upsert({ id: f.id, parent_id: f.parent_id, nombre: f.nombre, creado: f.creado })); },
    async deleteFolder(id) { ok(await client.from('carpetas').delete().eq('id', id)); },
    async saveNotebook(nb) {
      ok(await client.from('cuadernos').upsert({ id: nb.id, carpeta_id: nb.carpeta_id, titulo: nb.titulo, clase: nb.clase,
        diapositivas: nb.diapositivas, creado: nb.creado, actualizado: nb.actualizado }));
    },
    async deleteNotebook(id) { ok(await client.from('cuadernos').delete().eq('id', id)); }
  };
}

// ---------- Estado ----------
let store = localStore, client = null, session = null;
let folders = [], notebooks = [];
let nb = null, idx = 0, selectedFolder = null, running = false;
let saveTimer = null, dirty = false, saving = Promise.resolve();
const collapsed = new Set(JSON.parse(safeGet('sic:cuadernos:colapsadas') || '[]'));
const el = {
  tree: $('tree'), account: $('account'), empty: $('empty'), editor: $('editor'), loadError: $('load-error'),
  nbTitle: $('nb-title'), status: $('save-status'), folderSelect: $('folder-select'), overlineFolder: $('overline-folder'),
  slideTitle: $('slide-title'), notes: $('notes'), code: $('code'), run: $('run'), runAll: $('run-all'),
  output: $('output'), outputHead: $('output-head'), outputText: $('output-text'),
  counter: $('counter'), progress: $('progress'), back: $('back'), next: $('next'),
  moveLeft: $('move-left'), moveRight: $('move-right'), side: $('side'), sideBackdrop: $('side-backdrop'), sideToggle: $('side-toggle')
};

function setStatus(text, error = false) { el.status.textContent = text; el.status.classList.toggle('error', error); }
function folderPath(id) {
  const parts = []; const seen = new Set();
  for (let f = folders.find(x => x.id === id); f && !seen.has(f.id); f = folders.find(x => x.id === f.parent_id)) { seen.add(f.id); parts.unshift(f.nombre); }
  return parts.join(' / ');
}

// ---------- Diálogos propios (algunos navegadores bloquean prompt/confirm sin avisar) ----------
const modal = { root: $('modal'), title: $('modal-title'), text: $('modal-text'), input: $('modal-input'), ok: $('modal-ok'), cancel: $('modal-cancel') };
let modalResolve = null;
function openModal({ title, text = '', input = null, okLabel = 'Aceptar', danger = false, cancel = true }) {
  if (modalResolve) closeModal(null);
  modal.title.textContent = title;
  modal.text.textContent = text; modal.text.hidden = !text;
  modal.input.hidden = input === null; modal.input.value = input ?? '';
  modal.ok.textContent = okLabel; modal.ok.classList.toggle('danger', danger);
  modal.cancel.hidden = !cancel;
  modal.root.hidden = false;
  if (input === null) modal.ok.focus(); else { modal.input.focus(); modal.input.select(); }
  return new Promise(resolve => { modalResolve = resolve; });
}
function closeModal(value) {
  modal.root.hidden = true;
  const resolve = modalResolve; modalResolve = null;
  if (resolve) resolve(value);
}
modal.ok.addEventListener('click', () => closeModal(modal.input.hidden ? true : modal.input.value));
modal.cancel.addEventListener('click', () => closeModal(null));
modal.root.addEventListener('click', (e) => { if (e.target === modal.root) closeModal(null); });
modal.root.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') { e.stopPropagation(); closeModal(null); }
  if (e.key === 'Enter' && e.target === modal.input) { e.preventDefault(); modal.ok.click(); }
});
const askText = (title, value = '') => openModal({ title, input: value, okLabel: 'Guardar' });
const askConfirm = (title, text, okLabel = 'Eliminar', danger = true) => openModal({ title, text, okLabel, danger }).then(Boolean);
const notify = (title, text = '') => openModal({ title, text, cancel: false });

// ---------- Guardado ----------
function scheduleSave() {
  if (!nb) return;
  dirty = true; setStatus('Guardando…');
  clearTimeout(saveTimer);
  saveTimer = setTimeout(flush, 700);
}
function flush() {
  clearTimeout(saveTimer);
  if (!dirty || !nb) return saving;
  dirty = false;
  const target = store, snapshot = structuredClone(nb);
  snapshot.actualizado = nb.actualizado = now();
  saving = saving.then(() => target.saveNotebook(snapshot)).then(() => {
    const meta = notebooks.find(n => n.id === snapshot.id);
    if (meta) Object.assign(meta, { titulo: snapshot.titulo, carpeta_id: snapshot.carpeta_id, actualizado: snapshot.actualizado });
    if (!dirty) setStatus(target.nombre === 'nube' ? 'Guardado en la nube ✓' : 'Guardado en este navegador ✓');
  }).catch(err => { dirty = true; setStatus('No se pudo guardar: ' + err.message, true); });
  return saving;
}
window.addEventListener('beforeunload', (e) => {
  if (dirty) { flush(); if (store.nombre === 'nube') { e.preventDefault(); e.returnValue = ''; } }
});

// ---------- Árbol de carpetas ----------
function renderTree() {
  el.tree.textContent = '';
  const children = new Map();
  const ids = new Set(folders.map(f => f.id));
  for (const f of folders) {
    const parent = f.parent_id && ids.has(f.parent_id) ? f.parent_id : null;
    if (!children.has(parent)) children.set(parent, []);
    children.get(parent).push(f);
  }
  const byFolder = new Map();
  for (const n of notebooks) {
    const key = n.carpeta_id && ids.has(n.carpeta_id) ? n.carpeta_id : null;
    if (!byFolder.has(key)) byFolder.set(key, []);
    byFolder.get(key).push(n);
  }
  const sortName = (a, b) => a.nombre.localeCompare(b.nombre, 'es', { numeric: true });
  const sortNb = (a, b) => (a.titulo || '').localeCompare(b.titulo || '', 'es', { numeric: true });

  const addFolder = (f, depth) => {
    const open = !collapsed.has(f.id);
    const row = h('div', { class: 'row folder' + (selectedFolder === f.id ? ' selected' : ''), role: 'treeitem', 'aria-expanded': String(open) });
    row.style.setProperty('--depth', depth);
    const main = h('button', { type: 'button', class: 'row-main', title: folderPath(f.id) });
    main.append(h('span', { class: 'caret' }, open ? '▾' : '▸'), h('span', { class: 'row-icon' }, '📁'), h('span', { class: 'name' }, f.nombre));
    main.addEventListener('click', () => {
      if (selectedFolder === f.id || !open) { open ? collapsed.add(f.id) : collapsed.delete(f.id); safeSet('sic:cuadernos:colapsadas', JSON.stringify([...collapsed])); }
      selectedFolder = f.id; renderTree();
    });
    const actions = h('div', { class: 'row-actions' });
    const addSub = h('button', { type: 'button', title: 'Nueva subcarpeta', 'aria-label': 'Nueva subcarpeta en ' + f.nombre }, '＋📁');
    addSub.addEventListener('click', () => createFolder(f.id));
    const addNb = h('button', { type: 'button', title: 'Nuevo cuaderno aquí', 'aria-label': 'Nuevo cuaderno en ' + f.nombre }, '＋📄');
    addNb.addEventListener('click', () => createNotebook({ carpeta_id: f.id }));
    const ren = h('button', { type: 'button', title: 'Renombrar', 'aria-label': 'Renombrar ' + f.nombre }, '✎');
    ren.addEventListener('click', () => renameFolder(f));
    const del = h('button', { type: 'button', title: 'Eliminar carpeta', 'aria-label': 'Eliminar ' + f.nombre }, '🗑');
    del.addEventListener('click', () => deleteFolder(f));
    actions.append(addSub, addNb, ren, del);
    row.append(main, actions);
    el.tree.append(row);
    if (!open) return;
    for (const c of (children.get(f.id) || []).sort(sortName)) addFolder(c, depth + 1);
    for (const n of (byFolder.get(f.id) || []).sort(sortNb)) addNotebookRow(n, depth + 1);
  };
  const addNotebookRow = (n, depth) => {
    const row = h('div', { class: 'row notebook' + (nb && nb.id === n.id ? ' current' : ''), role: 'treeitem' });
    row.style.setProperty('--depth', depth);
    const main = h('button', { type: 'button', class: 'row-main', title: n.titulo || 'Cuaderno sin título' });
    main.append(h('span', { class: 'caret' }), h('span', { class: 'row-icon' }, '📄'), h('span', { class: 'name' }, n.titulo || 'Cuaderno sin título'));
    main.addEventListener('click', () => { openNotebook(n.id); closeSide(); });
    row.append(main);
    el.tree.append(row);
  };

  for (const f of (children.get(null) || []).sort(sortName)) addFolder(f, 0);
  const sueltos = (byFolder.get(null) || []).sort(sortNb);
  if (sueltos.length) {
    el.tree.append(h('div', { class: 'tree-section' }, 'SIN CARPETA'));
    for (const n of sueltos) addNotebookRow(n, 0);
  }
  if (!folders.length && !notebooks.length) {
    el.tree.append(h('div', { class: 'tree-empty' }, 'Aún no tienes carpetas ni cuadernos. Crea una carpeta por clase o abre un cuaderno desde una presentación.'));
  }
  renderFolderSelect();
}
function renderFolderSelect() {
  el.folderSelect.textContent = '';
  el.folderSelect.append(h('option', { value: '' }, 'Sin carpeta'));
  const options = folders.map(f => ({ id: f.id, path: folderPath(f.id) })).sort((a, b) => a.path.localeCompare(b.path, 'es', { numeric: true }));
  for (const o of options) el.folderSelect.append(h('option', { value: o.id }, o.path));
  if (nb) el.folderSelect.value = nb.carpeta_id || '';
}

async function createFolder(parentId = null, nombre = null) {
  nombre = nombre ?? await askText(parentId ? 'Nombre de la subcarpeta' : 'Nombre de la carpeta');
  if (!nombre || !nombre.trim()) return null;
  const f = { id: uid(), parent_id: parentId, nombre: nombre.trim().slice(0, 120), creado: now() };
  try {
    await store.saveFolder(f);
    folders.push(f); collapsed.delete(parentId); selectedFolder = f.id; renderTree();
    return f;
  } catch (err) { notify('No se pudo crear la carpeta', err.message); return null; }
}
async function renameFolder(f) {
  const nombre = await askText('Nuevo nombre de la carpeta', f.nombre);
  if (!nombre || !nombre.trim() || nombre.trim() === f.nombre) return;
  const updated = { ...f, nombre: nombre.trim().slice(0, 120) };
  try { await store.saveFolder(updated); Object.assign(f, updated); renderTree(); updateOverline(); }
  catch (err) { notify('No se pudo renombrar', err.message); }
}
async function deleteFolder(f) {
  if (!await askConfirm(`¿Eliminar la carpeta «${f.nombre}»?`, 'También se borran sus subcarpetas. Los cuadernos que contenga no se borran: pasan a «Sin carpeta».')) return;
  await flush();
  try {
    await store.deleteFolder(f.id);
    await reloadLists();
    if (nb && nb.carpeta_id && !folders.some(x => x.id === nb.carpeta_id)) nb.carpeta_id = null;
    if (selectedFolder && !folders.some(x => x.id === selectedFolder)) selectedFolder = null;
    renderTree(); updateOverline();
  } catch (err) { notify('No se pudo eliminar la carpeta', err.message); }
}

// ---------- Cuadernos ----------
async function createNotebook({ carpeta_id = selectedFolder, titulo = 'Cuaderno sin título', clase = null, tema = '' } = {}) {
  await flush();
  const t = now();
  const nuevo = { id: uid(), carpeta_id: carpeta_id || null, titulo, clase, diapositivas: [nuevaDiapositiva(tema)], creado: t, actualizado: t };
  try {
    await store.saveNotebook(nuevo);
    notebooks.push({ id: nuevo.id, carpeta_id: nuevo.carpeta_id, titulo, clase, creado: t, actualizado: t });
    if (carpeta_id) collapsed.delete(carpeta_id);
    showNotebook(nuevo, 0);
    closeSide();
    if (tema) el.notes.focus(); else el.nbTitle.select();
  } catch (err) { notify('No se pudo crear el cuaderno', err.message); }
}
async function openNotebook(id) {
  if (nb && nb.id === id) return;
  await flush();
  try {
    const data = await store.getNotebook(id);
    if (!data) { notify('Ese cuaderno ya no existe'); await reloadLists(); return; }
    if (!Array.isArray(data.diapositivas) || !data.diapositivas.length) data.diapositivas = [nuevaDiapositiva()];
    const pos = Number(safeGet('sic:cuadernos:pos:' + id)) || 0;
    showNotebook(data, pos);
  } catch (err) { notify('No se pudo abrir el cuaderno', err.message); }
}
function showNotebook(data, pos) {
  nb = data;
  safeSet('sic:cuadernos:ultimo', nb.id);
  el.empty.hidden = true; el.editor.hidden = false;
  el.nbTitle.disabled = false; el.nbTitle.value = nb.titulo || '';
  document.title = (nb.titulo || 'Cuaderno') + ' | Mis cuadernos';
  setStatus(store.nombre === 'nube' ? 'En la nube' : 'En este navegador');
  renderTree(); updateOverline();
  show(pos);
}
function closeNotebook() {
  nb = null; idx = 0;
  el.editor.hidden = true; el.empty.hidden = false;
  el.nbTitle.value = ''; el.nbTitle.disabled = true; setStatus('');
  document.title = 'Mis cuadernos | Python · Samsung Innovation Campus';
  renderTree();
}
async function deleteNotebook() {
  if (!nb || !await askConfirm(`¿Eliminar el cuaderno «${nb.titulo || 'sin título'}»?`, 'Se borran todas sus diapositivas. No se puede deshacer.')) return;
  clearTimeout(saveTimer); dirty = false;
  const id = nb.id;
  try {
    await saving;
    await store.deleteNotebook(id);
    notebooks = notebooks.filter(n => n.id !== id);
    closeNotebook();
  } catch (err) { notify('No se pudo eliminar el cuaderno', err.message); }
}
function updateOverline() {
  if (!nb) return;
  el.overlineFolder.textContent = (nb.carpeta_id && folderPath(nb.carpeta_id)) || 'SIN CARPETA';
}

// ---------- Diapositivas ----------
const slide = () => nb.diapositivas[idx];
const notesMin = () => (matchMedia('(max-width: 640px)').matches ? 110 : 180);
function autoGrow(t, min) {
  if (!t.offsetWidth) return; // oculto: la altura se calcula al volver a mostrarse
  t.style.height = 'auto'; t.style.height = Math.max(t.scrollHeight + 2, min) + 'px';
}
function fitEditors() { if (nb) { autoGrow(el.notes, notesMin()); autoGrow(el.code, 170); } }
function show(i) {
  if (!nb) return;
  idx = Math.max(0, Math.min(i, nb.diapositivas.length - 1));
  const s = slide(), n = nb.diapositivas.length;
  el.slideTitle.value = s.titulo || '';
  el.notes.value = s.notas || '';
  el.code.value = s.codigo || '';
  renderOutput(s);
  el.counter.textContent = `${String(idx + 1).padStart(2, '0')} / ${String(n).padStart(2, '0')}`;
  el.progress.style.width = ((idx + 1) / n * 100) + '%';
  el.back.disabled = idx === 0; el.next.disabled = idx === n - 1;
  el.moveLeft.disabled = idx === 0; el.moveRight.disabled = idx === n - 1;
  fitEditors();
  safeSet('sic:cuadernos:pos:' + nb.id, String(idx));
}
function renderOutput(s) {
  if (s.salida === null || s.salida === undefined) { el.output.hidden = true; return; }
  el.output.hidden = false;
  el.output.classList.toggle('has-error', !s.ok);
  el.outputHead.textContent = s.ok ? 'SALIDA' : 'ERROR DE PYTHON';
  el.outputText.textContent = s.salida || '(El programa terminó sin imprimir nada)';
}
function addSlide() {
  nb.diapositivas.splice(idx + 1, 0, nuevaDiapositiva());
  scheduleSave(); show(idx + 1); el.slideTitle.focus();
}
function duplicateSlide() {
  const copy = { ...structuredClone(slide()), id: uid() };
  copy.titulo = copy.titulo ? copy.titulo + ' (copia)' : '';
  nb.diapositivas.splice(idx + 1, 0, copy);
  scheduleSave(); show(idx + 1);
}
function moveSlide(delta) {
  const j = idx + delta;
  if (j < 0 || j >= nb.diapositivas.length) return;
  const list = nb.diapositivas; [list[idx], list[j]] = [list[j], list[idx]];
  scheduleSave(); show(j);
}
async function deleteSlide() {
  const s = slide();
  const hasContent = s.titulo || s.notas || s.codigo;
  if (hasContent && !await askConfirm(`¿Eliminar la diapositiva ${idx + 1}${s.titulo ? ' «' + s.titulo + '»' : ''}?`, 'Se borran su título, notas, código y salida.')) return;
  if (nb.diapositivas.length === 1) nb.diapositivas[0] = nuevaDiapositiva();
  else nb.diapositivas.splice(idx, 1);
  scheduleSave(); show(idx);
}

// ---------- Ejecución ----------
function setRunning(state) {
  running = state;
  el.run.disabled = state; el.runAll.disabled = state;
  el.run.textContent = state ? '⌛ Ejecutando…' : '▶ Ejecutar';
}
// Quita las líneas internas de Pyodide y deja solo las de tu código.
function cleanTraceback(error) {
  const text = String(error || '').replace(/^PythonError:\s*/, '');
  const start = text.indexOf('  File "<exec>"');
  return start < 0 ? text : 'Traceback (most recent call last):\n' + text.slice(start);
}
async function runSlide(i) {
  const book = nb, s = book.diapositivas[i];
  if (!window.SICPython) { s.salida = 'No se cargó el motor de Python (assets/live-python.js).'; s.ok = false; renderOutput(s); return false; }
  if (nb === book && idx === i) {
    el.output.hidden = false; el.output.classList.remove('has-error');
    el.outputHead.textContent = 'SALIDA · ejecutando Python';
    el.outputText.textContent = 'La primera ejecución descarga el intérprete Python. Puede tardar un poco y requiere Internet.';
  }
  try {
    const r = await window.SICPython.execute(s.codigo || '');
    s.ok = r.ok;
    s.salida = r.ok ? (r.output || '') : [r.output, cleanTraceback(r.error)].filter(Boolean).join('\n');
  } catch (err) {
    s.ok = false;
    s.salida = 'No se pudo ejecutar: ' + err.message + '\nVerifica tu conexión a Internet e inténtalo de nuevo.';
  }
  if (nb === book) { scheduleSave(); if (idx === i) renderOutput(s); }
  return s.ok;
}
async function runCurrent() {
  if (running || !nb) return;
  setRunning(true);
  try { await runSlide(idx); } finally { setRunning(false); }
}
async function runAll() {
  if (running || !nb) return;
  setRunning(true);
  const book = nb;
  try {
    for (let i = 0; i < book.diapositivas.length && nb === book; i++) {
      if (!(book.diapositivas[i].codigo || '').trim()) continue;
      show(i);
      if (!await runSlide(i)) break;
    }
  } finally { setRunning(false); }
}

// ---------- Cuenta y nube ----------
async function reloadLists() {
  el.loadError.hidden = true;
  try {
    [folders, notebooks] = await Promise.all([store.listFolders(), store.listNotebooks()]);
    renderTree();
    return true;
  } catch (err) {
    folders = []; notebooks = [];
    el.loadError.hidden = false;
    el.loadError.textContent = 'No se pudieron leer tus cuadernos de la nube: ' + err.message +
      '. Revisa que hayas ejecutado supabase/schema.sql en tu proyecto.';
  }
  renderTree();
  return false;
}
const findFolder = (nombre, parentId) =>
  folders.find(f => (f.parent_id || null) === parentId && f.nombre.toLowerCase() === nombre.toLowerCase());
async function ensureFolder(nombre, parentId = null) {
  return findFolder(nombre, parentId) || await createFolder(parentId, nombre);
}
async function folderDeClase(clase) {
  const semana = CLASES[clase]?.semana;
  const padre = semana ? await ensureFolder(semana) : null;
  if (semana && !padre) return null;
  return ensureFolder(nombreClase(clase), padre?.id || null);
}
// Una sola vez por cuenta: mete las carpetas sueltas «Clase N» dentro de su «Semana N».
async function agruparPorSemana() {
  const key = 'sic:cuadernos:semanas:' + (session?.user?.id || 'local');
  if (safeGet(key)) return;
  const movidas = [];
  try {
    for (const info of Object.values(CLASES)) {
      const suelta = findFolder(info.nombre, null);
      if (!suelta) continue;
      const semana = await ensureFolder(info.semana);
      if (!semana) throw new Error('no se pudo crear la carpeta ' + info.semana);
      const destino = findFolder(info.nombre, semana.id);
      if (!destino) {
        await store.saveFolder({ ...suelta, parent_id: semana.id });
        suelta.parent_id = semana.id;
      } else {
        // Ya existía «Semana N / Clase N»: se pasa el contenido y se quita la carpeta suelta.
        for (const f of folders.filter(x => x.parent_id === suelta.id)) {
          await store.saveFolder({ ...f, parent_id: destino.id }); f.parent_id = destino.id;
        }
        for (const n of notebooks.filter(x => x.carpeta_id === suelta.id)) {
          const full = await store.getNotebook(n.id);
          if (full) { full.carpeta_id = destino.id; await store.saveNotebook(full); }
          n.carpeta_id = destino.id;
        }
        await store.deleteFolder(suelta.id);
        folders = folders.filter(x => x.id !== suelta.id);
      }
      movidas.push(info.nombre);
    }
    safeSet(key, '1');
  } catch (err) {
    setStatus('No se pudieron ordenar las carpetas por semana: ' + err.message, true);
  }
  selectedFolder = null;
  renderTree();
  if (movidas.length) setStatus(`Ordené ${movidas.join(' y ')} dentro de su semana ✓`);
}
function renderAccount(message = '', isError = false) {
  el.account.textContent = '';
  const cfg = window.SIC_SUPABASE || {};
  const configured = Boolean(cfg.url && cfg.anonKey);
  if (!configured || !client) {
    const p = h('div');
    p.append(h('strong', {}, '💾 Guardado en este navegador. '));
    p.append(document.createTextNode(configured
      ? 'No se pudo cargar Supabase (¿sin Internet?).'
      : 'Para tenerlos en la nube y en cualquier dispositivo, configura Supabase (ver LEEME.md).'));
    el.account.append(p);
  } else if (!session) {
    const p = h('div');
    p.append(h('strong', {}, '💾 Guardado en este navegador. '));
    p.append(document.createTextNode('Inicia sesión para guardar en la nube:'));
    const form = h('form');
    const email = h('input', { type: 'email', required: '', placeholder: 'tu@correo.com', autocomplete: 'email', 'aria-label': 'Correo electrónico' });
    const send = h('button', { type: 'submit', class: 'mini-btn accent' }, 'Entrar');
    form.append(email, send);
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      send.disabled = true;
      const { error } = await client.auth.signInWithOtp({ email: email.value.trim(), options: { emailRedirectTo: location.origin + location.pathname } });
      send.disabled = false;
      renderAccount(error ? 'No se pudo enviar el enlace: ' + error.message : 'Te enviamos un enlace a ' + email.value.trim() + '. Ábrelo en este navegador.', Boolean(error));
    });
    el.account.append(p, form);
  } else {
    const p = h('div');
    p.append(h('strong', {}, '☁ En la nube · '));
    p.append(document.createTextNode(session.user.email || 'sesión iniciada'));
    const out = h('button', { type: 'button', class: 'mini-btn' }, 'Cerrar sesión');
    out.addEventListener('click', () => client.auth.signOut());
    el.account.append(p);
    const pendientes = localStore.count();
    if (pendientes) {
      const up = h('button', { type: 'button', class: 'mini-btn accent' }, `Subir ${pendientes} elemento(s) de este navegador a la nube`);
      up.addEventListener('click', migrateLocal);
      el.account.append(up);
    }
    el.account.append(out);
  }
  if (message) el.account.append(h('div', { class: 'msg' + (isError ? ' error' : '') }, message));
}
async function migrateLocal() {
  if (!session || !await askConfirm('¿Subir a la nube lo guardado en este navegador?', 'Se copiarán a tu cuenta las carpetas y cuadernos de este navegador y luego se borrarán de aquí.', 'Subir', false)) return;
  await flush();
  const remote = store, d = localStore.read();
  const depth = (f) => { let n = 0; const seen = new Set(); for (let p = f; p && p.parent_id && !seen.has(p.id); p = d.carpetas.find(x => x.id === p.parent_id)) { seen.add(p.id); n++; } return n; };
  try {
    for (const f of [...d.carpetas].sort((a, b) => depth(a) - depth(b))) await remote.saveFolder(f);
    for (const c of d.cuadernos) await remote.saveNotebook(c);
    localStore.clear();
    await reloadLists();
    renderAccount('Listo: tus cuadernos locales ya están en la nube.');
  } catch (err) { renderAccount('No se pudo completar la subida: ' + err.message + '. Lo que quedó en el navegador no se borró.', true); }
}
async function useSession(s) {
  await flush();
  session = s;
  store = s ? supabaseStore(client) : localStore;
  closeNotebook();
  renderAccount();
  if (await reloadLists()) await agruparPorSemana();
}
async function initAuth() {
  const cfg = window.SIC_SUPABASE || {};
  if (!cfg.url || !cfg.anonKey || !window.supabase) return;
  client = window.supabase.createClient(cfg.url, cfg.anonKey);
  const { data } = await client.auth.getSession();
  session = data.session;
  store = session ? supabaseStore(client) : localStore;
  client.auth.onAuthStateChange((_event, s) => {
    // Fuera del callback: Supabase recomienda no llamar a su cliente dentro de él.
    if ((s?.user?.id || null) !== (session?.user?.id || null)) setTimeout(() => useSession(s), 0);
    else session = s;
  });
}

// ---------- Eventos ----------
function bindText(input, apply) { input.addEventListener('input', () => { if (nb) { apply(input.value); scheduleSave(); } }); }
bindText(el.nbTitle, v => { nb.titulo = v; const meta = notebooks.find(n => n.id === nb.id); if (meta) meta.titulo = v; renderTree(); });
bindText(el.slideTitle, v => { slide().titulo = v; });
bindText(el.notes, v => { slide().notas = v; autoGrow(el.notes, notesMin()); });
bindText(el.code, v => { slide().codigo = v; autoGrow(el.code, 170); });
el.code.addEventListener('keydown', (e) => {
  if (e.key === 'Tab' && !e.shiftKey) {
    e.preventDefault();
    el.code.setRangeText('    ', el.code.selectionStart, el.code.selectionEnd, 'end');
    el.code.dispatchEvent(new Event('input'));
  }
});
el.folderSelect.addEventListener('change', () => {
  if (!nb) return;
  nb.carpeta_id = el.folderSelect.value || null;
  const meta = notebooks.find(n => n.id === nb.id); if (meta) meta.carpeta_id = nb.carpeta_id;
  if (nb.carpeta_id) collapsed.delete(nb.carpeta_id);
  scheduleSave(); renderTree(); updateOverline();
});
$('new-folder').addEventListener('click', () => createFolder(null));
$('new-notebook').addEventListener('click', () => createNotebook());
$('empty-new').addEventListener('click', () => createNotebook());
$('delete-notebook').addEventListener('click', deleteNotebook);
$('add-slide').addEventListener('click', addSlide);
$('dup-slide').addEventListener('click', duplicateSlide);
el.moveLeft.addEventListener('click', () => moveSlide(-1));
el.moveRight.addEventListener('click', () => moveSlide(1));
$('del-slide').addEventListener('click', deleteSlide);
el.back.addEventListener('click', () => show(idx - 1));
el.next.addEventListener('click', () => show(idx + 1));
el.run.addEventListener('click', runCurrent);
el.runAll.addEventListener('click', runAll);
$('clear-output').addEventListener('click', () => { if (!nb) return; slide().salida = null; slide().ok = true; renderOutput(slide()); scheduleSave(); });
$('stop-python').addEventListener('click', () => window.SICPython?.stop());
$('copy-code').addEventListener('click', async (e) => {
  const b = e.currentTarget;
  try { await navigator.clipboard.writeText(el.code.value); b.textContent = '¡Copiado!'; }
  catch (_) { el.code.select(); document.execCommand('copy'); b.textContent = '¡Copiado!'; }
  setTimeout(() => { b.textContent = 'Copiar código'; }, 1500);
});
function openSide() { el.side.classList.add('open'); el.sideBackdrop.classList.add('open'); el.sideToggle.setAttribute('aria-expanded', 'true'); }
function closeSide() { el.side.classList.remove('open'); el.sideBackdrop.classList.remove('open'); el.sideToggle.setAttribute('aria-expanded', 'false'); }
el.sideToggle.addEventListener('click', () => el.side.classList.contains('open') ? closeSide() : openSide());
el.sideBackdrop.addEventListener('click', closeSide);
window.addEventListener('resize', fitEditors);
document.addEventListener('keydown', (e) => {
  if (!modal.root.hidden) return;
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && nb) { e.preventDefault(); runCurrent(); return; }
  if (e.key === 'Escape') closeSide();
  if (!nb || e.target.closest('textarea,input,select,[contenteditable="true"]')) return;
  if (e.target.closest('button') && (e.key === ' ' || e.key === 'Enter')) return;
  if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); show(idx + 1); }
  if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); show(idx - 1); }
});

// ---------- Inicio ----------
(async () => {
  try { await initAuth(); } catch (err) { client = null; store = localStore; }
  renderAccount();
  if (await reloadLists()) await agruparPorSemana();
  const params = new URLSearchParams(location.search);
  if (params.get('nuevo') === '1') {
    history.replaceState(null, '', location.pathname);
    const clase = (params.get('clase') || '').replace(/[^\w-]/g, '').slice(0, 40) || null;
    const tema = (params.get('tema') || '').slice(0, 120);
    const carpeta = clase ? await folderDeClase(clase) : null;
    await createNotebook({ carpeta_id: carpeta?.id || null, clase,
      titulo: 'Práctica · ' + (tema || (clase ? nombreClase(clase) : 'nueva')), tema });
    return;
  }
  const last = safeGet('sic:cuadernos:ultimo');
  if (last && notebooks.some(n => n.id === last)) openNotebook(last);
})();
})();
