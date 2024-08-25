import { useState } from 'react';
import axios from 'axios';

function App() {
  const [name, setName] = useState('');
  const [pdfChoice, setPdfChoice] = useState('1');
  const [downloadLink, setDownloadLink] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const pdfUrls = {
        '1': 'http://127.0.0.1:5000/assets/shiki.pdf',
        '2': 'http://127.0.0.1:5000/assets/meguro.pdf'
      };
      const fontUrl = 'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400&display=swap'; // Google FontsからNoto Sans JPを取得
      const searchText = '氏名'; // 検索するテキストを指定

      const response = await axios.post('http://127.0.0.1:5000/update-pdf', {
        pdf_url: pdfUrls[pdfChoice],
        text: name,
        font_url: fontUrl,
        search_text: searchText
      });
      alert(response.data.message);
      setDownloadLink('http://127.0.0.1:5000/download-pdf');
    } catch (error) {
      if (error.response) {
        alert('Error: ' + error.response.data.error);
      } else {
        alert('Error: ' + error.message);
      }
    }
  };

  return (
    <div>
      <h1>Update PDF</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Select PDF file:
            <select value={pdfChoice} onChange={(e) => setPdfChoice(e.target.value)}>
              <option value="1">shiki.pdf</option>
              <option value="2">meguro.pdf</option>
            </select>
          </label>
        </div>
        <div>
          <label>
            Enter your name:
            <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
          </label>
        </div>
        <button type="submit">Update PDF</button>
      </form>
      {downloadLink && (
        <div>
          <a href={downloadLink} download="output.pdf">Download Updated PDF</a>
        </div>
      )}
    </div>
  );
}

export default App;