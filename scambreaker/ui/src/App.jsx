import React, { useState } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";
import "./App.css";

function App() {
  const [screen, setScreen] = useState("auth");
  const [consent, setConsent] = useState(false);

  // 1. Registration and Login
  if (screen === "auth") {
    return <Login onSuccess={() => setScreen("welcome")} />;
  }

  // 2. Monitoring Dashboard
  if (screen === "monitoring") {
    return <Dashboard onStop={() => setScreen("setup")} />;
  }

  return (
    <div className="app-container">

      {/* 3. Welcome Page */}
      {screen === "welcome" && (
        <div className="page-card">

          <div className="logo">🛡️</div>

          <div className="badge">
            AI-POWERED SCAM PROTECTION
          </div>

          <h1>ScamBreaker</h1>

          <h2>
            Stay One Step Ahead of Scammers
          </h2>

          <p>
            ScamBreaker helps identify suspicious conversations,
            detect manipulation techniques, and provide
            real-time safety guidance.
          </p>

          <button
            className="primary-btn"
            onClick={() => setScreen("privacy")}
          >
            Start Protection →
          </button>

          <div className="features">

            <div className="feature-card">
              <h3>🔍 Scam Detection</h3>
              <p>
                Identify suspicious conversation patterns
                and possible scam attempts.
              </p>
            </div>

            <div className="feature-card">
              <h3>📊 Risk Intelligence</h3>
              <p>
                Understand risk levels and potential
                manipulation techniques.
              </p>
            </div>

            <div className="feature-card">
              <h3>🛡️ Stay Protected</h3>
              <p>
                Receive safety recommendations when
                suspicious activity is detected.
              </p>
            </div>

          </div>

        </div>
      )}

      {/* 4. Privacy Consent Page */}
      {screen === "privacy" && (
        <div className="page-card">

          <div className="logo">🔐</div>

          <h1>Privacy & Consent</h1>

          <p>
            Your privacy matters. ScamBreaker requires
            your permission before accessing your
            laptop microphone.
          </p>

          <div className="info-box">

            <h3>How ScamBreaker Works</h3>

            <p>
              During the demonstration, your phone call
              can be placed on speakerphone.
            </p>

            <p>
              With your permission, the laptop microphone
              can capture the audio for scam analysis
              once microphone integration is enabled.
            </p>

            <p>
              ScamBreaker does not directly intercept
              cellular calls.
            </p>

          </div>

          <label
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              marginTop: "20px",
              marginBottom: "20px",
              textAlign: "left",
            }}
          >
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
            />

            <span>
              I understand and agree to microphone-based
              audio analysis during the demonstration.
            </span>
          </label>

          <button
            className="primary-btn"
            disabled={!consent}
            onClick={() => setScreen("setup")}
            style={{
              opacity: consent ? 1 : 0.5,
              cursor: consent ? "pointer" : "not-allowed",
            }}
          >
            Continue →
          </button>

          <button
            className="secondary-btn"
            onClick={() => setScreen("welcome")}
          >
            ← Back
          </button>

        </div>
      )}

      {/* 5. Protection Setup Page */}
      {screen === "setup" && (
        <div className="page-card">

          <div className="logo">🎙️</div>

          <h1>Protection Setup</h1>

          <h2>Get Ready for Scam Detection</h2>

          <div className="info-box">

            <h3>Step 1: Enable Speakerphone</h3>

            <p>
              Place your phone on speaker mode so
              the laptop microphone can hear the
              conversation.
            </p>

            <h3>Step 2: Position Your Phone</h3>

            <p>
              Keep your phone near the laptop in a
              quiet environment for clearer audio.
            </p>

            <h3>Step 3: Start Monitoring</h3>

            <p>
              Open the monitoring dashboard to view
              scam-risk information and safety guidance.
            </p>

            <p>
              Note: This button opens the dashboard.
              It does not automatically activate
              microphone capture.
            </p>

          </div>

          <button
            className="primary-btn"
            onClick={() => setScreen("monitoring")}
          >
            🛡️ Open Monitoring Dashboard
          </button>

          <button
            className="secondary-btn"
            onClick={() => setScreen("privacy")}
          >
            ← Back
          </button>

        </div>
      )}

    </div>
  );
}

export default App;