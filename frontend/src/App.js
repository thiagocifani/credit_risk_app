import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UserList from "./components/UserList";
import CreateUser from "./components/CreateUser";
import UserShow from "./components/UserShow";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UserList />} />
        <Route path="/users/new" element={<CreateUser />} />
        <Route path="/users/:id" element={<UserShow />} />
      </Routes>
    </Router>
  );
}

export default App;
