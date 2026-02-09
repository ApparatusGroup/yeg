'use client'

import { useRouter } from 'next/navigation'
import { FormEvent, useState } from 'react'

export default function SearchBar() {
  const [query, setQuery] = useState('')
  const router = useRouter()

  const submit = (e: FormEvent) => {
    e.preventDefault()
    router.push(`/search?q=${encodeURIComponent(query)}`)
  }

  return (
    <form onSubmit={submit} className="flex w-full max-w-2xl gap-2">
      <input
        className="w-full rounded-xl border border-zinc-300 bg-white px-4 py-3"
        placeholder="Find local honey..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button className="rounded-xl bg-[#00205B] px-4 py-3 font-medium text-white">Search</button>
    </form>
  )
}
