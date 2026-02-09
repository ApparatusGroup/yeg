import ProductCard, { ProductCardProps } from './ProductCard'

export default function ProductGrid({ products }: { products: ProductCardProps[] }) {
  if (!products.length) {
    return <p className="text-zinc-500">No products yet. Run crawlers to populate inventory.</p>
  }

  return (
    <section className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-4">
      {products.map((p) => (
        <ProductCard key={p.id} {...p} />
      ))}
    </section>
  )
}
