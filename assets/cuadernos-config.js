/* Conexión a Supabase para «Mis cuadernos».
 * Copia los valores de Supabase → Project Settings → API:
 *   url     → Project URL   (https://xxxx.supabase.co)
 *   anonKey → anon public key o publishable key (sb_publishable_…)
 * La clave «anon» es pública por diseño: los datos quedan protegidos por las
 * políticas RLS de supabase/schema.sql. Nunca pongas aquí la clave service_role.
 * Si los dejas vacíos, los cuadernos se guardan solo en este navegador.
 */
window.SIC_SUPABASE = {
  url: 'https://jscozkndbbalmujypgnj.supabase.co',
  anonKey: 'sb_publishable_JE8PHEOWfsYrI0i8o6p9EA_vqXSuWAM'
};
