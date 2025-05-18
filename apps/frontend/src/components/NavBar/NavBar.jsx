import React, { useState } from "react";
import { Link } from "react-router-dom";
import logopic from "../../assets/images/cutlery1.png";
import styles from "./navbar.module.css";

const NavBar = ({ onSignInClick }) => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <div className={styles.navContainer}>
      <div className={styles.logoContainer}>
        <img src={logopic} alt="Logo Image" className={styles.logo} />
        <span className={styles.logoText}>Nibbler</span>
      </div>

      <div className={styles.menuContainer}>
        <ul className={`${styles.links} ${menuOpen ? styles.active : ""}`}>
          <li>
            <Link to="/dashboard">Navigator</Link>
          </li>
          <li>
            <Link to="/aboutUs">About Us</Link>
          </li>
          <li>
            <Link to="/contactUs">Contact Us</Link>
          </li>
          <li className={styles.specialLiBtn}>
            <button className={styles.signInBtn} onClick={onSignInClick}>
              Sign In
            </button>
          </li>
        </ul>
        <button className={styles.burgerMenu} onClick={toggleMenu}>
          <div className={`${styles.bar} ${menuOpen ? styles.open : ""}`} />
          <div className={`${styles.bar} ${menuOpen ? styles.open : ""}`} />
          <div className={`${styles.bar} ${menuOpen ? styles.open : ""}`} />
        </button>
      </div>
    </div>
  );
};

export default NavBar;
