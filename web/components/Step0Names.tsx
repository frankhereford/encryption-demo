'use client';
import { useKeys } from './KeyContext';

export default function Step0Names() {
  const { aliceName, bobName, setAliceName, setBobName } = useKeys();

  return (
    <div className="step-card">
      <div className="step-header">
        <span className="step-badge">STEP 0</span>
        <span className="step-title">Name the Key Holders</span>
      </div>
      <p className="step-desc">
        Give the two key-custody parties a name. These names are used throughout the demo — they never leave your browser.
      </p>
      <div className="name-inputs">
        <div className="name-field">
          <label>Key holder 1</label>
          <input
            type="text"
            value={aliceName}
            onChange={(e) => setAliceName(e.target.value || 'Alice')}
            placeholder="Alice"
          />
        </div>
        <div className="name-field">
          <label>Key holder 2</label>
          <input
            type="text"
            value={bobName}
            onChange={(e) => setBobName(e.target.value || 'Bob')}
            placeholder="Bob"
          />
        </div>
      </div>
    </div>
  );
}
