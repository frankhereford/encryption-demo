import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Homomorphic Encryption Demo',
  description: 'Dual-custody Paillier homomorphic encryption voting demo',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
