import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

function SchemeDetails() {

    const { id } = useParams();

    const [scheme, setScheme] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {

        async function loadScheme() {

            try {

                const response = await axios.get(
                    `http://127.0.0.1:8000/api/schemes/${id}`
                );

                if (response.data.error) {

                    setError("Scheme not found.");

                } else {

                    setScheme(response.data);

                }

            } catch (error) {

                console.error(
                    "Error loading scheme:",
                    error
                );

                setError(
                    "Unable to load scheme details."
                );

            } finally {

                setLoading(false);

            }
        }

        loadScheme();

    }, [id]);


    if (loading) {

        return (
            <div className="scheme-details-page">

                <p className="small-title">
                    SCHEME DETAILS
                </p>

                <h1>
                    Loading scheme...
                </h1>

            </div>
        );

    }


    if (error || !scheme) {

        return (
            <div className="scheme-details-page">

                <p className="small-title">
                    SCHEME DETAILS
                </p>

                <h1>
                    Scheme not found
                </h1>

                <p>
                    {error}
                </p>

                <Link
                    to="/explore"
                    className="primary-button"
                >
                    Back to Explore
                </Link>

            </div>
        );

    }


    return (
        <div className="scheme-details-page">

            <p className="small-title">
                SCHEME DETAILS
            </p>


            <h1>
                {scheme.scheme_name}
            </h1>


            <p>
                {scheme.state || "All India"}
            </p>


            <div className="details-section">

                <h2>
                    About the Scheme
                </h2>

                <p>
                    {scheme.description ||
                        scheme.document ||
                        "Information about this scheme is not available."}
                </p>

            </div>


            <div className="details-section">

                <h2>
                    Eligibility
                </h2>

                <p>
                    {scheme.eligibility ||
                        "Eligibility information is not available."}
                </p>

            </div>


            <div className="details-section">

                <h2>
                    Benefits
                </h2>

                <p>
                    {scheme.benefits ||
                        "Benefit information is not available."}
                </p>

            </div>


            <div className="details-section">

                <h2>
                    Required Documents
                </h2>

                <p>
                    {scheme.required_documents ||
                        "Required document information is not available."}
                </p>

            </div>


            <div className="details-section">

                <h2>
                    Application Process
                </h2>

                <p>
                    {scheme.application_process ||
                        "Application process information is not available."}
                </p>

            </div>


            <div className="details-section">

                <h2>
                    Scheme Information
                </h2>

                <p>
                    <strong>Category:</strong>{" "}
                    {scheme.category || "Not specified"}
                </p>

                <p>
                    <strong>Occupation:</strong>{" "}
                    {scheme.occupation || "Not specified"}
                </p>

                <p>
                    <strong>Gender:</strong>{" "}
                    {scheme.gender || "Not specified"}
                </p>

                <p>
                    <strong>Age:</strong>{" "}
                    {scheme.min_age || "Not specified"}
                    {" - "}
                    {scheme.max_age || "Not specified"}
                </p>

                <p>
                    <strong>Income Limit:</strong>{" "}
                    {scheme.income_limit || "Not specified"}
                </p>

                <p>
                    <strong>Social Category:</strong>{" "}
                    {scheme.social_category || "Not specified"}
                </p>

            </div>


            <div className="details-section">

                <h2>
                    Official Information
                </h2>


                {scheme.application_url && (

                    <p>
                        <strong>
                            Application:
                        </strong>{" "}

                        <a
                            href={scheme.application_url}
                            target="_blank"
                            rel="noreferrer"
                        >
                            Apply for this scheme
                        </a>
                    </p>

                )}


                {scheme.official_source_url && (

                    <p>
                        <strong>
                            Official Source:
                        </strong>{" "}

                        <a
                            href={scheme.official_source_url}
                            target="_blank"
                            rel="noreferrer"
                        >
                            View Official Source
                        </a>
                    </p>

                )}


                {scheme.last_verified_date && (

                    <p>
                        <strong>
                            Last Verified:
                        </strong>{" "}
                        {scheme.last_verified_date}
                    </p>

                )}

            </div>


            <Link
                to="/explore"
                className="primary-button"
            >
                Back to Explore
            </Link>

        </div>
    );
}


export default SchemeDetails;