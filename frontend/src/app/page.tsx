import { JobForm } from "@/components/JobForm";
import { Briefcase } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center space-x-3 mb-4">
            <Briefcase className="h-10 w-10 text-primary" />
            <h1 className="text-4xl font-bold text-gray-900">HR Agent</h1>
          </div>
          <p className="text-xl text-gray-600">
            AI-Powered Intelligent Resume Screening
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Upload 100 resumes and get the top 5 candidates using RAG technology
          </p>
        </div>
        <JobForm />
      </div>
    </div>
  );
}

