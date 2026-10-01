import { useState } from "react";

function SearchBar({ onSearch }) {

    const [search, setSearch] = useState("");

    function handleSubmit(event) {

        event.preventDefault();

        if (onSearch) {
            onSearch(search);
        }
    }

    return (
        <form
            className="search-bar"
            onSubmit={handleSubmit}
        >

            <input
                type="text"
                placeholder="Search government schemes..."
                value={search}
                onChange={(event) =>
                    setSearch(event.target.value)
                }
            />

            <button type="submit">
                Search
            </button>

        </form>
    );
}

export default SearchBar;