import { Link } from "react-router-dom";

function Navbar() {
    return (
        <nav className="navbar">

            <Link to="/" className="logo">
                Yojana Mitra
            </Link>

            <div className="nav-links">

                <Link to="/dashboard">
                    Dashboard
                </Link>

                <Link to="/explore">
                    Explore
                </Link>

                <Link to="/chat">
                    Ask Yojana Mitra
                </Link>

                <Link to="/my-schemes">
                    My Schemes
                </Link>

                <Link to="/profile">
                    Profile
                </Link>

            </div>

        </nav>
    );
}

export default Navbar;