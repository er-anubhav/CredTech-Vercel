import { useState } from 'react';
import { Search, Building2, ChevronRight } from 'lucide-react';
import { Company } from '@/hooks/api';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

interface CompanySelectorProps {
  companies: Company[];
  selectedCompany: Company | null;
  onSelectCompany: (company: Company) => void;
  loading?: boolean;
}

export const CompanySelector = ({ 
  companies, 
  selectedCompany, 
  onSelectCompany, 
  loading = false 
}: CompanySelectorProps) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredCompanies = companies.filter(
    (company) =>
      company.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      company.ticker.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="w-80 bg-card border-r border-border h-full flex flex-col">
      <div className="p-4 border-b border-border">
        <h2 className="text-lg  text-card-foreground mb-3 flex items-center gap-2">
          <Building2 className="h-5 w-5 text-primary" />
          Companies
        </h2>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search companies..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="p-4 space-y-2">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-muted rounded-lg animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="p-2">
            {filteredCompanies.map((company) => (
              <button
                key={company.id}
                onClick={() => onSelectCompany(company)}
                className={`w-full p-3 rounded-lg text-left transition-all duration-200 group hover:bg-accent ${
                  selectedCompany?.id === company.id
                    ? 'bg-primary text-primary-foreground shadow-md'
                    : 'hover:bg-accent'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-sm truncate">
                      {company.name}
                    </div>
                    <div className={`text-xs ${
                      selectedCompany?.id === company.id
                        ? 'text-primary-foreground/70'
                        : 'text-muted-foreground'
                    }`}>
                      {company.ticker}
                    </div>
                  </div>
                  <ChevronRight 
                    className={`h-4 w-4 transition-transform group-hover:translate-x-1 ${
                      selectedCompany?.id === company.id
                        ? 'text-primary-foreground/70'
                        : 'text-muted-foreground'
                    }`} 
                  />
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};