import React, { useState } from 'react';

const TreePanel = ({ treeData, setSelectedDoctor }) => {
  const [expanded, setExpanded] = useState({});

  const toggleExpand = (dept) => {
    setExpanded((prev) => ({
      ...prev,
      [dept]: !prev[dept]
    }));
  };

  return (
    <div className="tree-container">
      <h3 className="section-title">🏥 Hospital Hierarchy</h3>
      <div className="tree-root">
        <div className="tree-item main-root">
          <span className="icon">🏛️</span> Departments
        </div>
        <div className="tree-children">
          {Object.entries(treeData).map(([dept, doctors]) => (
            <div key={dept} className="tree-branch">
              <div 
                className={`tree-item dept-item ${expanded[dept] ? 'expanded' : ''}`} 
                onClick={() => toggleExpand(dept)}
              >
                <span className="toggle-icon">{expanded[dept] ? '▼' : '▶'}</span>
                <span className="icon">📁</span> {dept}
              </div>
              {expanded[dept] && (
                <div className="tree-sub-children">
                  {doctors.map((doctor) => (
                    <div 
                      key={doctor.id} 
                      className="tree-item doc-item"
                      onClick={() => setSelectedDoctor(doctor)}
                    >
                      <span className="icon">👨‍⚕️</span> {doctor.name}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TreePanel;
