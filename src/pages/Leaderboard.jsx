import React, {useEffect,useState} from "react";
import axios from "axios";
export default function Leaderboard(){
  const [board,setBoard]=useState([]);
  const token = localStorage.getItem("token");
  useEffect(()=>{
    if(!token) return;
    axios.get("http://127.0.0.1:5000/leaderboard",{headers:{Authorization:token}}).then(r=>setBoard(r.data));
  },[]);
  if(!token) return <p>Please login</p>;
  return (<div>
    <h2 className="text-2xl mb-4">Leaderboard</h2>
    <ol className="list-decimal ml-6">
      {board.map(u=>(
        <li key={u.user_id} className="mb-2">{u.username} — {u.completed_lessons} lessons</li>
      ))}
    </ol>
  </div>)
}
