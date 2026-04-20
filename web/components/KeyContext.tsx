'use client';
import { createContext, useContext, useState } from 'react';

interface SharedKeys {
  pubJson: string;
  aliceJson: string;
  bobJson: string;
}

const KeyContext = createContext<{
  keys: SharedKeys | null;
  setKeys: (k: SharedKeys) => void;
  aliceName: string;
  bobName: string;
  setAliceName: (n: string) => void;
  setBobName: (n: string) => void;
}>({
  keys: null,
  setKeys: () => {},
  aliceName: 'Alice',
  bobName: 'Bob',
  setAliceName: () => {},
  setBobName: () => {},
});

export function KeyProvider({ children }: { children: React.ReactNode }) {
  const [keys, setKeys] = useState<SharedKeys | null>(null);
  const [aliceName, setAliceName] = useState('Alice');
  const [bobName, setBobName] = useState('Bob');
  return (
    <KeyContext.Provider value={{ keys, setKeys, aliceName, bobName, setAliceName, setBobName }}>
      {children}
    </KeyContext.Provider>
  );
}

export function useKeys() {
  return useContext(KeyContext);
}
