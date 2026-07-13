import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDropzone } from 'react-dropzone'
import GlassCard from '../components/GlassCard'
import { uploadFile } from '../api'

export default function UploadPage() {
  const navigate = useNavigate()
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')

  const onDrop = useCallback((accepted) => {
    const f = accepted[0]
    if (f && f.type === 'application/pdf') {
      setFile(f)
      setError('')
    } else {
      setError('Please upload a valid PDF file')
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    multiple: false,
  })

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    setError('')
    try {
      const { task_id } = await uploadFile(file)
      navigate(`/language/${task_id}`)
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="page-container">
      <GlassCard>
        <h1 className="title">Doc Translator</h1>
        <p className="subtitle">Upload a PDF document to translate it into any language</p>

        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          {isDragActive ? (
            <p style={{ color: 'rgba(255,255,255,0.8)' }}>Drop your PDF here...</p>
          ) : (
            <div>
              <p style={{ fontSize: '0.95rem', color: 'rgba(255,255,255,0.7)' }}>
                Drag & drop a PDF here, or click to browse
              </p>
              <p style={{ fontSize: '0.8rem', color: 'rgba(255,255,255,0.4)', marginTop: '0.5rem' }}>
                Only .pdf files up to 50MB
              </p>
            </div>
          )}
        </div>

        {file && (
          <div className="file-info">
            <span style={{ fontSize: '1.2rem' }}>📄</span>
            <span>{file.name}</span>
            <span style={{ color: 'rgba(255,255,255,0.4)', fontSize: '0.85rem' }}>
              ({(file.size / 1024 / 1024).toFixed(1)} MB)
            </span>
          </div>
        )}

        {error && (
          <p style={{ color: '#f87171', fontSize: '0.9rem', marginTop: '1rem', textAlign: 'center' }}>
            {error}
          </p>
        )}

        <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
          <button
            className="glass-button"
            onClick={handleUpload}
            disabled={!file || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload & Continue'}
          </button>
        </div>
      </GlassCard>
    </div>
  )
}
