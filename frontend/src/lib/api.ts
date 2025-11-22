import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface JobCreate {
  title: string;
  description: string;
}

export interface JobResponse {
  id: number;
  title: string;
  description: string;
  created_at: string;
}

export interface EvaluationResponse {
  candidate_id: number;
  candidate_name: string;
  overall_score: number;
  technical_score: number;
  experience_score: number;
  education_score: number;
  strengths: string[];
  concerns: string[];
  recommendation: string;
  ai_analysis?: string;
}

export interface TopCandidatesResponse {
  job_id: number;
  total_candidates: number;
  top_5: EvaluationResponse[];
}

export interface ReasoningStep {
  tool: string;
  input: Record<string, any>;
  output: string;
}

export interface ChatMessageResponse {
  response: string;
  reasoning: ReasoningStep[];
  tools_used: string[];
  success: boolean;
  session_id: string;
  error?: string;
}

export interface ChatMessageRequest {
  message: string;
  job_id?: number;
  session_id?: string;
}

export interface ChatHistoryMessage {
  id: number;
  role: 'user' | 'agent';
  content: string;
  reasoning?: any;
  tools_used?: string[];
  created_at: string;
}

export interface ChatHistoryResponse {
  session_id: string;
  messages: ChatHistoryMessage[];
}

export const jobsApi = {
  createJob: async (job: JobCreate): Promise<JobResponse> => {
    const response = await api.post<JobResponse>('/api/jobs', job);
    return response.data;
  },

  getJob: async (jobId: number): Promise<JobResponse> => {
    const response = await api.get<JobResponse>(`/api/jobs/${jobId}`);
    return response.data;
  },

  uploadResumes: async (jobId: number, files: File[]): Promise<{ uploaded: number; job_id: number }> => {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response = await api.post(`/api/jobs/${jobId}/resumes`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  evaluateCandidates: async (jobId: number): Promise<{ job_id: number; status: string; message: string }> => {
    const response = await api.post(`/api/jobs/${jobId}/evaluate`);
    return response.data;
  },

  getTopCandidates: async (jobId: number): Promise<TopCandidatesResponse> => {
    const response = await api.get<TopCandidatesResponse>(`/api/jobs/${jobId}/top-candidates`);
    return response.data;
  },
};

export const chatApi = {
  sendMessage: async (request: ChatMessageRequest): Promise<ChatMessageResponse> => {
    const response = await api.post<ChatMessageResponse>('/api/chat', request);
    return response.data;
  },

  getHistory: async (sessionId: string): Promise<ChatHistoryResponse> => {
    const response = await api.get<ChatHistoryResponse>(`/api/chat/sessions/${sessionId}`);
    return response.data;
  },

  clearSession: async (sessionId: string): Promise<{ status: string; session_id: string }> => {
    const response = await api.post(`/api/chat/sessions/${sessionId}/clear`);
    return response.data;
  },
};

