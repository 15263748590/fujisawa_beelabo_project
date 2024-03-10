import React from 'react'
import { Link } from 'react-router-dom'
const Header = () => {
  return (
    <div className="container">
    <header
      className="d-flex flex-wrap align-items-center gap-5 justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
      <Link to={"/"} className="d-flex align-items-center col-md-3 mb-2 mb-md-0 text-dark text-decoration-none">
        <h1 className="text-success fs-2"><img style={{ width : "100px"}} src="/assets/logo.png" alt='Fujisawa Todo App' /></h1>
      </Link>
      <div className="col-md-3 text-end">
        <button type="button" className="btn btn-outline-primary me-2">Login</button>
        <button type="button" className="btn btn-primary">Sign-up</button>
      </div>
    </header>
  </div>
  )
}

export default Header