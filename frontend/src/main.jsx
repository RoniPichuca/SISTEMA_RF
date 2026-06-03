import React,{useEffect,useState,useRef} from 'react';import{createRoot}from'react-dom/client';import{BarChart,Bar,XAxis,YAxis,Tooltip,ResponsiveContainer,LineChart,Line,CartesianGrid}from'recharts';import{Users,Clock,Brain,FileText,Camera,Settings,LogOut,Search,Trash2,Edit,Save}from'lucide-react';import api from'./services/api';import'./styles.css';
const menu=[['dashboard','Dashboard',Brain],['students','Estudiantes',Users],['recognition','Reconocimiento',Camera],['reports','Reportes',FileText],['settings','Configuración',Settings]];
function Login({onLogin}){const[u,setU]=useState('admin'),[p,setP]=useState('admin123'),[err,setErr]=useState('');async function submit(e){e.preventDefault();try{const form=new URLSearchParams();form.append('username',u);form.append('password',p);const{data}=await api.post('/auth/login',form);localStorage.setItem('token',data.access_token);onLogin()}catch{setErr('Credenciales inválidas o backend no disponible')}}return <div className="login"><form onSubmit={submit} className="login-card"><div className="logo">IA</div><h1>Sistema Inteligente de Asistencia</h1><p>Reconocimiento facial y analítica predictiva en tiempo real</p><input value={u} onChange={e=>setU(e.target.value)} placeholder="Usuario"/><input value={p} onChange={e=>setP(e.target.value)} placeholder="Contraseña" type="password"/><button>Ingresar al sistema</button>{err&&<small className="error">{err}</small>}<small>Demo: admin / admin123</small></form></div>}
function Layout(){const[page,setPage]=useState('dashboard');function logout(){localStorage.removeItem('token');location.reload()}const Page={dashboard:<Dashboard/>,students:<Students/>,recognition:<Recognition/>,reports:<Reports/>,settings:<SettingsPage/>}[page];return <div className="app"><aside><h2>FaceAI Pro</h2><p className="muted">Tesis universitaria</p>{menu.map(([id,label,Icon])=><button key={id} onClick={()=>setPage(id)} className={page===id?'active':''}><Icon size={18}/>{label}</button>)}<button onClick={logout} className="logout"><LogOut size={18}/>Cerrar sesión</button></aside><main>{Page}</main></div>}
function Card({title,value,icon:Icon}){return <div className="card"><div><p>{title}</p><h3>{value}</h3></div><Icon size={30}/></div>}
function Dashboard(){const[stats,setStats]=useState({}),[chart,setChart]=useState([]),[pred,setPred]=useState([]);useEffect(()=>{api.get('/dashboard/stats').then(r=>setStats(r.data));api.get('/dashboard/chart').then(r=>setChart(r.data));api.get('/dashboard/predictive').then(r=>setPred(r.data))},[]);return <><Header title="Dashboard administrativo" sub="Indicadores biométricos y asistencia institucional"/><section className="grid cards"><Card title="Total estudiantes" value={stats.totalEstudiantes||0} icon={Users}/><Card title="Asistencias" value={stats.totalAsistencias||0} icon={Save}/><Card title="Tardanzas" value={stats.tardanzas||0} icon={Clock}/><Card title="Precisión IA" value={(stats.precisionIA||0)+'%'} icon={Brain}/></section><section className="panel"><h3>Asistencia de los últimos días</h3><ResponsiveContainer height={260}><BarChart data={chart}><XAxis dataKey="fecha"/><YAxis/><Tooltip/><Bar dataKey="PRESENTE"/><Bar dataKey="TARDANZA"/></BarChart></ResponsiveContainer></section><section className="panel"><h3>Analítica predictiva</h3><table><thead><tr><th>Estudiante</th><th>Riesgo tardanza</th><th>Riesgo ausencia</th><th>Recomendación</th></tr></thead><tbody>{pred.map((x,i)=><tr key={i}><td>{x.estudiante}</td><td>{x.riesgoTardanza}%</td><td>{x.riesgoAusencia}%</td><td>{x.recomendacion}</td></tr>)}</tbody></table></section></>}
function Header({title,sub}){return <div className="header"><div><h1>{title}</h1><p>{sub}</p></div></div>}
function Students(){const[rows,setRows]=useState([]),[q,setQ]=useState(''),[form,setForm]=useState({codigo:'',dni:'',nombres:'',apellidos:'',grado:'3°',seccion:'A',email:'',telefono:''}),[edit,setEdit]=useState(null),[errors,setErrors]=useState({});
const load=()=>api.get('/students?q='+q).then(r=>setRows(r.data));
useEffect(()=>{load();},[]);

const soloLetras=/^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;
const soloNumeros=/^\d+$/;

function validateField(k,v){
 if(['nombres','apellidos','seccion'].includes(k)&&v&&!soloLetras.test(v))return 'Solo letras';
 if(['dni','telefono'].includes(k)&&v&&!soloNumeros.test(v))return 'Solo números';
 if(k==='dni'&&v&&v.length!==8)return 'El DNI debe tener 8 dígitos';
 if(k==='telefono'&&v&&v.length>9)return 'Máximo 9 dígitos';
 if(k==='email'&&v&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v))return 'Correo inválido';
 return '';
}

function handleChange(k,v){
 if(['nombres','apellidos','seccion'].includes(k))v=v.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g,'');
 if(['dni','telefono'].includes(k))v=v.replace(/\D/g,'');
 if(k==='dni')v=v.slice(0,8);
 if(k==='telefono')v=v.slice(0,9);
 setForm({...form,[k]:v});
 setErrors({...errors,[k]:validateField(k,v)});
}

function validateAll(){
 const e={};
 Object.keys(form).forEach(k=>{const msg=validateField(k,form[k]);if(msg)e[k]=msg});
 if(!form.codigo)e.codigo='Código obligatorio';
 if(!form.dni)e.dni='DNI obligatorio';
 if(!form.nombres)e.nombres='Nombres obligatorios';
 if(!form.apellidos)e.apellidos='Apellidos obligatorios';
 if(!form.grado)e.grado='Grado obligatorio';
 if(!form.seccion)e.seccion='Sección obligatoria';
 setErrors(e);
 return Object.keys(e).length===0;
}

async function save(e){e.preventDefault();if(!validateAll())return alert('Corrige los campos marcados');if(edit){await api.put('/students/'+edit,form)}else await api.post('/students',form);setEdit(null);setForm({codigo:'',dni:'',nombres:'',apellidos:'',grado:'3°',seccion:'A',email:'',telefono:''});setErrors({});load()}
async function del(id){if(confirm('¿Eliminar estudiante?')){await api.delete('/students/'+id);load()}}
async function upload(id,file){if(!file)return;if(!file.type.startsWith('image/'))return alert('Solo se permiten imágenes');const fd=new FormData();fd.append('file',file);await api.post(`/students/${id}/face`,fd);alert('Foto facial registrada')}
const fields=['codigo','dni','nombres','apellidos','grado','seccion','email','telefono'];
return <><Header title="Gestión de estudiantes" sub="CRUD completo con registro de rostro"/><section className="panel"><form className="form" onSubmit={save}>{fields.map(k=><div key={k} className="field"><input placeholder={k} value={form[k]||''} onChange={e=>handleChange(k,e.target.value)} inputMode={['dni','telefono'].includes(k)?'numeric':'text'} maxLength={k==='dni'?8:k==='telefono'?9:80}/>{errors[k]&&<small className="error">{errors[k]}</small>}</div>)}<button>{edit?'Actualizar':'Registrar'}</button></form></section><section className="panel"><div className="toolbar"><div><Search size={16}/><input placeholder="Buscar" value={q} onChange={e=>setQ(e.target.value)} onKeyUp={load}/></div></div><table><thead><tr><th>Código</th><th>Estudiante</th><th>Grado</th><th>Foto facial</th><th>Acciones</th></tr></thead><tbody>{rows.map(r=><tr key={r.id}><td>{r.codigo}</td><td>{r.nombres} {r.apellidos}</td><td>{r.grado} {r.seccion}</td><td><input type="file" accept="image/*" onChange={e=>upload(r.id,e.target.files[0])}/></td><td><button className="mini" onClick={()=>{setEdit(r.id);setForm(r);setErrors({})}}><Edit size={15}/></button><button className="mini danger" onClick={()=>del(r.id)}><Trash2 size={15}/></button></td></tr>)}</tbody></table></section></>}
function Recognition(){const video=useRef(null),canvas=useRef(null);const[result,setResult]=useState(null);async function start(){const s=await navigator.mediaDevices.getUserMedia({video:true});video.current.srcObject=s}async function recognize(){const c=canvas.current,v=video.current;c.width=v.videoWidth;c.height=v.videoHeight;c.getContext('2d').drawImage(v,0,0);const image=c.toDataURL('image/jpeg');try{const{data}=await api.post('/attendance/recognize',{image});setResult(data)}catch(e){setResult({recognized:false,message:e.response?.data?.detail||'Error de reconocimiento'})}}return <><Header title="Reconocimiento facial en tiempo real" sub="Detección biométrica, comparación de embeddings y asistencia automática"/><section className="recognition panel"><div><video ref={video} autoPlay playsInline/><canvas ref={canvas} hidden/><div className="actions"><button onClick={start}>Activar cámara</button><button onClick={recognize}>Reconocer y registrar</button></div></div><div className="result"><h3>Resultado IA</h3>{result?<pre>{JSON.stringify(result,null,2)}</pre>:<p>Active la cámara y capture un rostro registrado.</p>}</div></section></>}
function Reports(){const[rows,setRows]=useState([]);useEffect(()=>{api.get('/attendance').then(r=>setRows(r.data))},[]);return <><Header title="Reportes" sub="Historial, exportación PDF y Excel"/><section className="panel actions"><button onClick={()=>location.href='http://localhost:8000/api/reports/pdf'}>Exportar PDF</button><button onClick={()=>location.href='http://localhost:8000/api/reports/excel'}>Exportar Excel</button></section><section className="panel"><table><thead><tr><th>Fecha</th><th>Hora</th><th>Estudiante</th><th>Estado</th><th>Confianza</th></tr></thead><tbody>{rows.map(r=><tr key={r.id}><td>{r.fecha}</td><td>{r.hora}</td><td>{r.estudiante?.nombres} {r.estudiante?.apellidos}</td><td><span className="badge">{r.estado}</span></td><td>{Math.round(r.confianza*100)}%</td></tr>)}</tbody></table></section></>}
function SettingsPage(){return <><Header title="Configuración" sub="Parámetros del sistema biométrico"/><section className="panel"><h3>Configuración recomendada</h3><p>Hora límite de puntualidad: 08:00:00. Tolerancia facial: 0.48. Backend: FastAPI + MySQL + JWT.</p></section></>}
function App(){const[token,setToken]=useState(localStorage.getItem('token'));return token?<Layout/>:<Login onLogin={()=>setToken(localStorage.getItem('token'))}/>}createRoot(document.getElementById('root')).render(<App/>);
