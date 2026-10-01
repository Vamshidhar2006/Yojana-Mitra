import { Link } from "react-router-dom";
import ProfileCard from "../components/ProfileCard";

function Profile() {

    const savedProfile = localStorage.getItem(
        "yojanaProfile"
    );

    const profile = savedProfile
        ? JSON.parse(savedProfile)
        : null;


    return (
        <div className="profile-view-page">

            <div className="page-heading">

                <p className="small-title">
                    MY PROFILE
                </p>

                <h1>
                    Your Information
                </h1>

                <p>
                    This information is used to personalize
                    your scheme recommendations.
                </p>

            </div>


            <ProfileCard profile={profile} />


            {profile ? (

                <Link to="/profile-setup">

                    <button className="primary-button">
                        Edit Profile
                    </button>

                </Link>

            ) : (

                <Link to="/profile-setup">

                    <button className="primary-button">
                        Set Up Profile
                    </button>

                </Link>

            )}

        </div>
    );
}

export default Profile;