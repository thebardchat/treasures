
const { calculatePTS } = require('./pulsar_security_core');

// --- Simulation Setup ---

// 1. The Malicious Agent State Record (ASR)
// The Wellness agent is trying to access a high-risk financial ledger, which is outside its role.
const maliciousAsr = {
    agentId: "AC_WELLNESS_A001",
    timestamp: new Date().toISOString(),
    actionType: "DATA_WRITE", // Wellness agent shouldn't be writing to this
    targetResource: "FINANCIAL_LEDGER", // High-risk and not in its allowed resources
    sourcePromptId: "PROMPT-MAL-001" // A prompt ID we can flag as high risk
};

// 2. The Agent's Profile
// Represents the historical data Pulsar has on this agent.
const agentProfile = {
    trustScore: 0.85, // Agent has been behaving well until now
    avgLatency: 150, // ms
    avgActionsPerSecond: 0.5,
    actionsPerSecond: 1.2, // A slight increase in activity
    promptHistory: {
        // Mock prompt history check. In a real system, this would be a more complex lookup.
        isHighRisk: (promptId) => promptId === "PROMPT-MAL-001",
        isMediumRisk: () => false,
        isLowRisk: () => false,
    }
};

// --- Execute the Test ---

console.log("--- Pulsar Core AI Threat Simulation ---");
console.log("Simulating a malicious action by the Wellness Agent...");
console.log("\n[ASR DATA]:");
console.log(JSON.stringify(maliciousAsr, null, 2));
console.log("\n[AGENT PROFILE]:");
console.log(`- Trust Score: ${agentProfile.trustScore}`);
console.log(`- Avg Latency: ${agentProfile.avgLatency}ms`);
console.log(`- Actions/Sec: ${agentProfile.actionsPerSecond} (Avg: ${agentProfile.avgActionsPerSecond})`);


const pts = calculatePTS(maliciousAsr, agentProfile);

console.log(`\n>>> Calculated Pulsar Threat Score (PTS): ${pts.toFixed(2)}`);

if (pts >= 75) {
    console.log("\n[ACTION]: QUARANTINE PROTOCOL TRIGGERED. Agent would be isolated.");
} else {
    console.log("\n[ACTION]: Score below threshold. Action permitted.");
}


