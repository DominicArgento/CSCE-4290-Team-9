// BusinessList.js
import React from 'react';
import BusinessCard from './BusinessCard';

const BusinessList = ({ businesses }) => {
  return (
    <div>
      {businesses.map((business) => (
        <BusinessCard key={business.id} business={business} />
      ))}
    </div>
  );
};

export default BusinessList;


