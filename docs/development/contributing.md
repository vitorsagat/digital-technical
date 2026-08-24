# Contributing

Create a branch, keep changes scoped, add tests for behavior, run `make validate`,
and open a pull request. Changes to core ports require an architecture review.
Provider SDK imports belong only in adapters. Never commit credentials, customer
data, Terraform state, or generated plans.

Commit messages should describe intent. Pull requests should include risk,
validation evidence, rollout, and rollback notes.
