import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

function SchemeDetails() {

    const { id } = useParams();

    const [scheme, setScheme] = useState(null);
    const [loading, setLoading] = useState(true);

    const apiBaseUrl =
        window.location.hostname === "localhost"
            ? "http://127.0.0.1:8000"
            : "";

    useEffect(() => {

        async function loadScheme() {

            try {

                const response = await axios.get(
                    `${apiBaseUrl}/api/schemes/${id}`
                );

                if (response.data.error) {
                    setScheme(null);
                } else {
                    setScheme(response.data);
                }

            } catch (error) {

                console.error(
                    "Error loading scheme:",
                    error
                );

                setScheme(null);

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
                    Loading...
                </h1>

            </div>
        );

    }

    if (!scheme) {

        return (
            <div className="scheme-details-page">

                <p className="small-title">
                    SCHEME DETAILS
                </p>

                <h1>
                    Scheme not found
                </h1>

                <p>
                    Unable to load scheme details.
                </p>

                <Link
                    to="/explore"
                    className="view-button"
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

            <p className="scheme-state">
                {scheme.state || "All India"}
            </p>

            <div className="scheme-detail-card">

                <h3>
                    Category
                </h3>

                <p>
                    {scheme.category || "Government Scheme"}
                </p>

                <h3>
                    Benefits
                </h3>

                <p>
                    {scheme.benefits ||
                        "Information not available."}
                </p>

                <h3>
                    Eligibility
                </h3>

                <p>
                    {scheme.eligibility ||
                        "Eligibility information not available."}
                </p>

                <h3>
                    Required Documents
                </h3>

                <p>
                    {scheme.required_documents ||
                        "Information not available."}
                </p>

                <h3>
                    Application Process
                </h3>

                <p>
                    {scheme.application_process ||
                        "Application process information not available."}
                </p>

                {scheme.official_source_url && (

                    <a
                        href={scheme.official_source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="view-button"
                    >
                        Official Source
                    </a>

                )}

            </div>

        </div>

    );

}

export default SchemeDetails;