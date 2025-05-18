import { useState, useEffect } from "react";
import styles from "./contactUs.module.css";
import { useNavigate } from "react-router-dom";
import { Alert } from "@mui/material"; // Assuming you use Material-UI for alerts
import { useContactUs } from "../../apiServices/useService"; // Custom hook for contact us API

export const ContactUs = () => {
  const navigate = useNavigate();
  const { response, error, loading, contactUs } = useContactUs(); // Custom hook

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });
  
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowForm(true);
    }, 100); // Delay to trigger animation
    return () => clearTimeout(timer);
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await contactUs(formData);
      // Optionally: Show success message or navigate to a thank you page
      alert("Form submitted successfully!");
    } catch (error) {
      // Display error message using alerts from Material-UI or any other method
      console.error("Error submitting form:", error);
      alert("Failed to submit form. Please try again.");
    }
  };

  const handleButtonClickForContactUsPage = () => {
    navigate("/");
  };

  return (
    <div className={styles.contactUsPage}>
      <div className={styles.waveWrapper}>
        <div className={styles.wave}></div>
        <div className={styles.wave}></div>
        <div className={styles.wave}></div>
      </div>
      <div className={`${styles.container} ${showForm ? styles.fadeIn : ''}`}>
        <h2 className={styles.contactUsText}>Contact Us</h2>
        <p className={styles.contactUsPara}>
          Fill the form below and we will get back to you as soon as possible.
        </p>

        <div className={styles.formContainer}>
          <form onSubmit={handleSubmit}>
            <div className={styles.formGroup}>
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="subject">Subject</label>
              <input
                type="text"
                id="subject"
                name="subject"
                value={formData.subject}
                onChange={handleInputChange}
                required
              />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="message">Message</label>
              <textarea
                id="message"
                name="message"
                rows="5"
                value={formData.message}
                onChange={handleInputChange}
                required
              ></textarea>
            </div>
            <div className={styles.formGroup}>
              <button type="submit" disabled={loading}>
                {loading ? "Submitting..." : "Submit"}
              </button>
            </div>
          </form>
        </div>
        <button
          onClick={handleButtonClickForContactUsPage}
          className={styles.goToMainPage}
        >
          Go Back
        </button>

        {error && <Alert severity="error">{error.message}</Alert>}
      </div>
    </div>
  );
};
