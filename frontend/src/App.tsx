import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage, RegisterPage } from './AuthPages';
import { RegisterDetailsPage } from './RegisterDetailsPage';
import { AddDogPage } from './AddDogPage';
import { SetAvailabilityPage } from './SetAvailabilityPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/register/details" element={<RegisterDetailsPage />} />
        <Route path="/dogs" element={<AddDogPage />} />
        <Route path="/set-availability" element={<SetAvailabilityPage />} />
      </Routes>
    </Router>
  );
}

export default App;
