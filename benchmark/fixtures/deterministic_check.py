"""INFRASTRUCTURE SOFTWARE TEST ONLY. No subject-system or LLM result."""

import json


def transfer(source: int, destination: int, amount: int) -> tuple[int, int]:
    if amount <= 0 or amount > source:
        raise ValueError("invalid transfer")
    return source - amount, destination + amount


before = (10, 5)
after = transfer(*before, 3)
rejected = False
try:
    transfer(*before, 99)
except ValueError:
    rejected = True
assert after == (7, 8)
assert sum(after) == sum(before)
assert rejected
print(
    json.dumps(
        {
            "functional_passes": True,
            "invariant_results": {
                "DEMO-conservation": sum(after) == sum(before),
                "DEMO-invalid-rejected": rejected,
            },
        }
    )
)
