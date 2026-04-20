'use client';
import { useState } from 'react';
import CopyButton from './CopyButton';
import { useKeys } from './KeyContext';

async function sha1Last6(str: string): Promise<string> {
  const data = new TextEncoder().encode(str);
  const buf = await window.crypto.subtle.digest('SHA-1', data);
  const hex = Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, '0')).join('');
  return hex.slice(-6);
}

function fingerprint(s: string): string {
  return s.slice(0, 10) + '...' + s.slice(-10);
}

interface Keys {
  pubJson: string;
  aliceJson: string;
  bobJson: string;
  pubFp: string;
  aliceFp: string;
  bobFp: string;
  nFp: string;
  gFp: string;
  pFp: string;
  qFp: string;
}

export default function Step1KeyGen() {
  const [loading, setLoading] = useState(false);
  const [keys, setKeys] = useState<Keys | null>(null);
  const [error, setError] = useState('');
  const { setKeys: setSharedKeys, aliceName, bobName } = useKeys();

  const generate = async () => {
    setLoading(true);
    setError('');
    try {
      const { generateRandomKeys } = await import('paillier-bigint');
      // simpleVariant=true: g=n+1, lambda=(p-1)(q-1), mu=lambda^-1 mod n
      // This lets us reconstruct the private key from p, q, n alone at reveal time
      const { publicKey, privateKey } = await generateRandomKeys(2048, true);

      // _p and _q are private in TypeScript but accessible at runtime
      const pk = privateKey as unknown as { _p: bigint; _q: bigint };
      const pubJson = JSON.stringify({ n: publicKey.n.toString(), g: publicKey.g.toString() });
      const aliceJson = JSON.stringify({ p: pk._p.toString() });
      const bobJson = JSON.stringify({ q: pk._q.toString() });

      const [pubFp, aliceFp, bobFp] = await Promise.all([
        sha1Last6(pubJson),
        sha1Last6(aliceJson),
        sha1Last6(bobJson),
      ]);

      setSharedKeys({ pubJson, aliceJson, bobJson });
      setKeys({
        pubJson,
        aliceJson,
        bobJson,
        pubFp,
        aliceFp,
        bobFp,
        nFp: fingerprint(publicKey.n.toString()),
        gFp: fingerprint(publicKey.g.toString()),
        pFp: fingerprint(pk._p.toString()),
        qFp: fingerprint(pk._q.toString()),
      });
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="step-card">
      <div className="step-header">
        <span className="step-badge">STEP 1</span>
        <span className="step-title">Key Generation</span>
      </div>
      <p className="step-desc">
        Generate a 2048-bit Paillier public/private keypair. The private key is split — {aliceName} holds{' '}
        <em>p</em>, {bobName} holds <em>q</em>. Neither can decrypt alone.
      </p>

      <button onClick={generate} disabled={loading}>
        {loading && <span className="spinner" />}
        {loading ? 'Generating 2048-bit keys…' : keys ? 'Regenerate Keys' : 'Generate Keys'}
      </button>

      {error && <p className="error">{error}</p>}

      {keys && (
        <div className="output-block">
          <h4>Generated Keys</h4>

          <div className="output-row">
            <div className="output-label">
              Public Key — share with all voters — fingerprint: <code>{keys.pubFp}</code>
            </div>
            <div className="output-value">{keys.pubJson}</div>
            <CopyButton text={keys.pubJson} />
          </div>

          <hr className="divider" />

          <div className="output-row">
            <div className="output-label">
              {aliceName}&apos;s Key Part — keep secret — fingerprint: <code>{keys.aliceFp}</code>
            </div>
            <div className="output-value">{keys.aliceJson}</div>
            <CopyButton text={keys.aliceJson} />
          </div>

          <div className="output-row">
            <div className="output-label">
              {bobName}&apos;s Key Part — keep secret — fingerprint: <code>{keys.bobFp}</code>
            </div>
            <div className="output-value">{keys.bobJson}</div>
            <CopyButton text={keys.bobJson} />
          </div>

          <hr className="divider" />

          <div className="output-row">
            <div className="output-label">Key fingerprints (safe to display publicly)</div>
            <div className="output-value">
              {`n: ${keys.nFp}\ng: ${keys.gFp}\np: ${keys.pFp}  ← ${aliceName} only\nq: ${keys.qFp}  ← ${bobName} only`}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
