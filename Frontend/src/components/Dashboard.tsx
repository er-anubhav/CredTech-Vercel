import { useState } from 'react';
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useRef } from 'react';
import * as addCompanyService from '@/services/addCompany';
import { CompanySelector } from './CompanySelector';
import { ScoreCard } from './ScoreCard';
import { ScoreTrend } from './ScoreTrend';
import { NewsList } from './NewsList';
import { FeatureContributions } from './FeatureContributions';
import { useCompaniesWithRefetch, useCreditScore, useScoreHistory, useNews, Company } from '@/hooks/api';

export const Dashboard = () => {
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [open, setOpen] = useState(false);
  const [ticker, setTicker] = useState('');
  const [search, setSearch] = useState('');
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Refetch companies after add
  const { companies, loading: companiesLoading, error: companiesError, refetch } = useCompaniesWithRefetch();
  const { score, loading: scoreLoading } = useCreditScore(selectedCompany?.ticker || null);
  const { history, loading: historyLoading } = useScoreHistory(selectedCompany?.ticker || null);
  const { news, loading: newsLoading } = useNews(selectedCompany?.ticker || null);

  const handleSelectCompany = (company: Company) => {
    setSelectedCompany(company);
  };

  const handleAddCompany = async () => {
    if (!ticker) return;
    setAdding(true);
    setError(null);
    try {
      await addCompanyService.addCompany(ticker);
      await refetch();
      setOpen(false);
      setTicker('');
      setSearch('');
      // Optionally auto-select the new company
      const newCompany = companies.find(c => c.ticker.toLowerCase() === ticker.toLowerCase());
      if (newCompany) setSelectedCompany(newCompany);
    } catch (err: any) {
      setError(err.message || 'Failed to add company');
    } finally {
      setAdding(false);
    }
  };

  return (
    <div className="min-h-screen  font-serif  bg-background">
      <div className="flex h-screen">
        {/* Company Selector Sidebar */}
        <CompanySelector
          companies={companies}
          selectedCompany={selectedCompany}
          onSelectCompany={handleSelectCompany}
          loading={companiesLoading}
        />
        
        {/* Main Content */}
        <div className="flex-1">
          {/* Header */}
          <header className="bg-card border-b border-border p-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl text-card-foreground">
                  Credit Score Dashboard
                </h1>
                {selectedCompany && (
                  <p className="text-muted-foreground">
                    Analyzing {selectedCompany.name} ({selectedCompany.ticker})
                  </p>
                )}
              </div>
              <div className="text-sm text-muted-foreground">
                <Dialog open={open} onOpenChange={setOpen}>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="mb-4">Add Company</Button>
                  </DialogTrigger>
                  <DialogContent className="bg-white">
                    <DialogHeader>
                      <DialogTitle>Add Company</DialogTitle>
                      <DialogDescription>
                        Enter a ticker symbol to add a new company.
                      </DialogDescription>
                    </DialogHeader>
                    <div className="mt-4">
                      <Input
                        ref={inputRef}
                        placeholder="Type or pick a ticker (e.g. GOOGL)"
                        value={search}
                        onChange={e => {
                          setSearch(e.target.value);
                          setTicker(e.target.value);
                        }}
                        list="company-tickers"
                        className="mb-2"
                        autoFocus
                        onKeyDown={e => { if (e.key === 'Enter') handleAddCompany(); }}
                      />
                      <datalist id="company-tickers">
                        {companies.map(c => (
                          <option key={c.ticker} value={c.ticker}>{c.name}</option>
                        ))}
                      </datalist>
                      {error && <div className="text-red-500 text-sm mb-2">{error}</div>}
                      <Button onClick={handleAddCompany} disabled={adding || !ticker} className="w-full mt-2">
                        {adding ? 'Adding...' : 'Add'}
                      </Button>
                    </div>
                  </DialogContent>
                </Dialog>
              </div>
            </div>
          </header>

          {/* Dashboard Content */}
          <div className="flex-1 px-2 h-full w-full">
            {!selectedCompany ? (
              <div className="flex items-center justify-center h-[80%]">
                <div className="text-center max-w-md">
                  <div className="w-16 h-16 bg-primary-light rounded-full flex items-center justify-center mx-auto mb-4">
                    <div className="w-8 h-8 bg-primary rounded-full"></div>
                  </div>
                  <h2 className="text-xl text-card-foreground mb-2">
                    Welcome to Credit Score Dashboard
                  </h2>
                  <p className="text-muted-foreground">
                    Select a company from the sidebar to view detailed credit analysis, 
                    score trends, and the latest market news.
                  </p>
                </div>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-full mx-6">
                {/* Score Card - Full width on mobile, left column on desktop */}
                <div className="lg:col-span-1">
                  <ScoreCard score={score} loading={scoreLoading} />
                </div>

                {/* Feature Contributions - Right column on desktop */}
                <div className="lg:col-span-1">
                  <FeatureContributions 
                    contributions={score?.feature_contributions || null} 
                    loading={scoreLoading} 
                  />
                </div>

                {/* Score Trend - Full width */}
                <div className="lg:col-span-2">
                  <ScoreTrend history={history} loading={historyLoading} />
                </div>

                {/* News List - Full width */}
                <div className="lg:col-span-2">
                  <NewsList news={news} loading={newsLoading} />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};