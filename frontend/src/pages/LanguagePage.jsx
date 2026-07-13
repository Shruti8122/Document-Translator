import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import GlassCard from '../components/GlassCard'
import { startTranslation, fetchLanguages } from '../api'

export default function LanguagePage() {
  const { taskId } = useParams()
  const navigate = useNavigate()
  const [languages, setLanguages] = useState({})
  const [sourceLang, setSourceLang] = useState('en')
  const [targetLang, setTargetLang] = useState('')
  const [starting, setStarting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchLanguages()
      .then(setLanguages)
      .catch(() => setError('Failed to load languages'))
  }, [])

  const handleStart = async () => {
    if (!targetLang) {
      setError('Please select a target language')
      return
    }
    setStarting(true)
    setError('')
    try {
      const langEntry = Object.entries(languages).find(
        ([_, v]) => v.nllb === targetLang
      )
      const sourceEntry = Object.entries(languages).find(
        ([_, v]) => v.easyocr === sourceLang
      )
      await startTranslation(
        taskId,
        sourceEntry ? sourceEntry[1].easyocr : 'en',
        targetLang
      )
      navigate(`/progress/${taskId}`)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to start translation')
    } finally {
      setStarting(false)
    }
  }

  const langNames = Object.keys(languages).sort()

  return (
    <div className="page-container">
      <GlassCard>
        <h1 className="title">Select Languages</h1>
        <p className="subtitle">Choose the document language and the target translation language</p>

        <div style={{ marginBottom: '1.5rem' }}>
          <label
            style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontSize: '0.9rem',
              color: 'rgba(255,255,255,0.7)',
            }}
          >
            Document Language (for OCR)
          </label>
          <select
            className="glass-select"
            value={sourceLang}
            onChange={(e) => setSourceLang(e.target.value)}
          >
            {langNames.map((name) => (
              <option key={languages[name].easyocr} value={languages[name].easyocr}>
                {name}
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <label
            style={{
              display: 'block',
              marginBottom: '0.5rem',
              fontSize: '0.9rem',
              color: 'rgba(255,255,255,0.7)',
            }}
          >
            Translate to
          </label>
          <select
            className="glass-select"
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
          >
            <option value="">-- Select language --</option>
            {langNames.map((name) => (
              <option key={languages[name].nllb} value={languages[name].nllb}>
                {name}
              </option>
            ))}
          </select>
        </div>

        {error && (
          <p style={{ color: '#f87171', fontSize: '0.9rem', marginBottom: '1rem', textAlign: 'center' }}>
            {error}
          </p>
        )}

        <div style={{ textAlign: 'center' }}>
          <button
            className="glass-button"
            onClick={handleStart}
            disabled={starting || !targetLang}
          >
            {starting ? 'Starting...' : 'Start Translation'}
          </button>
        </div>
      </GlassCard>
    </div>
  )
}
