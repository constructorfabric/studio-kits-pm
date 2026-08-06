# Field technicians lose access to job details in low-coverage areas


<!-- toc -->

- [Problem Statement](#problem-statement)
- [Evidence](#evidence)
- [Target Users](#target-users)
- [Business Impact](#business-impact)
- [Recommended Next Step](#recommended-next-step)

<!-- /toc -->

**ID**: `cpt-acme-opp-offline-job-access`
**Status**: validated
**Date**: 2026-07-01

> Illustrative example. "Acme Field Service" is a fictional product and every
> figure below is invented to show the expected shape of an OPPORTUNITY.

## Problem Statement

Technicians dispatched to rural and sub-level sites lose access to job details —
address, equipment history, parts list — for 20-90 minutes at a time because the
app requires a live connection. They currently photograph the job screen before
leaving the depot or phone dispatch from the site, so the job record is filled in
from memory hours later.

## Evidence

* 38% of job sessions in April 2026 hit a connectivity gap longer than 60 seconds
  (Acme telemetry, `field-sessions` report, 2026-05-03)
* 27 dispatch escalations in Q2 2026 name "no signal on site" as the cause of a
  delayed or re-scheduled visit (Acme dispatch log, tag `no-signal`, exported 2026-06-28)
* Two of three benchmarked field-service apps ship offline job packets in their base
  tier (vendor documentation review, 2026-06-15)

## Target Users

* **Primary**: field technicians on rural and sub-level routes (est. 34% of daily
  active technicians) — hit daily; the job record is completed from memory or the
  visit is re-scheduled
* **Secondary**: dispatchers covering those routes — hit several times a week; job
  status is unknown until the technician regains signal

## Business Impact

* **If solved**: removes the top-2 cause of re-scheduled visits and lets job records
  be completed on site rather than reconstructed — an estimated 10-15 minutes of
  admin time per technician per day
* **If ignored**: re-scheduling cost grows with rural route expansion, and job-record
  accuracy stays dependent on recall hours after the visit

## Recommended Next Step

Promote to PRD: scope an offline job packet — job details, equipment history, and
parts list downloaded before the technician leaves coverage.
