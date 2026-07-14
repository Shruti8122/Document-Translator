import { Routes, Route } from "react-router-dom";

import UploadPage from "./pages/UploadPage";
import LanguagePage from "./pages/LanguagePage";
import ProgressPage from "./pages/ProgressPage";
import ResultPage from "./pages/ResultPage";

import AnimatedBackground from "./components/AnimatedBackground";

export default function App() {
  return (
    <>
      <AnimatedBackground />

      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/language/:taskId" element={<LanguagePage />} />
        <Route path="/progress/:taskId" element={<ProgressPage />} />
        <Route path="/result/:taskId" element={<ResultPage />} />
      </Routes>
    </>
  );
}