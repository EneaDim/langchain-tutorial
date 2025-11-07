import React from 'react'
import { templates, generate } from '../services/api'

export default function Generate({ documentId, onStarted }:{documentId:string, onStarted:(id:string)=>void}) {
  const [tpls,setTpls]=React.useState<any[]>([])
  const [tpl, setTpl] = React.useState<string>("executive_summary")

  React.useEffect(()=>{ templates().then(setTpls) },[])
  const start = async () => {
    const resp = await generate(documentId, tpl)
    onStarted(resp.job_id)
  }
  return (
    <div className="mt-6">
      <h2 className="font-semibold mb-2">Generate</h2>
      <select value={tpl} onChange={e=>setTpl(e.target.value)}>
        {tpls.map(t => <option key={t.id} value={t.id}>{t.title} ({t.content_kind})</option>)}
      </select>
      <button className="ml-2 px-3 py-1 border rounded" onClick={start}>Generate</button>
    </div>
  )
}
