"use client";

import { useState, useEffect, useRef } from 'react';
import { Document, getDocuments, uploadDocument, deleteDocument } from '@/lib/api';
import { Upload, File, CheckCircle, XCircle, Clock, Trash2, AlertCircle } from 'lucide-react';

interface FileUploadProps {
  projectId: string;
}

export default function FileUpload({ projectId }: FileUploadProps) {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Load documents on mount
  useEffect(() => {
    loadDocuments();
  }, [projectId]);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getDocuments(projectId);
      setDocuments(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load documents');
      console.error('Error loading documents:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFiles(files);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files ? Array.from(e.target.files) : [];
    if (files.length > 0) {
      handleFiles(files);
    }
  };

  const handleFiles = async (files: File[]) => {
    setError(null);

    for (const file of files) {
      // Validate file type
      const allowedTypes = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'text/plain',
      ];

      if (!allowedTypes.includes(file.type)) {
        setError(`File type not supported: ${file.name}. Please upload PDF, DOCX, XLSX, or TXT files.`);
        continue;
      }

      // Validate file size (50MB max)
      const maxSize = 50 * 1024 * 1024; // 50MB
      if (file.size > maxSize) {
        setError(`File too large: ${file.name}. Maximum size is 50MB.`);
        continue;
      }

      await uploadFile(file);
    }
  };

  const uploadFile = async (file: File) => {
    try {
      setUploading(true);
      await uploadDocument(projectId, file);
      await loadDocuments();
    } catch (err: any) {
      setError(err.response?.data?.detail || `Failed to upload ${file.name}`);
      console.error('Error uploading file:', err);
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (documentId: string) => {
    if (!confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      await deleteDocument(projectId, documentId);
      await loadDocuments();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete document');
      console.error('Error deleting document:', err);
    }
  };

  const getStatusIcon = (status: Document['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="text-green-500" size={20} />;
      case 'processing':
        return <Clock className="text-blue-500 animate-spin" size={20} />;
      case 'failed':
        return <XCircle className="text-red-500" size={20} />;
      default:
        return <Clock className="text-gray-400" size={20} />;
    }
  };

  const getStatusText = (status: Document['status']) => {
    switch (status) {
      case 'completed':
        return 'Processed';
      case 'processing':
        return 'Processing...';
      case 'failed':
        return 'Failed';
      default:
        return 'Pending';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
        }`}
      >
        <Upload className="mx-auto text-gray-400 mb-4" size={48} />
        <h3 className="text-lg font-medium text-gray-700 mb-2">Upload Documents</h3>
        <p className="text-gray-500 mb-4">
          Drag and drop files here, or click to browse
        </p>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.docx,.xlsx,.txt"
          onChange={handleFileChange}
          className="hidden"
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {uploading ? 'Uploading...' : 'Select Files'}
        </button>
        <p className="text-xs text-gray-400 mt-4">
          Supported: PDF, DOCX, XLSX, TXT (Max 50MB each)
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-start gap-2">
          <AlertCircle size={20} className="flex-shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {/* Documents List */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Uploaded Documents ({documents.length})
        </h3>

        {loading ? (
          <div className="text-center py-8 text-gray-500">Loading documents...</div>
        ) : documents.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No documents uploaded yet. Upload your first document to get started.
          </div>
        ) : (
          <div className="space-y-2">
            {documents.map((doc) => (
              <div
                key={doc.id}
                className="flex items-center justify-between bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center gap-3 flex-1">
                  <File className="text-gray-400 flex-shrink-0" size={24} />
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-gray-800 truncate">{doc.filename}</h4>
                    <div className="flex items-center gap-4 text-sm text-gray-500 mt-1">
                      <span>{formatFileSize(doc.file_size)}</span>
                      <span>{doc.chunk_count} chunks</span>
                      <span>Uploaded {new Date(doc.uploaded_at).toLocaleDateString()}</span>
                    </div>
                    {doc.error_message && (
                      <p className="text-sm text-red-600 mt-1">{doc.error_message}</p>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    {getStatusIcon(doc.status)}
                    <span className="text-sm font-medium text-gray-600">
                      {getStatusText(doc.status)}
                    </span>
                  </div>
                  <button
                    onClick={() => handleDeleteDocument(doc.id)}
                    className="text-red-500 hover:text-red-700 transition-colors"
                    title="Delete document"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
