
import { useState, useEffect } from 'react';
import * as apiService from '@/services/apiService';

export interface Company {
  id: number;
  name: string;
  ticker: string;
}

export interface CreditScore {
  score: number;
  explanation: string;
  feature_contributions: Record<string, number>;
  html_summary?: string;
}

export interface ScoreHistory {
  date: string;
  score: number;
  explanation: string;
}

export interface NewsItem {
  date: string;
  title: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  url: string;
}

// Hook for fetching companies (with refetch capability)
export const useCompaniesWithRefetch = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const data = await apiService.fetchCompanies();
      setCompanies(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch companies');
    } finally {
      setLoading(false);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchData();
    // eslint-disable-next-line
  }, []);

  return { companies, loading, error, refetch: fetchData };
};

// Hook for fetching credit score
export const useCreditScore = (ticker: string | null) => {
  const [score, setScore] = useState<CreditScore | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!ticker) return;
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await apiService.fetchCreditScore(ticker);
        setScore(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch credit score');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [ticker]);

  return { score, loading, error };
};

// Hook for fetching score history
export const useScoreHistory = (ticker: string | null) => {
  const [history, setHistory] = useState<ScoreHistory[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!ticker) return;
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await apiService.fetchScoreHistory(ticker);
        setHistory(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch score history');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [ticker]);

  return { history, loading, error };
};

// Hook for fetching news
export const useNews = (ticker: string | null) => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!ticker) return;
    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await apiService.fetchNews(ticker);
        setNews(data);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch news');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [ticker]);

  return { news, loading, error };
};
