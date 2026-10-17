# Fixtures

deterministic_check.py and demo-task.yaml form the infrastructure smoke test, not a subject task.
`researchctl smoke` actually executes the script and validates the resulting provenance record.

Future PostgreSQL fixtures must be synthetic domain state, pin migrations and image digest, define
UTC time/seed/schedule inputs, and reset independently for each evaluation. Never put credentials here.
Next: after baseline setup, add repeatable fixtures for two validated backend tasks.
