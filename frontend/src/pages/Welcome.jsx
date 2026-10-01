import { Link } from "react-router-dom";

function Welcome() {

    return (
        <div className="welcome-page">

            <div className="welcome-content">

                <p className="small-title">
                    YOUR GOVERNMENT SCHEME COMPANION
                </p>

                <h1>
                    Find the schemes
                    <br />
                    meant for you.
                </h1>

                <p className="welcome-text">
                    Yojana Mitra helps you discover government
                    schemes based on your profile, location
                    and needs.
                </p>

                <Link to="/profile-setup">
                    <button className="primary-button">
                        Get Started
                    </button>
                </Link>

            </div>

        </div>
    );
}

export default Welcome;