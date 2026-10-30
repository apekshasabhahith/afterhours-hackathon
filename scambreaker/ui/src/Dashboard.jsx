import React from "react";
import "./Dashboard.css";

function Dashboard({ onStop }) {

    // Sample API response
    // Later, P2's WebSocket will provide this data.

    const data = {
        level: "red",
        score: 90,
        scam_type: "cbi",
        stage: 4,
        claim: "CBI Officer",
        proof: false,
        reasons: [
            "Demanded immediate money transfer",
            "Threatened immediate arrest",
            "Created fear and urgency",
            "Claimed government authority without proof"
        ],
        next_move: "May demand an immediate transfer"
    };

    const stages = [
        {
            number: 1,
            title: "Hook",
            description: "Initial contact",
        },
        {
            number: 2,
            title: "Fake Authority",
            description: "Impersonation",
        },
        {
            number: 3,
            title: "Isolation & Threats",
            description: "Fear and pressure",
        },
        {
            number: 4,
            title: "Financial Exploitation",
            description: "Money demand",
        }
    ];

    return (

        <div className="dashboard">

            {/* HEADER */}

            <header className="dash-header">

                <div className="dash-logo">
                    🛡️ ScamBreaker
                    <span>INTELLIGENCE</span>
                </div>

                <div className="monitor-status">
                    <span className="red-dot"></span>
                    DEMO ANALYSIS
                </div>

            </header>


            <main className="dash-content">

                {/* PAGE TITLE */}

                <div className="dash-heading">

                    <div>
                        <p className="eyebrow">
                            SECURITY OVERVIEW
                        </p>

                        <h1>Threat Analysis</h1>

                        <p>
                            Understand suspicious conversation behaviour.
                        </p>
                    </div>

                    <div className="demo-label">
                        SAMPLE DATA
                    </div>

                </div>


                {/* EMERGENCY WARNING */}

                {data.level === "red" && (

                    <section className="emergency-alert">

                        <div className="alert-symbol">⚠️</div>

                        <div>
                            <h3>CRITICAL RISK DETECTED</h3>

                            <p>
                                Suspicious manipulation and financial
                                exploitation indicators detected.
                            </p>
                        </div>

                    </section>

                )}


                {/* RISK SCORE */}

                <section className="risk-card">

                    <div className="risk-info">

                        <p className="card-label">
                            OVERALL RISK SCORE
                        </p>

                        <h2>Threat Assessment</h2>

                        <p>
                            Risk level based on conversation analysis.
                        </p>

                    </div>

                    <div className="risk-score">

                        <div className="score-circle">
                            <strong>{data.score}</strong>
                            <span>/100</span>
                        </div>

                        <div className="risk-level">
                            HIGH RISK
                        </div>

                    </div>

                </section>


                {/* ANALYSIS GRID */}

                <section className="analysis-grid">


                    {/* SCAM TYPE */}

                    <div className="dash-card">

                        <p className="card-label">
                            IDENTIFIED SCAM
                        </p>

                        <h2>CBI Impersonation</h2>

                        <p className="muted">
                            Suspected government authority impersonation.
                        </p>

                        <div className="tag red-tag">
                            HIGH RISK
                        </div>

                    </div>


                    {/* IDENTITY */}

                    <div className="dash-card">

                        <p className="card-label">
                            CLAIMED IDENTITY
                        </p>

                        <h2>{data.claim}</h2>

                        <div className="verification">
                            <span>✕</span>
                            NOT VERIFIED
                        </div>

                        <p className="muted">
                            No verification proof provided.
                        </p>

                    </div>


                    {/* NEXT MOVE */}

                    <div className="dash-card prediction-card">

                        <p className="card-label">
                            AI NEXT-MOVE PREDICTION
                        </p>

                        <h2>What might happen next?</h2>

                        <p className="prediction-text">
                            {data.next_move}
                        </p>

                        <div className="prediction-tag">
                            PREDICTED ACTION
                        </div>

                    </div>


                </section>


                {/* MANIPULATION TIMELINE */}

                <section className="dash-card timeline-card">

                    <div className="section-heading">

                        <div>
                            <p className="card-label">
                                BEHAVIOURAL ANALYSIS
                            </p>

                            <h2>Manipulation Timeline</h2>
                        </div>

                        <span className="stage-count">
                            Stage {data.stage} of 4
                        </span>

                    </div>


                    <div className="timeline">

                        {stages.map((stage) => (

                            <div
                                className={`timeline-stage ${stage.number <= data.stage ? "active-stage" : ""
                                    } ${stage.number === data.stage ? "current-stage" : ""
                                    }`}
                                key={stage.number}
                            >

                                <div className="stage-circle">
                                    {stage.number <= data.stage ? "✓" : stage.number}
                                </div>

                                <h3>{stage.title}</h3>

                                <p>{stage.description}</p>

                                {stage.number === data.stage && (

                                    <span className="current-label">
                                        CURRENT STAGE
                                    </span>

                                )}

                            </div>

                        ))}

                    </div>

                </section>


                {/* TRANSCRIPT AND REASONS */}

                <section className="analysis-grid">


                    {/* TRANSCRIPT */}

                    <div className="dash-card">

                        <p className="card-label">
                            CONVERSATION MONITOR
                        </p>

                        <h2>Live Transcript</h2>

                        <div className="transcript">

                            <p>
                                <span>CALLER</span>
                                Your bank account is under investigation.
                            </p>

                            <p>
                                <span>CALLER</span>
                                We are from the CBI department.
                            </p>

                            <p className="suspicious-text">
                                <span>WARNING</span>
                                Transfer money immediately to avoid arrest.
                            </p>

                        </div>

                        <p className="muted demo-note">
                            Illustrative sample transcript. Not live audio.
                        </p>

                    </div>


                    {/* WARNING REASONS */}

                    <div className="dash-card">

                        <p className="card-label">
                            EXPLAINABLE AI
                        </p>

                        <h2>Why is this suspicious?</h2>

                        <div className="reason-list">

                            {data.reasons.map((reason, index) => (

                                <div className="reason" key={index}>

                                    <span>⚠</span>

                                    <p>{reason}</p>

                                </div>

                            ))}

                        </div>

                    </div>

                </section>


                {/* TELEGRAM STATUS */}

                <section className="telegram-card">

                    <div>
                        <h3>✈️ Telegram Notifications</h3>

                        <p>
                            Notification integration pending.
                        </p>
                    </div>

                    <span className="pending-tag">
                        NOT CONNECTED
                    </span>

                </section>


                {/* EMERGENCY GUIDANCE */}

                <section className="emergency-guidance">

                    <h2>Already transferred money?</h2>

                    <p>
                        Contact your bank immediately to report
                        the transaction and request assistance.
                        In India, call cybercrime helpline 1930
                        and report the incident through the
                        National Cyber Crime Reporting Portal.
                    </p>

                </section>


                {/* FOOTER BUTTONS */}

                <div className="dashboard-actions">

                    <button
                        className="report-button"
                        onClick={() => alert(
                            "PDF report integration will be connected with P2's backend."
                        )}
                    >
                        ↓ Download PDF Report
                    </button>

                    <button
                        className="stop-button"
                        onClick={onStop}
                    >
                        ■ Stop Protection
                    </button>

                </div>


            </main>

            <footer className="dash-footer">
                ScamBreaker © 2026 | Digital Safety Intelligence
            </footer>

        </div>

    );

}

export default Dashboard;