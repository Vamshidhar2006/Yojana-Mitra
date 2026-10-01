import { Link } from "react-router-dom";
import { useState } from "react";

function SchemeCard({ scheme }) {

    const [saved, setSaved] = useState(() => {

        const savedSchemes =
            JSON.parse(
                localStorage.getItem("savedSchemes")
            ) || [];

        return savedSchemes.some(
            (item) =>
                String(item.scheme_id) ===
                String(scheme.scheme_id)
        );
    });


    function handleSave() {

        const savedSchemes =
            JSON.parse(
                localStorage.getItem("savedSchemes")
            ) || [];


        if (saved) {

            const updatedSchemes =
                savedSchemes.filter(
                    (item) =>
                        String(item.scheme_id) !==
                        String(scheme.scheme_id)
                );

            localStorage.setItem(
                "savedSchemes",
                JSON.stringify(updatedSchemes)
            );

            setSaved(false);

        } else {

            savedSchemes.push(scheme);

            localStorage.setItem(
                "savedSchemes",
                JSON.stringify(savedSchemes)
            );

            setSaved(true);
        }
    }


    return (
        <div className="scheme-card">

            <div className="scheme-card-top">

                <span className="scheme-category">
                    {scheme.category ||
                        "Government Scheme"}
                </span>


                <button
                    className="save-button"
                    onClick={handleSave}
                    aria-label={
                        saved
                            ? "Remove saved scheme"
                            : "Save scheme"
                    }
                >
                    {saved ? "♥" : "♡"}
                </button>

            </div>


            <h2>
                {scheme.scheme_name}
            </h2>


            <p className="scheme-state">
                {scheme.state || "All India"}
            </p>


            <p className="scheme-description">

                {scheme.description ||
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
    );
}


export default SchemeCard;