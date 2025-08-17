import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeart, faUser, faSearch, faPlus } from '@fortawesome/free-solid-svg-icons'
import { faGithub } from '@fortawesome/free-brands-svg-icons'

function App() {
  return (
    <div className="min-h-screen bg-base-100">
      {/* Navbar */}
      <div className="navbar bg-primary text-primary-content">
        <div className="flex-1">
          <a className="btn btn-ghost text-xl">
            <FontAwesomeIcon icon={faHeart} className="mr-2" />
            My Awesome App
          </a>
        </div>
        <div className="flex-none">
          <button className="btn btn-square btn-ghost">
            <FontAwesomeIcon icon={faSearch} />
          </button>
          <button className="btn btn-square btn-ghost">
            <FontAwesomeIcon icon={faUser} />
          </button>
        </div>
      </div>

      {/* Hero Section */}
      <div className="hero min-h-96 bg-base-200">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">Hello there!</h1>
            <p className="py-6">
              This is a sample Vite React app with Tailwind CSS 3.0, DaisyUI, and Font Awesome icons.
            </p>
            <button className="btn btn-primary">
              <FontAwesomeIcon icon={faPlus} className="mr-2" />
              Get Started
            </button>
          </div>
        </div>
      </div>

      {/* Cards Section */}
      <div className="container mx-auto px-4 py-8">
        <h2 className="text-3xl font-bold text-center mb-8">Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <div className="card bg-base-100 shadow-xl">
            <div className="card-body">
              <h2 className="card-title">
                <FontAwesomeIcon icon={faHeart} className="text-red-500" />
                Tailwind CSS 3.0
              </h2>
              <p>Utility-first CSS framework for rapid UI development.</p>
              <div className="card-actions justify-end">
                <button className="btn btn-primary btn-sm">Learn More</button>
              </div>
            </div>
          </div>

          <div className="card bg-base-100 shadow-xl">
            <div className="card-body">
              <h2 className="card-title">
                <FontAwesomeIcon icon={faUser} className="text-blue-500" />
                DaisyUI
              </h2>
              <p>Beautiful component library built on top of Tailwind CSS.</p>
              <div className="card-actions justify-end">
                <button className="btn btn-secondary btn-sm">Explore</button>
              </div>
            </div>
          </div>

          <div className="card bg-base-100 shadow-xl">
            <div className="card-body">
              <h2 className="card-title">
                <FontAwesomeIcon icon={faGithub} className="text-gray-700" />
                Font Awesome
              </h2>
              <p>Thousands of beautiful icons at your disposal.</p>
              <div className="card-actions justify-end">
                <button className="btn btn-accent btn-sm">Icons</button>
              </div>
            </div>
          </div>

        </div>
      </div>

      {/* Footer */}
      <footer className="footer footer-center p-4 bg-base-300 text-base-content">
        <div>
          <p>Copyright © 2024 - All right reserved by My Awesome App</p>
        </div>
      </footer>
    </div>
  )
}

export default App
