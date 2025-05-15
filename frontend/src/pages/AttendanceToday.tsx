import React, { useEffect, useState } from "react";
import axios from "axios";
import { FaCalendarAlt, FaDownload, FaSearch } from "react-icons/fa";

const AttendanceToday = () => {
  interface AttendanceRow {
    NAME: string;
    Time: string;
    Date: string;
  }

  const [rows, setRows] = useState<AttendanceRow[]>([]);
  const [status, setStatus] = useState("");
  const [statusType, setStatusType] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchAttendanceData();
  }, []);

  const fetchAttendanceData = async () => {
    try {
      setIsLoading(true);
      const res = await axios.post("http://localhost:5000/whole");
      
      if (res.data && res.data.rows && res.data.rows.length > 0) {
        setRows(res.data.rows);
        setStatus("");
      } else {
        setStatus("No attendance records found for today.");
        setStatusType("info");
      }
    } catch (err) {
      setStatus("Failed to fetch attendance records. Please try again.");
      setStatusType("error");
    } finally {
      setIsLoading(false);
    }
  };

  const exportToCSV = () => {
    if (rows.length === 0) return;
    
    const csvRows = [];
    const headers = ['Name', 'Time', 'Date'];
    csvRows.push(headers.join(','));
    
    rows.forEach((row) => {
      const rowData = [
        `"${row.NAME}"`,
        `"${row.Time}"`,
        `"${row.Date}"`
      ];
      csvRows.push(rowData.join(','));
    });
    
    const csvString = csvRows.join('\n');
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', `attendance_export_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  const filteredRows = rows.filter(row => 
    row.NAME.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <>
      <div className="card">
        <div className="card-header">
          <h2>
            <FaCalendarAlt className="inline-block mr-2" />
            Today's Attendance
          </h2>
          <div>
            <button 
              className="btn btn-outline inline-flex items-center"
              onClick={exportToCSV}
              disabled={rows.length === 0}
            >
              <FaDownload className="mr-2" /> Export CSV
            </button>
          </div>
        </div>
        
        <div className="mb-4">
          <p className="text-gray-500">{currentDate}</p>
        </div>
        
        <div className="form-group">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
              <FaSearch className="text-gray-400" />
            </div>
            <input
              type="text"
              className="form-control pl-10"
              placeholder="Search by employee name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
        
        {isLoading ? (
          <div className="text-center py-4">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
            <p className="mt-2">Loading attendance records...</p>
          </div>
        ) : status ? (
          <div className={`alert alert-${statusType}`}>
            {status}
          </div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Time</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {filteredRows.length > 0 ? (
                  filteredRows.map((row, idx) => (
                    <tr key={idx}>
                      <td>{row.NAME}</td>
                      <td>{row.Time}</td>
                      <td>{row.Date}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={3} className="text-center py-4 text-gray-500">
                      {searchTerm ? "No matching records found" : "No attendance records available"}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
};

export default AttendanceToday;