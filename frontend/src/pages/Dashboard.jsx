import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

import ProfileCard from "../components/ProfileCard";
import SchemeCard from "../components/SchemeCard";

function Dashboard() {

    const [profile, setProfile] = useState(null);
    const [schemes, setSchemes] = useState([]);
    const [loading, setLoading] = useState(true);

    const apiBaseUrl =
        window.location.hostname === "localhost"
            ? "http://127.0.0.1:8000"
            : "";

    useEffect(() => {

        // Get profile if the user has already created one
        const savedProfile =
            localStorage.getItem("yojanaProfile");

        if (savedProfile) {

            try {

                setProfile(
                    JSON.parse(savedProfile)
                );

            } catch (error) {

                console.error(
                    "Error reading profile:",
                    error
                );

            }
        }

        // Load public schemes
        async function loadSchemes() {

            try {

                const response = await axios.get(
                    `${apiBaseUrl}/api/schemes`
                );

                setSchemes(
                    response.data.schemes
                );

            } catch (error) {

                console.error(
                    "Error loading schemes:",
                    error
                );

            } finally {

                setLoading(false);

            }
        }

        loadSchemes();

    }, []);

    return (

        <div className="dashboard">

            <div className="dashboard-top">

                <div>

                    <p className="small-title">
                        {profile
                            ? "PERSONALIZED DASHBOARD"
                            : "GOVERNMENT SCHEMES"}
                    </p>

                    <h1>
                        Welcome to Yojana Mitra
                    </h1>

                    <p>
                        Discover government schemes that
                        may be relevant to you.
                    </p>

                </div>

            </div>

            {profile ? (

                <div className="dashboard-profile">

                    <ProfileCard
                        profile={profile}
                    />

                </div>

            ) : (

                <div className="dashboard-profile">

                    <div className="profile-card">

                        <h3>
                            Make your experience more personal
                        </h3>

                        <p>
                            Add your basic profile information
                            to discover schemes that may be
                            relevant to you.
                        </p>

                        <Link
                            to="/profile-setup"
                            className="primary-button"
                        >
                            Set Up My Profile
                        </Link>

                    </div>

                </div>

            )}

            <div className="dashboard-cards">

                <Link
                    to="/explore"
                    className="dashboard-card"
                >

                    <div className="card-icon">
                        🔎
                    </div>

                    <h2>
                        Explore Schemes
                    </h2>

                    <p>
                        Browse government schemes by
                        category, state and other filters.
                    </p>

                </Link>

                <Link
                    to="/chat"
                    className="dashboard-card"
                >

                    <div className="card-icon">
                        💬
                    </div>

                    <h2>
                        Ask Yojana Mitra
                    </h2>

                    <p>
                        Ask questions and get personalized
                        scheme information.
                    </p>

                </Link>

                <Link
                    to="/my-schemes"
                    className="dashboard-card"
                >

                    <div className="card-icon">
                        ❤️
                    </div>

                    <h2>
                        My Schemes
                    </h2>

                    <p>
                        View the schemes you have saved
                        or recently explored.
                    </p>

                </Link>

            </div>

            <div className="scheme-section">

                <div className="section-heading">

                    <p className="small-title">
                        AVAILABLE SCHEMES
                    </p>

                    <h2>
                        Explore Government Schemes
                    </h2>

                    <p>
                        Browse schemes available across
                        India without needing to log in.
                    </p>

                </div>

                {loading && (

                    <p>
                        Loading schemes...
                    </p>

                )}

                {!loading &&
                    schemes.length === 0 && (

                        <p>
                            Schemes could not be loaded
                            right now. Please try again.
                        </p>

                    )}

                {!loading &&
                    schemes.length > 0 && (

                        <div className="scheme-grid">

                            {schemes
                                .slice(0, 6)
                                .map((scheme) => (

                                    <SchemeCard
                                        key={scheme.scheme_id}
                                        scheme={scheme}
                                    />

                                ))}

                        </div>

                    )}

            </div>

            <div className="map-preview">

                <h2>
                    Explore Schemes Across India
                </h2>

                <p>
                    Select a state to discover government
                    schemes available in that region.
                </p>

                <Link to="/explore">

                    <button className="primary-button">
                        Explore India
                    </button>

                </Link>

            </div>

        </div>

    );

}

export default Dashboard;