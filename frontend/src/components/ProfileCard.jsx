function ProfileCard({ profile }) {

    if (!profile) {
        return (
            <div className="profile-card">

                <h3>
                    Your Profile
                </h3>

                <p>
                    Profile information is not available.
                </p>

            </div>
        );
    }

    return (
        <div className="profile-card">

            <h3>
                Your Profile
            </h3>

            <div className="profile-details">

                <p>
                    <strong>Age:</strong> {profile.age}
                </p>

                <p>
                    <strong>State:</strong> {profile.state}
                </p>

                <p>
                    <strong>Occupation:</strong> {profile.occupation}
                </p>

                <p>
                    <strong>Income:</strong> ₹{profile.income}
                </p>

                <p>
                    <strong>Gender:</strong> {profile.gender}
                </p>

                <p>
                    <strong>Category:</strong> {profile.social_category}
                </p>

            </div>

        </div>
    );
}

export default ProfileCard;