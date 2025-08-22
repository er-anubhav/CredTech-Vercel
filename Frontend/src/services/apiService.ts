import { Company, CreditScore, ScoreHistory, NewsItem } from '@/hooks/api';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchCompanies(): Promise<Company[]> {
  const response = await fetch(`${BASE_URL}/companies`);
  if (!response.ok) throw new Error('Failed to fetch companies');
  return response.json();
}

export async function fetchCompany(ticker: string): Promise<Company> {
  const response = await fetch(`${BASE_URL}/company/${ticker}`);
  if (!response.ok) throw new Error('Failed to fetch company');
  return response.json();
}

export async function fetchCreditScore(ticker: string): Promise<CreditScore> {
  const response = await fetch(`${BASE_URL}/score/${ticker}`);
  if (!response.ok) throw new Error('Failed to fetch credit score');
  return response.json();
}

export async function fetchScoreHistory(ticker: string): Promise<ScoreHistory[]> {
  const response = await fetch(`${BASE_URL}/score_history/${ticker}`);
  if (!response.ok) throw new Error('Failed to fetch score history');
  return response.json();
}

export async function fetchNews(ticker: string): Promise<NewsItem[]> {
  const response = await fetch(`${BASE_URL}/news/${ticker}`);
  if (!response.ok) throw new Error('Failed to fetch news');
  return response.json();
}
