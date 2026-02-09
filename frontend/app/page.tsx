import SearchBar from '@/components/SearchBar'

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col items-center justify-center gap-8 px-4">
      <h1 className="text-center text-4xl font-semibold tracking-tight">Find what Edmonton has in stock</h1>
      <SearchBar />
    </main>
  )
}
