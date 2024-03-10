import React, { useState, useEffect } from 'react';
import { Link , useParams } from 'react-router-dom';
import Category from '../Category';

const TaskList = () => {
    const [categories, setCategories] = useState([]);
    const [tasks, setTasks] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);

    const { categoryId } = useParams();

    // フィルターの値を管理する状態
  const [filter, setFilter] = useState('');

    // フィルターに基づいてタスクをフィルタリングする
    const filteredTasks = tasks.filter(task =>
        task.name.toLowerCase().includes(filter.toLowerCase())
    );

    console.log(categoryId);
    useEffect(() => {
        async function fetchCategories() {
            const response = await fetch(`http://127.0.0.1:8000/categories/${categoryId}`);
            const categories = await response.json();
            setCategories(categories);
        }

        async function fetchTask() {
            try{
                const response = await fetch(`http://127.0.0.1:8000/categories/${categoryId}/tasks`);
                const tasks = await response.json();
                setTasks(tasks);    
            }catch(error){
                console.log(error);
            
            }
        }
      
        fetchCategories();

        fetchTask();
    }, []);
    
    console.log(tasks);

    return (
        <div className="container">
            <div className="input-group mb-3">
                <span className="input-group-text" id="basic-addon1">検索</span>
                <input 
                type="text" 
                className="form-control" 
                value={filter}
                onChange={(e) => setFilter(e.target.value)} 
                placeholder="タスク名" 
                aria-label="category" 
                aria-describedby="basic-addon1" />
            </div>
            <Link to={"/task/task_add"} state={{ParentCategory : categories}}>
                タスク追加
            </Link>
            <div className='category-title'>
                <h2 className='mb-3'>{categories.name}</h2>
            </div>
            {filteredTasks.map(task => (
                <TaskRow key={task.id} task={task} />
            ))}
        </div>
    )
}

const TaskRow = ({ task }) => {
    return (
        <div className="row mb-3">
            <div className="col-2 category-status d-flex align-items-center justify-content-center">
                <Status status={task.status} />
            </div>
            <div className="col-6 category-progress">
                <div className="progress progress-tasuku p-3 align-items-center ">
                    <Link to={`/tasks/${task.id}`}>{task.name}</Link>
                </div>
            </div>
        </div>
    );
}

const Status = ({ status }) => {

    switch (status) {
        case 0:
            return <StatusButton buttonclassName="btn-secondary" statusName="未着手" />;
        case 1:
            return <StatusButton buttonclassName="btn-warning" statusName="進行中" />;
        case 2:
            return <StatusButton buttonclassName="btn-info" statusName="完了" />;
        default:
            return <StatusButton buttonclassName="btn-secondary" statusName="未着手" />;
    }
}

const StatusButton = ({ buttonClass, statusName }) => {
    return (
        <button type="button" className={`btn ${buttonClass} btn-sm`}>{statusName}</button>
    );
}

export default TaskList;