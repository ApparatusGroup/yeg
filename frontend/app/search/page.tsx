import ProductGrid from '@/components/ProductGrid'
import SearchBar from '@/components/SearchBar'

export default function SearchPage() {
  return (
    <main className="mx-auto max-w-7xl p-4">
      <div className="mb-6">
        <SearchBar />
      </div>
      <ProductGrid products={[]} />
    </main>
  )
}
