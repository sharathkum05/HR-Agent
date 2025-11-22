"use client";

import { Card, CardContent } from "@/components/ui/card";
import { ChatHistoryMessage, ReasoningStep } from "@/lib/api";
import { User, Bot, ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

interface ChatMessageProps {
  message: ChatHistoryMessage;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const [showReasoning, setShowReasoning] = useState(false);
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div className={`flex items-start space-x-3 max-w-3xl ${isUser ? "flex-row-reverse space-x-reverse" : ""}`}>
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? "bg-primary text-primary-foreground" : "bg-secondary text-secondary-foreground"
        }`}>
          {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
        </div>
        
        <Card className={`flex-1 ${isUser ? "bg-primary/10" : ""}`}>
          <CardContent className="p-4">
            <div className="whitespace-pre-wrap text-sm">{message.content}</div>
            
            {!isUser && (message.tools_used && message.tools_used.length > 0 || message.reasoning) && (
              <div className="mt-3 pt-3 border-t">
                <button
                  onClick={() => setShowReasoning(!showReasoning)}
                  className="flex items-center space-x-2 text-xs text-gray-500 hover:text-gray-700"
                >
                  {showReasoning ? (
                    <>
                      <ChevronUp className="h-3 w-3" />
                      <span>Hide reasoning</span>
                    </>
                  ) : (
                    <>
                      <ChevronDown className="h-3 w-3" />
                      <span>Show reasoning</span>
                    </>
                  )}
                </button>
                
                {showReasoning && (
                  <div className="mt-2 space-y-2">
                    {message.tools_used && message.tools_used.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-gray-600 mb-1">Tools Used:</div>
                        <div className="flex flex-wrap gap-1">
                          {message.tools_used.map((tool, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                            >
                              {tool}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {message.reasoning && Array.isArray(message.reasoning) && message.reasoning.length > 0 && (
                      <div>
                        <div className="text-xs font-semibold text-gray-600 mb-1">Reasoning Steps:</div>
                        <div className="space-y-2">
                          {message.reasoning.map((step: ReasoningStep, idx: number) => (
                            <div key={idx} className="text-xs bg-gray-50 p-2 rounded">
                              <div className="font-medium text-gray-700">{step.tool}</div>
                              {step.input && (
                                <div className="text-gray-600 mt-1">
                                  Input: {JSON.stringify(step.input, null, 2)}
                                </div>
                              )}
                              <div className="text-gray-500 mt-1 truncate">
                                Output: {typeof step.output === 'string' ? step.output.substring(0, 200) : JSON.stringify(step.output).substring(0, 200)}...
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
            
            <div className="text-xs text-gray-400 mt-2">
              {new Date(message.created_at).toLocaleTimeString()}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

