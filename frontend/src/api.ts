const apiUrl = import.meta.env.VITE_API_URL;  // ✅ Vite uses import.meta.env!

export async function fetchOwners() {
    const response = await fetch(`${apiUrl}/owners/`);
    if (!response.ok) throw new Error('Failed to fetch owners');
    return await response.json();
  }