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

interface VoteEntry {
  json: string;
  hash: string;
}

export default function Step3Tally() {
  const [pubKeyStr, setPubKeyStr] = useState('');
  const [voteInput, setVoteInput] = useState('');
  const { keys } = useKeys();
  const [votes, setVotes] = useState<VoteEntry[]>([]);
  const [addError, setAddError] = useState('');
  const [tally, setTally] = useState<{ json: string } | null>(null);
  const [tallyLoading, setTallyLoading] = useState(false);
  const [tallyError, setTallyError] = useState('');

  const addVote = async () => {
    setAddError('');
    const trimmed = voteInput.trim();
    if (!trimmed) return;
    try {
      JSON.parse(trimmed);
      const hash = await sha1Last6(trimmed);
      setVotes((v) => [...v, { json: trimmed, hash }]);
      setVoteInput('');
    } catch {
      setAddError('Invalid JSON — paste the full encrypted vote object.');
    }
  };

  const removeVote = (i: number) => setVotes((v) => v.filter((_, idx) => idx !== i));

  const computeTally = async () => {
    setTallyLoading(true);
    setTallyError('');
    setTally(null);
    try {
      const { PublicKey } = await import('paillier-bigint');
      const parsed = JSON.parse(pubKeyStr.trim());
      const pubKey = new PublicKey(BigInt(parsed.n), BigInt(parsed.g));

      // Start with encrypted zero for each candidate
      let tallyAlice: bigint = pubKey.encrypt(0n);
      let tallyBob: bigint = pubKey.encrypt(0n);

      for (const v of votes) {
        const data = JSON.parse(v.json);
        const encAlice = BigInt(data.alice);
        const encBob = BigInt(data.bob);
        // Paillier addition = ciphertext multiplication mod n²
        tallyAlice = pubKey.addition(tallyAlice, encAlice);
        tallyBob = pubKey.addition(tallyBob, encBob);
      }

      const tallyJson = JSON.stringify({
        alice: tallyAlice.toString(),
        bob: tallyBob.toString(),
      });
      setTally({ json: tallyJson });
    } catch (e) {
      setTallyError(String(e));
    } finally {
      setTallyLoading(false);
    }
  };

  return (
    <div className="step-card">
      <div className="step-header">
        <span className="step-badge">STEP 3</span>
        <span className="step-title">Tally the Votes</span>
      </div>
      <p className="step-desc">
        The poll conductor adds encrypted votes together using homomorphic addition. The running total
        stays encrypted — the conductor never sees individual votes or the final count.
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

      <label>Add Encrypted Vote</label>
      <textarea
        rows={3}
        placeholder={'{"alice":"...","bob":"..."}'}
        value={voteInput}
        onChange={(e) => setVoteInput(e.target.value)}
      />
      <button onClick={addVote} disabled={!voteInput.trim()}>
        Add Vote
      </button>
      {addError && <p className="error">{addError}</p>}

      {votes.length > 0 && (
        <>
          <label>Votes collected ({votes.length})</label>
          <div className="votes-list">
            {votes.map((v, i) => (
              <div key={i} className="vote-item">
                <span>
                  …{v.json.slice(-40)} <strong>[{v.hash}]</strong>
                </span>
                <button onClick={() => removeVote(i)}>✕</button>
              </div>
            ))}
          </div>
        </>
      )}

      <button
        onClick={computeTally}
        disabled={tallyLoading || votes.length === 0 || !pubKeyStr.trim()}
      >
        {tallyLoading && <span className="spinner" />}
        {tallyLoading ? 'Computing…' : 'Compute Encrypted Tally'}
      </button>

      {tallyError && <p className="error">{tallyError}</p>}

      {tally && (
        <div className="output-block">
          <h4>Encrypted Tally</h4>
          <div className="output-row">
            <div className="output-label">
              Encrypted tally JSON (give to Alice &amp; Bob to decrypt)
            </div>
            <div className="output-value">{tally.json}</div>
            <CopyButton text={tally.json} />
          </div>
        </div>
      )}
    </div>
  );
}
