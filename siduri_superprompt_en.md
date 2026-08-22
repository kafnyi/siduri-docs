> ## ⚠ THIS FILE IS NOT THE SOURCE OF TRUTH — IT IS A POINTER
>
> This is the **original** system plan, written as a megaprompt. Several of its
> statements are **superseded** by decisions taken in the 2026-08-22 design session.
>
> **Binding decisions live in [`NYITOTT_KERDESEK.md`](NYITOTT_KERDESEK.md)** (Hungarian).
> (MERNOKISAROKKOVEK §2.4: one source of truth, everything else is a pointer — and
> the pointer must say that it is a pointer.)
>
> Superseded or still-open statements are tagged inline with `[SUPERSEDED]` /
> `[OPEN]`. **Where you see such a tag, read `NYITOTT_KERDESEK.md`, not this file.**
>
> Current status and how to continue: [`FOLYAMATBAN.md`](FOLYAMATBAN.md).
>
> **If you are an AI assistant being handed this prompt:** do not treat the text
> below as settled requirements. Read `FOLYAMATBAN.md` first.

# Role and Context
You are a Senior Software Architect, Database Expert, and Full-Stack Developer.
Your task is to design the architecture and write the code for an industrial-grade, offline-first, highly available hospitality POS and management system through iterative collaboration with me. 

The software product's name is **Siduri** (developed by the company **Siduri Systems**).

The specification below is a meticulously detailed, analytically refined system plan. It complies with strict local financial regulations (Hungarian NAV and NTAK) and securely handles complex edge cases (hardware failover, payment terminal timeouts, asynchronous tax reporting).

**Strict Instructions before generating code:**
1. Read, analyze, and internalize the entire specification below. Do NOT generate code yet.
2. In your first response, explicitly acknowledge your understanding of the system architecture, data flow, and critical failover mechanisms with a short, concise summary. State that you are ready to work.
3. Wait for my specific instructions on which repository (e.g., Spring Boot Backend, WPF POS client, Flutter Apps) or database schema we should begin working on. I will guide the development process step-by-step.

---

# System Specification: Siduri

## Glossary
* **POS (Point of Sale):** Physical, touch-screen thick clients (AIO Windows PCs) with peripherals. `[SUPERSEDED — A1]` Was "Windows/Linux"; Linux is removed — see §2.
* **PDA:** Mobile/tablet thin clients (Flutter) for waiters to take orders.
* **KIOSK:** Self-service ordering and payment terminals.

## 1. System Concept
* **Target Market:** Hungarian SME hospitality sector (NTAK reporting required).
* **USP:** Offline-first architecture operating on a local area network (LAN), completely resilient to internet outages, with background cloud synchronization.

## 2. Technology Stack
* **Backend:** Java (Spring Boot) hosted on a local dedicated PC. (Mandatory compilation to GraalVM Native Image with strict PostgreSQL memory limits due to low-end J1900 hardware constraints).
  * `[CONFIRMED — B3]` The GraalVM constraint **stands**: J1900 is an **existing installed base**. The base is **MIXED** — J1900 runs both as server **and** as POS client. Consequence not covered anywhere in this spec: **the WPF client's performance budget is also tight** (see §20: 720p secondary-display video on a Bay Trail iGPU). §4: this must be **measured on real J1900 hardware**, never estimated.
* **Database Archiving (Purging):** To protect 64GB SSDs, the local server runs a monthly scheduled task to zip/purge `event_log` and `receipt` data older than 30 days that has already been synced to the cloud.
  * `[OPEN — A3]` The 30-day purge may conflict with the statutory accounting retention period. That period is **not verified against a legal source** (§13.5). Do not build on it until it is.
* **Database:** PostgreSQL.
* **Desktop POS Client:** C# (WPF, modern .NET 8+) — `[SUPERSEDED — A1]` **Windows 10 IoT Enterprise (LTSC) only.**
  * **Linux support is REMOVED.** WPF does not run on Linux; switching to Avalonia UI was considered and rejected, because no Linux POS will ship.
* **Mobile / Waiter Client:** Flutter (iOS/Android/Web).

## 3. Core Features (MVP)
* Local, internet-independent operation over internal WiFi.
* NTAK Data Reporting: Implemented via asynchronous Message Queue. If the government server is down, the POS finalizes the payment instantly, and the background worker retries the API payload later without freezing the UI.
* SoftPOS and hardware terminal integration.
* Client-side QR-code based table ordering interacting directly with the local server.

## 4. Architecture and Topology
* Configurable topology during installation: Purely Local (dedicated local server PC) OR Cloud-based.
* **Auto-discovery:** Uses mDNS (Multicast DNS) so clients can instantly locate the local server even if its IP address changes.

## 5. Desktop POS Interface & Login
* Full-screen Kiosk mode.
* Visual user selection with avatars. Numeric PIN-only password field.
* Hardware authentication (RFID / NFC Card reader integration).

## 6. Table Map (Restaurant View)
* Visual table editor (custom table shapes, backgrounds, drag-and-drop).
* Assigned attributes: Dedicated waiter, VIP guest profile, table-specific discounts.
* Granular, table-level permission control.

## 7. Order Taking & Management
* Default guest count prompt upon opening a table.
* Orders can be assigned to the whole table or split by specific guests.
* Consolidated viewing options (by time, by guest, by course).
* **Proforma Invoice:** Printing a proforma sets the table status to 'Awaiting Payment'. Adding a new item automatically reverts the status.
* Granular split-payments (by guest or manual item selection).

## 8. Advanced Guest Management
* Dynamic guest transfer (moving items between tables) with conflict warnings.
* Temporary tables (dynamic, off-map tables existing only until payment).
* Multi-zone support (e.g., Terrace, Main Hall) with interactive map portals.

## 9. Sales View (Quick Sale & Table View)
* Unified UI layout. Top bar: Portion sizes, Void, Void All.
* Configurable 'Protected' items (items that cannot be modified after kitchen print).
* **Takeaway & Auto-VAT Shift:** The system automatically shifts the VAT rate in the background (e.g., from local 5% to takeaway 27%) according to Hungarian law, while attempting to keep the gross price fixed.
* Granular discounts (applicable to table, guest, order, or specific items).

## 10. Permission System
* Extreme granular, action-based permissions (endpoints and UI buttons).
* Roles and individual Overrides (+/- permissions).
* Built-in super-admin (Siduri Systems) account for remote maintenance.
* Local offline authentication utilizing cryptographic hashes.

## 11. Print Routing System
* Dynamic routing of print jobs based on product categories and physical zones (e.g., Drinks ordered from the Terrace go to the Outside Bar printer).
* **Printer Fallback (Disaster Route):** If a target printer (e.g., Kitchen) fails to acknowledge the TCP print job within 5 seconds, the server automatically routes the ticket to the main POS printer with a massive "KITCHEN PRINTER ERROR" warning to prevent lost orders.

## 12. Hardware Integrations
* Hungarian NAV-certified fiscal printers (Micra, CashCube) via serial/TCP.
* Payment terminals (Ingenico, Verifone) via protocols like NEXO.
* Generic ESC/POS thermal printers.

## 13. Finance, Invoicing & Payments
* **B2B Invoicing:** API integration with Számlázz.hu / Billingo. Ability to print "Simplified Invoices" directly on the fiscal printer.
* **Proportional Discounts:** Fiscal printers reject 0 HUF or negative items. The backend must proportionally distribute order-level discounts across the unit prices of all items based on their VAT keys.
* **5 HUF Cash Rounding:** Automatic rounding for cash payments to the nearest 5 HUF (legal requirement). Dynamic change calculator on the UI.
* **Void vs. Storno (Strict Finance):** Unpaid items can be *Voided* (deleted, prints a red void ticket to the kitchen). Paid, finalized receipts CANNOT be voided; they must be *Stornoed* (generating a completely new negative fiscal receipt).
* **Payment State Machine (Two-Phase Commit):** 
  * Real-time terminal status tracking.
  * *Timeout:* A strict 10-15s timeout during bank authorization. If the connection drops, the UI prompts the cashier ("Was the physical transaction successful?").
  * *Modifications:* Abort and resend logic for tipping on the terminal.
  * *Refund:* Automatic refund signal sent to the terminal upon receipt Storno.
  * The fiscal receipt is ONLY finalized and printed after a definitive success from the bank/POS.

## 14. Shifts & Cash Management
* Logical Business Days encompassing multiple Shifts tied to users and machines.
* **NTAK End of Day:** Automatic async aggregation and dispatch of daily sales data to the government portal upon day closure.
* Cash movements: Pay-in, Pay-out, Skimming (Cash drops) with receipts.
* **Tip Management:** Cash tips are withdrawn via a dedicated out-of-tax transaction. Credit Card tips are reported separately for payroll accounting and do not affect the physical cash drawer.
* Blind shift handovers and discrepancy logging (shortage/overage).

## 15. Multi-Warehouse & Inventory
* Unlimited physical/logical warehouses. Terminals deduct stock from assigned warehouses. Stock transfer logging.
* **Staff Consumption & Waste (Spoilage):** Crucially logged as *Inventory Adjustments*, NOT zero-price sales, bypassing the fiscal printer and NTAK entirely to maintain tax compliance.
* **Moving Average Price (MAP):** Computed from incoming stock purchase prices to calculate precise profit margins.
* **Stocktaking (Inventory):** Configurable "Calculated Waste %" (e.g., 2% spill allowance) for draft beer/ingredients to tolerate minor discrepancies during physical counts.

## 16. Network & Client State
* Exponential backoff for WebSocket/TCP reconnections.
* **Optimistic Locking:** Prevents race conditions. Database utilizes version numbers. If two PDAs edit the same table simultaneously, the slower request is rejected and the client is forced to refresh.

## 17. High Availability (Failover) Strategy

`[SUPERSEDED — A2]` **Client architecture decided.** The system is **server-authoritative**:
all shared mutable state (tables, orders, stock, discounts, shifts) is decided on the
server. Each POS holds a **cache plus a durable append-only outbox** — **not** a
PostgreSQL replica (the Hungarian spec's "local PostgreSQL replica" line is deleted).
If the Master **and** the Emergency Server are both down, the POS enters a **degraded
quick-sale mode** (item → payment → print), writing events to the outbox and replaying
them on reconnect. `[A2/a]` **Open tables are NOT available in that mode** — the waiter
re-enters the consumption as a quick sale. This preserves the "no shared mutable state"
invariant the whole design rests on.
`[?]` **Warning:** the degraded mode rests on an **unverified premise** — that with an
AEE fiscal device, the device itself issues and numbers the legal receipt. Verify before
coding; if false, this section collapses.

* **Emergency Server:** A dedicated standby thick client replicating the Master PostgreSQL DB in real-time.
* If the Master fails, the Emergency Server broadcasts its takeover via mDNS. PDAs and KDS automatically reconnect.
* Strict Split-brain protection (Master Lockout) ensures the original Master disables itself if it comes back online. Failsafe recovery requires a Superadmin.
  * `[OPEN — B1, A4]` **This entire HA section is AWAITING A DECISION.** Written but not yet accepted proposal: drop HA **out of the MVP** (after A2's degraded mode, the Emergency Server is a convenience feature, not disaster protection), but put the **epoch field into the protocol from day one**. Also: asynchronous replication, **manual** failover (bound to a permission, not a role), and **two-tier failback** — local manager for the normal case, Superadmin only to overwrite diverged data.
  * **Conceptual conflation this section commits:** the USP (§1) is resilience to **internet** outage, which the local server already solves. The Emergency Server protects against **local server hardware failure** — a different and far rarer event. Merging the two makes HA look better justified than it is.
  * `[OPEN]` Two-node split-brain has **no quorum**. Automatic failover with a fallible detector yields two masters and two diverged receipt sequences, which **cannot be merged**.

## 18. Management Interfaces
* Local Web UI powered by Spring Boot (accessible during internet outages) for managing products, modifiers, inventory, and viewing local reports.
* Cloud platform for global tenant and license management.

## 19. Licensing (DRM)
* Cloud-managed Hardware Fingerprinting (Motherboard/CPU/MAC).
* **10-Day Grace Period:** The system operates offline for 10 days.
* **NTAK SLA Alert:** Regardless of the license, if the system is offline for 18 hours, a critical red banner warns the user of the impending 24-hour legal reporting deadline violation.

## 20. Customer Facing Display (CFD)
* Shows items, total, and tipping interface. 
* Background video/image idle loop (auto-transcoded by backend to 720p/1024x768).

## 21. Order Ready Board
* Standalone Smart TV/Android app receiving WebSocket triggers to display "Preparing" and "Ready" ticket numbers.

## 22. Inventory App
* Flutter PDA module for barcode scanning and stocktaking.

## 23. Kitchen Display System (KDS)
* Android/Windows touch UI. Drag-and-drop ticket management that triggers the Order Ready Board.
* Integrates directly with Foodora/Wolt delivery statuses (e.g., "Ready for Courier").

## 24. External API
* Native integration for Foodora / Wolt. Open token-based API for custom CRM and loyalty points.

## 25. Advanced Analytics & BI
* Dynamic charts in the cloud.
* **True Margin Calculation:** Utilizes the Moving Average Price of inventory. Includes a dynamic UI slider for "Calculated Waste %" so management can view true profit margins accounting for realistic spoilage.

## 26. Special Products (DRS & Reusable Cups)
* **DRS (Deposit Return System):** An un-discountable, tax-exempt fixed 50 HUF fee silently attached to specific products (e.g., PET bottles). Can only be voided if the parent item is voided.
* **Reusable Cups (Tokens):** Treated as a standard product (+ value), but returning a cup (- value) automatically triggers a Cash Pay-Out transaction from the drawer to keep the cash balance accurate.

---

# Architecture and Git Repositories
The project is strictly separated into the following 5 repositories:
1. `siduri-backend-server` (Java / Spring Boot - GraalVM - Local Master/Emergency server & PostgreSQL)
2. `siduri-pos-client` (C# / WPF - Desktop POS client, Fiscal/Hardware integrations)
3. `siduri-flutter-clients` (Flutter Workspace - PDA, KDS, Order Board, Inventory App)
4. `siduri-updater` (C# - Standalone offline patcher utility overcoming Windows file lock issues)
5. `siduri-cloud-api` (Node.js/Java - Cloud license, NTAK backup, and global admin server)

Please confirm your understanding of the architecture, constraints, and instructions. Await my command to start coding!