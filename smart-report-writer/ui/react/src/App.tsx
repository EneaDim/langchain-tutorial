import React from 'react'
import Upload from './pages/Upload'
import Generate from './pages/Generate'
import Status from './pages/Status'

export default function App() {
  const [docId, setDocId] = React.useState<string|undefined>()
  const [jobId, setJobId] = React.useState<string|undefined>()

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold">Smart Report Writer</h1>
      <Upload onUploaded={setDocId}/>
      {docId && <Generate documentId={docId} onStarted={setJobId} />}
      {jobId && <Status jobId={jobId} />}
    </div>
  )
}
