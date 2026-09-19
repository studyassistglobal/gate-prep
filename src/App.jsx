import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout.jsx';
import Home from './pages/Home.jsx';
import Course from './pages/Course.jsx';
import Chapter from './pages/Chapter.jsx';
import Tests from './pages/Tests.jsx';
import NotFound from './pages/NotFound.jsx';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="/course/:courseId" element={<Course />} />
        <Route path="/course/:courseId/:subjectId/:chapterId" element={<Chapter />} />
        <Route path="/tests" element={<Tests />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
