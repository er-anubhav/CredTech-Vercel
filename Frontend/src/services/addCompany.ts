import { Company } from '@/hooks/api';
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function addCompany(ticker: string): Promise<Company> {
  const response = await fetch(`${BASE_URL}/add_company/${ticker}`, {
    method: 'POST',
  });
  if (!response.ok) throw new Error('Failed to add company');
  return response.json();
}
