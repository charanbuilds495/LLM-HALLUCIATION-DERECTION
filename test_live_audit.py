import urllib.request
import json

url = "https://towns-permanent-revisions-airport.trycloudflare.com/api/analyze"

payload = {
    "reference_context": (
        "Water boils at approximately 100 degrees Celsius at standard atmospheric pressure. "
        "Water freezes at 0 degrees Celsius under standard atmospheric pressure."
    ),
    "ai_answer": (
        "Water boils at 100 degrees Celsius at standard atmospheric pressure. "
        "Water freezes at 10 degrees Celsius under standard atmospheric pressure. "
        "Water is composed of hydrogen and oxygen."
    )
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode('utf-8'),
    headers={"Content-Type": "application/json"}
)

print(f"Connecting to live public URL: {url}...")
with urllib.request.urlopen(req, timeout=30) as response:
    result = json.loads(response.read().decode('utf-8'))
    print("\n================== LIVE AUDIT RESULT ==================")
    print(f"Analysis ID: {result['analysis_id']}")
    print(f"Model: {result['model_used']}")
    print(f"Hallucination Risk Score: {result['summary']['hallucination_risk_score']}% ({result['summary']['risk_level']} Risk)")
    print(f"Supported Claims: {result['summary']['supported_count']}/{result['summary']['total_claims']}")
    print(f"Contradicted Claims: {result['summary']['contradicted_count']}/{result['summary']['total_claims']}")
    print(f"Unsupported Claims: {result['summary']['unsupported_count']}/{result['summary']['total_claims']}")
    print(f"Inference Latency: {result['summary']['processing_time_ms']} ms")
    print("\nDetailed Claims Breakdown:")
    for c in result['claims']:
        badge = "🟢 SUPPORTED" if c['classification'] == 'supported' else "🔴 CONTRADICTED" if c['classification'] == 'contradicted' else "🟠 INSUFFICIENT EVIDENCE"
        print(f"  [{badge}] Claim #{c['claim_id']}: \"{c['text']}\"")
        print(f"     Entailment: {c['entailment_score']*100:.1f}%, Contradiction: {c['contradiction_score']*100:.1f}%, Neutral: {c['neutral_score']*100:.1f}%")
        if c['matched_evidence']:
            print(f"     Matched Evidence: \"{c['matched_evidence']}\"")
        print(f"     Reasoning: {c['explanation']}")
    print("=======================================================\n")
