import { useState } from "react";
import { Link } from "react-router-dom";

function Navbar() {

    const [menuOpen, setMenuOpen] = useState(false);

    function closeMenu() {
        setMenuOpen(false);
    }

    return (
        <nav className="navbar">

            <Link
                to="/"
                className="logo"
                onClick={closeMenu}
            >
                Yojana Mitra
            </Link>

            <button
                className="menu-button"
                onClick={() => setMenuOpen(!menuOpen)}
                aria-label="Toggle menu"
            >
                ☰
            </button>

            <div
                className={`nav-links ${
                    menuOpen ? "mobile-open" : ""
                }`}
            >

                <Link
                    to="/dashboard"
                    onClick={closeMenu}
                >
                    Dashboard
                </Link>

                <Link
                    to="/explore"
                    onClick={closeMenu}
                >
                    Explore
                </Link>

                <Link
                    to="/chat"
                    onClick={closeMenu}
                >
                    Ask Yojana Mitra
                </Link>

                <Link
                    to="/yojana-lm-chat"
                    onClick={closeMenu}
                >
                    Ask YojanaLM
                </Link>

                <Link
                    to="/my-schemes"
                    onClick={closeMenu}
                >
                    My Schemes
                </Link>

                <Link
                    to="/profile"
                    onClick={closeMenu}
                >
                    Profile
                </Link>

            </div>

        </nav>
    );
}

export default Navbar;