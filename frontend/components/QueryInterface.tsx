"use client";

import { useState, useEffect, useRef } from 'react';
import { Query, getQueries, submitQuery, Citation } from '@/lib/api';
import { Send, Loader2, BookOpen, FileText, AlertCircle } from 'lucide-react';

interface QueryInterfaceProps {
  projectId: string;
}

export default function QueryInterface({ projectId }: QueryInterfaceProps) {
  const [queries, setQueries] = useState<Query[]>([]);
  const [queryText, setQueryText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<'gpt-4' | 'claude-3-5-sonnet'>('gpt-4');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load query history on mount
  useEffect(() => {
    loadQueries();
  }, [projectId]);

  // Auto-scroll to bottom when new queries are added
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [queries]);

  const loadQueries = async () => {
    try {
      setError(null);
      const data = await getQueries(projectId);
      setQueries(data);
    } catch (err: any) {
      if (err.response?.status !== 404) {
        setError(err.response?.data?.detail || 'Failed to load query history');
      }
      console.error('Error loading queries:', err);
    }
  };

  const handleSubmitQuery = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!queryText.trim()) {
      setError('Please enter a question');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await submitQuery({
        project_id: projectId,
        query_text: queryText,
        model: selectedModel,
        top_k: 5,
        similarity_threshold: 0.7,
      });

      setQueries([...queries, response]);
      setQueryText('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process query');
      console.error('Error submitting query:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Model Selector */}
      <div className="mb-4 flex items-center gap-4">
        <label className="text-sm font-medium text-gray-700">AI Model:</label>
        <div className="flex gap-2">
          <button
            onClick={() => setSelectedModel('gpt-4')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              selectedModel === 'gpt-4'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            GPT-4
          </button>
          <button
            onClick={() => setSelectedModel('claude-3-5-sonnet')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              selectedModel === 'claude-3-5-sonnet'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Claude 3.5 Sonnet
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-start gap-2">
          <AlertCircle size={20} className="flex-shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {/* Query History */}
      <div className="flex-1 overflow-y-auto space-y-6 mb-4 bg-gray-50 rounded-lg p-4">
        {queries.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center py-12">
            <BookOpen size={48} className="text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-700 mb-2">
              Ask your first question
            </h3>
            <p className="text-gray-500">
              Query your documents using natural language powered by AI
            </p>
          </div>
        ) : (
          queries.map((query) => (
            <div key={query.id} className="space-y-3">
              {/* User Query */}
              <div className="flex justify-end">
                <div className="bg-blue-600 text-white rounded-lg px-4 py-3 max-w-[80%]">
                  <p className="text-sm">{query.query_text}</p>
                </div>
              </div>

              {/* AI Response */}
              <div className="flex justify-start">
                <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 max-w-[80%] shadow-sm">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs font-medium text-gray-500 uppercase">
                      {query.model_used}
                    </span>
                  </div>
                  <p className="text-gray-800 whitespace-pre-wrap">{query.response_text}</p>

                  {/* Citations */}
                  {query.citations && query.citations.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                        <FileText size={16} />
                        Sources ({query.citations.length})
                      </h4>
                      <div className="space-y-2">
                        {query.citations.map((citation: Citation, idx: number) => (
                          <div
                            key={`${citation.chunk_id}-${idx}`}
                            className="bg-gray-50 rounded p-3 text-sm"
                          >
                            <div className="flex items-start justify-between gap-2 mb-1">
                              <span className="font-medium text-gray-700">
                                {citation.document_name}
                                {citation.page_number && ` (Page ${citation.page_number})`}
                              </span>
                              <span className="text-xs text-gray-500 whitespace-nowrap">
                                {(citation.similarity_score * 100).toFixed(1)}% match
                              </span>
                            </div>
                            <p className="text-gray-600 text-xs line-clamp-3">
                              {citation.text}
                            </p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="mt-2 text-xs text-gray-400">
                    {new Date(query.created_at).toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Query Input */}
      <form onSubmit={handleSubmitQuery} className="flex gap-2">
        <input
          type="text"
          value={queryText}
          onChange={(e) => setQueryText(e.target.value)}
          placeholder="Ask a question about your documents..."
          disabled={loading}
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
        <button
          type="submit"
          disabled={loading || !queryText.trim()}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 size={20} className="animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <Send size={20} />
              Send
            </>
          )}
        </button>
      </form>
    </div>
  );
}
