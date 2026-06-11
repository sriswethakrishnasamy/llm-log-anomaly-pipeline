import json
import random
import os

def generate_telemetry_dataset():
    # 1. Define distinct, real-world database & system log anomaly templates
    raw_log_templates = [
        {
            "log": "[WARN] HikariPool-1 - Connection is not available, request timed out after 30000ms. Active: 20, Idle: 0, Waiting: 14",
            "issue": "Database Connection Pool Exhaustion",
            "root_cause": "Unclosed database connections in asynchronous tasks or insufficient maximum pool sizing under high traffic concurrent spikes.",
            "remediation": "Wrap transactional repositories in try-with-resources blocks and scale connection pool limits dynamically."
        },
        {
            "log": "[ERROR] org.hibernate.exception.LockAcquisitionException: Deadlock found when trying to get lock; try restarting transaction",
            "issue": "Database Structural Deadlock",
            "root_cause": "Two or more concurrent operations locked matching transaction rows in a conflicting hierarchical sequence.",
            "remediation": "Enforce identical row-locking sequences across all updating backend methods and implement retry logic mechanisms."
        },
        {
            "log": "[CRITICAL] io.netty.handler.timeout.ReadTimeoutException: Inbound HTTP gateway connection dropped after 5000ms idle state.",
            "issue": "Microservice Communication Timeout",
            "root_cause": "Downstream REST dependency failed to respond within the allocated thread pool timeout boundary.",
            "remediation": "Implement an isolated Resilience4j Circuit Breaker pattern with a graceful fallback state strategy."
        },
        {
            "log": "[WARN] org.springframework.cache.interceptor: Cache 'user_sessions' missed. Direct fallback hitting disk database repository.",
            "issue": "Distributed Cache Stampede Risk",
            "root_cause": "Massive high-volume concurrent reads requesting an expired or evicted cache key simultaneously.",
            "remediation": "Apply mutex locks on cache misses or implement background asynchronous cache refreshment strategies."
        }
    ]

    # 2. Programmatically generate 2,000 randomized training samples
    dataset = []
    timestamps = ["2026-06-11 20:15:32", "2026-06-11 21:04:11", "2026-06-11 21:45:00", "2026-06-11 22:12:09"]

    for _ in range(2000):
        template = random.choice(raw_log_templates)
        ts = random.choice(timestamps)
        formatted_log = f"[{ts}] {template['log']}"
        
        instruction = f"Analyze the following system log trace for potential transactional hazards or structural deadlocks:\n\n{formatted_log}"
        
        output_json = {
            "status": "CRITICAL" if "ERROR" in formatted_log or "CRITICAL" in formatted_log else "WARNING",
            "issue": template["issue"],
            "root_cause": template["root_cause"],
            "remediation": template["remediation"]
        }
        
        dataset.append({
            "instruction": instruction,
            "output": json.dumps(output_json, indent=2)
        })

    # 3. Create the data directory if it doesn't exist and save as JSONL
    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "train_logs_dataset.jsonl")
    
    with open(output_path, "w") as f:
        for entry in dataset:
            f.write(json.dumps(entry) + "\n")

    print(f"🎉 Success! Generated {len(dataset)} production log samples and saved to {output_path}")

if __name__ == "__main__":
    generate_telemetry_dataset()