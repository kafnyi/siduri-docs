> ## ⚠ THIS FILE IS AN INPUT DOCUMENT — NOT THE SOURCE OF TRUTH
>
> **Origin:** written by Gemini for the user, **BEFORE** the 2026-08-22 Claude design
> session. The user supplied it during that session with the explicit warning:
> *„ez az előtti állapot, hogy ezt a sessiont elkezdtem veled, így lehetnek benne
> outdate-d vagy felülírt infók."*
>
> **Binding decisions live in [`NYITOTT_KERDESEK.md`](NYITOTT_KERDESEK.md).**
> Current status: [`FOLYAMATBAN.md`](FOLYAMATBAN.md).
>
> **A section-by-section reconciliation against the current decisions is at the
> BOTTOM of this file.** One statement in §5 is **SUPERSEDED** and must not be
> built on. Read the reconciliation before using anything here.

---

# Siduri Systems - Cloud API & Web Management Interface Specification

## 1. Context and Architectural Role
This document outlines the specifications for the **Cloud Infrastructure, Web Management Portal, and Business Intelligence (BI)** modules of the **Siduri POS** system.
While Siduri is an offline-first local system (running on a local Spring Boot server), it relies on a central Cloud architecture (`siduri-cloud-api`) for global tenant management, licensing, data backup, and advanced business administration.

## 2. The Hybrid Web Architecture (Crucial Concept)
The Web Management Interface must be designed with a **Hybrid Access** model to ensure the restaurant manager can work even during an internet outage.
* **Cloud Access:** The primary access point for managers is via the cloud portal (e.g., `admin.sidurisystems.hu`).
* **Local Fallback (Local Web):** The exact same web interface (Category 2 Admin) is also served locally by the restaurant's local Java Spring Boot server.
* **POS Integration:** Within the physical C# WPF POS application, a user with Manager privileges can toggle "Admin Access", which displays the local network connection details (SSID, IP:Port, and a QR code) allowing managers to open the Web Admin on their own laptop/tablet via the local network without internet.

## 3. Interface Categories & Responsibilities
The management functions are divided into strict categories:

### Category 1: Operative Management (Available on Web & Physical POS)
* **Products & Modifiers:** Creating and editing products, categories, VAT keys, and modifiers (e.g., "Extra cheese").
* **Table Maps:** Managing the visual layout of the restaurant, zones, and background images.
* **Local Users:** Managing POS PIN codes, avatars, and names for local staff.

### Category 2: Deep Administration (Available strictly via Web Interface)
* **Inventory & Warehouses:** Full multi-warehouse management, transfers, and logging.
* **Recipes (BOM - Bill of Materials):** Defining ingredient breakdown for products.
* **Purchasing (Bevételezés):** Adding incoming stock. Crucially, the UI must allow/require entering the **Purchase Unit Price** (Beszerzési egységár). The system calculates the **Moving Average Price** from these entries.
* **Inventory Adjustments:** Specific interfaces for registering *Staff Consumption (Repi)* and *Waste/Spoilage (Selejt)*. These must be logged as inventory movements, strictly bypassing fiscal (NAV) and NTAK sales reporting.
* **Stocktaking (Standolás):** Digital recording of stock. The UI allows printing physical stocktaking sheets and entering the data later.

## 4. Advanced Analytics and BI (Business Intelligence)
The web interface includes a robust BI dashboard rendering dynamic charts, pie charts, and peak-traffic heatmaps.
* **Drill-down Reports:** Detailed views on revenue, waiter performance, table turnover rates, and stock depletion.
* **True Margin Calculation (Valós Árrés):**
  * The profit margin is strictly calculated using the *Moving Average Price* of the ingredients.
  * **Interactive BI Slider:** The reporting UI features a dynamic slider for **"Calculated Waste %"** (Kalkulált veszteség). The manager can set this (e.g., 2% draft beer spill allowance), and the dashboard recalculates the True Profit Margin in real-time, factoring in theoretical waste.

## 5. Licensing, DRM, and Tenant Management (Cloud Only)
The `siduri-cloud-api` acts as the ultimate gatekeeper for the software.
* **Hardware Fingerprinting:** The cloud stores the Motherboard/CPU/MAC hash of the licensed local servers.
* **Heartbeat & Grace Period:** Local servers ping the cloud daily. If offline, the cloud grants a 10-day Grace Period.
* **NTAK SLA Monitoring:** Although local servers report to NTAK directly, the local UI throws a critical red alert if the system is offline for 18 hours (violating the 24-hour legal reporting SLA).
* **Superadmin (Siduri Systems Account):** A hardcoded, undeletable provider profile used for maintenance. Its password is managed globally in the Cloud and synced down to local servers.
  * `[!] SECURITY CONCERN — see reconciliation §R4 below.`
* **Emergency Failback Authorization:** If a local site enters "Emergency Server" mode (Failover), restoring the Master Server (Failback) requires cryptographic authorization generated from the Cloud Superadmin interface.
  * `[SUPERSEDED — see reconciliation §R1 below. Failback is now AUTOMATIC.]`

## 6. Special Data Handling Rules in the Admin Interface
* **DRS (Deposit Return System - REpont):** Admin users must be able to link a fixed, non-discountable, tax-exempt +50 HUF DRS fee to parent items (e.g., PET bottles).
* **Reusable Cups (Repohár):** UI must allow setting up tokens that act as both positive products (sale) and negative products (return), which trigger automated `PAY_OUT` cash drawer transactions.

## 7. Tech Stack Directives
* **Cloud Backend:** Node.js or Java (Spring Boot) handling REST/GraphQL endpoints for the Web UI.
* **Web Frontend:** Recommended to use Flutter Web (to share models with the PDA/KDS apps) OR a robust React/Vue/Angular dashboard.
* **Database:** Cloud PostgreSQL holding multi-tenant data, safely isolating each restaurant's backups and analytics.

---
---

# RECONCILIATION against the 2026-08-22 decisions

> Written during the Claude design session, after reading this document.
> **This section is the part that matters** — the body above is an input, not a plan.

## R1 `[SUPERSEDED]` Failback via Cloud Superadmin cryptographic authorization (§5)

**The document says:** restoring the Master after a failover requires cryptographic
authorization generated from the Cloud Superadmin interface.

**This is SUPERSEDED.** The binding decision (`NYITOTT_KERDESEK.md`, item `A4`) is:
**failback is AUTOMATIC** once the main and the standby have seen each other
stably for 1 minute and can actually communicate. The old spec's
„only with the Siduri Systems superadmin" rule was **explicitly rejected**,
because the situation is by definition a server failure at the site — precisely
when support is least reachable, and the site cannot wait.

**Do not build the cloud-authorization path.** What *is* required instead:
flapping protection (growing backoff + a shutoff limit) and the extraction of
orphaned transactions before the old main is rewound.

## R2 `[CONFIRMED and now CENTRAL]` The Hybrid Web architecture (§2)

**This is the single most valuable thing in this document**, and it directly
answers a question that was open in the session: *are the cloud's warehouse and
recipe functions the same as the local admin's, or different?*

**The user confirmed (2026-08-22): they are the SAME, just served from elsewhere.**
Combined with §2 here, that gives a concrete architecture:

> **ONE web admin application, served from TWO places** — from the cloud portal,
> and from the site's own local server when there is no internet.

**Why this matters so much:** the session flagged that „every setting available on
the POS must also be available in the cloud" is a §6 seam requirement that
**guarantees silent drift** if two separate UIs are maintained. The hybrid model
**removes the drift at the root** — there is only one UI. What remains is to keep
the two *backends* (local server / cloud API) in parity, which is exactly what the
single settings schema + parity guard (`B16.7`) is for.

**`[ ]` One consequence to verify:** the local server that serves this UI is,
per the 2026-08-22 decisions, **typically a working POS machine on J1900
hardware**. Serving a web app on top of PostgreSQL + the Java server + the WPF
client is additional load. → added to `MERESEK.md` (M14).

## R3 `[NEW — not previously captured]` The POS „Admin Access" toggle (§2)

A manager toggles it on the POS, and the POS displays the local connection details
(SSID, IP:Port, QR code) so the manager can open the web admin on their own
laptop or tablet over the LAN, without internet.

**Good, practical, and cheap.** Two notes:
- It exposes the site's network details on a screen in the venue → it must be
  **permission-gated**, and ideally time-limited (the details disappear after N
  minutes). Otherwise anyone glancing at the till learns how to reach the server.
- The QR code is a **discovery aid, not authentication.** Whoever opens the page
  must still log in. Worth stating explicitly so nobody treats the QR as a token.

## R4 `[!]` `[SECURITY CONCERN — decision needed]` A globally managed Superadmin password synced down (§5)

**The document says:** the Superadmin profile's password is managed globally in
the cloud and **synced down to local servers**.

**This is a single point of catastrophic failure.** One shared secret, replicated
to every customer site, means **one compromise exposes every installation** —
including sites that are offline and cannot be rotated. It also means the secret
sits at rest on machines that (per the 2026-08-22 decisions) are **working POS
machines standing behind a bar**, physically stealable.

**Suggested alternatives (decision needed):**
- **Per-site credentials**, derived or issued individually — a leak affects one site.
- **Challenge–response:** the site displays a challenge, support generates a
  time-limited response from the cloud. Nothing reusable is ever stored on site.
  This also works offline, which the shared-password model does not solve better.
- Either way: **short validity, full audit, and no long-lived shared secret at rest.**

→ recorded as an open item under `B6` / `F7`.

## R5 `[CLARIFICATION]` Category 1 / Category 2 vs. „everything on POS must be in the cloud"

These do not conflict, but the **direction** must be stated, or someone will
misread it:

- The user's rule is **POS → cloud**: everything settable on the POS must also be
  settable in the cloud.
- It is **not** cloud → POS: Category 2 (warehouses, recipes, purchasing,
  stocktaking, inventory adjustments) is **web-only and stays web-only** —
  it does not have to appear on the POS.

The parity guard (`B16.7`) must therefore check **one direction only**, otherwise
it will produce false findings for every Category 2 screen.

## R6 `[CONFIRMED]` Items here that match the existing plan

Moving Average Price from purchase unit prices; the „Calculated Waste %" BI
slider; staff consumption and waste as inventory movements bypassing fiscal and
NTAK reporting; printable stocktaking sheets with later data entry; hardware
fingerprinting; the 10-day grace period; the 18-hour NTAK alert; DRS; reusable
cup tokens triggering a cash pay-out. All of these are already in the plan
(spec §12–§26) and are unaffected by the 2026-08-22 decisions.

**Note:** the 24-hour NTAK limit and the 18-hour alert remain an
**unverified premise** (`C11`) — this document repeats the claim but does not
source it, so it does not verify it.

## R7 `[ ]` Tech stack note — Flutter Web for the admin UI (§7)

Not decided. One consideration for when it is: the same UI is served from the
**local** server for offline use, and opened on **whatever device the manager
owns** — often an older laptop or tablet. Flutter Web's bundle size and rendering
approach are heavier than a plain HTML/JS dashboard on such devices. The server
side is unaffected (it only serves static files), so this is a **client-device**
question, not a J1900 question.

The stated benefit — sharing models with the PDA/KDS Flutter apps — is real and
points the other way. **Genuine trade-off; decide with the phase plan (`E1`),
not now.**
