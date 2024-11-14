import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import api from "../api";

interface AuthorsProps {
  id: number;
  author: string;
}

const Dashboard: React.FC = () => {
  const [authors, setAuthors] = useState<AuthorsProps[]>([]);

  const fetchAuthors = async (): Promise<void> => {
    try {
      const response = await api.get("/author/");
      setAuthors(response.data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    fetchAuthors();
  }, []);
  return (
    <>
        <Header />

      <div className="container text-center mt-5">
        <table
          className="table"
          style={{
            width: "100%",
            borderCollapse: "collapse",
            backgroundColor: "#bcb8b1",
            color: "#463f3a",
          }}
        >
          <thead style={{ backgroundColor: "#e0afa0" }}>
            <tr>
              <th style={{ padding: "10px", border: "1px solid #8a817c" }}>
                Id
              </th>
              <th style={{ padding: "10px", border: "1px solid #8a817c" }}>
                Author
              </th>
            </tr>
          </thead>
          <tbody>
            {authors.length > 0 ? (
              authors.map((item) => (
                <tr key={item.id}>
                  <td style={{ padding: "10px", border: "1px solid #8a817c" }}>
                    {item.id}
                  </td>
                  <td style={{ padding: "10px", border: "1px solid #8a817c" }}>
                    {item.author}
                  </td>
                </tr>
              ))
            ) : (
              <p>No data found</p>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default Dashboard;
