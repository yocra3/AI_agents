---
name: start-task
description: Prepare a clean local task branch when explicitly requested or when an active implementation-coordinator workflow needs its task branch. Do not use for ordinary edits on an existing task branch.
---

# Start Task

Prepare the workspace only for a direct request or when an explicitly invoked
implementation-coordinator workflow needs its task branch. The task branch keeps unrelated work
out of the task's commits and all of the task's work on one branch; for the coordinator, the
task is its contract.

1. Inspect Git status and the current branch.
2. If the correct dedicated task branch is already active, preserve it instead of creating
   another one and go to step 5. In an active implementation-coordinator workflow, pending
   changes that belong to the contract and its implementation plan, such as Blockers entries or
   a delegate's uncommitted work for the contract, stay on it without blocking. Any other pending
   change, unrelated to the contract or in a direct request, remains blocking and requires user
   direction.
3. If pending work exists, do not commit or move it automatically. The only exception is an active
   implementation-coordinator handoff containing exactly the specification or methods document
   path explicitly authorized by the user: verify that diff and carry it unchanged onto the task
   branch. Any other pending path remains blocking and requires user direction.
4. Determine `feat`, `fix`, or `chore` from the task and create a concise slugged branch.
5. Confirm the branch and final local status.

Keep work local. Do not pull, push, merge, or otherwise contact a remote unless the user
explicitly asks for that remote operation.
