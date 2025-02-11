import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <nav className="navbar">
      <h1>Gestion des Conversations</h1>
      <div>
        <Link to="/">📂 Conversations</Link>
        <Link to="/stats">📊 Statistiques</Link>
      </div>
    </nav>
  );
};

export default Header;
