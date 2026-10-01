import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function MySchemes() {

    const [savedSchemes, setSavedSchemes] = useState([]);


    function loadSavedSchemes() {

        const schemes =
            JSON.parse(
                localStorage.getItem("savedSchemes")
            ) || [];

        setSavedSchemes(schemes);
    }


    useEffect(() => {

        loadSavedSchemes();

    }, []);


    function removeScheme(schemeId) {

        const updatedSchemes =
            savedSchemes.filter(
                (scheme) =>
                    String(scheme.scheme_id) !==
                    String(schemeId)
            );

        localStorage.setItem(
            "savedSchemes",
            JSON.stringify(updatedSchemes)
        );

        setSavedSchemes(updatedSchemes);
    }


    return (
        <div className="my-schemes-page">

            <div className="page-heading">

                <p className="small-title">
                    MY SCHEMES
                </p>

                <h1>
                    Saved Schemes
                </h1>

                <p>
                    Schemes you save will appear here.
                </p>

            </div>


            {savedSchemes.length === 0 ? (

                <div className="empty-state">

                    <div className="empty-icon">
                        ♡
                    </div>

                    <h2>
                        No saved schemes yet
                    </h2>

                    <p>
                        Explore schemes and save the ones
                        you want to keep for later.
                    </p>

                    <Link
                        to="/explore"
                        className="primary-button"
                    >
                        Explore Schemes
                    </Link>

                </div>

            ) : (

                <div className="scheme-grid">

                    {savedSchemes.map((scheme) => (

                        <div
                            className="scheme-card"
                            key={scheme.scheme_id}
                        >

                            <div className="scheme-card-top">

                                <span className="scheme-category">
                                    {scheme.category ||
                                        "Government Scheme"}
                                </span>

                                <button
                                    className="save-button"
                                    onClick={() =>
                                        removeScheme(
                                            scheme.scheme_id
                                        )
                                    }
                                >
                                    ♥
                                </button>

                            </div>


                            <h2>
                                {scheme.scheme_name}
                            </h2>


                            <p className="scheme-state">
                                {scheme.state ||
                                    "All India"}
                            </p>


                            <p className="scheme-description">

                                {scheme.description ||
                                    scheme.document ||
                                    "Government scheme information available."}

                            </p>


                            <div className="scheme-actions">

                                <Link
                                    to={`/scheme/${scheme.scheme_id}`}
                                    className="view-button"
                                >
                                    View Details
                                </Link>

                            </div>

                        </div>

                    ))}

                </div>

            )}

        </div>
    );
}


export default MySchemes;