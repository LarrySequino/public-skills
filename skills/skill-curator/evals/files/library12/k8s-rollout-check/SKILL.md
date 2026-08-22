---
name: k8s-rollout-check
description: >
  Verify a Kubernetes rollout actually finished: replica readiness, restart loops, probe failures,
  pending pods, and the cluster events emitted while the deploy was running. Use right after
  shipping to a cluster, or when a deploy reports success and the service is still misbehaving.
  NOT for authoring the manifests (use helm-chart-author instead).
---

# Kubernetes Rollout Check

"Deployment succeeded" means the API accepted the object, not that the service works.

## Procedure

1. Check the rollout status and the replica counts together. Desired, current,
   updated, and available are four different numbers and only the last one matters.
2. List pods and look at restart counts, not just phase. A pod in Running with nine
   restarts is a crash loop that happens to be between crashes.
3. Read the events since the deploy started. Image pull failures, failed scheduling,
   and evicted pods all show up here and nowhere else.
4. Check readiness probe failures separately from liveness. A failing readiness probe
   holds traffic back quietly; a failing liveness probe restarts the pod loudly.
5. Compare the running image digest against the one that was meant to ship. A tag
   that did not move is the quietest failed deploy there is.
6. Watch error rate and latency for one full traffic cycle before calling it done.

## Verdict

Healthy, degraded, or roll back. Say which, and if it is roll back, give the command.
