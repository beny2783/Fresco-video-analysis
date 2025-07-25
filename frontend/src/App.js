import React, { useState } from 'react';
import { apiUrl } from './config';

function tryParseJSON(jsonString) {
  if (!jsonString) return null;
  // Remove Markdown code block if present
  const codeBlockRegex = /^```(?:json)?\s*([\s\S]*?)\s*```$/i;
  const match = jsonString.match(codeBlockRegex);
  const cleanString = match ? match[1] : jsonString;
  try {
    const o = JSON.parse(cleanString);
    if (o && typeof o === 'object') return o;
  } catch (e) {}
  return null;
}

function RecipeDisplay({ data }) {
  if (!data) return null;
  return (
    <div style={{ background: '#fff', padding: 24, borderRadius: 8, boxShadow: '0 2px 8px #eee', marginTop: 24 }}>
      <h3>{data.recipe_name || 'Recipe'}</h3>
      {data.serving_size && <p><strong>Serving Size:</strong> {data.serving_size}</p>}
      {data.ingredients && Array.isArray(data.ingredients) && (
        <div>
          <strong>Ingredients:</strong>
          <ul>
            {data.ingredients.map((ing, i) => {
              if (typeof ing === 'string') return <li key={i}>{ing}</li>;
              // Use 'item' or 'name' for ingredient name
              const name = ing.item || ing.name || '';
              const quantity = ing.quantity ? ` - ${ing.quantity}` : '';
              const notes = ing.notes ? `, ${ing.notes}` : '';
              return <li key={i}>{name}{quantity}{notes}</li>;
            })}
          </ul>
        </div>
      )}
      {data.method && (
        <div>
          <strong>Method:</strong>
          <ol>
            {Array.isArray(data.method)
              ? data.method.map((step, i) => <li key={i}>{step}</li>)
              : <li>{data.method}</li>}
          </ol>
        </div>
      )}
      {data.additional_notes && <p><strong>Notes:</strong> {data.additional_notes}</p>}
    </div>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResponse(null);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    setResponse(null);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch(`${apiUrl}/analyze`, {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.toString());
    } finally {
      setLoading(false);
    }
  };

  let recipeData = null;
  if (response && response.status === 'success') {
    recipeData = tryParseJSON(response.gemini_response);
  }

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2>Recipe Video Analyzer (Gemini API Test)</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="video/*" onChange={handleFileChange} />
        <button type="submit" disabled={!file || loading} style={{ marginLeft: 8 }}>
          {loading ? 'Analyzing...' : 'Upload & Analyze'}
        </button>
      </form>
      {error && (
        <div style={{ color: 'red', marginTop: 16 }}>Error: {error}</div>
      )}
      {response && response.status === 'success' && recipeData ? (
        <>
          <RecipeDisplay data={recipeData} />
          <pre style={{ background: '#f4f4f4', padding: 16, marginTop: 16, borderRadius: 4 }}>
            {JSON.stringify(recipeData, null, 2)}
          </pre>
        </>
      ) : response && (
        <pre style={{ background: '#f4f4f4', padding: 16, marginTop: 16, borderRadius: 4 }}>
          {JSON.stringify(response, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default App;
