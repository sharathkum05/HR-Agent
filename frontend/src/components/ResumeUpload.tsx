"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { jobsApi } from "@/lib/api";
import { Upload, File, X, CheckCircle2 } from "lucide-react";

interface ResumeUploadProps {
  jobId: number;
  onUploadComplete?: (count: number) => void;
}

export function ResumeUpload({ jobId, onUploadComplete }: ResumeUploadProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [uploadCount, setUploadCount] = useState(0);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const pdfFiles = acceptedFiles.filter(
      (file) => file.type === "application/pdf" || file.name.endsWith(".pdf")
    );
    setFiles((prev) => [...prev, ...pdfFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
    },
  });

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) return;

    setUploading(true);
    try {
      const result = await jobsApi.uploadResumes(jobId, files);
      setUploadCount(result.uploaded);
      setUploaded(true);
      setFiles([]);
      if (onUploadComplete) {
        onUploadComplete(result.uploaded);
      }
    } catch (error) {
      console.error("Error uploading resumes:", error);
      alert("Failed to upload resumes. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Upload Resumes</CardTitle>
        <CardDescription>
          Upload PDF resumes for candidate screening (up to 100 resumes)
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {!uploaded ? (
          <>
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                isDragActive
                  ? "border-primary bg-primary/5"
                  : "border-gray-300 hover:border-primary/50"
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <p className="text-sm text-gray-600 mb-2">
                {isDragActive
                  ? "Drop the PDF files here"
                  : "Drag & drop PDF resumes here, or click to select"}
              </p>
              <p className="text-xs text-gray-500">
                Only PDF files are supported
              </p>
            </div>

            {files.length > 0 && (
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium">
                    {files.length} file{files.length !== 1 ? "s" : ""} selected
                  </p>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setFiles([])}
                  >
                    Clear All
                  </Button>
                </div>
                <div className="max-h-48 overflow-y-auto space-y-2">
                  {files.map((file, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-2 bg-gray-50 rounded"
                    >
                      <div className="flex items-center space-x-2">
                        <File className="h-4 w-4 text-gray-500" />
                        <span className="text-sm">{file.name}</span>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => removeFile(index)}
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
                <Button
                  onClick={handleUpload}
                  disabled={uploading || files.length === 0}
                  className="w-full"
                >
                  {uploading ? "Uploading..." : `Upload ${files.length} Resume${files.length !== 1 ? "s" : ""}`}
                </Button>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-8">
            <CheckCircle2 className="mx-auto h-12 w-12 text-green-500 mb-4" />
            <p className="text-lg font-semibold mb-2">
              Successfully uploaded {uploadCount} resume{uploadCount !== 1 ? "s" : ""}!
            </p>
            <Button
              variant="outline"
              onClick={() => {
                setUploaded(false);
                setUploadCount(0);
              }}
            >
              Upload More Resumes
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

