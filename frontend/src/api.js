import axios from 'axios'

const client = axios.create({ baseURL: '/api' })

export async function uploadFile(file) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await client.post('/upload', form)
  return data
}

export async function startTranslation(taskId, sourceLang, targetLang) {
  const { data } = await client.post('/start-translation', {
    task_id: taskId,
    source_lang: sourceLang,
    target_lang: targetLang,
  })
  return data
}

export async function getProgress(taskId) {
  const { data } = await client.get(`/progress/${taskId}`)
  return data
}

export function getResultUrl(taskId) {
  return `/api/result/${taskId}`
}

export function getDownloadUrl(taskId) {
  return `/api/result/${taskId}/download`
}

export async function fetchLanguages() {
  const { data } = await client.get('/languages')
  return data
}
