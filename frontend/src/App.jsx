import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Welcome from "./pages/Welcome";
import ProfileSetup from "./pages/ProfileSetup";
import Dashboard from "./pages/Dashboard";
import Explore from "./pages/Explore";
import Chat from "./pages/Chat";
import MySchemes from "./pages/MySchemes";
import SchemeDetails from "./pages/SchemeDetails";
import Profile from "./pages/Profile";

function App() {
    return (
        <BrowserRouter>

            <Navbar />

            <Routes>

                <Route
                    path="/"
                    element={<Welcome />}
                />

                <Route
                    path="/profile-setup"
                    element={<ProfileSetup />}
                />

                <Route
                    path="/dashboard"
                    element={<Dashboard />}
                />

                <Route
                    path="/explore"
                    element={<Explore />}
                />

                <Route
                    path="/chat"
                    element={<Chat />}
                />

                <Route
                    path="/my-schemes"
                    element={<MySchemes />}
                />

                <Route
                    path="/scheme/:id"
                    element={<SchemeDetails />}
                />

                <Route
                    path="/profile"
                    element={<Profile />}
                />

            </Routes>

        </BrowserRouter>
    );
}

export default App;