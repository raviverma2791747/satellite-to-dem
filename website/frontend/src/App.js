import { Route, Routes } from "react-router-dom";
import  Home  from "./pages/home/Home";
import  About  from "./pages/about/About";
import Header from "./components/Header";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="d-flex flex-column justify-content-between min-vh-100">
      <Header/>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
      <Footer/>
    </div>
  );
}

export default App;
