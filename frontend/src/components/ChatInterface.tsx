"use client";

import { useState, useEffect, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ChatMessage } from "./ChatMessage";
import { chatApi, ChatHistoryMessage, ChatMessageResponse } from "@/lib/api";
import { Send, Loader2, Sparkles, Trash2, Bot } from "lucide-react";

interface ChatInterfaceProps {
  jobId?: number;
  sessionId?: string;
}

export function ChatInterface({ jobId, sessionId: initialSessionId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatHistoryMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | undefined>(initialSessionId);
  const [thinking, setThinking] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (initialSessionId) {
      loadHistory(initialSessionId);
    }
  }, [initialSessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const loadHistory = async (sid: string) => {
    try {
      const history = await chatApi.getHistory(sid);
      setMessages(history.messages);
      setSessionId(sid);
    } catch (error) {
      console.error("Error loading chat history:", error);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ChatHistoryMessage = {
      id: Date.now(),
      role: "user",
      content: input,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setThinking(true);

    try {
      const response: ChatMessageResponse = await chatApi.sendMessage({
        message: input,
        job_id: jobId,
        session_id: sessionId,
      });

      const agentMessage: ChatHistoryMessage = {
        id: Date.now() + 1,
        role: "agent",
        content: response.response,
        reasoning: response.reasoning,
        tools_used: response.tools_used,
        created_at: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, agentMessage]);
      setSessionId(response.session_id);
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage: ChatHistoryMessage = {
        id: Date.now() + 1,
        role: "agent",
        content: "Sorry, I encountered an error. Please try again.",
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setThinking(false);
    }
  };

  const handleClear = async () => {
    if (sessionId) {
      try {
        await chatApi.clearSession(sessionId);
      } catch (error) {
        console.error("Error clearing session:", error);
      }
    }
    setMessages([]);
    setSessionId(undefined);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Card className="w-full h-[600px] flex flex-col">
      <CardHeader className="flex-shrink-0 border-b">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sparkles className="h-5 w-5 text-primary" />
            <CardTitle>Chat with HR Agent</CardTitle>
          </div>
          {messages.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleClear}
              className="text-gray-500"
            >
              <Trash2 className="h-4 w-4 mr-2" />
              Clear
            </Button>
          )}
        </div>
        {jobId && (
          <p className="text-sm text-gray-500 mt-1">Job ID: {jobId}</p>
        )}
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto p-4 space-y-4" ref={chatContainerRef}>
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-center">
            <div>
              <Sparkles className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Start a conversation with the HR Agent
              </h3>
              <p className="text-sm text-gray-500 max-w-md">
                Ask me to find candidates, evaluate resumes, compare candidates, or answer questions about job postings.
                <br />
                <br />
                <strong>Example:</strong> "Find me the top 5 candidates for job #1"
              </p>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {thinking && (
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
                  <Bot className="h-4 w-4" />
                </div>
                <Card className="bg-gray-50">
                  <CardContent className="p-4">
                    <div className="flex items-center space-x-2">
                      <Loader2 className="h-4 w-4 animate-spin text-primary" />
                      <span className="text-sm text-gray-600">Agent is thinking...</span>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </CardContent>

      <div className="flex-shrink-0 border-t p-4">
        <div className="flex space-x-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask the agent anything..."
            disabled={loading}
            className="flex-1"
          />
          <Button
            onClick={handleSend}
            disabled={loading || !input.trim()}
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>
    </Card>
  );
}


