import React, { useState } from "react";

const Filters = ({ onFilterChange }) => {
  const [filters, setFilters] = useState({
    gizmo_id: "",
    is_archived: "",
    model: ""
  });

  const handleChange = (e) => {
    const newFilters = { ...filters, [e.target.name]: e.target.value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="filters">
      <input type="text" name="gizmo_id" placeholder="Agent" onChange={handleChange} />
      <select name="is_archived" onChange={handleChange}>
        <option value="">Tous</option>
        <option value="1">Archivé</option>
        <option value="0">Actif</option>
      </select>
      <input type="text" name="model" placeholder="Modèle" onChange={handleChange} />
    </div>
  );
};

export default Filters;
