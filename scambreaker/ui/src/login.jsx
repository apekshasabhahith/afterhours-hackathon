import React, { useState } from "react";
import "./Login.css";

function PasswordInput({ value, onChange, placeholder }) {
    const [visible, setVisible] = useState(false);

    return (
        <div style={{ position: "relative", width: "100%", marginBottom: "15px" }}>
            <input
                type={visible ? "text" : "password"}
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                style={{
                    width: "100%",
                    boxSizing: "border-box",
                    paddingRight: "45px",
                    marginBottom: 0
                }}
            />

            <button
                type="button"
                onClick={() => setVisible(!visible)}
                aria-label={visible ? "Hide password" : "Show password"}
                style={{
                    position: "absolute",
                    right: "12px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    background: "transparent",
                    border: "none",
                    padding: "4px",
                    cursor: "pointer",
                    fontSize: "17px",
                    color: "#55baff",
                    width: "30px",
                    height: "30px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    zIndex: 5
                }}
            >
                {visible ? "🙈" : "👁"}
            </button>
        </div>
    );
}

function Login({ onSuccess }) {
    const [isRegister, setIsRegister] = useState(true);

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [registeredUser, setRegisteredUser] = useState(null);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    const rules = [
        { text: "Minimum 8 characters", valid: password.length >= 8 },
        { text: "One uppercase letter (A-Z)", valid: /[A-Z]/.test(password) },
        { text: "One lowercase letter (a-z)", valid: /[a-z]/.test(password) },
        { text: "One number (0-9)", valid: /[0-9]/.test(password) },
        { text: "One special character (@#$!)", valid: /[^A-Za-z0-9]/.test(password) }
    ];

    const passwordValid = rules.every(rule => rule.valid);

    const handleRegister = (e) => {
        e.preventDefault();
        setError("");
        setSuccess("");

        if (!name || !email || !password || !confirmPassword) {
            setError("Please fill in all fields.");
            return;
        }

        if (!passwordValid) {
            setError("Please satisfy all password requirements.");
            return;
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match!");
            return;
        }

        setRegisteredUser({ name, email, password });
        setSuccess("Registration successful! Please login.");

        setPassword("");
        setConfirmPassword("");
        setIsRegister(false);
    };

    const handleLogin = (e) => {
        e.preventDefault();
        setError("");

        if (
            registeredUser &&
            email === registeredUser.email &&
            password === registeredUser.password
        ) {
            onSuccess();
        } else {
            setError("Invalid email or password.");
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">

                <div className="auth-logo">🛡️</div>
                <h1>ScamBreaker</h1>

                <p className="auth-subtitle">
                    Your Digital Safety Starts Here
                </p>

                <div className="auth-tabs">
                    <button
                        type="button"
                        className={isRegister ? "active" : ""}
                        onClick={() => {
                            setIsRegister(true);
                            setError("");
                            setSuccess("");
                        }}
                    >
                        Register
                    </button>

                    <button
                        type="button"
                        className={!isRegister ? "active" : ""}
                        onClick={() => {
                            setIsRegister(false);
                            setError("");
                            setSuccess("");
                        }}
                    >
                        Login
                    </button>
                </div>

                {isRegister ? (
                    <form onSubmit={handleRegister}>

                        <h2>Create Account</h2>

                        <input
                            type="text"
                            placeholder="Full Name"
                            value={name}
                            onChange={e => setName(e.target.value)}
                        />

                        <input
                            type="email"
                            placeholder="Email Address"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                        />

                        <PasswordInput
                            placeholder="Create Password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                        />

                        <div className="password-rules">
                            <strong>Password must contain:</strong>

                            {rules.map((rule, index) => (
                                <div
                                    key={index}
                                    className={rule.valid ? "valid" : "invalid"}
                                >
                                    {rule.valid ? "✓" : "✗"} {rule.text}
                                </div>
                            ))}
                        </div>

                        <PasswordInput
                            placeholder="Confirm Password"
                            value={confirmPassword}
                            onChange={e => setConfirmPassword(e.target.value)}
                        />

                        {confirmPassword && (
                            <p className={
                                password === confirmPassword
                                    ? "match-success"
                                    : "match-error"
                            }>
                                {password === confirmPassword
                                    ? "✓ Passwords match"
                                    : "✗ Passwords do not match"}
                            </p>
                        )}

                        {error && <p className="auth-error">{error}</p>}
                        {success && <p className="auth-success">{success}</p>}

                        <button type="submit" className="auth-submit">
                            Create Account
                        </button>

                    </form>
                ) : (
                    <form onSubmit={handleLogin}>

                        <h2>Welcome Back</h2>

                        <input
                            type="email"
                            placeholder="Email Address"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                        />

                        <PasswordInput
                            placeholder="Enter Password"
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                        />

                        {error && <p className="auth-error">{error}</p>}

                        <button type="submit" className="auth-submit">
                            Login
                        </button>

                    </form>
                )}

                <p className="auth-footer">
                    Protected by ScamBreaker Security
                </p>

            </div>
        </div>
    );
}

export default Login;