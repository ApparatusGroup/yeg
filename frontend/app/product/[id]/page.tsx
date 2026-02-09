export default function ProductDetailsPage({ params }: { params: { id: string } }) {
  return (
    <main className="mx-auto max-w-4xl p-4">
      <h1 className="text-2xl font-semibold">Product {params.id}</h1>
      <p className="mt-2 text-zinc-600">Product detail screen scaffold.</p>
    </main>
  )
}
