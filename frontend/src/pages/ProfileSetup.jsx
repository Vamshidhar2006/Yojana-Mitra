import { useState } from "react";
import { useNavigate } from "react-router-dom";

function ProfileSetup() {

    const navigate = useNavigate();

    const [profile, setProfile] = useState({
        age: "",
        state: "",
        occupation: "",
        income: "",
        gender: "",
        social_category: ""
    });


    function handleChange(event) {

        const { name, value } = event.target;

        setProfile({
            ...profile,
            [name]: value
        });
    }


    function handleSubmit(event) {

        event.preventDefault();


        const age = Number(profile.age);
        const income = Number(profile.income);


        if (age < 1 || age > 120) {

            alert("Please enter a valid age.");

            return;
        }


        if (income < 0) {

            alert("Income cannot be negative.");

            return;
        }


        const profileToSave = {
            age: age,
            state: profile.state,
            occupation: profile.occupation,
            income: income,
            gender: profile.gender,
            social_category: profile.social_category
        };


        localStorage.setItem(
            "yojanaProfile",
            JSON.stringify(profileToSave)
        );


        navigate("/dashboard");
    }


    return (
        <div className="profile-page">

            <div className="profile-box">

                <p className="small-title">
                    PROFILE SETUP
                </p>


                <h1>
                    Tell us about yourself
                </h1>


                <p>
                    This helps Yojana Mitra find government
                    schemes that may be relevant to you.
                </p>


                <form onSubmit={handleSubmit}>

                    {/* AGE */}

                    <label>
                        Age
                    </label>

                    <input
                        type="number"
                        name="age"
                        value={profile.age}
                        onChange={handleChange}
                        placeholder="Enter your age"
                        min="1"
                        max="120"
                        required
                    />


                    {/* STATE */}

                    <label>
                        State / Union Territory
                    </label>

                    <select
                        name="state"
                        value={profile.state}
                        onChange={handleChange}
                        required
                    >

                        <option value="">
                            Select your state
                        </option>

                        <option value="Andhra Pradesh">
                            Andhra Pradesh
                        </option>

                        <option value="Arunachal Pradesh">
                            Arunachal Pradesh
                        </option>

                        <option value="Assam">
                            Assam
                        </option>

                        <option value="Bihar">
                            Bihar
                        </option>

                        <option value="Chhattisgarh">
                            Chhattisgarh
                        </option>

                        <option value="Goa">
                            Goa
                        </option>

                        <option value="Gujarat">
                            Gujarat
                        </option>

                        <option value="Haryana">
                            Haryana
                        </option>

                        <option value="Himachal Pradesh">
                            Himachal Pradesh
                        </option>

                        <option value="Jharkhand">
                            Jharkhand
                        </option>

                        <option value="Karnataka">
                            Karnataka
                        </option>

                        <option value="Kerala">
                            Kerala
                        </option>

                        <option value="Madhya Pradesh">
                            Madhya Pradesh
                        </option>

                        <option value="Maharashtra">
                            Maharashtra
                        </option>

                        <option value="Manipur">
                            Manipur
                        </option>

                        <option value="Meghalaya">
                            Meghalaya
                        </option>

                        <option value="Mizoram">
                            Mizoram
                        </option>

                        <option value="Nagaland">
                            Nagaland
                        </option>

                        <option value="Odisha">
                            Odisha
                        </option>

                        <option value="Punjab">
                            Punjab
                        </option>

                        <option value="Rajasthan">
                            Rajasthan
                        </option>

                        <option value="Sikkim">
                            Sikkim
                        </option>

                        <option value="Tamil Nadu">
                            Tamil Nadu
                        </option>

                        <option value="Telangana">
                            Telangana
                        </option>

                        <option value="Tripura">
                            Tripura
                        </option>

                        <option value="Uttar Pradesh">
                            Uttar Pradesh
                        </option>

                        <option value="Uttarakhand">
                            Uttarakhand
                        </option>

                        <option value="West Bengal">
                            West Bengal
                        </option>

                        <option value="Andaman and Nicobar Islands">
                            Andaman and Nicobar Islands
                        </option>

                        <option value="Chandigarh">
                            Chandigarh
                        </option>

                        <option value="Dadra and Nagar Haveli and Daman and Diu">
                            Dadra and Nagar Haveli and Daman and Diu
                        </option>

                        <option value="Delhi">
                            Delhi
                        </option>

                        <option value="Jammu and Kashmir">
                            Jammu and Kashmir
                        </option>

                        <option value="Ladakh">
                            Ladakh
                        </option>

                        <option value="Lakshadweep">
                            Lakshadweep
                        </option>

                        <option value="Puducherry">
                            Puducherry
                        </option>

                    </select>


                    {/* OCCUPATION */}

                    <label>
                        Occupation
                    </label>

                    <select
                        name="occupation"
                        value={profile.occupation}
                        onChange={handleChange}
                        required
                    >

                        <option value="">
                            Select your occupation
                        </option>

                        <option value="Student">
                            Student
                        </option>

                        <option value="Farmer">
                            Farmer
                        </option>

                        <option value="Self Employed">
                            Self Employed
                        </option>

                        <option value="Government Employee">
                            Government Employee
                        </option>

                        <option value="Private Employee">
                            Private Employee
                        </option>

                        <option value="Business">
                            Business
                        </option>

                        <option value="Unemployed">
                            Unemployed
                        </option>

                        <option value="Homemaker">
                            Homemaker
                        </option>

                        <option value="Retired">
                            Retired
                        </option>

                        <option value="Other">
                            Other
                        </option>

                    </select>


                    {/* INCOME */}

                    <label>
                        Annual Family Income
                    </label>

                    <input
                        type="number"
                        name="income"
                        value={profile.income}
                        onChange={handleChange}
                        placeholder="Example: 300000"
                        min="0"
                        required
                    />

                    <p className="form-help">
                        Enter the approximate annual income of
                        your family, as some schemes use family
                        income for eligibility.
                    </p>


                    {/* GENDER */}

                    <label>
                        Gender
                    </label>

                    <select
                        name="gender"
                        value={profile.gender}
                        onChange={handleChange}
                        required
                    >

                        <option value="">
                            Select gender
                        </option>

                        <option value="Male">
                            Male
                        </option>

                        <option value="Female">
                            Female
                        </option>

                        <option value="Other">
                            Other
                        </option>

                    </select>


                    {/* SOCIAL CATEGORY */}

                    <label>
                        Social Category
                    </label>

                    <select
                        name="social_category"
                        value={profile.social_category}
                        onChange={handleChange}
                        required
                    >

                        <option value="">
                            Select category
                        </option>

                        <option value="General">
                            General
                        </option>

                        <option value="OBC">
                            OBC
                        </option>

                        <option value="SC">
                            SC
                        </option>

                        <option value="ST">
                            ST
                        </option>

                        <option value="EWS">
                            EWS
                        </option>

                    </select>


                    <button
                        type="submit"
                        className="primary-button"
                    >
                        Save Profile
                    </button>

                </form>

            </div>

        </div>
    );
}

export default ProfileSetup;