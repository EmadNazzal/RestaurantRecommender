import  NavBar  from "../NavBar/NavBar";
import { useState } from "react";
import styles from "./welcomepage.module.css";
import stylesContainer from "../../App.module.css";
import ModalPopUp from "../ModalPopUp/ModalPopUp";
import { useNavigate } from "react-router-dom";
import bkVideo from '../../assets/images/bkVideo.mp4'
export const WelcomePage = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const navigate = useNavigate();

  const handleOpenModal = () => {
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const handleButtonClickForDashboard = () => {
    navigate("/dashboard");
  };

  return (
    <>
      <div className={styles.parentContainerForWelcomePage}>
        <video
          className={styles.backgroundVideo}
          autoPlay
          muted
          loop
        >
          <source src={bkVideo} />
          Your browser does not support the video tag.
        </video>

        <div className={styles.pillarHolder}>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
          <div className={styles.pillars}></div>
        </div>

        <div className={styles.circlesContainer}>
          <div className={styles.circle1}></div>
          <div className={styles.circle2}></div>
          <div className={styles.circle3}></div>
          <div className={styles.circle4}></div>
        </div>

        <NavBar onSignInClick={handleOpenModal} />
        <div className={`${styles.mainDiv} ${stylesContainer.mainContainer}`}>
         
          <ModalPopUp open={modalOpen} handleClose={handleCloseModal} />
        </div>
        <div className={styles.mainText}>
          Manhattan.
          <br />
          Food.
          <br />
          Detector<span className={styles.detectorDot}>.</span>
        </div>
        <div className={styles.btnContainer}>
          <button
            className={styles.mainDashBtn}
            onClick={handleButtonClickForDashboard}
          >
            Get Started 
          </button>
        </div>
      </div>
    </>
  );
};
