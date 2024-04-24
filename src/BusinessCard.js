// BusinessCard.js
import React from 'react';

const BusinessCard = ({ business }) => {
  return (
    <div className="business-card">
      <h2>{business.name}</h2>
      <p>{business.address}</p>
      <p>{business.description}</p>
      {/* Display sentiment analysis results */}
    </div>
  );
};

export default BusinessCard;

