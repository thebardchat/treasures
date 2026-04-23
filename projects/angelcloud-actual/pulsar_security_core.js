
const agentRoles = require('./data/agent_roles.json');
const resourceRisks = require('./data/resource_risk.json');

/**
 * Calculates the Pulsar Threat Score (PTS) for a given Agent State Record (ASR).
 * This is the core of the Pulsar AI Layer 2 threat detection engine.
 * @param {object} asr The Agent State Record to analyze.
 * @param {object} agentProfile The profile of the agent, including trust score and historical data.
 * @returns {number} The calculated Pulsar Threat Score (0-100+).
 */
function calculatePTS(asr, agentProfile) {
    const S_Access = calculateResourceRoleMismatchScore(asr, agentProfile);
    const S_Behavior = calculateIdentityBehaviorDeltaScore(asr, agentProfile);
    const M_PIM = getPredictiveIntentMultiplier(asr, agentProfile);

    const W_IBD = 0.4; // Weight for Behavioral Deviation
    const W_RT = 0.6;  // Weight for Resource/Role Mismatch

    const pts = ((W_IBD * S_Behavior) + (W_RT * S_Access)) * M_PIM;

    return Math.min(pts, 100); // Cap score at 100 for simplicity, though it can be higher.
}

/**
 * Calculates the Resource/Role Mismatch Score (S_Access).
 * This is the most critical component, focusing on whether the AI Agent is acting outside its defined security perimeter.
 * @param {object} asr The Agent State Record.
 * @param {object} agentProfile The agent's profile.
 * @returns {number} The S_Access score (0-100+).
 */
function calculateResourceRoleMismatchScore(asr, agentProfile) {
    const agentRole = agentRoles[asr.agentId];
    if (!agentRole) {
        return 100; // Unrecognized agent ID is a maximum threat.
    }

    const baseRisk = resourceRisks[asr.targetResource] || resourceRisks.default_risk;

    let accessDeviationFactor = 1;
    if (!agentRole.allowed_actions.includes(asr.actionType)) {
        accessDeviationFactor = 5; // Severe deviation
    } else if (!agentRole.allowed_resources.includes(asr.targetResource)) {
        accessDeviationFactor = 3; // Moderate deviation
    }

    // Agent Trust Score (0.1 to 1.0). A lower trust score exponentially increases the risk.
    const agentTrustScore = agentProfile.trustScore || 0.5;

    const sAccess = baseRisk * (accessDeviationFactor / agentTrustScore);
    return sAccess;
}

/**
 * Calculates the Identity-Behavior Delta Score (S_Behavior).
 * This captures subtle anomalies in the 'how' and 'when' an agent acts.
 * @param {object} asr The Agent State Record.
 * @param {object} agentProfile The agent's profile with historical averages.
 * @returns {number} The S_Behavior score (0-100+).
 */
function calculateIdentityBehaviorDeltaScore(asr, agentProfile) {
    // Time Anomaly: Compare current action latency to agent's average.
    const executionTime = Date.now() - new Date(asr.timestamp).getTime();
    const timeAnomaly = Math.abs(executionTime - agentProfile.avgLatency) / agentProfile.avgLatency;
    const timeAnomalyScore = Math.min(timeAnomaly * 50, 100); // Normalize to 0-100

    // Frequency Deviation: Compare actions per second to baseline.
    const frequencyDeviation = Math.log1p(agentProfile.actionsPerSecond / agentProfile.avgActionsPerSecond);

    const sBehavior = timeAnomalyScore * frequencyDeviation;
    return sBehavior;
}

/**
 * Gets the Predictive Intent Multiplier (M_PIM).
 * This is the unique multiplier based on the traceable intent from the Source/Prompt ID.
 * @param {object} asr The Agent State Record.
 * @param {object} agentProfile The agent's profile, including prompt history.
 * @returns {number} The M_PIM multiplier (>= 1.0).
 */
function getPredictiveIntentMultiplier(asr, agentProfile) {
    if (agentProfile.promptHistory.isHighRisk(asr.sourcePromptId)) {
        return 3.0; // High PIM Risk
    } else if (agentProfile.promptHistory.isMediumRisk(asr.sourcePromptId)) {
        return 2.0; // Medium PIM Risk
    } else if (agentProfile.promptHistory.isLowRisk(asr.sourcePromptId)) {
        return 1.5; // Low PIM Risk
    }
    return 1.0; // No prior flags
}

module.exports = { calculatePTS };
