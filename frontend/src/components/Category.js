import React, { useState, useEffect } from 'react';
import { Link , useParams } from 'react-router-dom';
import moment from 'moment';
function Category() {
  const [categories, setCategories] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const {id} = useParams();
  
  useEffect(() => {
    async function fetchCategories() {
      const offsetPages = (id - 1) * itemsPerPage;
      if (id === undefined) {
        const response = await fetch("http://127.0.0.1:8000/categories");
        const categories = await response.json();
        setCategories(categories);
   
      }else {
        const response = await fetch("http://127.0.0.1:8000/categories" + "?start=" + offsetPages + "&limit=" + itemsPerPage );
        const categories = await response.json();
        setCategories(categories);
   
      }
   }

    fetchCategories();
  }, []);

  console.log(categories);
  return (
    <div className="container">
      <CategoryList categories={categories} />
      <Pagination
        itemsPerPage={itemsPerPage}
        totalItems={categories.length}
      />
    </div>
  );
}

const CategoryList = ({ categories }) => {
  return (
    <div className="categories-list mb-5" id="category-list">
      {categories.map(category => (
        <CategoryRow key={category.id} category={category} />
      ))}
      <Link to={`/category_add`} className="add_btn"><span>+</span></Link>
    </div>
  );
}
  
const CategoryRow = ({ category }) => {
    // Convert date to desired format
    const dateYmd = moment(category.limit_date).format('YYYY年MM月DD日');
    return (
      <div className="row mb-2">
        <div className="col-2 category-progress d-flex align-items-center justify-content-center">
          <div className="progress progress-100 w-100">
            <p>100%</p>
          </div>
        </div>
        <div className="col-4 small-text">
          {dateYmd}
        </div>
        <div className="col-4 category-name">
        <img style={{ width : "15px", marginRight: "0.25rem"}} className='mr-2' src="/assets/progress-100.png" alt='100%' /> 
            <Link to={`/categories/${category.id}/tasks/`}>{category.name}</Link>
        </div>
        <div className="col-1 category-status">
          <CheckBoXLabel id={category.id} />
          {/* <input checked type="checkbox" name="category" id={category.id} /> */}
        </div>
      </div>
    );
}

const CheckBoXLabel = () =>{
  return (
    <label>
      <div class="checkbox_wrapper">
        <input type="checkbox" id="checkbox" />
        <span class="custom"></span>
      </div> 
    </label> 
  );
}

// ページネーションコンポーネント
const Pagination = ({ itemsPerPage, totalItems, paginate }) => {
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalItems / itemsPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <nav className="d-flex align-items-center justify-content-center" aria-label="Page navigation">
        <ul className="pagination">
        {pageNumbers.map(number => (
          <li key={number} className='page-item'>
            <Link to={`/${number}`} className='page-link'>
              {number}
            </Link>
          </li>
        ))}
        </ul>
    </nav>
    );
}
export default Category