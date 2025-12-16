export default function Register(){
  async function submit(e){
    e.preventDefault();
    const data = { email: e.target.email.value, username: e.target.username.value, phone: e.target.phone.value, password: e.target.password.value, password2: e.target.password2.value };
    const res = await fetch("http://localhost:8000/auth/register/", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(data) });
    const json = await res.json();
    alert(JSON.stringify(json));
  }
  return (<form onSubmit={submit}><input name="email"/><input name="username"/><input name="phone"/><input type="password" name="password"/><input type="password" name="password2"/><button>Register</button></form>);
}
