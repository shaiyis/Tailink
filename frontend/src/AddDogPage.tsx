import { useState } from "react";
import { useNavigate } from "react-router-dom";

export function AddDogPage() {
  const [name, setName] = useState('');
  const [breed, setBreed] = useState('');
  const [age, setAge] = useState('');
  const [about, setAbout] = useState('');
  const [picture, setPicture] = useState<File | null>(null);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('name', name);
    formData.append('breed', breed);
    formData.append('age', age);
    formData.append('about', about);
    if (picture) formData.append('picture', picture);

    const token = localStorage.getItem("token"); // or however you store it

    try {
      for (const pair of formData.entries()) {
          console.log(`${pair[0]}:`, pair[1]);
      }
      console.log(token)     
      
      const response = await fetch(`${import.meta.env.VITE_API_URL}owner/dogs/my/`, {
        method: 'POST',
        headers: {
          Authorization: `Token ${token}`,
        },
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to add dog");

      alert("Dog added successfully!");
      navigate('/set-availability'); // or wherever you want to go
    } catch (error) {
      console.error(error);
      alert("Error adding dog");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="bg-white p-6 rounded-2xl shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-6">🐶 Add Your Dog</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium">Name</label>
            <input
              type="text"
              className="w-full border border-gray-300 p-2 rounded-xl"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Breed</label>
            <input
              type="text"
              className="w-full border border-gray-300 p-2 rounded-xl"
              value={breed}
              onChange={(e) => setBreed(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Age</label>
            <input
              type="number"
              className="w-full border border-gray-300 p-2 rounded-xl"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">About</label>
            <textarea
              className="w-full border border-gray-300 p-2 rounded-xl"
              value={about}
              onChange={(e) => setAbout(e.target.value)}
              rows={3}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium">Picture</label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) =>
                setPicture(e.target.files ? e.target.files[0] : null)
              }
              className="w-full"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-green-500 text-white py-2 rounded-xl hover:bg-green-600 transition"
          >
            Add Dog
          </button>
        </form>
      </div>
    </div>
  );
}
