import React from 'react'
import { job } from '../services/api'

export default function Status({ jobId }:{jobId:string}) {
  const [data,setData] = React.useState<any>()
  React.useEffect(()=>{
    const t = setInterval(async ()=>setData(await job(jobId)), 1500)
    return ()=>clearInterval(t)
  },[jobId])
  return (
    <div className="mt-6">
      <h2 className="font-semibold mb-2">Status</h2>
      <pre className="bg-gray-100 p-2 rounded">{JSON.stringify(data,null,2)}</pre>
    </div>
  )
}
