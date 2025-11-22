"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { EvaluationResponse } from "@/lib/api";
import { TrendingUp, TrendingDown, Award, AlertCircle } from "lucide-react";

interface CandidateCardProps {
  candidate: EvaluationResponse;
  rank: number;
}

export function CandidateCard({ candidate, rank }: CandidateCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600";
    if (score >= 65) return "text-blue-600";
    if (score >= 50) return "text-yellow-600";
    return "text-red-600";
  };

  const getRecommendationColor = (rec: string) => {
    if (rec.includes("Strong")) return "bg-green-100 text-green-800";
    if (rec.includes("Good")) return "bg-blue-100 text-blue-800";
    if (rec.includes("Moderate")) return "bg-yellow-100 text-yellow-800";
    return "bg-red-100 text-red-800";
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary text-primary-foreground font-bold">
              #{rank}
            </div>
            <div>
              <CardTitle className="text-xl">{candidate.candidate_name}</CardTitle>
              <CardDescription>
                Candidate ID: {candidate.candidate_id}
              </CardDescription>
            </div>
          </div>
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${getRecommendationColor(candidate.recommendation)}`}>
            {candidate.recommendation}
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center space-x-2">
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm font-medium">Overall Score</span>
              <span className={`text-lg font-bold ${getScoreColor(candidate.overall_score)}`}>
                {candidate.overall_score.toFixed(1)}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${getScoreColor(candidate.overall_score).replace("text-", "bg-").replace("-600", "-500")}`}
                style={{ width: `${candidate.overall_score}%` }}
              />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-3 bg-gray-50 rounded">
            <div className="text-xs text-gray-600 mb-1">Technical</div>
            <div className={`text-lg font-semibold ${getScoreColor(candidate.technical_score)}`}>
              {candidate.technical_score.toFixed(0)}
            </div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded">
            <div className="text-xs text-gray-600 mb-1">Experience</div>
            <div className={`text-lg font-semibold ${getScoreColor(candidate.experience_score)}`}>
              {candidate.experience_score.toFixed(0)}
            </div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded">
            <div className="text-xs text-gray-600 mb-1">Education</div>
            <div className={`text-lg font-semibold ${getScoreColor(candidate.education_score)}`}>
              {candidate.education_score.toFixed(0)}
            </div>
          </div>
        </div>

        {candidate.strengths.length > 0 && (
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Award className="h-4 w-4 text-green-600" />
              <span className="text-sm font-semibold">Strengths</span>
            </div>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
              {candidate.strengths.map((strength, idx) => (
                <li key={idx}>{strength}</li>
              ))}
            </ul>
          </div>
        )}

        {candidate.concerns.length > 0 && (
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <AlertCircle className="h-4 w-4 text-yellow-600" />
              <span className="text-sm font-semibold">Concerns</span>
            </div>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
              {candidate.concerns.map((concern, idx) => (
                <li key={idx}>{concern}</li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

