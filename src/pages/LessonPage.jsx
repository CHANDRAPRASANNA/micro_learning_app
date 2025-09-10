import React, {useEffect,useState} from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
export default function LessonPage(){
  const {id}=useParams();
  const [lesson,setLesson]=useState(null);
  const [score,setScore]=useState(null);
  const token = localStorage.getItem("token");
  useEffect(()=>{
    if(!token) return;
    axios.get("http://127.0.0.1:5000/lesson/"+id,{headers:{Authorization:token}}).then(r=>setLesson(r.data));
  },[id]);
  const submitQuiz = async (e)=>{
    e.preventDefault();
    let correct=0;
    lesson.quiz.forEach((q,idx)=>{
      const ans = e.target[`q${idx}`].value;
      if(ans===q.answer) correct++;
    });
    setScore(`${correct} / ${lesson.quiz.length}`);
    // save progress
    await axios.post("http://127.0.0.1:5000/progress",{lesson_id: lesson.id, completed:true},{headers:{Authorization:token}});
  }
  if(!token) return <p>Please login</p>;
  if(!lesson) return <p>Loading...</p>;
  return (<div>
    <h2 className="text-2xl">{lesson.title}</h2>
    <p className="mt-3">{lesson.content}</p>
    <form onSubmit={submitQuiz} className="mt-4">
      {lesson.quiz.map((q,idx)=>(
        <div key={idx} className="mb-3">
          <p>{q.question}</p>
          {q.options.map((opt,i)=>(
            <label key={i} className="block"><input type="radio" name={`q${idx}`} value={opt} required/> {opt}</label>
          ))}
        </div>
      ))}
      <button className="px-3 py-1 bg-blue-600 rounded">Submit</button>
    </form>
    {score && <p className="mt-3">Score: {score}</p>}
  </div>)
}
