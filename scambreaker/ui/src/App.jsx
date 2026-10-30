import React, { useState } from "react";
import "./App.css";
import Dashboard from "./Dashboard";

function App() {
  const [screen, setScreen] = useState("welcome");
  const [consent, setConsent] = useState(false);

  // Dashboard navigation
  if (screen === "monitoring") {
    return (
      <Dashboard
        onStop={() => setScreen("setup")}
      />
    );
  }

  return (
    <div className="app">

      <nav className="navbar">
        <div className="logo">🛡️ ScamBreaker</div>

        <div className="status">
          <span className="status-dot"></span>
          {screen === "welcome"
            ? "Protection System"
            : screen === "privacy"
              ? "Privacy First"
              : "Protection Setup"}
        </div>
      </nav>

      {/* WELCOME SCREEN */}

      {screen === "welcome" && (
        <main className="welcome">

          <div className="badge">
            CYBERSECURITY INTELLIGENCE
          </div>

          <h1>
            Don't let scams
            <br />
            <span>control your decisions.</span>
          </h1>

          <p className="subtitle">
            Real-time scam conversation analysis.
            <br />
            Understand manipulation before it's too late.
          </p>

          <div className="welcome-buttons">
            <button
              className="start-button"
              onClick={() => setScreen("privacy")}
            >
              Start Protection →
            </button>
          </div>

          <div className="features">

            <div className="feature-card">
              <span className="feature-icon">🔍</span>
              <h3>Scam Detection</h3>
              <p>
                Identify suspicious conversations
                and impersonation attempts.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">📊</span>
              <h3>Risk Intelligence</h3>
              <p>
                Understand manipulation stages
                and suspicious behaviour.
              </p>
            </div>

            <div className="feature-card">
              <span className="feature-icon">🛡️</span>
              <h3>Stay Protected</h3>
              <p>
                Receive warnings and guidance
                before taking risky actions.
              </p>
            </div>

          </div>
        </main>
      )}

      {/* PRIVACY SCREEN */}

      {screen === "privacy" && (
        <main className="privacy-container">

          <div className="privacy-icon">🔐</div>

          <div className="badge">
            YOUR PRIVACY MATTERS
          </div>

          <h1 className="privacy-title">
            Your safety.
            <br />
            <span>Your control.</span>
          </h1>

          <p className="privacy-description">
            Before starting ScamBreaker, please understand
            how your conversation data is used.
          </p>

          <div className="privacy-card">

            <div className="privacy-item">
              <span>🎙️</span>
              <div>
                <h3>Microphone Access</h3>
                <p>
                  ScamBreaker uses your laptop microphone
                  to capture nearby phone speakerphone audio
                  after permission and activation.
                </p>
              </div>
            </div>

            <div className="privacy-item">
              <span>🔍</span>
              <div>
                <h3>Conversation Analysis</h3>
                <p>
                  Captured audio is used for scam analysis
                  and identifying manipulation techniques.
                </p>
              </div>
            </div>

            <div className="privacy-item">
              <span>🛑</span>
              <div>
                <h3>You Are In Control</h3>
                <p>
                  You can stop protection whenever you want.
                  ScamBreaker does not automatically intercept
                  cellular calls.
                </p>
              </div>
            </div>

            <div className="privacy-item">
              <span>🔒</span>
              <div>
                <h3>Consent Required</h3>
                <p>
                  Monitoring starts only after you explicitly
                  provide consent and activate protection.
                  Obtain consent from other participants
                  where required.
                </p>
              </div>
            </div>

          </div>

          <label className="consent-label">
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
            />

            <span>
              I understand and agree to the privacy
              and microphone usage policy.
            </span>
          </label>

          <div className="privacy-buttons">

            <button
              className="back-button"
              onClick={() => setScreen("welcome")}
            >
              ← Back
            </button>

            <button
              className="start-button"
              disabled={!consent}
              onClick={() => setScreen("setup")}
            >
              Continue →
            </button>

          </div>

        </main>
      )}

      {/* PROTECTION SETUP SCREEN */}

      {screen === "setup" && (
        <main className="privacy-container">

          <div className="privacy-icon">🎙️</div>

          <div className="badge">
            ALMOST READY
          </div>

          <h1 className="privacy-title">
            Set up your
            <br />
            <span>protection.</span>
          </h1>

          <p className="privacy-description">
            Complete these steps before starting
            ScamBreaker monitoring.
          </p>

          <div className="privacy-card">

            <div className="privacy-item">
              <span>📱</span>
              <div>
                <h3>Step 1: Prepare your phone</h3>
                <p>
                  Place your phone nearby and enable
                  speakerphone during the conversation.
                </p>
              </div>
            </div>

            <div className="privacy-item">
              <span>💻</span>
              <div>
                <h3>Step 2: Prepare your laptop</h3>
                <p>
                  Keep your laptop microphone enabled
                  and positioned near your phone.
                </p>
              </div>
            </div>

            <div className="privacy-item">
              <span>🔐</span>
              <div>
                <h3>Step 3: Allow microphone access</h3>
                <p>
                  ScamBreaker will request microphone
                  permission when monitoring starts.
                </p>
              </div>
            </div>

          </div>

          <div className="privacy-buttons">

            <button
              className="back-button"
              onClick={() => setScreen("privacy")}
            >
              ← Back
            </button>

            <button
              className="start-button"
              onClick={() => setScreen("monitoring")}
            >
              Start Monitoring →
            </button>

          </div>

        </main>
      )}

      {screen === "welcome" && (
        <footer>
          ScamBreaker © 2026 | Your Digital Safety Companion
        </footer>
      )}

    </div>

  );
}

export default App;