import React, { useState } from 'react';
import SearchBar from './SearchBar';
import BusinessList from './BusinessList';
import './App.css'; // Import the CSS file for styling

function App() {
  const [businesses, setBusinesses] = useState([]);

  const handleSearch = (query) => {
    // Implement search functionality here
    // For now, let's just log the search query to the console
    console.log("Search query:", query);
    // Update businesses state with fetched data based on search query
    // For testing purposes, let's simulate some dummy data
    setBusinesses([
      { id: 1, name: "Business 1", address: "123 Main St", description: "A great place to eat." },
      { id: 2, name: "Business 2", address: "456 Elm St", description: "Awesome food and atmosphere." }
    ]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Sentiment Analysis Website</h1>
        <SearchBar onSearch={handleSearch} /> {/* Render the SearchBar component */}
        <BusinessList businesses={businesses} /> {/* Render the BusinessList component */}
      </header>
    </div>
  );
}

export default App;
