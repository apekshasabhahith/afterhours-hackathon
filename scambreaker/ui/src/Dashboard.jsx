import React, { useState } from "react";
import "./Dashboard.css";

const scenarios = [
    {
        name: "Fake CBI Officer",
        level: "red",
        score: 95,
        scam_type: "Government Impersonation",
        stage: 4,
        claim: "CBI Officer",
        proof: false,
        reasons: [
            "Threatened immediate arrest",
            "Demanded an immediate money transfer",
            "Created fear and urgency",
            "Claimed government authority without proof"
        ],
        next_move: "May demand an immediate money transfer",
        transcript:
            "Caller: I am calling from CBI. Transfer money immediately to avoid arrest."
    },
    {
        name: "Bank OTP Scam",
        level: "red",
        score: 90,
        scam_type: "Bank Impersonation",
        stage: 4,
        claim: "Bank Employee",
        proof: false,
        reasons: [
            "Requested a confidential OTP",
            "Claimed an account security issue",
            "Attempted to obtain banking information"
        ],
        next_move: "May attempt an unauthorised bank transaction",
        transcript:
            "Caller: I am from your bank. Share the OTP to secure your account."
    },
    {
        name: "Suspicious Delivery Call",
        level: "yellow",
        score: 55,
        scam_type: "Delivery Scam",
        stage: 2,
        claim: "Delivery Agent",
        proof: false,
        reasons: [
            "Requested an unexpected payment",
            "Provided an unverified delivery claim",
            "Used urgency to encourage payment"
        ],
        next_move: "May send a suspicious payment link",
        transcript:
            "Caller: Your parcel is on hold. Pay a small fee using this link."
    },
    {
        name: "Normal Conversation",
        level: "green",
        score: 8,
        scam_type: "No scam detected",
        stage: 1,
        claim: "No suspicious identity claim",
        proof: true,
        reasons: [
            "No suspicious financial demand detected",
            "No threats detected",
            "No obvious manipulation pattern detected"
        ],
        next_move: "No suspicious next action identified",
        transcript:
            "Caller: Hello! I am calling to confirm your appointment for tomorrow."
    },
    {
        name: "Financial Pressure Scam",
        level: "red",
        score: 92,
        scam_type: "Financial Fraud",
        stage: 4,
        claim: "Unknown Caller",
        proof: false,
        reasons: [
            "Demanded immediate payment",
            "Created financial pressure",
            "Discouraged verification",
            "Used urgency to influence the victim"
        ],
        next_move: "May demand additional money",
        transcript:
            "Caller: Transfer the money right now. Do not delay or contact anyone."
    }
];

function Dashboard({ onStop }) {
    const [selected, setSelected] = useState(0);

    const data = scenarios[selected];

    const riskLabel = {
        red: "CRITICAL",
        yellow: "WARNING",
        green: "LOW RISK"
    };

    function downloadReport() {
        window.print();
    }

    function openTelegram() {
        window.open(
            "https://t.me/ScamBreakerSecurityBot",
            "_blank",
            "noopener,noreferrer"
        );
    }

    return (
        <div className="dashboard">

            <header className="dashboard-header">
                <h2>🛡️ ScamBreaker</h2>
                <span>Scenario Testing Mode</span>
            </header>

            <main className="dashboard-content">

                <section className="scenario-selector">
                    <h2>Test Scam Scenarios</h2>
                    <p>Select a scenario to test ScamBreaker.</p>

                    <select
                        value={selected}
                        onChange={(event) =>
                            setSelected(Number(event.target.value))
                        }
                    >
                        {scenarios.map((scenario, index) => (
                            <option key={index} value={index}>
                                {scenario.name}
                            </option>
                        ))}
                    </select>
                </section>

                <section className={`risk-card ${data.level}`}>
                    <h2>Risk Assessment</h2>

                    <div className="risk-score">
                        {data.score}
                        <span>/100</span>
                    </div>

                    <h3>{riskLabel[data.level]}</h3>
                    <p>{data.scam_type}</p>
                </section>

                <section className="dashboard-card">
                    <h3>Identity Verification</h3>
                    <p>
                        <strong>Claimed Identity:</strong> {data.claim}
                    </p>
                    <p>
                        <strong>Verified:</strong>{" "}
                        {data.proof ? "Yes" : "No"}
                    </p>
                </section>

                <section className="dashboard-card">
                    <h3>Manipulation Timeline</h3>

                    {[
                        "Hook",
                        "Fake Authority",
                        "Isolation and Threats",
                        "Financial Exploitation"
                    ].map((stage, index) => (
                        <div
                            key={index}
                            className={`timeline-item ${index + 1 <= data.stage ? "active" : ""
                                }`}
                        >
                            <span>{index + 1}</span>
                            <p>{stage}</p>
                        </div>
                    ))}

                    <p>
                        <strong>Current Stage:</strong> {data.stage}/4
                    </p>
                </section>

                <section className="dashboard-card">
                    <h3>Conversation Analysis</h3>
                    <div className="transcript">
                        {data.transcript}
                    </div>
                </section>

                <section className="dashboard-card">
                    <h3>Why Was This Detected?</h3>

                    {data.reasons.map((reason, index) => (
                        <p className="reason" key={index}>
                            ⚠️ {reason}
                        </p>
                    ))}
                </section>

                <section className="dashboard-card">
                    <h3>Predicted Next Move</h3>
                    <p>{data.next_move}</p>
                </section>

                {data.level === "red" && (
                    <section className="emergency-card">
                        🚨 Critical Scam Warning!

                        <p>
                            Do not transfer money or share OTPs or banking
                            information. Verify the caller independently.
                        </p>

                        <p>
                            If you have lost money to cyber fraud in India,
                            call 1930 immediately.
                        </p>
                    </section>
                )}

                {/* Telegram Alerts */}
                <section className="telegram-card">
                    <div className="telegram-heading">
                        <span className="telegram-icon">✈️</span>
                        <div>
                            <h3>Telegram Scam Alerts</h3>
                            <p>Get scam warnings through Telegram.</p>
                        </div>
                    </div>

                    <div className="telegram-status">
                        <span className="status-indicator"></span>
                        Bot available — backend connection pending
                    </div>

                    <button
                        className="telegram-button"
                        onClick={openTelegram}
                    >
                        Open ScamBreaker Bot ↗
                    </button>

                    <p className="telegram-note">
                        Open the bot and press Start to activate your
                        Telegram conversation. Automatic scam alerts
                        will work after backend integration.
                    </p>
                </section>

                {/* Action Buttons */}
                <div className="action-buttons">

                    <button
                        className="download-button"
                        onClick={downloadReport}
                    >
                        📄 Download Report
                    </button>

                    <button
                        className="stop-button"
                        onClick={onStop}
                    >
                        Stop Protection
                    </button>

                </div>

            </main>
        </div>
    );
}

export default Dashboard;