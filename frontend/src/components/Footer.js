import React from 'react';
import { Link } from 'react-router-dom';


const Footer = () => {
    return (
        <footer className="bg-primary text-center text-lg-start text-white mt-5">
            <div className="container p-4">
                <div className="row my-4 justify-content-between">
                    <div className="col-lg-3 col-md-6 mb-4 mb-md-0">
                        <p className="text-center display-6"><img style={{ width : "100px"}} src="/assets/logo.png" alt='Fujisawa Todo App' /></p>

                        <ul className="list-unstyled d-flex flex-row justify-content-center">
                            <li>
                                <a className="text-white px-2" href="#!">
                                    <i className="fab fa-facebook-square"></i>
                                </a>
                            </li>
                            <li>
                                <a className="text-white px-2" href="#!">
                                    <i className="fab fa-instagram"></i>
                                </a>
                            </li>
                            <li>
                                <a className="text-white ps-2" href="#!">
                                    <i className="fab fa-youtube"></i>
                                </a>
                            </li>
                        </ul>
                    </div>
                    <div className="col-lg-3 col-md-6 mb-4 mb-md-0">
                        <h5 className="text-uppercase mb-3">アプリの詳細</h5>
                        <div>
                            <p>このアプリは、自身で期限を付けられるメモアプリです。</p>
                        </div>
                    </div>
                </div>
            </div>
            <div className="text-center p-3" style={{ backgroundColor : "rgba(255, 255, 255, 0.2)"}}>
                © 2023 memo :
                <Link className="text-white" to={"/"}> Fujisawa Todo App</Link>
            </div>
        </footer>
    );
}

export default Footer;