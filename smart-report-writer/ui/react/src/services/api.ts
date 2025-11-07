import axios from 'axios'
const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

export async function upload(file: File){
  const form = new FormData()
  form.append('file', file)
  const {data} = await axios.post(`${base}/v1/uploads`, form)
  return data.data
}
export async function templates(){
  const {data} = await axios.get(`${base}/v1/templates`)
  return data.data
}
export async function generate(document_id: string, template_id: string){
  const {data} = await axios.post(`${base}/v1/generate`, {document_id, template_id})
  return data
}
export async function job(job_id: string){
  const {data} = await axios.get(`${base}/v1/jobs/${job_id}`)
  return data
}
