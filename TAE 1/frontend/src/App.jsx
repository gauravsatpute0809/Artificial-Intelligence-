import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import ChatPanel from './components/ChatPanel';
import TreePanel from './components/TreePanel';

function App() {
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [treeData, setTreeData] = useState({});

  useEffect(() => {
    fetch('/get_doctors')
      .then(res => res.json())
      .then(data => setTreeData(data))
      .catch(err => console.error("Error fetching doctors:", err));
  }, []);

  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <div className="panel chatbot-panel">
          <ChatPanel selectedDoctor={selectedDoctor} setSelectedDoctor={setSelectedDoctor} />
        </div>
        <div className="panel tree-panel">
          <TreePanel treeData={treeData} setSelectedDoctor={setSelectedDoctor} />
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;
