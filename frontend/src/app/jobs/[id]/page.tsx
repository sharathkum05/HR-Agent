"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { JobForm } from "@/components/JobForm";
import { ResumeUpload } from "@/components/ResumeUpload";
import { TopCandidates } from "@/components/TopCandidates";
import { ChatInterface } from "@/components/ChatInterface";
import { jobsApi, JobResponse } from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Loader2 } from "lucide-react";

export default function JobPage() {
  const params = useParams();
  const router = useRouter();
  const jobId = parseInt(params.id as string);
  const [job, setJob] = useState<JobResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"upload" | "results" | "chat">("upload");

  useEffect(() => {
    if (jobId) {
      fetchJob();
    }
  }, [jobId]);

  const fetchJob = async () => {
    try {
      const jobData = await jobsApi.getJob(jobId);
      setJob(jobData);
    } catch (error) {
      console.error("Error fetching job:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadComplete = (count: number) => {
    // Switch to results tab after upload
    setTimeout(() => {
      setActiveTab("results");
    }, 1000);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card>
          <CardContent className="p-8 text-center">
            <p className="text-gray-600 mb-4">Job not found</p>
            <Button onClick={() => router.push("/")}>Go Home</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <Button
          variant="ghost"
          onClick={() => router.push("/")}
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Home
        </Button>

        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{job.title}</h1>
          <p className="text-gray-600">{job.description}</p>
        </div>

        <div className="flex space-x-4 mb-6 border-b">
          <button
            onClick={() => setActiveTab("upload")}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === "upload"
                ? "border-b-2 border-primary text-primary"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            Upload Resumes
          </button>
          <button
            onClick={() => setActiveTab("results")}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === "results"
                ? "border-b-2 border-primary text-primary"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            Top Candidates
          </button>
          <button
            onClick={() => setActiveTab("chat")}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === "chat"
                ? "border-b-2 border-primary text-primary"
                : "text-gray-600 hover:text-gray-900"
            }`}
          >
            Chat with Agent
          </button>
        </div>

        {activeTab === "upload" && (
          <ResumeUpload jobId={jobId} onUploadComplete={handleUploadComplete} />
        )}

        {activeTab === "results" && <TopCandidates jobId={jobId} />}

        {activeTab === "chat" && <ChatInterface jobId={jobId} />}
      </div>
    </div>
  );
}

