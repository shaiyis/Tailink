import { useEffect, useState } from "react";

export function SetAvailabilityPage() {
  const [dogs, setDogs] = useState<{ name: string }[]>([]);
  const [ownerUsername, setOwnerUsername] = useState('');
  const [selectedDogName, setSelectedDogName] = useState('');
  const [place, setPlace] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');

  const token = localStorage.getItem('token');

  useEffect(() => {
    // Fetch current user data to get username
    const fetchUser = async () => {
      const res = await fetch(`${import.meta.env.VITE_API_URL}owner/auth/me/`, {
        headers: { Authorization: `Token ${token}` },
      });
      const data = await res.json();
      setOwnerUsername(data.username);
    };

    // Fetch user's dogs
    const fetchDogs = async () => {
      const res = await fetch(`${import.meta.env.VITE_API_URL}owner/dogs/my/`, {
        headers: { Authorization: `Token ${token}` },
      });
      const data = await res.json();
      setDogs(data); // expecting [{ name: "Pashosho" }, ...]
    };

    fetchUser();
    fetchDogs();
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      owner_username: ownerUsername,
      dog: selectedDogName,
      place_name: place,
      start_time: new Date(startTime).toISOString(),
      end_time: new Date(endTime).toISOString(),
    };

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}owner/owner-availability/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to set availability");

      alert("Availability set!");
    } catch (err) {
      console.error(err);
      alert("Error setting availability");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="bg-white p-6 rounded-2xl shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-4">Set Availability</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Select Dog</label>
            <select
              value={selectedDogName}
              onChange={(e) => setSelectedDogName(e.target.value)}
              required
              className="w-full border border-gray-300 p-2 rounded-xl"
            >
              <option value="">-- Choose a dog --</option>
              {dogs.map((dog, index) => (
                <option key={index} value={dog.name}>
                  {dog.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium">Place</label>
            <input
              type="text"
              className="w-full border border-gray-300 p-2 rounded-xl"
              value={place}
              onChange={(e) => setPlace(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium">Start Time</label>
            <input
              type="datetime-local"
              value={startTime}
              onChange={(e) => setStartTime(e.target.value)}
              className="w-full border border-gray-300 p-2 rounded-xl"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium">End Time</label>
            <input
              type="datetime-local"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
              className="w-full border border-gray-300 p-2 rounded-xl"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-green-500 text-white py-2 rounded-xl hover:bg-green-600 transition"
          >
            Submit Availability
          </button>
        </form>
      </div>
    </div>
  );
}
