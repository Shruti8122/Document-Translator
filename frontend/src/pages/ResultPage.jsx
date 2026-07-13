import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import GlassCard from '../components/GlassCard'
import { getResultUrl, getDownloadUrl } from '../api'

export default function ResultPage() {
  const { taskId } = useParams()
  const navigate = useNavigate()
  const [ready, setReady] = useState(false)

  useEffect(() => {
    setReady(true)
  }, [taskId])

  const pdfUrl = getResultUrl(taskId)
  const downloadUrl = getDownloadUrl(taskId)

  return (
    <div className="page-container">
      <GlassCard style={{ maxWidth: '900px' }}>
        <h1 className="title">Translation Complete</h1>
        <p className="subtitle">Your translated document is ready</p>

        {ready && (
          <>
            <iframe
              src={pdfUrl}
              className="pdf-embed"
              title="Translated PDF"
            />
            <div className="button-group">
              <a href={downloadUrl} download className="glass-button" style={{ textDecoration: 'none' }}>
                Download PDF
              </a>
              <button
                className="glass-button"
                onClick={() => navigate('/')}
                style={{ background: 'rgba(255,255,255,0.1)', borderColor: 'rgba(255,255,255,0.2)' }}
              >
                Translate Another
              </button>
            </div>
          </>
        )}
      </GlassCard>
    </div>
  )
}
