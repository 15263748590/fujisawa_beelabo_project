import React, { useState } from 'react'
import { Link , useLocation } from 'react-router-dom'
import DatePicker, { registerLocale } from "react-datepicker"
import ja from 'date-fns/locale/ja';
import "react-datepicker/dist/react-datepicker.css"
const TaskAdd = ( ) => {

    const [task, setTask] = useState();
    const location = useLocation();
    const { ParentCategory } = location.state;

    console.log(ParentCategory);
    const initialDate = new Date()
    const [startDate, setStartDate] = useState(initialDate)
    registerLocale('ja', ja);


    const handleChange = (date) => {
        setStartDate(date)
    }


    const handleButtonClick = async () => {
        const params = {
            "id" : 0,
            "name": task.name,
            "category_id" : ParentCategory.id,
            "description": task.description,
            "order_number" : 0,
            "status" : 0,
            
        };

        console.log(params);

        async function fetchTask() {
            const response = await fetch(`http://127.0.0.1:8000/tasks/` , {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(params) // パラメーターをJSON形式でエンコード);
            });
            const data = await response.json();
            console.log(data);
        }
  
        fetchTask();
    };
    return (
        <div className="container mt-3">
            <div className="input-group mb-4">
                <input 
                    type="text"
                    className="form-control"
                    placeholder="タスク名"
                    aria-label="task_name" 
                    aria-describedby="input-group-right" 
                    onChange={(e) => {
                        setTask({
                        ...task,
                        name: e.target.value
                        });
                    }}
                />
            </div>
            <div className="categories-list mb-3">
                <div className="form-floating">
                    <textarea className="form-control"
                        placeholder="Leave a comment here"
                        id="floatingTextarea"
                        defaultValue=""
                        style={{height: "360px"}}
                        onChange={(e) => {
                            setTask({
                            ...task,
                            description: e.target.value
                            });
                        }} 
                        />
                    <label name="category">タスク詳細</label>
                </div>
            </div>
            <div className="d-flex flex-wrap align-items-center justify-content-end py-3 mb-4 border-bottom">
                <div className="col-md-3 text-end">
                    <button 
                    type="button" 
                    className="btn btn-outline-primary me-2"
                    onClick={handleButtonClick}
                    >新規追加</button>
                    {/* </Link> */}
                </div>
            </div>
        </div>
    )
}

export default TaskAdd