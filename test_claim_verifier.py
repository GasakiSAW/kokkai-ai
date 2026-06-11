from analysis.claim_verifier import verify_claim

evaluation = [
    {"evaluation":"改善傾向"},
    {"evaluation":"改善傾向"},
    {"evaluation":"悪化傾向"}
]

print(
    verify_claim(
        {},
        evaluation
    )
)
