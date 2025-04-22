import { Link,useNavigate } from "react-router-dom";
import clock from "../../assets/icons/clock.png";
import brainstrom from "../../assets/icons/brainstorm.png";
import man_walking from "../../assets/icons/man-walking.png";
import spiral from "../../assets/icons/spiral.png";
import handleLogout from "../helpers/handle_logout";

import "../../style/Home.css";

const Home = () => {

  const navigate = useNavigate();

  return (
    <div className="home-wrapper">
      <nav className="navbar">
        <div className="nav-logo">Parkinsons Prediction</div>
        <div className="nav-links">
          <Link to="/home">Home</Link>
          <Link to="/spiral">Spiral</Link>
          <Link to="/gait">Gait</Link>
          <Link to="/bradykinesia">Bradykinesia</Link>
          <Link to="/tremors">Tremors</Link>
          <button onClick={()=>handleLogout(navigate)} >Logout</button>
        </div>
      </nav>

      <main className="home-container">
        <div className="home-header">
          <h1>Parkinson's Disease</h1>
          <p>
            Parkinson's disease is a progressive neurological disorder that affects movement.
            It develops gradually, sometimes starting with a barely noticeable tremor in just one hand.
            While tremors are common, the disorder also commonly causes stiffness or slowing of movement.
          </p>

          <h2>Early Detection Using MDS-UPDRS</h2>
          <p>
            Our application uses the Movement Disorder Society Unified Parkinson's Disease Rating Scale (MDS-UPDRS)
            to help in early detection of Parkinson’s disease through the following symptoms:
          </p>
        </div>

        <div className="module-section">
          <Link to="/spiral" className="module-card">
            <img src={spiral}  />
            <div className="module-info">
              <span className="module-title">Spiral Drawing</span>
              <span className="module-desc">Analyzing spiral drawings for signs of bradykinesia and tremors</span>
            </div>
          </Link>

          <Link to="/gait" className="module-card">
            <img src={man_walking} />
            <div className="module-info">
              <span className="module-title">Gait Analysis</span>
              <span className="module-desc">Evaluating walking patterns for inconsistencies and freezing</span>
            </div>
          </Link>

          <Link to="/bradykinesia" className="module-card">
            <img src={clock} />
            <div className="module-info">
              <span className="module-title">Bradykinesia</span>
              <span className="module-desc">Measuring slowness of movement through finger tapping</span>
            </div>
          </Link>

          <Link to="/tremors" className="module-card">
            <img src={brainstrom} />
            <div className="module-info">
              <span className="module-title">Rest Tremors</span>
              <span className="module-desc">Analyzing hand rest tremors for intensity and frequency</span>
            </div>
          </Link>
        </div>
      </main>
    </div>
  );
};

export default Home;
