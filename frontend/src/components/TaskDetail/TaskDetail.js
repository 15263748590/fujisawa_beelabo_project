import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import TaskUpdateButton from './TaskUpdateButton';


function TaskDetail() {
    const { taskId } = useParams();

    const [task, setTask] = useState();
    const [status, setStatus] = useState();

    useEffect(() => {
      async function fetchTask() {
        const response = await fetch(`http://127.0.0.1:8000/tasks/${taskId}`);
        const data = await response.json();
        setTask(data);
      }

      fetchTask();
    });
    console.log(task);
    return (
    <div className="task-detail">
      {task ? (
        <div className='container'>
          <h2 className="fs-3 mb-4">{task.name}</h2>
          <select onChange={
            (e) => {
              setStatus(e.target.value);
            }
          } className='mb-4' value={task.status}>
            <option value="0">未完了</option>
            <option value="1">進行中</option>
            <option value="2">完了</option>
          </select>
          <div className="categories-list">
            <div className="form-floating">
              <textarea 
                onChange={(e) => {
                  setTask({
                    ...task,
                    description: e.target.value
                  });
                }} 
              className="form-control" placeholder="Leave a comment here" id="floatingTextarea" style={{height: "360px"}}
              defaultValue={task.description}
              ></textarea>
              <label name="aa">タスク内容</label>
            </div>
          </div>
          <div className="d-flex flex-wrap align-items-center justify-content-end py-3 mb-4 border-bottom">
            <div className="col-md-3 text-end">
              <TaskUpdateButton task={task} status={status} />
            </div>
          </div>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}


const TaskButton = ({ status }) => {
  const statusclassName = status === 0 ? 'btn-danger' : 'btn-success';
  const statusName = status === 0 ? '未完了' : status === 1 ? '進行中' : '完了';
  return (
    <button className={`btn ${statusclassName} btn-sm`}>{statusName}</button>
  );
}

export default TaskDetail;