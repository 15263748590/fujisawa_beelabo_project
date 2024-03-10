import logo from './logo.svg';
import './App.css';

import React from 'react';
import Header from './components/Header';
import Category from './components/Category';
import TaskDetail from './components/TaskDetail/TaskDetail';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TaskList from './components/Categories/TaskList';
import Footer from './components/Footer';
import CategoryAdd from './components/Categories/CategoryAdd';
import TaskAdd from './components/TaskDetail/TaskAdd';

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Category />} />
        <Route path="/:id" element={<Category />} />
        <Route path="/categories/:categoryId/tasks" element={<TaskList />} />
        <Route path="/tasks/:taskId" element={<TaskDetail />} />
        <Route path="/category_add" element={<CategoryAdd />} />
        <Route path="/tasks/task_add" element={<TaskAdd />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
