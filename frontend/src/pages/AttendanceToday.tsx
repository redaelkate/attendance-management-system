import React from "react";

const AttendanceToday = () => {
  return (
    <div className="powerbi-container">
      <iframe
        title="dataset TP police-department-incidents"
        width="1280"
        height="720"
        src="https://app.powerbi.com/reportEmbed?reportId=397853d9-a2e2-42a3-b690-8aeed2d3fa0c&autoAuth=true&ctid=0b578d97-bb35-4c75-863a-9280b97ff86e&actionBarEnabled=true"
        frameBorder="0"
        allowFullScreen={true}
      ></iframe>
    </div>
  );
};

export default AttendanceToday;