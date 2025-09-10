import React, {useEffect,useState} from "react";
import axios from "axios";
import { Link } from "react-router-dom";
export default function Dashboard(){
  const [lessons,setLessons]=useState([]);
  const token = localStorage.getItem("token");
  useEffect(()=>{
    if(!token) return;
    axios.get("http://127.0.0.1:5000/lessons",{headers:{Authorization:token}}).then(r=>setLessons(r.data)).catch(()=>setLessons([]));
  },[]);
  if(!token) return <p>Please login to view lessons.</p>;
  return (<div>
    <h1 className="text-2xl mb-4">Lessons</h1>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {lessons.map(l=>(
        <div key={l.id} className="p-4 bg-gray-800 rounded">
          <h3 className="font-semibold">{l.title}</h3>
          <p className="text-sm mt-2 line-clamp-3">{l.content}</p>
          <Link to={`/lesson/${l.id}`} className="inline-block mt-3 text-blue-400">Open</Link>
        </div>
      ))}
    </div>
  </div>)
}
