// src/pages/PowerBIDashboard.jsx
import React from "react";

const PowerBIDashboard = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-3xl font-semibold text-center mb-6">Attendance Dashboard</h2>
      <div className="flex justify-center">
        <iframe
          title="Attendance Dashboard"
          width="1140"
          height="541.25"
          src="https://app.powerbi.com/reportEmbed?reportId=828f9841-ff0a-4328-8535-ff9b38144c70&autoAuth=true&ctid=0b578d97-bb35-4c75-863a-9280b97ff86e"
          allowFullScreen={true}
          className="border rounded shadow-lg"
        ></iframe>
      </div>
    </div>
  );
};

export default PowerBIDashboard;
