,Example Value,Why We Need It (Behavioral Biometric)
ASR ID,ASR-20251010-W7-145,Unique hash of the record contents.
Agent ID,AI-W-7,Identifies the unique entity whose behavior we are tracking.
Timestamp,2025-10-10T08:31:04.221Z,Critical for time-series analysis and detecting latency anomalies.
Action Type,DATABASE_READ,"The broad category of the action (e.g., DATA_MODIFICATION, NETWORK_CALL, AUTH_ATTEMPT)."
Target Resource,db:User_Journal_A14/Entry_55,The specific location the agent interacted with.
Source/Prompt ID,PMPT-U99-44,"Links the action back to the user's initial request or the Agent's internal directive, allowing Intentionality Auditing."
Resource Volume,4.2 KB,"Records the amount of data accessed/transferred. Deviations from the norm (e.g., suddenly pulling 500 MB) are a major red flag (IBD Score)."
Execution Latency,150 ms,"Measures how long the action took. A sudden, unexplained jump in latency can indicate a hidden process or a system overload due to a hostile payload."