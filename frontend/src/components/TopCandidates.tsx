"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CandidateCard } from "./CandidateCard";
import { jobsApi, TopCandidatesResponse } from "@/lib/api";
import { Sparkles, Loader2 } from "lucide-react";

interface TopCandidatesProps {
  jobId: number;
}

export function TopCandidates({ jobId }: TopCandidatesProps) {
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [data, setData] = useState<TopCandidatesResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchTopCandidates = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await jobsApi.getTopCandidates(jobId);
      setData(result);
    } catch (err) {
      setError("Failed to fetch top candidates. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluate = async () => {
    setEvaluating(true);
    setError(null);
    try {
      await jobsApi.evaluateCandidates(jobId);
      // Wait a bit then fetch results
      setTimeout(() => {
        fetchTopCandidates();
      }, 2000);
    } catch (err) {
      setError("Failed to start evaluation. Please try again.");
      console.error(err);
    } finally {
      setEvaluating(false);
    }
  };

  useEffect(() => {
    fetchTopCandidates();
  }, [jobId]);

  if (loading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center space-x-2">
              <Sparkles className="h-5 w-5" />
              <span>Top 5 Candidates</span>
            </CardTitle>
            <CardDescription>
              {data
                ? `Showing top 5 out of ${data.total_candidates} candidates`
                : "AI-powered candidate evaluation results"}
            </CardDescription>
          </div>
          <Button
            onClick={handleEvaluate}
            disabled={evaluating}
            variant="outline"
          >
            {evaluating ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Evaluating...
              </>
            ) : (
              "Run Evaluation"
            )}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded text-red-800 text-sm">
            {error}
          </div>
        )}

        {data && data.top_5.length > 0 ? (
          <div className="space-y-4">
            {data.top_5.map((candidate, index) => (
              <CandidateCard
                key={candidate.candidate_id}
                candidate={candidate}
                rank={index + 1}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            <p>No candidates evaluated yet.</p>
            <p className="text-sm mt-2">
              Upload resumes and click "Run Evaluation" to get started.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

