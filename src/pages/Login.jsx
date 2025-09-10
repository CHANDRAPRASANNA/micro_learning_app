import React, {useState} from "react";
import axios from "axios";
export default function Login(){
  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");
  const [msg,setMsg]=useState("");
  const base="http://127.0.0.1:5000";
  const register = async ()=>{
    try{
      await axios.post(base+"/register",{username,password});
      setMsg("Registered. Now login.");
    }catch(e){ setMsg(e.response?.data?.error || "Error") }
  }
  const login = async ()=>{
    try{
      const res = await axios.post(base+"/login",{username,password});
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("user_id", res.data.user_id);
      setMsg("Logged in");
      window.location.href="/";
    }catch(e){ setMsg(e.response?.data?.error || "Login failed") }
  }
  return (<div className="max-w-md">
    <h2 className="text-2xl mb-4">Login / Register</h2>
    <input className="block mb-2 p-2 rounded bg-gray-800" placeholder="username" value={username} onChange={e=>setUsername(e.target.value)} />
    <input type="password" className="block mb-2 p-2 rounded bg-gray-800" placeholder="password" value={password} onChange={e=>setPassword(e.target.value)} />
    <div className="flex gap-2">
      <button onClick={login} className="px-3 py-1 bg-blue-600 rounded">Login</button>
      <button onClick={register} className="px-3 py-1 bg-gray-600 rounded">Register</button>
    </div>
    {msg && <p className="mt-3">{msg}</p>}
  </div>)
}
