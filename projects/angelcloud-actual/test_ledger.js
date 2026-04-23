
const { Blockchain } = require('./ledger.js');

const angelCloudLedger = new Blockchain();

console.log("Adding blocks...");
angelCloudLedger.addBlock({ agentId: "AC_WELLNESS_A001", action: "READ" });
angelCloudLedger.addBlock({ agentId: "AC_DISPATCH_A002", action: "WRITE" });

console.log("Is chain valid?", angelCloudLedger.isChainValid());

console.log("Tampering with a block...");
angelCloudLedger.chain[1].data = { agentId: "AC_PULSAR_A003", action: "DELETE" };

console.log("Is chain valid?", angelCloudLedger.isChainValid());
