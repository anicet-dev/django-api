import {useEffect, useState} from "react";
export default function Dashboard(){
  const [user,setUser] = useState(null);
  useEffect(()=> {
    const token = localStorage.getItem("access"); if(!token) return;
    fetch("http://localhost:8000/auth/me/", { headers: { Authorization: `Bearer ${token}` } }).then(r=>r.json()).then(setUser);
  },[]);
  if(!user) return <div>Not logged</div>;
  return <div>Welcome {user.username} ({user.email}) - role: {user.role}</div>;
}
