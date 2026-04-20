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
}>({ keys: null, setKeys: () => {} });

export function KeyProvider({ children }: { children: React.ReactNode }) {
  const [keys, setKeys] = useState<SharedKeys | null>(null);
  return <KeyContext.Provider value={{ keys, setKeys }}>{children}</KeyContext.Provider>;
}

export function useKeys() {
  return useContext(KeyContext);
}
