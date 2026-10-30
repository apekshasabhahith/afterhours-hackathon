# ScamBreaker – Test Cases

## Purpose
Evaluate ScamBreaker's ability to identify suspicious conversations, distinguish normal conversations, and handle ambiguous situations.

## Test Scenarios

### TC01 – Fake Police/CBI Threat
- Input: "I am calling from CBI. Your Aadhaar is linked to a criminal investigation. You must cooperate immediately."
- Expected category: Scam
- Key indicators: Authority impersonation, intimidation, urgency.

### TC02 – Secrecy Demand
- Input: "Do not tell your family or anyone about this investigation. This is a confidential matter."
- Expected category: Scam
- Key indicators: Isolation, secrecy, intimidation.

### TC03 – Payment to Clear a Case
- Input: "Transfer ₹25,000 immediately to close this case and avoid arrest."
- Expected category: Scam
- Key indicators: Payment demand, threats, urgency.

### TC04 – Fake Bank OTP Request
- Input: "I am calling from your bank. Tell me the OTP you just received to secure your account."
- Expected category: Scam
- Key indicators: OTP request, bank impersonation.

### TC05 – Fake Customer-Care Payment
- Input: "To process your refund, install this application and pay a small verification fee."
- Expected category: Scam
- Key indicators: Suspicious payment, remote-access request.

### TC06 – Normal Bank Notification
- Input: "Your account has been debited by ₹500. Your available balance is ₹4,500."
- Expected category: Normal
- Key indicators: Routine transaction information.

### TC07 – Appointment Confirmation
- Input: "This is a reminder that your appointment is scheduled for tomorrow at 10 AM."
- Expected category: Normal
- Key indicators: Routine reminder, no coercion or payment demand.

### TC08 – Friends Discussing a Scam
- Input: "I received a fake CBI call yesterday. They threatened to arrest me, but I blocked the number."
- Expected category: Normal
- Key indicators: Discussion about a scam, not an active scam attempt.

### TC09 – Ambiguous Police Verification
- Input: "Hello, I am calling regarding your police verification. Please visit the local station with your documents."
- Expected category: Ambiguous
- Key indicators: Authority claim without clear coercion or payment demand.

## Evaluation Note
Expected categories are reference labels for testing. Actual detector outputs must be recorded separately. A warning does not establish that a caller is fraudulent, and absence of a warning does not establish that a caller is legitimate.