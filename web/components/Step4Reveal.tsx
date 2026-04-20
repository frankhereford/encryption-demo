'use client';
import { useState } from 'react';
import { useKeys } from './KeyContext';

interface Result {
  alice: number;
  bob: number;
}

// Extended Euclidean / modular inverse
function modInverse(a: bigint, m: bigint): bigint {
  let [oldR, r] = [a, m];
  let [oldS, s] = [1n, 0n];
  while (r !== 0n) {
    const q = oldR / r;
    [oldR, r] = [r, oldR - q * r];
    [oldS, s] = [s, oldS - q * s];
  }
  return ((oldS % m) + m) % m;
}

export default function Step4Reveal() {
  const [tallyStr, setTallyStr] = useState('');
  const [pubKeyStr, setPubKeyStr] = useState('');
  const [aliceKeyStr, setAliceKeyStr] = useState('');
  const [bobKeyStr, setBobKeyStr] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState('');
  const { keys, aliceName, bobName } = useKeys();

  const reveal = async () => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const { PublicKey, PrivateKey } = await import('paillier-bigint');

      const tally = JSON.parse(tallyStr.trim());
      const pub = JSON.parse(pubKeyStr.trim());
      const alicePart = JSON.parse(aliceKeyStr.trim());
      const bobPart = JSON.parse(bobKeyStr.trim());

      const n = BigInt(pub.n);
      const g = BigInt(pub.g);
      const p = BigInt(alicePart.p);
      const q = BigInt(bobPart.q);

      // Reconstruct private key using simple-variant formulas (g = n+1, lambda=(p-1)(q-1))
      const lambda = (p - 1n) * (q - 1n);
      const mu = modInverse(lambda, n);

      const pubKey = new PublicKey(n, g);
      const privKey = new PrivateKey(lambda, mu, pubKey, p, q);

      const alice = Number(privKey.decrypt(BigInt(tally.alice)));
      const bob = Number(privKey.decrypt(BigInt(tally.bob)));

      setResult({ alice, bob });
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  const ready = tallyStr.trim() && pubKeyStr.trim() && aliceKeyStr.trim() && bobKeyStr.trim();
  const winner =
    result
      ? result.alice > result.bob
        ? 'alice'
        : result.bob > result.alice
        ? 'bob'
        : 'tie'
      : null;

  return (
    <div className="step-card">
      <div className="step-header">
        <span className="step-badge">STEP 4</span>
        <span className="step-title">Reveal Results</span>
      </div>
      <p className="step-desc">
        Both {aliceName} and {bobName} must provide their key parts to reconstruct the private key and decrypt the
        tally. Either party withholding their key prevents decryption entirely.
      </p>

      <label>Encrypted Tally (JSON)</label>
      <textarea
        rows={3}
        placeholder={'{"alice":"...","bob":"..."}'}
        value={tallyStr}
        onChange={(e) => setTallyStr(e.target.value)}
      />

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

      <div className="label-row">
        <label>{aliceName}&apos;s Key Part (JSON — contains p)</label>
        {keys && <button className="populate-btn" onClick={() => setAliceKeyStr(keys.aliceJson)}>Populate</button>}
      </div>
      <textarea
        rows={2}
        placeholder={'{"p":"..."}'}
        value={aliceKeyStr}
        onChange={(e) => setAliceKeyStr(e.target.value)}
      />

      <div className="label-row">
        <label>{bobName}&apos;s Key Part (JSON — contains q)</label>
        {keys && <button className="populate-btn" onClick={() => setBobKeyStr(keys.bobJson)}>Populate</button>}
      </div>
      <textarea
        rows={2}
        placeholder={'{"q":"..."}'}
        value={bobKeyStr}
        onChange={(e) => setBobKeyStr(e.target.value)}
      />

      <button onClick={reveal} disabled={loading || !ready}>
        {loading && <span className="spinner" />}
        {loading ? 'Decrypting…' : 'Reveal Final Tally'}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="output-block">
          <h4>Final Results</h4>
          <div className="tally-result">
            <div className={`tally-candidate${winner === 'alice' ? ' winner' : ''}`}>
              <div className="name">{aliceName}</div>
              <div className="count">{result.alice}</div>
            </div>
            <div className={`tally-candidate${winner === 'bob' ? ' winner' : ''}`}>
              <div className="name">{bobName}</div>
              <div className="count">{result.bob}</div>
            </div>
          </div>
          {winner === 'tie' && (
            <p
              style={{ textAlign: 'center', marginTop: '0.75rem', color: '#888', fontSize: '0.85rem' }}
            >
              It&apos;s a tie!
            </p>
          )}
        </div>
      )}
    </div>
  );
}
