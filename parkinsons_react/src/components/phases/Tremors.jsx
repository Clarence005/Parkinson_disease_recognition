import { Link } from "react-router-dom";
import "../../style/Nav.css";

export default function Tremors(){
    return <div className="wrapper">
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
        <h1>Tremors Test - Comming soon...</h1>
    </div>
}