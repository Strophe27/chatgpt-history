import React from "react";

const Sidebar = ({ selectedFolder, setSelectedFolder }) => {
  return (
    <div className="sidebar">
      <h3>📂 Dossiers</h3>
      <ul>
        <li className={selectedFolder === "Tous" ? "active" : ""} onClick={() => setSelectedFolder("Tous")}>📁 Tous</li>
        <li className={selectedFolder === "Travail" ? "active" : ""} onClick={() => setSelectedFolder("Travail")}>📁 Travail</li>
        <li className={selectedFolder === "Personnel" ? "active" : ""} onClick={() => setSelectedFolder("Personnel")}>📁 Personnel</li>
        <li className={selectedFolder === "Favoris" ? "active" : ""} onClick={() => setSelectedFolder("Favoris")}>⭐ Favoris</li>
      </ul>
    </div>
  );
};

export default Sidebar;
