import React from 'react'
import { upload } from '../services/api'

export default function Upload({ onUploaded }: { onUploaded: (id: string)=>void }) {
  const [file, setFile] = React.useState<File|null>(null)
  const send = async () => {
    if (!file) return
    const res = await upload(file)
    onUploaded(res.document_id)
  }
  return (
    <div className="mt-6">
      <h2 className="font-semibold mb-2">Upload</h2>
      <input type="file" onChange={e=>setFile(e.target.files?.[0]||null)} />
      <button className="ml-2 px-3 py-1 border rounded" onClick={send}>Send</button>
    </div>
  )
}
