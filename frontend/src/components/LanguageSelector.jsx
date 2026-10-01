import { useEffect, useState } from "react";

function LanguageSelector() {
    const [language, setLanguage] = useState(() => {
        return localStorage.getItem("yojanaLanguage") || "English";
    });

    useEffect(() => {
        localStorage.setItem("yojanaLanguage", language);
    }, [language]);

    function handleChange(event) {
        setLanguage(event.target.value);
    }

    const languages = [
        "English",
        "Hindi",
        "Telugu",
        "Tamil",
        "Kannada",
        "Malayalam",
        "Marathi",
        "Gujarati",
        "Bengali",
        "Odia"
    ];

    return (
        <div className="language-selector">
            <label htmlFor="language">Language</label>

            <select
                id="language"
                value={language}
                onChange={handleChange}
            >
                {languages.map((item) => (
                    <option key={item} value={item}>
                        {item}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default LanguageSelector;