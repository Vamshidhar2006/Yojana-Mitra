import { useEffect, useState } from "react";
import axios from "axios";

import SearchBar from "../components/SearchBar";
import IndiaMap from "../components/IndiaMap";
import SchemeCard from "../components/SchemeCard";

function Explore() {

    const [selectedState, setSelectedState] = useState("");
    const [schemes, setSchemes] = useState([]);
    const [featuredSchemes, setFeaturedSchemes] = useState([]);
    const [loading, setLoading] = useState(false);


    // Load a few schemes when Explore page opens
    useEffect(() => {

        async function loadFeaturedSchemes() {

            try {

                const response = await axios.get(
                    "http:///api/schemes"
                );

                setFeaturedSchemes(
                    response.data.schemes.slice(0, 6)
                );

            } catch (error) {

                console.error(
                    "Error loading schemes:",
                    error
                );

            }
        }

        loadFeaturedSchemes();

    }, []);


    function handleSearch(searchText) {

        console.log(
            "Searching for:",
            searchText
        );

    }


    async function handleStateSelect(stateName) {

        setSelectedState(stateName);
        setLoading(true);

        try {

            const response = await axios.get(
                "http:///api/schemes",
                {
                    params: {
                        state: stateName
                    }
                }
            );

            setSchemes(
                response.data.schemes
            );

        } catch (error) {

            console.error(
                "Error loading schemes:",
                error
            );

            setSchemes([]);

        } finally {

            setLoading(false);

        }
    }


    return (
        <div className="explore-page">

            <div className="page-heading">

                <p className="small-title">
                    EXPLORE
                </p>

                <h1>
                    Discover Government Schemes
                </h1>

                <p>
                    Explore schemes from across India
                    or search for something specific.
                </p>

            </div>


            <SearchBar
                onSearch={handleSearch}
            />


            <IndiaMap
                onStateSelect={handleStateSelect}
            />


            {/* Featured schemes */}

            {!selectedState &&
                featuredSchemes.length > 0 && (

                <div className="scheme-section">

                    <div className="section-heading">

                        <p className="small-title">
                            EXPLORE
                        </p>

                        <h2>
                            Government Schemes
                        </h2>

                        <p>
                            Browse a few schemes from
                            our collection.
                        </p>

                    </div>


                    <div className="scheme-grid">

                        {featuredSchemes.map(
                            (scheme) => (

                            <SchemeCard
                                key={scheme.scheme_id}
                                scheme={scheme}
                            />

                        ))}

                    </div>

                </div>

            )}


            {/* Selected state */}

            {selectedState && (

                <div className="selected-state-results">

                    <p className="small-title">
                        SELECTED STATE
                    </p>

                    <h2>
                        Schemes in {selectedState}
                    </h2>

                    {loading && (
                        <p>
                            Loading schemes...
                        </p>
                    )}

                    {!loading &&
                        schemes.length === 0 && (
                        <p>
                            No schemes found for this state.
                        </p>
                    )}

                </div>

            )}


            {/* State schemes */}

            {selectedState &&
                !loading &&
                schemes.length > 0 && (

                <div className="scheme-section">

                    <div className="section-heading">

                        <p className="small-title">
                            AVAILABLE SCHEMES
                        </p>

                        <h2>
                            Schemes in {selectedState}
                        </h2>

                    </div>


                    <div className="scheme-grid">

                        {schemes.map(
                            (scheme) => (

                            <SchemeCard
                                key={scheme.scheme_id}
                                scheme={scheme}
                            />

                        ))}

                    </div>

                </div>

            )}

        </div>
    );
}

export default Explore;