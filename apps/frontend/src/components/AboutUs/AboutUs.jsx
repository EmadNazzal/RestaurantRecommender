import React from 'react';
import { useNavigate } from 'react-router-dom';
import { GitHub, LinkedIn } from '@mui/icons-material';
import Button from '@mui/material/Button';
import styles from './aboutUs.module.css';
import teamBg from '../../assets/images/meetTheTeam.jpg'; // Background image
import emmaImg from '../../assets/images/emma.jpeg';
import hanImg from '../../assets/images/han.jpeg';
import emadImg from '../../assets/images/index1.jpg';
import carloImg from '../../assets/images/carlo.png';
import riinImg from '../../assets/images/riin.jpg';



const teamMembers = [
  { name: 'Emma', role: 'Coordination Lead', avatar: emmaImg, github: 'https://github.com/emma-nolan',  linkedin: 'https://www.linkedin.com/in/emma-nolan-092363320/' },
  { name: 'Carlo', role: 'Data Lead', avatar: carloImg, github: 'https://github.com/Carlofinnegan', linkedin: 'https://www.linkedin.com/in/carlo-finnegan-830714246/' },
  { name: 'Riin', role: 'Backend Code Lead', avatar: riinImg, github: 'https://github.com/RiinKal', linkedin: 'https://www.linkedin.com/in/riin-kaljurand-1252a8ba/' },
  { name: 'Han', role: 'Maintenance Lead', avatar: hanImg, github: 'https://github.com/chugalugzzz', linkedin: 'https://www.linkedin.com/in/hanzhengbusiness/' },
  { name: 'Emad', role: 'Customer & Frontend Lead', avatar: emadImg, github: 'https://github.com/EmadNazzal', linkedin: 'https://www.linkedin.com/in/emadnazzal95/' },
];

// export default function AboutUs() {
//   const [currentIndex, setCurrentIndex] = useState(0);
//   const navigate = useNavigate();

//   const handlePrev = () => {
//     setCurrentIndex((prevIndex) => (prevIndex === 0 ? teamMembers.length - 1 : prevIndex - 1));
//   };

//   const handleNext = () => {
//     setCurrentIndex((prevIndex) => (prevIndex === teamMembers.length - 1 ? 0 : prevIndex + 1));
//   };

//   const handleGoBack = () => {
//     navigate('/');
//   };

//   return (
//     <div className={styles.page}>
//       <Button variant="contained" color="primary" sx={{width:"200px", position:"absolute", zIndex:"100000", top:"10px", left:"10px"}} onClick={handleGoBack}>
//         Go Back
//       </Button>

//       <div className={styles.heroSection}>
//         <img src={teamBg} alt="Team Background" className={styles.heroImage} />
//         <div className={styles.heroContent}>
//           <h1>Meet Our Team</h1>
//           <p>Get to know the amazing people behind our success.</p>
//         </div>
//       </div>

//       <div className={styles.sliderContainer}>
//         <button className={styles.navButton} onClick={handlePrev}>&lt;</button>
//         <div className={styles.slider}>
//           {teamMembers.map((member, index) => (
//             <div
//               key={index}
//               className={`${styles.teamMember} ${index === currentIndex ? styles.active : ''}`}
//             >
//               <img alt={`${member.name}'s avatar`} src={member.avatar} className={styles.avatar} />
//               <div className={styles.memberInfo}>
//                 <h2>{member.name}</h2>
//                 <p>{member.role}</p>
//                 <div className={styles.socialLinks}>
//                   <a href={`${member.github}`} target='_blank' className={styles.socialLink}><GitHub /></a>
//                   <a href={`${member.twitter}`} target='_blank' className={styles.socialLink}><Twitter /></a>
//                   <a href={`${member.facebook}`} target='_blank' className={styles.socialLink}><Facebook /></a>
//                   <a href={`${member.linkedin}`} target='_blank' className={styles.socialLink}><LinkedIn /></a>
//                 </div>
//               </div>
//             </div>
//           ))}
//         </div>
//         <button className={styles.navButton} onClick={handleNext}>&gt;</button>
//       </div>

//       <footer className={styles.footer}>
//         <div className={styles.footerContent}>
//           <div className={styles.footerLinks}>
//             <a href="/privacy-policy" className={styles.footerLink}>Privacy Policy</a>
//             <a href="/terms-of-service" className={styles.footerLink}>Terms of Service</a>
//             <a href="/contact-us" className={styles.footerLink}>Contact Us</a>
//           </div>
//           <div className={styles.footerInfo}>
//             <p>© 2024 Nibbler. All rights reserved.</p>
//             <p>Dublin 4, Dublin, Ireland</p>
//             <p>Email: info@company.com</p>
//           </div>
//         </div>
//       </footer>
//     </div>
//   );
// }

export default function AboutUs() {
  const navigate = useNavigate();

  const handleGoBack = () => {
    navigate('/');
  };

  return (
    <div className={styles.page}>
      <Button variant="contained" color="primary" sx={{ width: "200px", position: "absolute", zIndex: "100000", top: "10px", left: "10px" }} onClick={handleGoBack}>
        Go Back
      </Button>

      <div className={styles.heroSection}>
        <img src={teamBg} alt="Team Background" className={styles.heroImage} />
        <div className={styles.heroContent}>
          <h1>Meet Our Team</h1>
          <p>Get to know the amazing people behind our success.</p>
        </div>
      </div>

      <div className={styles.teamContainer}>
        {teamMembers.map((member, index) => (
          <div key={index} className={styles.teamMember}>
            <img alt={`${member.name}'s avatar`} src={member.avatar} className={styles.avatar} />
            <div className={styles.memberInfo}>
              <h2>{member.name}</h2>
              <p>{member.role}</p>
              <div className={styles.socialLinks}>
                <a href={`${member.github}`} target='_blank' className={styles.socialLink}><GitHub /></a>
                {/* <a href={`${member.twitter}`} target='_blank' className={styles.socialLink}><Twitter /></a>
                <a href={`${member.facebook}`} target='_blank' className={styles.socialLink}><Facebook /></a> */}
                <a href={`${member.linkedin}`} target='_blank' className={styles.socialLink}><LinkedIn /></a>
              </div>
            </div>
          </div>
        ))}
      </div>

      <footer className={styles.footer}>
        <div className={styles.footerContent}>
          <div className={styles.footerLinks}>
            {/* <a href="/privacy-policy" className={styles.footerLink}>Privacy Policy</a>
            <a href="/terms-of-service" className={styles.footerLink}>Terms of Service</a>
            <a href="/contact-us" className={styles.footerLink}>Contact Us</a> */}
          </div>
          <div className={styles.footerInfo}>
            <p>Â© 2024 Nibbler. All rights reserved.</p>
            <p>Dublin 4, Dublin, Ireland</p>
            {/* <p>Email: info@company.com</p> */}
          </div>
        </div>
      </footer>
    </div>
  );
}