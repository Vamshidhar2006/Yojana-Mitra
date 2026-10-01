import { useState } from "react";
import india from "@svg-maps/india";

function IndiaMap({ onStateSelect }) {

    const [selectedState, setSelectedState] = useState("");

    function handleStateClick(location) {

        const stateName = location.name;

        setSelectedState(stateName);

        if (onStateSelect) {
            onStateSelect(stateName);
        }
    }

    return (
        <div className="india-map-container">

            <div className="india-map-header">

                <div>

                    <p className="small-title">
                        EXPLORE INDIA
                    </p>

                    <h2>
                        Discover schemes by state
                    </h2>

                    <p>
                        Select a state to explore government
                        schemes available in that region.
                    </p>

                </div>

                {selectedState && (
                    <div className="selected-state">

                        <span>
                            Selected state
                        </span>

                        <strong>
                            {selectedState}
                        </strong>

                    </div>
                )}

            </div>

            <div className="india-map">

                <svg
                    viewBox={india.viewBox}
                    className="india-svg-map"
                    role="img"
                    aria-label="Map of India"
                >

                    {india.locations.map((location) => (

                        <path
                            key={location.id}
                            d={location.path}
                            name={location.name}
                            className="svg-map-location"
                            onClick={() => handleStateClick(location)}
                            tabIndex="0"
                            role="button"
                            aria-label={location.name}
                            onKeyDown={(event) => {

                                if (
                                    event.key === "Enter" ||
                                    event.key === " "
                                ) {
                                    handleStateClick(location);
                                }

                            }}
                        />

                    ))}

                </svg>

            </div>

        </div>
    );
}

export default IndiaMap;