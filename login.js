export default function Login(){
  async function submit(e){
    e.preventDefault();
    const res = await fetch("http://localhost:8000/auth/login/", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ email:e.target.email.value, password:e.target.password.value })});
    const json = await res.json();
    if(json.access){ localStorage.setItem("access", json.access); localStorage.setItem("refresh", json.refresh); alert("Logged in"); }
    else alert(JSON.stringify(json));
  }
  return (<form onSubmit={submit}><input name="email"/><input type="password" name="password"/><button>Login</button></form>);
}
