'use client';
import { useState } from 'react';
import CopyButton from './CopyButton';
import { useKeys } from './KeyContext';

async function sha1Last6(str: string): Promise<string> {
  const data = new TextEncoder().encode(str.trim());
  const buf = await window.crypto.subtle.digest('SHA-1', data);
  const hex = Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, '0')).join('');
  return hex.slice(-6);
}

export default function Step2Vote() {
  const [pubKeyStr, setPubKeyStr] = useState('');
  const [vote, setVote] = useState<'alice' | 'bob' | null>(null);
  const { keys } = useKeys();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ voteJson: string; hash: string } | null>(null);
  const [error, setError] = useState('');

  const castVote = async () => {
    if (!vote || !pubKeyStr.trim()) return;
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const { PublicKey } = await import('paillier-bigint');
      const parsed = JSON.parse(pubKeyStr.trim());
      const pubKey = new PublicKey(BigInt(parsed.n), BigInt(parsed.g));

      // encrypt returns bigint directly
      const encAlice: bigint = pubKey.encrypt(vote === 'alice' ? 1n : 0n);
      const encBob: bigint = pubKey.encrypt(vote === 'bob' ? 1n : 0n);

      const voteJson = JSON.stringify({
        alice: encAlice.toString(),
        bob: encBob.toString(),
      });

      const hash = await sha1Last6(voteJson);
      setResult({ voteJson, hash });
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="step-card">
      <div className="step-header">
        <span className="step-badge">STEP 2</span>
        <span className="step-title">Cast a Vote</span>
      </div>
      <p className="step-desc">
        Paste the public key, choose a candidate. Your vote is encrypted with Paillier before leaving
        this page — the tally conductor sees only ciphertext.
      </p>

      <div className="label-row">
        <label>Public Key (JSON)</label>
        {keys && <button className="populate-btn" onClick={() => setPubKeyStr(keys.pubJson)}>Populate</button>}
      </div>
      <textarea
        rows={3}
        placeholder={'{"n":"...","g":"..."}'}
        value={pubKeyStr}
        onChange={(e) => setPubKeyStr(e.target.value)}
      />

      <label>Your Vote</label>
      <div className="vote-options">
        <button
          className={`vote-btn${vote === 'alice' ? ' selected' : ''}`}
          onClick={() => setVote('alice')}
        >
          Alice
        </button>
        <button
          className={`vote-btn${vote === 'bob' ? ' selected' : ''}`}
          onClick={() => setVote('bob')}
        >
          Bob
        </button>
      </div>

      <button onClick={castVote} disabled={loading || !vote || !pubKeyStr.trim()}>
        {loading && <span className="spinner" />}
        {loading ? 'Encrypting…' : 'Encrypt & Cast Vote'}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="output-block">
          <h4>Encrypted Vote</h4>
          <div className="output-row">
            <div className="output-label">
              SHA-1 fingerprint (last 6 chars) — remember this to verify your vote was counted
            </div>
            <div style={{ marginTop: '0.4rem' }}>
              <span className="hash-badge">{result.hash}</span>
            </div>
          </div>
          <div className="output-row" style={{ marginTop: '0.75rem' }}>
            <div className="output-label">Encrypted vote JSON (give this to the tally conductor)</div>
            <div className="output-value">{result.voteJson}</div>
            <CopyButton text={result.voteJson} />
          </div>
        </div>
      )}
    </div>
  );
}
