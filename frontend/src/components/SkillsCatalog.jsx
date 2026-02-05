import React, { useState, useEffect } from 'react';
import './SkillsCatalog.css';

const SkillsCatalog = () => {
  const [skills, setSkills] = useState([]);
  const [categories, setCategories] = useState([]);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedType, setSelectedType] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCategories();
    fetchSkills();
  }, []);

  useEffect(() => {
    fetchSkills();
  }, [selectedCategory, selectedType]);

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/skills/categories');
      const data = await response.json();
      setCategories(data.parent_categories);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  };

  const fetchSkills = async () => {
    try {
      const params = new URLSearchParams();
      if (selectedCategory !== 'all') params.append('category', selectedCategory);
      if (selectedType !== 'all') params.append('skill_type', selectedType);
      if (search) params.append('search', search);

      const response = await fetch(`http://localhost:8000/api/skills/catalog?${params}`);
      const data = await response.json();
      setSkills(data.skills);
      setLoading(false);
    } catch (err) {
      console.error('Failed to load skills:', err);
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchSkills();
  };

  const groupedSkills = skills.reduce((acc, skill) => {
    const category = skill.category || 'Uncategorized';
    if (!acc[category]) acc[category] = [];
    acc[category].push(skill);
    return acc;
  }, {});

  return (
    <div className="skills-catalog">
      <div className="catalog-header">
        <h1>Skills Catalog</h1>
        <p>Explore 300+ technical skills across multiple domains</p>
      </div>

      <div className="filters">
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="search"
            placeholder="Search skills..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-btn">Search</button>
        </form>

        <div className="filter-group">
          <label>Type:</label>
          <select
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Skills</option>
            <option value="tech">Technology Skills</option>
            <option value="data">Data Skills</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Category:</label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Categories</option>
            {categories.map(cat => (
              <option key={cat.name} value={cat.name}>
                {cat.name} ({cat.count})
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading skills...</div>
      ) : (
        <div className="skills-results">
          <div className="results-header">
            <h2>Found {skills.length} skills</h2>
          </div>

          <div className="skills-grid">
            {Object.entries(groupedSkills).map(([category, categorySkills]) => (
              <div key={category} className="category-group">
                <h3 className="category-title">
                  {category}
                  <span className="skill-count">({categorySkills.length})</span>
                </h3>
                <div className="skills-list">
                  {categorySkills.map(skill => (
                    <div key={skill.id} className="skill-card">
                      <div className="skill-header">
                        <h4>{skill.name}</h4>
                        {skill.skill_category && (
                          <span className={`skill-badge ${skill.skill_category.toLowerCase()}`}>
                            {skill.skill_category}
                          </span>
                        )}
                      </div>
                      {skill.description && (
                        <p className="skill-description">{skill.description}</p>
                      )}
                      {skill.roles && (
                        <div className="skill-roles">
                          <strong>Roles:</strong> {skill.roles}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {skills.length === 0 && (
            <div className="no-results">
              <p>No skills found matching your criteria</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SkillsCatalog;
