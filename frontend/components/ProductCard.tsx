export type ProductCardProps = {
  id: string
  title: string
  storeName: string
  price: string
}

export default function ProductCard({ title, storeName, price }: ProductCardProps) {
  return (
    <article className="rounded-xl border border-zinc-200 bg-white p-3 shadow-sm">
      <div className="mb-3 aspect-[4/5] rounded-lg bg-zinc-100" />
      <h3 className="line-clamp-2 text-sm font-medium">{title}</h3>
      <p className="mt-1 text-sm font-semibold">{price}</p>
      <p className="text-xs text-zinc-500">{storeName}</p>
    </article>
  )
}
