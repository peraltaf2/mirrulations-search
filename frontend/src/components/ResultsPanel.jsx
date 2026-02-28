import {ColorRing} from 'react-loader-spinner'
const CFR_BASE_URL = "https://www.ecfr.gov/search#query";

export default function ResultsPanel({ results }) {
  if (!results || results.length === 0) {
    return (
      <div className="results">
        <ColorRing
visible={true}
height="80"
width="80"
ariaLabel="color-ring-loading"
wrapperStyle={{}}
wrapperClass="color-ring-wrapper"
colors={['#e15b64', '#f47e60', '#f8b26a', '#abbd81', '#849b87']}
/>
      </div>
    );
  }

  return (
    <div className="results">
      {results.map((item, index) => (
        <div key={item.docket_id || index} className="result-card">
          <h3 className="result-title">{item.title}
          </h3>

          <div className="result-meta">
            <p><strong>Agency:</strong> {item.agency_id}</p>
            <p><strong>Document Type:</strong> {item.document_type}</p>
            <a href={CFR_BASE_URL}><p><strong>CFR:</strong> {item.cfrPart}</p></a>
            <p><strong>Publication Date:</strong> {item.publication_date}</p>
          </div>

          {item.summary && (
            <p className="result-summary">
              {item.summary}
            </p>
          )}

        </div>
      ))}
    </div>
  );
}