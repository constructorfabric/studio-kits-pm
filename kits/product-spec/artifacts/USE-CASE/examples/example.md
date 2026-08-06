# UC: Download a day's jobs for offline use


<!-- toc -->

- [Actors](#actors)
- [Preconditions](#preconditions)
- [Main Flow](#main-flow)
- [Alternative Flows](#alternative-flows)
- [Acceptance Criteria](#acceptance-criteria)
- [Traceability](#traceability)

<!-- /toc -->

**ID**: `cpt-acme-usecase-download-jobs-offline`
**Status**: reviewed
**Date**: 2026-07-05

> Illustrative example built on the OPPORTUNITY example in this kit. "Acme Field
> Service" is a fictional product.

## Actors

* **Primary**: Field technician (authenticated app user with an assigned route)
* **Secondary**: Dispatch backend (serves the downloadable job packet)

## Preconditions

* Technician is authenticated in the app
* At least one job is assigned to the technician for the selected day
* Device has enough free storage for the day's job packet

## Main Flow

1. Technician opens the day's route and taps "Make available offline"
2. System shows the packet size and the jobs it covers, and asks for confirmation
3. Technician confirms the download
4. System downloads the job packet in the background and shows progress on the route header
5. System marks the route as "Available offline" when the download completes
6. Technician opens a job out of coverage and views details, equipment history, and parts list

## Alternative Flows

* **A1 — Connection lost mid-download**: at step 4, the system pauses the download and
  resumes automatically when connectivity returns; already-downloaded jobs stay available.
  Flow resumes at step 4.
* **A2 — Insufficient storage**: at step 2, the system shows required vs available space and
  offers to release older offline routes. Flow ends; no partial download is started.
* **A3 — Job reassigned after download**: when the device is next online, the system marks the
  affected job as withdrawn and removes it from the offline packet. Flow ends after the
  technician acknowledges.

## Acceptance Criteria

* A downloaded route opens fully (job details, equipment history, parts list) out of coverage
* An interrupted download resumes without restarting from zero after connectivity returns
* Attempting a download with insufficient storage starts no partial download and shows required space
* The route header reflects offline state: not downloaded / in progress (with %) / available offline / withdrawn job present

## Traceability

* **Implements**: `cpt-acme-opp-offline-job-access` — gives technicians the job data they
  currently photograph or phone in for, which is the primary problem documented in the
  opportunity
