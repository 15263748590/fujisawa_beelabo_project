import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import DatePicker, { registerLocale } from "react-datepicker"
import ja from 'date-fns/locale/ja';
import "react-datepicker/dist/react-datepicker.css"
const CategoryAdd = () => {

    const [category, setCategory] = useState();
    console.log(category);
    const initialDate = new Date()
    const [startDate, setStartDate] = useState(initialDate)
    registerLocale('ja', ja);


    const handleChange = (date) => {
        setStartDate(date)
    }


    const handleButtonClick = async () => {
        const params = {
            "id" : 0,
            "name": category.name,
            "description": category.description,
            "order_number" : 0,
            "limit_date": startDate,
        };

        async function fetchCategory() {
            const response = await fetch(`http://127.0.0.1:8000/categories/` , {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json' 
                },
                body: JSON.stringify(params) // パラメーターをJSON形式でエンコード);
            });
            const data = await response.json();
            console.log(data);
        }
  
        fetchCategory();
    };
    return (
        <div className="container mt-3">
            <div className="input-group mb-4">
                <input 
                    type="text"
                    className="form-control"
                    placeholder="カテゴリ名"
                    aria-label="category_name" 
                    aria-describedby="input-group-right" 
                    onChange={(e) => {
                        setCategory({
                        ...category,
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
                            setCategory({
                            ...category,
                            description: e.target.value
                            });
                        }} 
                        />
                    <label name="category">カテゴリ詳細</label>
                </div>
            </div>
            <div>
                <h3>締切日</h3>
                <DatePicker
                    locale='ja'
                    dateFormat="yyyy/MM/dd"
                    selected={startDate}
                    onChange={handleChange}
                />

            </div>
            <div className="d-flex flex-wrap align-items-center justify-content-end py-3 mb-4 border-bottom">
                <div className="col-md-3 text-end">
                    {/* <Link to="/category_add_completed"> */}
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

export default CategoryAdd