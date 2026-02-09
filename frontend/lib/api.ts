const API_URL = process.env.NEXT_PUBLIC_API_URL

export async function searchProducts(query: string) {
  if (!API_URL) {
    throw new Error('NEXT_PUBLIC_API_URL is not configured')
  }

  const response = await fetch(`${API_URL}/search`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  })

  if (!response.ok) {
    throw new Error('Search request failed')
  }

  return response.json()
}
