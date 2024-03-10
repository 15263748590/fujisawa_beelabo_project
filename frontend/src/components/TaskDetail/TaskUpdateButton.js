import React, { useState, Suspense, useEffect } from 'react';
import { useParams } from 'react-router-dom';


const TaskUpdateButton = ({ task , status } ) => {
  const [result, setResult] = useState();
  const [isLoading, setIsLoading] = useState(false);
  const {taskId} = useParams();
  const handleButtonClick = async () => {
    setIsLoading(true);
    const params = {
      "id": task.id,
      "name": task.name,
      "category_id": task.category_id,
      "description": task.description,
      "status": status,
      "order_number": task.order_number,
    };

    try {
      const response = await fetch(`http://127.0.0.1:8000/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json' 
        },
        body: JSON.stringify(params) // パラメーターをJSON形式でエンコード
      });
      console.log(response.ok);
      console.log(params);
      if (response.ok) {
        const data = response.json();
        console.log('成功:', data);
        setResult(response)
        // 成功した処理
        setIsLoading(false);

      } else {
        console.log('エラー:', response.status);
        // エラー処理
        setResult(response)
      }
    } catch (error) {
      console.error('エラーが発生しました:', error);
      // エラー処理
      setIsLoading(false);

    }

  };

  return (
    <div>
      <button className='btn btn-outline-primary' onClick={handleButtonClick} disabled={isLoading}>
        更新
      </button>
      {isLoading ? (
        <p>ローディング中...</p>
      ) : result ? (
        <p>{result.status === 'success' ? '成功!' : '失敗!'}</p>
      ) : null}
    </div>
  );
};

export default TaskUpdateButton;