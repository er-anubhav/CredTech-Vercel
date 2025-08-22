import { BarChart3 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface FeatureContributionsProps {
  contributions: Record<string, number> | null;
  loading?: boolean;
}

export const FeatureContributions = ({ contributions, loading = false }: FeatureContributionsProps) => {
  if (loading) {
    return (
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <div className="h-5 w-5 bg-muted rounded animate-pulse" />
            <div className="h-6 w-40 bg-muted rounded animate-pulse" />
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="">
                <div className="h-4 w-32 bg-muted rounded animate-pulse" />
                <div className="h-3 bg-muted rounded animate-pulse" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!contributions) {
    return (
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-card-foreground">
            <BarChart3 className="h-5 w-5 text-primary" />
            Feature Contributions
          </CardTitle>
        </CardHeader>
        <CardContent className="flex items-center justify-center h-40">
          <p className="text-muted-foreground">No contribution data available</p>
        </CardContent>
      </Card>
    );
  }

  const maxAbsValue = Math.max(...Object.values(contributions).map(v => Math.abs(v)), 1);
  const sortedContributions = Object.entries(contributions).sort(([,a], [,b]) => Math.abs(b) - Math.abs(a));

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-card-foreground">
          <BarChart3 className="h-5 w-5 text-primary" />
          Feature Contributions
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="">
          {sortedContributions.map(([feature, value]) => {
            if (value === 0) return null;
            const percentage = (Math.abs(value) / maxAbsValue) * 100;
            const isPositive = value > 0;
            return (
              <div key={feature} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-card-foreground">
                    {feature}
                  </span>
                  <span className={`text-sm ${isPositive ? 'text-success' : 'text-destructive'}`}>
                    {isPositive ? '+' : ''}{value}
                  </span>
                </div>
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-700 ease-out ${isPositive ? 'bg-success' : 'bg-destructive'}`}
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
        <div className="mt-1 pb-6 bg-accent rounded-lg">
          <p className="text-xs text-muted-foreground">
            Positive values indicate positive contributions to the credit score, negative values indicate negative impacts.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};