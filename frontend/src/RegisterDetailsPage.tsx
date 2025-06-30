import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

export function RegisterDetailsPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const { username, email, password } = location.state || {};
  
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [gender, setGender] = useState('');
    const [age, setAge] = useState('');
    const [city, setCity] = useState('');
    const [aboutMe, setAboutMe] = useState('');
    const [picture, setPicture] = useState<File | null>(null);
  
    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
  
      const formData = new FormData();
      formData.append("username", username);
      formData.append("email", email);
      formData.append("password", password);
      formData.append("first_name", firstName);
      formData.append("last_name", lastName);
      formData.append("gender", gender);
      formData.append("age", age);
      formData.append("city", city);
      formData.append("about_me", aboutMe);
      if (picture) formData.append("picture", picture);
  
      try {
        /*for (const pair of formData.entries()) {
            console.log(`${pair[0]}:`, pair[1]);
        }*/         
        const response = await fetch(`${import.meta.env.VITE_API_URL}owner/register/`, {
          method: "POST",
          body: formData,
        });
  
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Register failed:', errorData);
            const errorMessage = errorData.non_field_errors?.[0] || errorData.detail || 'Unknown error';
            alert('Register failed: ' + errorMessage);
            return;
        }
        
        // Handle the response if the status is 201 (Created)
        else if (response.status === 201) { 
            const data = await response.json();
            console.log('Registered successfully:', data);
        }

        // Redirect to login page after successful registration
        navigate("/login");
      } catch (error) {
        alert("Failed to register");
      }
    };
  
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
          <div className="bg-white p-6 rounded-2xl shadow-md w-full max-w-md">
            <h1 className="text-3xl font-bold text-center mb-6">🐾 Complete your profile</h1>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium">First Name</label>
                <input
                  type="text"
                  className="w-full border border-gray-300 p-2 rounded-xl"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Last Name</label>
                <input
                  type="text"
                  className="w-full border border-gray-300 p-2 rounded-xl"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Gender</label>
                <select
                  className="w-full border border-gray-300 p-2 rounded-xl"
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  required
                >
                  <option value="" disabled>
                    Select your gender
                  </option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                  <option value="prefer_not_to_say">Prefer not to say</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium">Age</label>
                <input
                  type="number"
                  min="0"
                  max="120"
                  className="w-full border border-gray-300 p-2 rounded-xl"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium">City</label>
                <input
                  type="text"
                  className="w-full border border-gray-300 p-2 rounded-xl"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium">About Me</label>
                <textarea
                  className="w-full border border-gray-300 p-2 rounded-xl"
                  value={aboutMe}
                  onChange={(e) => setAboutMe(e.target.value)}
                  rows={4}
                  placeholder="Tell us a bit about yourself"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Profile Picture</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => {
                    if (e.target.files && e.target.files.length > 0) {
                      setPicture(e.target.files[0]);
                      // console.log("Selected file:", e.target.files?.[0]);
                    } else {
                      setPicture(null);
                    }
                  }}
                  className="w-full"
                />
              </div>
    
              <button
                type="submit"
                className="w-full bg-green-500 text-white py-2 rounded-xl hover:bg-green-600 transition"
              >
                Complete Registration
              </button>
            </form>
          </div>
        </div>
    );
}
  