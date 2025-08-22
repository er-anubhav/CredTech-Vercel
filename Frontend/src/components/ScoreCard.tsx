import { TrendingUp, Info } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CreditScore } from '@/hooks/api';

interface ScoreCardProps {
  score: CreditScore | null;
  loading?: boolean;
}

const getScoreColor = (score: number) => {
  if (score >= 750) return 'text-success';
  if (score >= 650) return 'text-warning';
  return 'text-destructive';
};

const getScoreBg = (score: number) => {
  if (score >= 750) return 'bg-success-light';
  if (score >= 650) return 'bg-warning-light';
  return 'bg-destructive-light';
};

export const ScoreCard = ({ score, loading = false }: ScoreCardProps) => {
  if (loading) {
    return (
      <Card className="shadow-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <div className="h-5 w-5 bg-muted rounded animate-pulse" />
            <div className="h-6 w-32 bg-muted rounded animate-pulse" />
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="h-20 w-40 bg-muted rounded animate-pulse" />
            <div className="space-y-2">
              <div className="h-4 bg-muted rounded animate-pulse" />
              <div className="h-4 bg-muted rounded animate-pulse" />
              <div className="h-4 w-3/4 bg-muted rounded animate-pulse" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!score) {
    return (
      <Card className="shadow-card">
        <CardContent className="flex items-center justify-center h-48">
          <div className="text-center text-muted-foreground">
            <Info className="h-8 w-8 mx-auto mb-2" />
            <p>Select a company to view credit score</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-card-foreground">
          <TrendingUp className="h-5 w-5 text-primary" />
          Credit Score
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-baseline gap-3">
            <div className={`text-6xl font-bold ${getScoreColor(score.score)}`}>
              {score.score}
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreBg(score.score)} ${getScoreColor(score.score)}`}>
              {score.score >= 750 ? 'Excellent' : score.score >= 650 ? 'Good' : 'Fair'}
            </div>
          </div>
          
          <div className="bg-gradient-score p-4 rounded-lg border border-border">
            <h4 className="font-medium text-card-foreground mb-2 flex items-center gap-2">
              <Info className="h-4 w-4" />
              
              Explanation
            </h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {score.explanation}
              </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};