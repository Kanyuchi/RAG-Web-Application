"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { Project } from '@/lib/api';
import ProjectList from '@/components/ProjectList';
import FileUpload from '@/components/FileUpload';
import QueryInterface from '@/components/QueryInterface';
import { ArrowLeft, Upload, MessageSquare, LogOut, User } from 'lucide-react';

export default function DashboardPage() {
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [activeTab, setActiveTab] = useState<'documents' | 'query'>('documents');
  const { user, logout, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  const handleBackToProjects = () => {
    setSelectedProject(null);
    setActiveTab('documents');
  };

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
        <div className="animate-pulse text-green-600">Loading...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
      {/* Header with Glassmorphism */}
      <header className="bg-white/80 backdrop-blur-lg shadow-lg border-b border-green-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {selectedProject && (
                <button
                  onClick={handleBackToProjects}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg bg-green-100 text-green-700 hover:bg-green-200 transition-all duration-200 shadow-sm hover:shadow-md"
                >
                  <ArrowLeft size={20} />
                  <span className="font-medium">Back</span>
                </button>
              )}
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-green-700 to-emerald-600 bg-clip-text text-transparent">
                  {selectedProject ? selectedProject.name : 'RAG Intelligence Platform'}
                </h1>
                {selectedProject?.description && (
                  <p className="text-sm text-gray-600 mt-1">{selectedProject.description}</p>
                )}
              </div>
            </div>

            {/* User Menu */}
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2 px-3 py-2 bg-green-50 rounded-lg border border-green-200">
                <User size={18} className="text-green-600" />
                <span className="text-sm font-medium text-green-800">{user?.name}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-3 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg transition-all duration-200 border border-red-200"
              >
                <LogOut size={18} />
                <span className="text-sm font-medium">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        {!selectedProject ? (
          /* Project Selection View */
          <ProjectList onSelectProject={setSelectedProject} />
        ) : (
          /* Project Detail View with Modern Layout */
          <div className="space-y-6">
            {/* Tab Navigation with Modern Design */}
            <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-lg p-2 inline-flex gap-2 border border-green-100">
              <button
                onClick={() => setActiveTab('documents')}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg text-sm font-semibold transition-all duration-300 ${
                  activeTab === 'documents'
                    ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-lg transform scale-105'
                    : 'text-gray-700 hover:bg-green-50'
                }`}
              >
                <Upload size={18} />
                Documents
              </button>
              <button
                onClick={() => setActiveTab('query')}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg text-sm font-semibold transition-all duration-300 ${
                  activeTab === 'query'
                    ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-lg transform scale-105'
                    : 'text-gray-700 hover:bg-green-50'
                }`}
              >
                <MessageSquare size={18} />
                Query AI
              </button>
            </div>

            {/* Tab Content with Enhanced Card Design */}
            <div className="bg-white/90 backdrop-blur-sm rounded-xl shadow-2xl border border-green-100 overflow-hidden">
              <div className="p-8">
                {activeTab === 'documents' ? (
                  <FileUpload projectId={selectedProject.id} />
                ) : (
                  <div className="h-[calc(100vh-350px)]">
                    <QueryInterface projectId={selectedProject.id} />
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Modern Footer */}
      <footer className="bg-white/80 backdrop-blur-lg border-t border-green-100 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-gray-600">Powered by RAG Technology</span>
            </div>
            <div className="text-gray-500">
              FastAPI · PostgreSQL · Qdrant · Next.js
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
