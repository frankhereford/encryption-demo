import { KeyProvider } from '@/components/KeyContext';
import Step1KeyGen from '@/components/Step1KeyGen';
import Step2Vote from '@/components/Step2Vote';
import Step3Tally from '@/components/Step3Tally';
import Step4Reveal from '@/components/Step4Reveal';

export default function Home() {
  return (
    <main className="container">
      <h1>Homomorphic Encryption Demo</h1>
      <p className="subtitle">
        Dual-custody Paillier encryption · all crypto runs client-side in your browser
      </p>
      <KeyProvider>
        <Step1KeyGen />
        <Step2Vote />
        <Step3Tally />
        <Step4Reveal />
      </KeyProvider>
    </main>
  );
}
