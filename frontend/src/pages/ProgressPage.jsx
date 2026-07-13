import { useState, useEffect, useRef } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import GlassCard from '../components/GlassCard'
import { getProgress } from '../api'

export default function ProgressPage() {
  const { taskId } = useParams()
  const navigate = useNavigate()
  const [progress, setProgress] = useState(0)
  const [message, setMessage] = useState('Starting...')
  const [error, setError] = useState('')
  const intervalRef = useRef(null)

  useEffect(() => {
    const poll = async () => {
      try {
        const data = await getProgress(taskId)
        if (data.error) {
          setError(data.error)
          clearInterval(intervalRef.current)
          return
        }
        setProgress(data.progress || 0)
        setMessage(data.message || 'Processing...')
        if (data.error) {
          setError(data.error)
          clearInterval(intervalRef.current)
        }
        if (data.progress === 100) {
          clearInterval(intervalRef.current)
          setTimeout(() => navigate(`/result/${taskId}`), 800)
        }
      } catch {
        setError('Connection lost. Check if the server is running.')
        clearInterval(intervalRef.current)
      }
    }
    poll()
    intervalRef.current = setInterval(poll, 1500)
    return () => clearInterval(intervalRef.current)
  }, [taskId, navigate])

  return (
    <div className="page-container">
      <GlassCard style={{ textAlign: 'center' }}>
        {error ? (
          <>
            <h1 className="title" style={{ color: '#f87171' }}>
              Error
            </h1>
            <p className="subtitle">{error}</p>
            <button
              className="glass-button"
              onClick={() => navigate('/')}
              style={{ marginTop: '1rem' }}
            >
              Try Again
            </button>
          </>
        ) : (
          <>
            <h1 className="title">Translating Your Document</h1>
            <p className="subtitle">Please wait while we process your document</p>

            <div style={{ margin: '2rem 0' }}>
              <div className="progress-bar-container">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p style={{ fontSize: '1.5rem', fontWeight: '700', marginTop: '1rem', color: '#a78bfa' }}>
                {progress}%
              </p>
            </div>

            <p className="status-text">{message}</p>

            {progress === 0 && (
              <p
                style={{
                  fontSize: '0.8rem',
                  color: 'rgba(255,255,255,0.4)',
                  marginTop: '1rem',
                }}
              >
                The models are loading on first run. This may take a few minutes.
              </p>
            )}
          </>
        )}
      </GlassCard>
    </div>
  )
}
