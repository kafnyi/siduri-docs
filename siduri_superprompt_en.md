# Siduri — System Superprompt

**Product:** Siduri — Hungarian hospitality POS and management system
**Vendor:** Siduri Systems
**Document status:** complete, current specification, written for machine consumption
**Last updated:** 2026-08-23 (after the close of design session 3)

---

# Role and Context

You are a Senior Software Architect, Database Expert, and Full-Stack Developer.
Your task is to design the architecture and write the code for an
industrial-grade, offline-first, highly available hospitality POS and management
system, through iterative collaboration with the operator.

The specification below is complete and current. It complies with Hungarian
financial and tourism reporting regulation (NAV, NTAK, DRS) and handles hardware
failover, payment-terminal timeouts, asynchronous tax reporting, and peripheral
outages.

## Strict instructions before generating code

1. Read, analyse and internalise the entire specification. **Do NOT generate code yet.**
2. In your first response, acknowledge your understanding of the architecture, data flow, and the critical failover and degraded-mode mechanisms in a short, concise summary. State that you are ready to work.
3. Wait for specific instructions on which repository or database schema to begin with.
4. **Never add AI attribution** to any commit message, code comment, document, or artifact. No co-author trailers, no session links, no model identifiers.
5. **Anything marked `[UNVERIFIED]` must not be built upon** until confirmed against a primary source.
6. **Anything marked `[MEASURE]` must not be given a number by estimation.** Real hardware only.

## Tag legend

| Tag | Meaning |
|-----|---------|
| `BASE` | Architectural foundation — not optional, not deferrable |
| `MVP` | Part of the first shippable release |
| `v1` / `v2` | Later expansion rings |
| `VISION` | Direction, not scheduled work |
| `[OPEN]` | Not yet decided |
| `[UNVERIFIED]` | Assumption requiring source confirmation before coding |
| `[MEASURE]` | Number obtainable only by measurement |

## Companion documents

`NYITOTT_KERDESEK.md` (Hungarian) holds the **reasoning** behind every decision,
the rejected alternatives, and the self-corrections. `FOLYAMATBAN.md` holds
current status. `MERESEK.md` holds the measurement register.
`siduri_spec_hu.md` is this same specification in Hungarian, for humans.

---

# 1. Glossary

## 1.1 Devices and roles

| Term | Meaning |
|------|---------|
| **POS** | Physical touch-screen **thick client** (AIO PC) with peripherals. Windows only. |
| **Thin client** | Phone or tablet (Flutter) used by waiters for order taking. |
| **KDS** | Kitchen Display System. |
| **Order Ready Board** | Customer-call display ("Preparing" / "Ready"). |
| **Kiosk** | Self-service ordering and payment terminal. |
| **Main server** | The site's authoritative server. Typically runs on a working POS machine. |
| **Backup server** | Standby server, **always on a Windows POS thick client**. |
| **Witness** | A machine that votes on whether the main server is reachable. |
| **Cloud** | Siduri's central platform: licensing, archive, web admin, analytics. |

## 1.2 Day concepts — four distinct things

| Term | Meaning |
|------|---------|
| **MUNKANAP** (business day) | The **site's** business day. Not a calendar day. Multiple may be opened on one date. **Hard maximum 23 h 45 min.** |
| **MŰSZAK** (shift / fiscal day) | **Per-device** concept — that cash register's fiscal day. Multiple per business day, per machine and per user. |
| **NTAK tárgynap** (reporting day) | NTAK's day concept. **Derived from the OPENING date**, therefore effectively equal to MUNKANAP. **NOT a calendar day.** |
| **Calendar day** | Wall calendar. Display and a few legal timestamps only. |

## 1.3 Operating states

| Term | Meaning |
|------|---------|
| **Normal** | Client reaches the server; all integrations live. |
| **Reduced operation** | Umbrella term with two causes: **(a)** the client cannot reach any server (degraded / quick-sale mode), **(b)** a protected integration is temporarily disabled. Staff learn **one pattern with two subtypes**, not two separate worlds. |
| **Degraded mode** | Client reaches neither main nor backup server. Quick sale into a local outbox. |
| **Emergency mode** | The backup server has taken over. |
| **Orphan transaction** | A transaction that exists on one server but not the other, because replication did not catch up before the outage. |

## 1.4 Product concepts

| Term | Meaning |
|------|---------|
| **Product** | Sellable item. Mandatory main category, two VAT rates, NTAK classification. |
| **Variant (kiszerelés)** | **Child** of a product: own gross price, own recipe quantity, own volume/weight. E.g. 0.3 l and 0.5 l draught beer. |
| **Modifier** | **Always a deviation** from the default. The default is the recipe. |
| **Modifier group** | Set of modifiers with `min` / `max` / `FreeLimit` rules. |
| **Composite menu** | A product built from **menu components**; explodes into its components on the receipt. |
| **Recipe (BOM)** | The product's ingredient composition. |

---

# 2. Product concept

* **Target market:** Hungarian SME hospitality — sites subject to NTAK reporting.
* **Primary USP:** **offline-first**. The system runs on the site LAN and is resilient to internet outage; it synchronises with the cloud afterwards.
* **Secondary USP:** **high availability** — a backup server against main-server hardware failure.

> **Do not conflate these two.** Internet-outage resilience is provided by the
> local server. The backup server defends against a **different and much rarer**
> event: hardware failure of the local server. Conflating them makes HA look more
> justified than it is.

## 2.1 Business model

* **Single-machine use without table management: free.** Entry tier.
* **Paid tiers** for everything else, described by the **integration and feature registry** (§19.7).
* The support platform already exists and is out of scope.

---

# 3. Design principles

These are not style rules. Every concrete decision traces back to them, and they
break ties.

| # | Principle |
|---|-----------|
| **A1** | **One source of truth.** Every other file is a pointer, and must say so about itself. |
| **A2** | **No silent failure.** What broke must be visible — to the user, in the log, or both. Silently swallowed errors are forbidden. |
| **A3** | **Do not tell the customer what they want.** Where a customer may have a genuine business reason to deviate from a computed value, the computed value is a **one-shot fill helper, never a live reference**. |
| **A4** | **Copy, do not reference.** If inheriting a value would later silently change the derived one, copy it. |
| **A5** | **The two error directions are not equal.** VAT too high is a financial disadvantage; VAT too low is a legal violation. The mechanism must lean toward the **smaller harm**. |
| **A6** | **Rarely executed code fails first in production.** Prefer paths that run often. |
| **A7** | **Every "temporary" bypass becomes permanent** unless it has an enforced expiry. |
| **A8** | **Offering the bypass teaches the bypass.** The system must never proactively propose the workaround. |
| **A9** | **Hardware is a given, not a choice.** The installed J1900 base is a constraint; design for it, not against it. |
| **A10** | **No AI attribution** in any commit, code, document, or receipt. |

---

# 4. Technology stack and target hardware

## 4.1 Stack

| Layer | Technology | Note |
|-------|-----------|------|
| **Backend** | Java (Spring Boot), **GraalVM Native Image** | Native compilation is a **constraint**, not an optimisation — J1900 memory limits |
| **Database** | PostgreSQL | Strict memory limits |
| **POS client** | C# / WPF, .NET 8+ | **Windows 10 IoT Enterprise (LTSC) only.** Linux support REMOVED |
| **Mobile / thin client** | Flutter | PDA, KDS, order board, inventory app |
| **Updater** | C# standalone utility | Works around Windows file-lock problems |
| **Cloud** | Java or Node.js | Licensing, archive, web admin |

**Avalonia was evaluated and rejected:** WPF does not run on Linux, but no Linux
POS will ship, so the migration cost would never be recovered.

## 4.2 Target hardware `BASE`

**Installed base is Intel J1900 (Bay Trail), 64 GB SSD.** The base is **MIXED**:
the same machine type runs **as server AND as POS client**.

Consequences:

* The GraalVM constraint stands.
* **The WPF client's performance budget is also tight** — e.g. 720p secondary-display video on a Bay Trail iGPU is non-trivial.
* `[MEASURE]` **Every performance figure must be measured on real J1900 hardware, never estimated** (`MERESEK.md` M1–M3, M12–M14).
* **CMOS batteries on 10+ year old machines are dead or dying.** This is not theoretical: after a power cut the clock may report a date years in the past. The system must survive this (§9.5).

---

# 5. Topology and deployment size classes

## 5.1 Size classes are RECOMMENDATIONS, not constraints `BASE`

**The software must never reject a configuration.** If the customer decides
otherwise in full knowledge of the risk, that is accepted and recorded by the
**risk acceptance form** (§24.4).

| Machines | Main server | Backup server | Fiscal device |
|----------|-------------|---------------|---------------|
| **1** | **the cash register IS the server** | none | 1 |
| **2–3** | on a POS | **optional** | recommend one per machine |
| **4+** | on a POS, or dedicated if affordable | **strongly recommended** | **emphatically: at least 2** |

**"No backup server" is a first-class configuration, not a fault state** — in
that case a takeover must never even be offered.

## 5.2 Role placement rules `BASE`

* **The backup server is NEVER a dedicated machine — always a Windows POS thick client.**
* The main server **typically also runs on a POS**; a dedicated machine is possible where affordable.
* **Thin clients, KDS and order boards can carry neither role.**
* **Server and client may run on the same machine** — a supported configuration.

**Four consequences:**

1. The backup machine's load spikes **at the worst possible moment** — takeover happens during peak.
2. The machine carrying the role **can be switched off by staff**, because to them it is "just a till".
3. **The server must be a Windows Service**, not a process inside the cashier's session.
4. **Update ordering is a hard requirement** on `siduri-updater`: role-carrying machines must not update simultaneously.

## 5.3 Discovery

**mDNS** on the site LAN so clients find the server after IP changes. Role
changes (§7) propagate over mDNS.

---

# 6. Server-authoritative model and degraded mode

## 6.1 Base model `BASE`

**All shared mutable state is decided on the server:** tables, orders, stock,
discounts, shifts, permissions.

The POS holds a **cache plus a durable, append-only outbox** — **NOT a PostgreSQL
replica.** (The earlier "local PostgreSQL replica" design is deleted.)

## 6.2 Degraded mode (quick sale) `MVP`

When the client can reach **neither the main nor the backup** server:

* **Quick sale is possible:** item → payment → print.
* Events are written to the **local outbox** and replayed on reconnect.
* **Open tables are NOT available.** The waiter re-enters the consumption manually as a quick sale.

**Why tables are unavailable:** this preserves the *"no shared mutable state"*
invariant on which the whole degraded mode rests. If two machines could
independently modify the same table, reconciliation on reconnect would be
unsolvable.

**All three parts are in the MVP:** local log, degraded UI, reconnect
reconciliation.

`[UNVERIFIED]` **The entire degraded mode rests on one premise:** on an AEE
device the legal receipt is issued and numbered **by the fiscal device itself**,
so server outage does not block receipt issuance. **Must be verified before coding.**

## 6.3 Each machine enters reduced operation independently `BASE`

Reduced operation is a **per-machine state, not a site state**. If one machine's
WiFi glitches, that machine degrades; the others continue.

**Beneficial side effect:** the reconciliation code **runs often** — not once a
year in a real disaster for the first time (principle A6).

## 6.4 Degraded mode and NTAK `MVP`

NTAK has an **official path for service outages**: the order summary's
`osszesitett` flag and the `osszesitettIndoklasa` field. See §11.6.

**Requirement:** degraded mode must record a **reason code** (power cut / server
failure / network failure) so the justification can be filled automatically.

## 6.5 Staff messages `MVP`

Three messages, using the word "network" (never "internet"):

1. **Server suspect** — "We cannot reach the server. Please check the server machine and the network."
2. **This machine is at fault** — "This machine cannot reach the network. Check this machine's network connection."
3. **Undetermined** — when we cannot tell.

Plus a **separate, quieter indicator for missing internet**, which is **never a
fault state** and **never influences** the "server or me?" decision.

---

# 7. High availability

## 7.1 Base decisions `MVP`

* HA **stays in the MVP** — deliberately, against the opposite recommendation.
* The backup machine is **also a J1900**.
* Working assumption: **asynchronous replication**. `[MEASURE]` The claim "synchronous is impossible" is **not yet measured** (`MERESEK.md` M4).
* The "automatically switch from synchronous to asynchronous" branch is **rejected** (silent failure, A2).
* **The epoch field (fencing) is a REQUIREMENT**, present in the protocol from day one.
* **`[BASE]` Mandatory protection against replication-slot WAL accumulation.**
  A replication slot belonging to a disconnected standby makes the primary
  **retain WAL indefinitely** → **the disk fills** → **THE PRIMARY STOPS.**
  On a 64 GB SSD this is a matter of days.

  **Especially dangerous here**, because it joins two facts we had treated
  separately: the backup server is **a POS machine**, and **"the machine carrying
  the role can be switched off by staff, because to them it is just a till"**
  (§5.2). A standby disconnected for days is therefore **not an edge case but the
  predictable consequence of a risk we already documented.**

  | # | Solution |
  |---|----------|
  | a | **The limit is DISK-based, not time-based** — the real constraint is space. Cap the WAL a slot may retain; beyond the limit the slot is invalidated |
  | b | **Consequence that must be stated:** after slot invalidation the standby **cannot catch up incrementally** — a **full resynchronisation** is required. That is a heavy operation on J1900 and must be scheduled **outside peak hours** |
  | c | **It must be loud** (principle A2), never a silent slot drop |
  | d | **Alert BEFORE the threshold:** a warning at half the budget — the stoppage must not be the first signal |
  | e | `[MEASURE]` Interaction of WAL size with the 30-day purge and the 64 GB SSD |

## 7.2 Two-stage failover `MVP`

**The machine checks; the human decides.**

1. The POS **immediately and visibly** signals reduced operation and states what to check.
2. The machine must **recognise when IT is the one off the network** — not the server.
3. **Takeover is offered only after 5 minutes**, and only if the witnesses also cannot reach the server.
4. **A HUMAN presses the button.**

## 7.3 Witness scheme `MVP`

Split-brain cannot be solved with two nodes. Therefore other site machines vote
on whether the main server is reachable.

**Client self-diagnosis ladder, in order:**

1. Can I reach my own network interface?
2. Can I reach the default gateway?
3. Can the witnesses reach the server?
4. **Last rung only:** is there internet — to a **public** address, over HTTPS (not ICMP), with two separate signals (name resolution + reachability). **This never influences the "server or me?" decision**; it appears only in a separate, labelled line.

## 7.4 Takeover paths `MVP`

| Path | When | Data loss |
|------|------|-----------|
| **Clean takeover** | The old main is alive and reachable from the backup | **Zero** — the backup drains unreplicated transactions BEFORE taking over |
| **Hard takeover** | The old main is genuinely dead | **Orphan transactions are unavoidable** |

**Pre-takeover collection from clients:** the backup collects unacknowledged data
from client outboxes. **This does not block the first receipt** — because of
two-layer numbering (§8) the backup can serve immediately and collection runs in
parallel. Its purpose is **completeness and verification**, not collision
avoidance.

## 7.5 Failback `MVP`

* **AUTOMATIC** once main and backup **see each other and talk for 1 continuous minute**.
* The old "superuser account only" rule is **rejected**.
* **Extraction of orphan transactions is automatic and mandatory.**
* **Booking them is NOT automatic** — duplicate fiscal receipt risk requires a human decision.
**Orphan transactions are resolved EXCLUSIVELY on a Siduri support surface.**
This task is **taken away from the customer entirely** — a duplicate fiscal
document is a legal consequence, resolving it requires **cross-reading the fiscal
device's own journal**, and that is expertise, not a button press. It is rare
(only after a hard takeover), so support involvement scales fine. It is the same
escalation pattern as the raw audit (§18.4) and persistent integration disable
(§19.4).

**Two constraints:**

| # | Constraint |
|---|-----------|
| a | **An unresolved orphan must NOT block trading** — it goes to a quarantine queue and the site keeps working |
| b | **The customer must SEE that unresolved items exist**, even though they cannot act on them (principle A2). We take away the **resolution**, never the **knowledge** |
* **Role swap happens immediately once stable** — no deferral to a quiet window.

## 7.6 Flap protection `MVP`

**Increasing backoff** after every automatic failback, plus a **shutoff limit**
after which automation disables itself and **says so loudly**.
`[MEASURE]` Thresholds come from measurement (`MERESEK.md` M6).

## 7.7 What HA does NOT solve `BASE`

> **Server HA does not protect against the fiscal device.** If a site has a
> single fiscal device and the machine it is attached to dies, open tables cannot
> be closed anywhere. A duplicated server helps not at all.

Mitigation: **recommend one fiscal device per machine**, emphatically at least
two from 4 machines, plus **print redirection** (§19.6).

---

# 8. Document numbering

## 8.1 Two-layer numbering `BASE`

| Layer | Format | Issued by | Nullable |
|-------|--------|-----------|----------|
| **SIDURI number** | `xxxxxxyyyzzzzz` | us | no |
| **FISCAL number** | `Axxxxxxxxx/yyyy/zzzzz` | the fiscal device | **yes** |

**SIDURI number composition:** `xxxxxx` = the **BUSINESS DAY** date (not the
calendar date), `yyy` = device number, `zzzzz` = daily sequence.
Example: `26082200300347`.

**Rationale:**

* **Restarts daily → can never run out.**
* **The date prefix makes numeric order equal chronological order.**
* **Every issuing device numbers from its own disjoint range** (till 2 uses `002…`) → **collision is structurally impossible**, zero coordination is needed, and **the backup server can serve IMMEDIATELY on takeover.**

**Why the fiscal number cannot be our identifier:**

* **It only arrives AFTER printing** — until then the document would have no identifier, and on a print failure it never would.
* We do not control it.
* **Not every document has one** — proformas, stock movements and cash movements never do.

The fiscal number **is stored alongside the document**, because voiding requires it.

## 8.2 Device identity and clone protection `MVP`

* The device-number space is **SHARED across all device types** (POS, thin client, kiosk) — so later expansion of thin clients does not break numbering.
* The server issues the identifier, and **no registration means no document**.
* **This alone does not stop a clone.** Missing piece: **hardware fingerprint + rotating credential**. Two fingerprints on one identifier → **both blocked** until a human resolves it.
* **Machine replacement is an explicit, authorised operation**, not an accidental side effect.

## 8.3 Fiscal device identity on the document `MVP`

**The document stores WHICH fiscal device printed it.** With print redirection
(§19.6) the SIDURI number belongs to the **issuing** machine and the fiscal
number to the **printing** device — the two layers intentionally diverge, and it
must be possible to see why afterwards.

---

# 9. Day concepts, day close, clock

## 9.1 MUNKANAP (business day) `BASE`

The **site's** business day. Not a calendar day; multiple may open on one date.

| Threshold | Behaviour |
|-----------|-----------|
| **23:00** | Soft warning |
| **23:30** | Strong warning |
| **23:45** | **Unconditional forced close** |

**Why 23:45 and not 24 h:** the NTAK day-close validation is
`zarasIdopontja − nyitasIdopontja <= 24 hours`, **synchronous, error key
`Conflict`** — a day longer than 24 hours is **rejected outright**. The 15
minutes are margin.

> **CRITICAL: compute the duration on an ABSOLUTE (UTC) basis, never on wall
> clock.** On the autumn DST night a 06:00 → 06:00 "day" is 24 hours by wall
> clock but **25 hours in real time**. This is the single most likely way to earn
> one rejection per year.

**Measurement uses a monotonic clock** (the server's non-resettable upward
counter), and the cut decision takes the **more conservative** of the monotonic
and wall-clock elapsed values. A server restart resets the monotonic clock — fall
back to wall clock and signal that.

## 9.2 MŰSZAK (shift / fiscal day) `BASE`

**Per-device** — that cash register's fiscal day. Multiple per business day, per
machine and per user.

* Cash in/out and skimming **with a document**.
* Shift handover **with unchanged drawer balance** (no skimming) is allowed.
* **Drawer discrepancy logged at open** (shortage / surplus registered).
* **Built-in denomination calculator** for shift close: a multiplying counter
  (20 000 × 4, 10 000 × 3, …) for totalling cash. `v1`
  **Store the denomination breakdown in the shift-close record**, not just the
  total — when investigating a discrepancy the denomination structure often
  reveals what happened (a missing 20 000 note is not sloppy counting, it is one
  banknote).

## 9.3 Automatic day close `MVP`

A customer-configurable **planned day-close time** (e.g. 04:00).

**Sequence:**

1. **Pre-phase, 5 minutes before close:** opening new orders and starting new payments is blocked; in-flight operations may finish.
2. **Close each device's MŰSZAK.**
3. **Close the MUNKANAP.**
4. Meanwhile inform users: *"automatic day close in progress, please wait"*.

**Mandatory gap between close and next open:** configurable, **minimum 5
minutes, default 10 minutes.**

> **The gap IS the safety margin.** 04:00 close + 10 minutes → the business day
> can mathematically be at most **23 h 50 min**. No separate guard is needed for
> the 24-hour limit: it follows from the shape of the configuration.

**Four mandatory additions:**

| # | Rule | Why |
|---|------|-----|
| a | **Closing the MUNKANAP must not depend on every device's shift being closed.** Mark unreachable devices and close them at their next power-on | A POS switched off overnight is unreachable at 04:00. If that blocked, automation would never run |
| b | **Automation must NOT close open GUEST tables** — they cross the boundary | The guest gets one bill, not two |
| c | **Validate the configuration at save time**, and **display the computed maximum**: "close 04:00, reopen 04:10 → business day at most 23:50" | No hidden arithmetic |
| d | **The 23:45 forced close remains as a backstop**, even with automation enabled | Automation can fail: server down, device stuck |

**Manual close:** separately enableable. If it happened, automation has nothing to do.

**Why a 24/7 site needs the planned close:** relying only on the forced cut makes
the day boundary **drift 15 minutes earlier every cycle** — one hour in four
days, all the way round within a month, eventually firing **Saturday 22:00 at
peak**.

## 9.4 Orders crossing the business-day boundary `MVP`

The order **crosses the boundary** and belongs to the tárgynap **in which it
started** — consistent with the tárgynap being derived from the opening date.

`[OPEN]` **Does NTAK accept an order summary for a tárgynap after that tárgynap's
day close has been submitted?** The specification contains neither a prohibition
nor a permission. At a 24/7 site this is a daily occurrence, so it must be asked.

## 9.5 Clock synchronisation `BASE`

**Time source order at the site:**

1. **NTP**, if internet is available.
2. **The fiscal device's clock** — the AEE synchronises over its own mobile network, so **it is the most reliable clock on site even without internet.**
3. **The site server, toward the clients.** Clients sync **to it**, not to the internet — so the site stays internally consistent offline.

**Fix first, complain second:**

| Deviation | Response |
|-----------|----------|
| **< 2 min** | **Fix silently.** No message |
| **2–15 min** | Fix if a source exists. If not: **non-blocking** warning + audit entry |
| **> 15 min** | **Prominent, acknowledgeable** warning — **still non-blocking** |
| **> 2 h, or a different DATE** | **The ONLY blocking case.** One-button escape: "set clock from the fiscal device" |

**When we set the clock vs. only check it:**

| When | What |
|------|------|
| **Before day open** | **Check AND SET** |
| **At the 23:00 / 23:30 warnings** | **CHECK ONLY. Never set** |

> **INVARIANT: never move the clock forward while a business day is open.**
> Both `nyitasIdopontja` and `zarasIdopontja` come from our clock, so absolute
> drift cancels in the difference — **unless we correct mid-day**. A silent
> 12-minute forward correction would turn a 23:40 day into 23:52. Backward
> correction is also forbidden, as it would scramble ordering.

**The real hazard on this hardware is not sub-minute drift but the dead CMOS
battery** — "the machine thinks it is 2014", after every power cut.

**Every clock change is an audited event**, with old and new values.
**Ordering never depends on the wall clock** — a monotonic counter provides it.

---

# 10. Fiscal operation

## 10.1 Three operating modes `BASE`

| # | Mode | Output | Note |
|---|------|--------|------|
| **1** | **Internal system** (no fiscal device) | Paper must carry the mark **"NEM ADÓÜGYI BIZONYLAT"** (NOT A FISCAL DOCUMENT) — **a mandatory element** | Does not discharge the receipt obligation |
| **2** | **Online cash register (AEE)** | Fiscal receipt with fiscal number | Current primary target |
| **3** | **e-cash register** (Decree 8/2025. (III. 31.) NGM) | e-receipt, Nyugtatár | Later direction |

## 10.2 We do not write our own fiscal software `BASE`

**Stated decision:** we will not write software for a NAV-approved fiscal printer,
now or later. **We integrate with existing vendor software.**

**Resulting constraints:**

* The vendor's driver-protocol documentation is **copyright protected**, and **there is no partner agreement** — only a single, empty email reply so far.
* **Its content must never appear in any published material** — no quotation, no command table, no "paraphrased but recognisable" description. **The repositories always stay private.**
* The vendor-specific driver lives in a **separated module** so it can be lifted out at any time.
* **There is no support contract, no notification of firmware changes, and no test device.**

> **Scheduling gate:** development proceeds, **but the fiscal layer must not be
> FINALISED before vendor contact and a physical test device are secured.** The
> fiscal milestone cannot be closed without a device.

## 10.3 The department (gyűjtő) allocation is a hard constraint `BASE`

The allocation received has **8 fixed slots, none free**:

| # | Department | Tax letter |
|---|-----------|------------|
| 1 | Product 5% | A00 |
| 2 | Product 18% | B00 |
| 3 | Product 27% | C00 |
| 4 | Service charge 5% | A00 |
| 5 | **TAM** (exempt) | E00 |
| 6 | Service charge 18% | B00 |
| 7 | Service charge 27% | C00 |
| 8 | **AJT** (excise-stamped goods) | D00 |

**Consequences:**

1. **The VAT rate set is fixed: 5 / 18 / 27 / TAM / AJT.** Nothing else can be sent. **Validate at product-master save time**, not at print time — by then it is too late.
2. **Service charge has its own per-rate departments.** Service charge **must not be folded into the product line**, and must be computed **split by VAT rate**, not as one closing amount.
3. **AJT is effectively unused in hospitality** — the only candidate free slot, if the vendor permits reallocation. `[OPEN]`
4. Any new need (e.g. DRS deposit) must fit inside an existing slot.

**Confirmed by two independent sources:** NTAK's `afaKategoria` value set is
`A_5`, `B_18`, `C_27`, `D_AJT`, `E_0` — letter for letter the same.

## 10.4 Line types in the fiscal layer `MVP`

| Case | Handling |
|------|----------|
| **Priced modifier** | **Its own line**, on its own VAT rate |
| **Unpriced modifier** | **Text line under the product** — not a line item; no price, no VAT, no department |
| **Subtractive modifier** (e.g. "no cheese −100") | **Must NOT be sent as a negative-price sale line** — in the protocol a negative price means *line void*. Route via the discount mechanism, or fold into the product price |
| **Deposit return** | Negative quantity — natively supported by the protocol |
| **Whole-bill discount** | **Distributed across lines in proportion to VAT rate** |

`[UNVERIFIED]` **The zero-amount line.** The protocol declares it supported, but
per the operator's knowledge **the device does not accept it**. **Working
assumption: it does not.** The text-line solution is correct regardless — if no
line item is sent, the zero-amount question never arises. (`MERESEK.md` M15)

## 10.5 Void and storno `MVP`

* **Open line** = deletable (void).
* **Closed, paid receipt** = **storno only**, via a negative document.
* Storno **requires the original fiscal number** — hence it is stored (§8.1).

`[UNVERIFIED]` The "entirely new negative fiscal receipt" mechanism.

## 10.6 Network exposure of the vendor service `BASE`

**The vendor service listens on a port and does NOT check whether the request
came from localhost or from outside.**

**Two consequences:**

1. **Print redirection (§19.6) is technically free** — nothing needs opening.
2. **But the risk already exists, independent of us:** on the site network **anyone, from any device, can send fiscal commands without authentication** — open a document, add lines, void. **If guest WiFi is not separated from the operational network, a guest can do this from their phone.**

> **Mandatory installation precondition: physical or VLAN separation of guest
> WiFi from the operational network.** Not a recommendation. A mandatory item on
> the installation checklist; non-compliance is a subject of the risk acceptance
> form.

Additional mitigation: firewall rules on our own machines restricting the fiscal
service port to known hosts. This does not fix the root cause but narrows it.

`[OPEN]` Does the service have **any** authentication, IP restriction, or listen-address setting — question for the vendor.

---

# 11. NTAK data reporting

Source: **NTAK Hospitality — RMS Interface Specification v1.06** (MTÜ,
2024-06-10), the official technical specification.

## 11.1 Fundamentals `BASE`

* **Tárgynap (reporting day):** *"the date equal to the opening date of the currently open day"*; when the day crosses midnight, *"the day derived from the opening timestamp"*. Therefore **effectively the MUNKANAP** — not a calendar day.
* **Two message types:** order summary (turnover data) and day close.

## 11.2 Send cadence `BASE`

| Message | When |
|---------|------|
| **Order summary** | **Every 15 minutes**, covering orders recorded since the previous send. **The interval must be parameterisable** — it must not be hard-coded |
| **Day close** | At business-day close, **but at least every 24 hours** |

> **This materially changes the offline design.** During a longer internet outage
> a missed send accumulates **every 15 minutes**; these must be queued and, on
> reconnect, replayed **in order and without overlap**. The outbound NTAK queue
> must be a first-class, durable, monitored queue — exactly like the receipt outbox.

## 11.3 Processing-receipt retrieval `MVP`

Every submission returns a **processing identifier in a synchronous response**,
and **the processing result MUST be queried** — within **24 hours** of
submission, and at the latest within **1 month**, after which it is no longer
available.

**Submitting is not enough: the acknowledgement must be collected and stored.**
This is a second, retrospective process.

## 11.4 Hard validations `BASE`

| Validation | Type | Consequence |
|-----------|------|-------------|
| `zarasIdopontja − nyitasIdopontja <= 24 h` | **synchronous**, `Conflict` | Day close rejected → hence the 23:45 business-day cap (§9.1) |
| `rendelesVege − rendelesKezdete <= 24 h` | **synchronous**, `Conflict` | **An open order cannot stay open longer than 24 hours** |
| `nyitasIdopontja <= sysDate`, `zarasIdopontja <= sysDate` | synchronous, `Future` | **If our clock runs ahead, the message is rejected** |
| `nyitasIdopontja >= previous zarasIdopontja` | asynchronous | No overlapping periods |
| After `ADOTT_NAPON_ZARVA`, no further day close for that tárgynap | asynchronous, `UniqueConstraint` | **See §11.7 — irreversible** |
| The sum of line totals must equal the order total | — | **Hard constraint on menu splitting** (§13.4) |

**The 24-hour order limit applies only to SUBMITTED orders.** Staff tables and
waste are exempt because they are not submitted.
`[UNVERIFIED]` NTAK has an `EGYEB / NEM_VENDEGLATAS` line category, but the order
classification value set is only `NORMAL / SZTORNO / HELYESBITO` — **there is no
"non-turnover" order classification.** If staff consumption turns out to be
reportable, the limit applies to it too.

**An internal limit is needed regardless:** a staff table open for weeks is an
operational fault → warn at day open for every non-guest order older than the
previous business day.

## 11.5 Line-level fields `BASE`

| Field | Content |
|-------|---------|
| `megnevezes` | max 255 chars, mandatory, non-empty |
| `fokategoria` / `alkategoria` | From the standard value set (§11.8) |
| `afaKategoria` | `A_5` / `B_18` / `C_27` / `D_AJT` / `E_0` |
| `bruttoEgysegar` | May be fractional — **but we send whole forints** (§15.2) |
| `mennyisegiEgyseg` | `DARAB` / `LITER` / `KILOGRAMM` / `EGYSEG` / `ADAG` |
| `mennyiseg` | **the product's own pack size** (e.g. 0.33) |
| `tetelszam` | **how many were ordered** (e.g. 2) |
| `tetelOsszesito` | **integer**, `tetelszam × bruttoEgysegar`, commercial rounding |

**`mennyiseg` and `tetelszam` are two different things.** Two 0.33 l cans:
`mennyisegiEgyseg = LITER`, `mennyiseg = 0.33`, `tetelszam = 2`.

**Therefore the product master needs TWO NTAK fields:** unit of measure **and**
pack quantity. This maps directly onto the variant model (§12.4).

> The specification's **guidance** says a 0.33 l canned soft drink should use
> `LITER`, not `DARAB`. **This is a Note, not a validation** — the field's only
> validations are `NotNull` and `Enum`, so **`DARAB` passes.** The system
> **supports both**, **offers** the recommended value, but **the customer
> decides** (principle A3).

**Order-level fields:** `helybenFogyasztott` (bool — **"in mixed cases, mark as
on-premises"**), `rendelesBesorolasa` (`NORMAL` / `SZTORNO` / `HELYESBITO`),
`osszesitett` + `osszesitettIndoklasa`.

**Mapping `helybenFogyasztott`:** our model is finer (per-line fulfilment mode).
Rule: **true if at least one line is consumed on premises**; only a fully
takeaway order is false. VAT is per line, so mixed orders still report correctly.

## 11.6 Degraded mode in NTAK `MVP`

`osszesitett` (bool) + `osszesitettIndoklasa`:

> *"Marks that a given order summary contains the sales of a longer period
> (max 1 business day) in aggregate. Usable only in case of service outage, e.g.
> power cut or system failure. In normal reporting it must be sent as false."*

**This is exactly our degraded mode.** No bespoke solution is needed.

| # | Consequence |
|---|-------------|
| a | **Aggregation is capped at 1 business day** — longer outages must be split per day |
| b | **A justification string is required** → degraded mode must record a **reason code** |
| c | In normal operation the flag must be **false** — never set it true "just in case" |

## 11.7 Closed and zero-turnover days `MVP`

**This is OUR software's obligation, not the customer's on the NTAK portal.**
Verbatim:

> *"Every RMS software must send a day close message even if the hospitality unit
> was closed on that tárgynap. […] A day close message must also be sent if no
> order summary was submitted during opening hours. […] Day close messages must be
> submitted for every tárgynap."*

> ## ⚠️ HAZARD: never send the "closed" signal AHEAD of time
>
> The validation: *"For a tárgynap that already has an `ADOTT_NAPON_ZARVA` day
> close submitted, no further day close messages may be submitted."*
>
> If we sent it at 23:55 and the venue opened at 23:58, **that tárgynap would be
> permanently sealed** — their real turnover's day close could never be
> submitted. **Not reversible.** And this is not hypothetical: 23:55 is exactly
> when a bar or night buffet opens.

**Correct approach — send retrospectively, never ahead:**

| # | Rule |
|---|------|
| a | `ADOTT_NAPON_ZARVA` / `FORGALOM_NELKULI_NAP` may be sent **only once the tárgynap has definitively ended** |
| b | **A daily job** (suggested 01:00) walks unclosed tárgynap records and sends the correct classification based on the **opening-hours pattern** |
| c | **If the pattern says they should have been open but no day was opened:** this is a **question**, not automation — at the next day open: *"were you closed yesterday, or did someone forget to open the day?"* |
| d | **On server start, backfill** every missing tárgynap close |
| e | **While closed (site server powered off) THE CLOUD sends them.** The site server owns this while online; the cloud steps in when the pattern says closed **and** the server has not reported for X hours. Duplicates are rejected by the `UniqueConstraint` |

**Opening-hours pattern** (weekly schedule + exception days/holidays), configured
in the web UI. Dual purpose: it tells us when to signal automatically, and when
they **should** have been open — which is not the same thing and cannot be automated.

## 11.8 Category value set `BASE`

| Main category | Subcategories |
|---------------|---------------|
| **Food** (`ETEL`) | breakfast, sandwich, starter, soup, main, side, pickle/salad, tasting, bakery, dessert, snack, **main with side**, **food package**, other |
| **Non-alcoholic, made on site** (`ALKMENTESITAL_HELYBEN`) | water, lemonade/syrup/fresh-squeezed, non-alcoholic cocktail, tea/hot chocolate/milk-based, **drink package**, coffee |
| **Non-alcoholic, not made on site** (`ALKMENTESITAL_NEM_HELYBEN`) | water, pulpy soft drink, carbonated soft drink, still soft drink, **drink package** |
| **Alcoholic** (`ALKOHOLOSITAL`) | cocktail/mixed, liqueur, spirit, beer, wine, sparkling wine, **drink package** |
| **Other** (`EGYEB`) | other, **service charge**, **tip**, delivery fee, non-hospitality, eco packaging, plastic packaging, **discount** |

**Two important consequences:**

1. **Discount, tip and service charge are STANDALONE LINE ITEMS in NTAK**, not modifiers of the total. This matches the department finding (§10.3), where service charge has its own departments.
2. **Package categories exist only within a single main category.** There is **no mixed (food + drink) package category** → a classic combo menu **must be split** (§13.4).

**The ENUM value sets may change in future**, and software must be prepared.
**NTAK categories, units of measure and VAT categories must NOT be hard-coded** —
they must come from configuration, updatable without client reinstallation.

## 11.9 Who sets the categories `MVP`

**Setting the exact NTAK main/subcategory for products and menu items is the
CUSTOMER's job.** We build the environment and the capability.

**Two things remain our responsibility:**

1. **The hard gate stays:** without an NTAK category a product cannot be saved at an NTAK-liable site. Not because we want to dictate the category, but because **a missing category means a rejected submission**, which becomes our operational problem.
2. **Menu components also get their own NTAK category** — because of the split they are standalone line items.

## 11.10 Certification `BASE`

**MTÜ Igazolás** (certificate) and a **validation test** are required before
going live, with per-site certificates and message signing. **This is an external
gate that dominates the schedule** — lead time, not development work.

**Certificate expiry monitoring is required — IN THE CLOUD, not on the site
server.** If the site server is the thing that is down, it cannot raise the alarm.
Escalating alerts at **60 / 30 / 14 / 7 / 1 days**; the last two **also reach us**,
not only the customer. Obtaining a new certificate has lead time.
**The same expiry monitor serves every other credential** (licence, invoicing API
key, cloud certificates) — one shared mechanism is cheaper than three separate ones.

---

# 12. Product catalogue

## 12.1 Category structure `MVP`

* **Maximum 4 category levels, including the main category.**
* **The main category is mandatory**, subcategories optional.
* **A VAT default may be set at any level and inherits downward** — a deeper level may override.

**Why bottom-up inheritance:** the deeper category often knows the correct rate
better. Example: *Drinks → Soft drinks → made on site / canned* — the VAT rate is
decided at the leaf, not at the root.

## 12.2 VAT on the product `BASE`

* **Two VAT fields, both mandatory:** on-premises and takeaway.
* **A "same" flag** — it **copies at the moment of saving**, it does **not reference** (principle A4).
* **If the on-premises rate is changed, the flag switches itself off** and the takeaway value stays unchanged.
* **Hard gate: no product may be saved with incomplete VAT data.**
* Default: **27%** (principle A5 — the safer direction).

**Why copy and not reference:** with a reference, lowering the on-premises rate
would **silently lower the takeaway VAT too** — a serious violation. **The two
error directions are not equal**: VAT too high is a financial disadvantage, VAT
too low is a violation.

**VAT classification is the customer's responsibility** — we provide the capability.

## 12.3 Pricing on the product `BASE`

* **The gross price is the truth.** If the price list says 1500, it is 1500; net and VAT derive from it.
* **On a VAT-rate change the GROSS stays** (1500 stays 1500). Net revenue changes, the price list does not. **The UI must state that this immediately rewrites the margin.**
* **There is NO separate takeaway gross price.** If a burger is 1500 and is taken away, the operator loses ~21 points of margin — **that is how it works in Hungary, and it is priced in.** Only the **two VAT rates** are separate.

**Derived consequence:** since gross is identical but VAT differs, **net revenue
differs per fulfilment mode** → **every margin and food-cost report must be
computed split by fulfilment mode**, never on blended gross. A report is required
showing **what the takeaway share costs the owner.**

## 12.4 Variants `MVP`

**A variant is a CHILD of the product, not a separate product.**

| Inherited | Own |
|-----------|-----|
| base name, category, VAT rates, NTAK category | **gross price**, recipe quantity, **volume/weight**, barcode |

> **The system does NOT compute prices.** A 0.5 l draught beer is 1000 HUF; the
> 0.3 l is **not 600 but whatever the customer says** (e.g. 750). Weight/volume
> pricing must **also** exist, but only where asked for. (Principle A3)

**The variant's volume/weight populates the NTAK `mennyiseg` field** (§11.5) — so
it must be structured data, not just part of the name.

**POS presentation:** separate buttons for 2–3 variants (fastest), a popup for
more — configurable.

## 12.5 Price history `BASE`

* **The document stores the price, VAT AND name AT TIME OF SALE** — not a reference to the product.
* **The product master also carries price history** (from when to when, at what price). Without it, "why did March's margin drop" is unanswerable.

## 12.6 Product lifecycle `BASE`

Three states: **active / inactive / soft-deleted**.
**None of them hides the product from HISTORY.** Physical deletion does not exist.

## 12.7 Purchase price and margin `MVP`

* **Gross entry** (as the restaurateur reads the delivery note).
* **MANDATORY purchase VAT rate.**
* **Margin and food cost are computed on NET.** Both values stored, both shown in the UI.

**Why:** purchase VAT is deductible, therefore not a cost. Gross-based margin
would be **21–27% wrong** — and margin is the system's most important business report.

## 12.8 Allergens `MVP`

**A statutory obligation** (EU 1169/2011): the venue must inform guests about the
14 EU allergens, and this is actively inspected.

> **An allergen belongs to the INGREDIENT, not to the product.** Putting 14 codes
> on the product would mean **every recipe change silently invalidates** the list
> — and a stale allergen list is more dangerous than a missing one.

| # | Rule |
|---|------|
| a | **Allergens are assigned to ingredients.** A product's allergen list is **derived from the recipe** and is **LIVE** — it updates itself when the recipe changes |
| b | **Modifiers count too** (extra cheese → milk). Derivation walks them |
| c | **Manual override is possible**, but with a **prominent marker** — needed for cross-contamination and bought-in prepared items |
| d | **An "Allergen info" button on the POS** → instant list; printable on the proforma on request |
| e | **Accuracy is the customer's responsibility** — we provide the capability |

> **This is the ONE place where principles A3/A4 do NOT apply and the inverse
> holds: here a LIVE derivation is required, not a copy.** The reason is
> principle A5 — the error directions are unequal here too, but the other way
> round: **a missed allergen warning can kill someone**, a superfluous one is
> merely inconvenient.

## 12.9 Age-restricted (18+) products `v1`

A configurable **18+ flag**, **inherited at category level, overridable per product**.

| # | Rule |
|---|------|
| a | **Warns ONCE PER ORDER**, on the first age-restricted line — **not per line.** A prompt that fires on every beer gets clicked through: **it becomes noise, not protection** |
| b | **Configurable per site, with a mode-dependent default:** ON by default in quick-sale/bar mode (the guest is at the counter), **OFF by default in table service** (the waiter already saw the guest at the table) |
| c | **Audited** — but be clear that **this does not transfer legal liability to the cashier.** A logged click is **internal employer evidence** that the process ran; nothing more |

---

# 13. Modifiers and menus

## 13.1 The core rule `BASE`

> **The default state is the RECIPE. A modifier is ALWAYS a deviation or an
> important special request → it is ALWAYS printed and ALWAYS shown on the KDS.
> No exceptions.**

Ketchup is part of the burger's recipe, not a modifier. A customer wanting a
"no ketchup" option creates a **subtractive modifier**. This avoids turning every
recipe line into an automatic modifier, and **eliminates the "default vs.
deviation" distinction from the printing logic entirely.**

**The `default` (pre-selected) flag remains, but ONLY for pre-selection** — it
speeds up mandatory-choice groups (e.g. "which side?").
**It has no effect on printing: whatever is on the line gets printed.**

## 13.2 Subtractive modifier `MVP`

* **It must reach into the parent product's recipe** — having its own recipe is not enough; it must be able to remove an ingredient from the parent's deduction.
* **It references an INGREDIENT, not a specific recipe line.** So one "No ketchup" modifier works on every product whose recipe contains ketchup; where it does not, it does nothing (warn at configuration time).
* **It writes stock back** — that is its purpose.
* **It has a separate fiscal path** from additive modifiers (§10.4).

## 13.3 Modifier group `MVP`

| Field | Meaning |
|-------|---------|
| `min` / `max` | how many **must / may** be chosen |
| `FreeLimit` | how many may be chosen **FREE** before the rest are charged |
| **Free-selection mode** | **most expensive / cheapest / FIRST-CHOSEN** — **default: FIRST-CHOSEN** |
| Per-modifier quantity | Configurable, with a maximum |

`min`/`max` and `FreeLimit` are **independent** (e.g. `min=0, max=8, FreeLimit=3`).

**The free-selection mode is set by the customer, per product if desired.** The
group provides the default; the product-group assignment may override it.

**Modifiers are selectable regardless of stock** — stock shortage does not
disable a modifier.

## 13.4 Composite menu `MVP`

**Structure:** an "is menu" flag on a product + **menu components**; each
component has `min`/`max` (default exactly 1) and a set of selectable
**products**; the system auto-pops until every component is filled.

| # | Decision |
|---|----------|
| a | **The surcharge lives on the component–product PAIRING**, not on the component ("drink: soft drink +0, fresh-squeezed +390") |
| b | **A menu component is a distinct entity**, not a modifier group — its options are **products**, with their own recipe, stock, VAT rate and NTAK category |
| c | **The menu EXPLODES into its components on the receipt.** The menu name is a header text line; the components sit under it, each on its own VAT rate |
| d | Price is split **in proportion to the components' individual list prices**, the rounding remainder going to the **largest component**. **Deterministic** |

**Why the split is mandatory — three independent reasons:**

1. **Fiscal:** a mixed-VAT menu (5% food + 27% bottled soft drink) cannot be sent as one line because it must go to two departments.
2. **NTAK:** there is no mixed package category (§11.8).
3. **Stock:** each component consumes its own recipe.

**Components receive WHOLE-FORINT unit prices** (§15.2) — so the total stays
exact at any quantity, satisfying NTAK's requirement that line totals sum to the
order total.

**Example:** menu 2490; burger list price 1990 (5%), soft drink 690 (27%).
Ratio 1990 : 690 → burger 1849, drink 641. Sum **2490**. ✔
Three menus: 5547 + 1923 = **7470** = 2490 × 3. ✔

*In principle a food-only menu could be reported as a single `ETELCSOMAG` line.
**We do not use that** — we split uniformly: one code path beats two.*

---

# 14. DRS — mandatory deposit return

## 14.1 Facts `BASE`

| Item | Content |
|------|---------|
| **Amount** | **50 HUF per unit**, uniformly, for non-reusable (single-use) packaging |
| **Scope** | **0.1–3 litre**, ready-to-drink or concentrate beverage packaging — glass, metal, plastic |
| **Exception** | **milk and milk-containing beverages** |
| **VAT** | **NOT part of the taxable base** — it is **outside the scope of VAT**. It must be shown on the receipt **separately from the product price** |
| **On return** | **The taxable base may not be reduced** by the deposit |
| **Reusable packaging** | **Different rule:** the general deposit rules of the VAT Act apply — the deposit **is** part of the taxable base |
| **Return point** | A hospitality unit is **not obliged** to operate one; joining is voluntary |

Legal basis: Government Decree 450/2023. (X. 4.); NAV tax ruling 2023-11.

## 14.2 The hospitality-specific rule

For on-premises consumption, **if the packaging stays at the venue**, the deposit
**is not charged to the guest**. For takeaway, when the bottle leaves with the
guest, it **must be charged**, as a separate line, outside the scope of VAT.

## 14.3 Our implementation `MVP`

> **Default: the deposit IS charged, regardless of fulfilment mode.** A per-site
> setting exists: *"do not charge the deposit for on-premises consumption"* — off
> by default.

**Why:** in practice **the bottle is often handed over even for on-premises
consumption and not taken back**, or the venue does not handle returns at all —
**and this is the more common case.** The exemption is an option, not an
obligation. (Principles A3 + A5)

**The state of this setting must be recorded alongside the document** — it must
be possible to see afterwards under which rule it was produced.

## 14.4 Work items

| # | Item | Tag |
|---|------|-----|
| a | Product master: **`DRS-liable packaging`** flag + **`packaging type`** (single-use / reusable) — different VAT treatment | `MVP` |
| b | The amount is a **central, versioned parameter** (currently 50 HUF), **not a code constant**; historical documents keep the historical value | `MVP` |
| c | Charging is bound to the **fulfilment mode**. On mode change it can be **added or removed on the open order**, audited | `MVP` |
| d | **A separate receipt line under the product, on its own department** | `MVP` |
| e | **The deposit is NOT revenue** — a pass-through item. It must be **excluded** from turnover reports, commission bases and the day-close turnover figure | `MVP` |
| f | Return (guest brings the bottle back): natively supported by the protocol (negative quantity), **but the venue is not obliged to be a return point** | `v1/v2` |
| g | **DRS balance** (paid on purchase vs. recovered on return) | `v2` |

`[OPEN]` **Which department the deposit goes to.** The 8 fixed slots have no DRS
slot; TAM is the only candidate, **but TAM means "subject-exempt", which is not
the same as "outside the scope of VAT"**. On the NTAK side `E_0` is the likely
target. **This belongs to actual commissioning** — preceded by vendor
consultation, since it may already be solved on their side.

## 14.5 Reusable cups `v1`

Handled as a standard product (+ value); the **return** (− value) automatically
triggers a **cash pay-out** transaction from the drawer so the drawer balance
stays accurate.

---

# 15. Money, rounding, currency

## 15.1 Gross-based arithmetic `BASE`

**If the price list says 1500, then 1500 is the truth**; net and VAT derive from it.

> **Back-calculation happens PER VAT-RATE GROUP, AT DOCUMENT LEVEL, not per
> line** — because that is how the fiscal device computes, and per-line rounding
> guarantees a 1–2 HUF discrepancy between our totals and the device's receipt.

## 15.2 Money representation `BASE`

| Type | Use | Storage |
|------|-----|---------|
| **Price / amount** | sale price, line total, grand total, payment | **whole forints (int64)** |
| **Unit cost** | purchase unit price, moving average, recipe ingredient | **high-precision decimal (6 dp)** |

**Floating point anywhere near money is FORBIDDEN.**

> **Whole forints everywhere.** The fiscal device cannot handle fractional
> forints; NTAK can be aligned to it as long as the totals match — **therefore
> whole forints govern, uniformly.**
>
> It is also technically better: **an integer unit price multiplies exactly by
> quantity.** With a fractional unit price and integer line totals, three menus
> would round per line and the three lines might not sum to 3× the menu price —
> violating NTAK's own requirement.

High-precision unit cost is required because **one gram of flour genuinely costs
a fractional forint**; rounded to whole forints, a 200-portion recipe's cost
drifts by orders of magnitude.

## 15.3 Rounding `BASE`

* **Cash payments only, to 5 HUF.**
* **In mixed payment it applies to the CASH PORTION**, not the grand total. From 1234 HUF: 1000 by card + 234 cash → the cash portion becomes **235**.
* **We compute it, send it, and compare the device's response.** On mismatch the document **must not close silently** — it is an error requiring operator intervention (principle A2).

## 15.4 Foreign currency (EUR) `MVP`

* **Rate entered before day open, valid until overwritten.**
* **The fiscal device's own FX rate setting must also be written and read back** — otherwise the receipt shows a different rate than the system.
* **The document stores the rate used.**
* **If no rate is entered at day open:** carry the previous one forward with a **prominent warning**; **do not block.** (At 06:00 nobody will hunt for an exchange rate; blocking would just make them disable currency acceptance.)
* **Change is given in HUF.**
* **Cash only.** Card FX is the terminal's business.

---

# 16. Payment, discount, service charge, tip

## 16.1 Payment safety — state machine `BASE`

* **Two-phase commit for card payments.**
* **On terminal timeout, UI confirmation** (Yes / Cancel) — never an automatic assumption.
* **On amount change**, cancel + resend.
* **On storno**, automatic refund command.
* **On printer failure, a pending transaction** — never silent swallowing.
* **Internet warning BEFORE card payment:** the existing internet indicator (§6.5)
  is wired into the payment flow so staff learn before starting the payment, not
  after a 45-second timeout. **The wording states a fact and prescribes no
  solution:** *"No external internet connection. The card terminal will probably
  not work."* — **offering a workaround is forbidden** (principle A8, §19.5).

## 16.2 Who prints `BASE`

**THE CLIENT prints**, because it holds the fiscal device and the printer.
**Exception: thin clients** — the server prints for them.

**"Pre-registering print intent on the server" is REJECTED**, for two reasons:
the server must not sit in the critical path of every print (a stuttering server
would delay every receipt), and **without a server, emergency mode would not work
either**.

**Accepted risk:** if the client prints and then dies before reporting, the
fiscal device holds a closed fiscal document the system does not know about.
**Resolution: through support, from the fiscal device's own journal.**

**Mitigation that does not violate the decision:** the client records the print
intent **LOCALLY** (into the same local outbox that degraded mode already uses)
before calling the device. **Cost: one local disk write, zero network, zero
server dependency.** After a power cut or crash — the typical case — the evidence
is there; a physically destroyed machine needs support anyway.

## 16.3 Payment methods `MVP`

* Cash (with rounding), card (integrated or manual), voucher, foreign currency.
* **Mixed payment** supported.
* **Optional receipt printing** on a thermal printer where not mandatory.
* **QR customer code** for the digital document.

## 16.4 Discount `MVP`

* **Whole-bill discount distributed across lines in proportion to VAT rate** — so no amount lands on the wrong department.
* Discounts on a line, a table, or the grand total.
* **Discounts above a threshold require a reason** and are audited (§18.4).
* **In NTAK a discount is a standalone line item** (`EGYEB / KEDVEZMENY`).

## 16.5 Service charge `MVP`

* **Must be computed split by VAT rate**, because the fiscal department allocation gives it **its own per-rate slots** (§10.3).
* **Must not be folded into product lines.**
* **In NTAK it is also a standalone line item** (`EGYEB / SZERVIZDIJ`).
* **Typo protection:** a **soft confirmation above a configurable threshold**
  ("Are you sure, 25%? That is unusually high."), default threshold 15%; a
  **hard cap only at absurd values** (above 100%), which is certainly a slip.
  **No hard 15% ceiling** — there is no statutory maximum, and it would violate
  principle A3 (an event venue's contractual service charge may be higher).
* **A genuine legal requirement:** the service charge rate **must be disclosed in
  advance**. The system must support the text shown on the price list / menu.

## 16.6 Tip `MVP`

* **Cash tips:** withdrawn at shift end.
* **Card tips:** reported separately for accounting; **they do not alter the physical drawer**.
* **The NTAK day close carries an `osszesBorravalo` field** → tips must be aggregated per day.
* **In NTAK a standalone line item** (`EGYEB / BORRAVALO`).
* **Per-user tip report** in the cloud admin UI, for month-end payroll. `MVP`
* **Why it must not come from the drawer:** if card tips are paid out in cash at
  shift end, **the physical drawer falls short** of the expected closing balance.
  **The rule: never an untracked drawer withdrawal.** If the customer does pay it
  out in cash, that is a **separate, documented cash movement**, not a silent
  drawer reduction.
* `[UNVERIFIED]` **The taxation of tips** (tip vs. service charge, cash vs. card)
  is non-trivial — a question for the accountant. The design consequence (the
  per-user report) is the same under either outcome.

## 16.7 Invoicing and the receipt/invoice interlock `BASE`

VAT invoice via Számlázz.hu / Billingo API, **or** a "simplified invoice" on the
fiscal printer.

> **Mutual exclusion — mandatory.** If the guest receives a VAT invoice AND the
> transaction is also closed on the fiscal device, the same sale is reported
> **twice to the authority** — once through the cash register's reporting, once
> through the Online Invoice system. Revenue appears inflated, and the taxpayer
> has to explain the discrepancy.

**Two distinct paths are required, not one prohibition:**

| Path | When | Flow |
|------|------|------|
| **A) Invoice from the start** | The guest asks BEFORE payment | The basket switches to **invoice mode** → **nothing is sent to the fiscal device**; anything printed carries **"NEM ADÓÜGYI BIZONYLAT"** |
| **B) Invoice requested afterwards** | The receipt is already printed | **The receipt must be STORNOED first**, and only then may the invoice be issued |

**Path B is the more common one** — the guest asks after seeing the receipt.

| # | Constraint |
|---|-----------|
| a | **Software interlock:** in invoice mode, calling the fiscal adapter is **structurally impossible**, not merely disabled |
| b | The document **records which path produced it** |
| c | **Both paths report identically to NTAK** — NTAK depends on turnover, not on document type |

## 16.8 Vouchers `v1`

**Two kinds of voucher exist, with opposite tax treatment** (VAT Act,
implementing the EU voucher directive):

| Type | What it is | VAT AT SALE | VAT AT REDEMPTION |
|------|-----------|-------------|-------------------|
| **Single-purpose** | The applicable rate and place of supply are **known at sale** (e.g. "one pizza") | **Taxable** | none |
| **Multi-purpose** | Redeemable for anything, mixed rates (classic gift voucher) | **Outside the scope of VAT** | **The tax point arises here** |

**A single "Voucher" product type is NOT enough** — the product master needs a
**`voucher` flag + `voucher type`**.

| # | Item |
|---|------|
| a | **Selling a multi-purpose voucher is outside VAT scope** → **the same department problem as DRS** (§10.3): there is no free slot. **This question is merged with the DRS question** to the vendor/NAV |
| b | **Redemption is a PAYMENT METHOD, not a product.** Redeemed lines are taxed and reported normally |
| c | `[UNVERIFIED]` The NTAK classification for the SALE of a multi-purpose voucher — likely `EGYEB / NEM_VENDEGLATAS`, but must be confirmed |
| d | **Outstanding voucher register** (issued / redeemed / expired) — a balance-sheet liability. `v2` |

## 16.9 Split bill `MVP`

**Two split modes exist:**

| Mode | What it does | Difficulty |
|------|-------------|------------|
| **Equal split (n ways)** | Divides the whole bill into n parts | **Rounding** + proportional allocation of VAT and service charge |
| **Item split (who ate what)** | Each guest pays their own lines | A **shared line** (one bottle of wine for four) must be sub-split |

| # | Rule |
|---|------|
| a | **Deterministic remainder distribution:** 10 000 / 3 → 3 333 + 3 333 + **3 334**. The same split always yields the same numbers |
| b | **Splitting happens PER VAT RATE, not on the grand total.** In a mixed basket each part must receive a proportional VAT structure — otherwise wrong amounts land on the departments |
| c | **Service charge is allocated the same way**, per VAT rate (§16.5) |
| d | **Each part is its OWN document with its own SIDURI number** — the daily-sequence scheme handles this (§8.1) |
| e | `[UNVERIFIED]` In NTAK, is a split bill **one** order summary with several payment methods, or **several** order summaries? Per-document splitting is more likely |

---

# 17. Stock, recipes, purchasing

## 17.1 Warehouses `MVP`

* **Unlimited warehouses** (main, bar, …), **inter-warehouse movements documented**.
* **Recipes (BOM)** with ingredients and quantities.

## 17.2 Goods receipt and moving average `MVP`

* Purchase unit price → **moving average price** maintenance.
* **Gross entry + mandatory purchase VAT rate; margin on net** (§12.7).
* **Margin calculation split by fulfilment mode** (§12.3).

## 17.3 Staff consumption and waste `MVP`

**Recorded strictly as INVENTORY MOVEMENTS, never as sales** — clean accounting.

`[UNVERIFIED]` That these are genuinely outside NTAK reporting. NTAK has an
`EGYEB / NEM_VENDEGLATAS` line category, but the order classification value set
is only `NORMAL / SZTORNO / HELYESBITO`. If they turn out to be reportable, the
24-hour order limit (§11.4) applies to them too.

## 17.4 Stocktake `MVP`

* **The ONLY legitimate stock "overwrite"** — but recorded as a **correction movement** so the discrepancy stays visible. Stock counts are never overwritten without a trace.
* **Settled to the cut-off date**, not to the entry timestamp.
* **Configurable "calculated waste %"** (e.g. 2% draught loss) to tolerate shortfall.
* **A stocktake overwrite requires a reason** and is audited.
* PDA module with barcode scanning; **printable count sheets** generated on the web and entered afterwards.

## 17.5 Modifiers and stock `MVP`

* **Modifiers are selectable regardless of stock.**
* **Subtractive modifiers write stock back** (§13.2).

## 17.6 Stock must NEVER block a sale `BASE`

> **Stock level must NEVER block POS selling.** If a goods receipt was missed and
> software stock shows zero, the guest must still receive the physically present
> product.

| # | Rule |
|---|------|
| a | **Negative stock is invisible to the cashier** — stock is not their concern. The cloud admin shows it to management with an **unambiguous red indicator** |
| b | **A later goods receipt fills the negative automatically** |
| c | **"Negative stock" and "sold out" are TWO DIFFERENT things.** Negative stock is a data error → invisible to the cashier. **"Sold out" is a manual flag** set by staff, and it **does grey out the button** — that is genuine information for the guest |
| d | ⚠️ **Numerical trap: moving average on negative stock.** If stock is −5 and 10 are received at a new price, the moving-average calculation **produces nonsense on a negative base**, and every margin figure afterwards is wrong. The negative base must be **handled explicitly** (the negative portion at the last known cost), and it must be **flagged** that the item's average derives from a correction |

---

# 18. Permissions and audit

## 18.1 Permission levels `MVP`

* **The customer can create and modify permission LEVELS** (e.g. "Head Bartender"), not just per-user exceptions.
* **A NEW permission arriving with an update is DENIED by default on existing levels**, but with a **prominent notification** so they can decide (principles A2 + A5).
* Per-table permission handling.

## 18.2 The Siduri admin account `BASE`

**Inviolable:**

* The customer **cannot modify it**, **cannot reduce its rights**, **cannot change its password**.
* **A fixed offline login is required** — even if the password was changed before an update.
* Proposal: **per-site credential**, with **visible audit**.

## 18.3 Login `MVP`

* Full-screen kiosk mode with an immediate login screen.
* Users listed with **avatars and names**; a **PIN-only** password field.
* **Hardware login:** RFID / NFC card reader.

## 18.4 Audit log `BASE`

### Principles

* **Append-only** — no `UPDATE`, no `DELETE`, **enforced at database level**.
* **Hash chain** on the security stream: each record contains the previous record's hash → later rewriting or excision is **mathematically detectable**.
* **Cloud anchoring:** the chain's current hash is periodically pushed to the cloud. Without it, the chain does not protect against restoring **the whole database** to an earlier state.
* **Not even the Siduri admin may delete.** Purge by age only, into the cloud archive.

### Record content

**Who** (user + device + their role AT THAT TIME) · **when** (device clock +
server clock + monotonic sequence) · **what** · **where** · **before / after** ·
and where mandatory: **why** (reason code + free text).

* **An audit record references the user EXCLUSIVELY by an internal UUID, never by
  a plain-text name.** Three reasons, two of which are not privacy-related:
  correct normalisation; **the hash chain survives a name change** (otherwise a
  name change would leave us with either a stale name or the need to rewrite an
  immutable record — **breaking the chain**); and it keeps a
  **pseudonymisation lever** for the rare case that demands one (swap the
  **display layer**, chain untouched).
  **The role, however, stays a SNAPSHOT** (the role at that time), because the
  current role would lie. So: **identity = UUID (reference), role = snapshot (copy).**

### TWO separate streams

| | **(A) Security / accounting** | **(B) Operational** |
|---|---|---|
| **Content** | storno, discount, price override, permissions, settings, day/shift open and close, failover, stocktake overwrite, clock change, no-sale drawer open, integration enable/disable, risk acceptance | line entry, table moves, order state — **the source of table history and user history** |
| **Hash chain** | **yes** | no |
| **Retention** | **8 years** (cloud) | **1 year** (cloud) |
| **Local retention** | **30 days** | **30 days** |
| **Order of magnitude / site / day** | ~150–300 records | ~3000–5000 records |
| **Annual size / site** | tens of MB | ~0.5 GB |

> **Storage is not consumed by security events but by the table-history view** —
> which is the value delivered to the customer, so it is worth it. The hash chain
> is justified only on stream (A): on 5000 rows/day it is waste and slows writes;
> on 200 rows/day it is free. `[MEASURE]` `MERESEK.md` M18.

### Events requiring a reason

Document storno · deleting a line already sent to the kitchen · discount above
threshold · manual price override · stocktake overwrite · no-sale drawer open ·
"unpaid" close · **temporary integration disable**.

### Access

* **Only WE see the raw audit.** The customer never gets a raw database-row view; requested data is sent to them.
* **The customer gets curated, visual views**, placed contextually:
  * **table history** — click a table, see that business day's events;
  * **user history** — *"logged in, added 1 gyros to table 3, logged out"*.
  * Attractive, easily readable presentation, not a dry list.
* **Technical consequence:** the log must be **efficiently queryable per entity** (table, user, order) → **indexing requirement**. An **event → human sentence** template set is needed, **in all three languages**.
* **READS are NOT logged.** Instead, **permission settings** govern who may see what. **Consequence: logging permission changes becomes more important** — it is the only trace of who could access what.

### Employment-law warning

**We warn only; we do NOT supply a template.** This is the employer's obligation,
and an outdated template would be blamed on us.

**The warning must appear where the feature is used** (when opening user
history), **not only once at installation** — because that view is **employee
monitoring**, however attractively presented.

### When the log cannot be written

**Lenient variant:** write into a pre-allocated local emergency buffer, raise a
prominent alarm, and merge as soon as possible. Only when the emergency buffer is
also full does operation stop.

---

# 19. Integrations

## 19.1 Two integration classes `BASE`

> **The dividing line is not which integration it is, but whether it carries
> LEGAL or FINANCIAL consequence.**

| | **A) Protected integrations** | **B) Customer devices** |
|---|---|---|
| **Which** | fiscal device, card terminal, NTAK | printers, KDS, order board |
| **Consequence** | legal / financial | purely operational |
| **Enabling** | **Siduri only** | **the site manager** |
| **Disabling** | delegated right, **1-hour expiry** | **freely, no expiry** |
| **Configuration** (address, assignment, relocation) | Siduri | **the site manager** |
| **Escalation, cloud notification** | yes | no |
| **Audit** | security stream | operational stream |

**Why class (B) does not get the machinery:** a kitchen printer left disabled
**surfaces within two minutes** — the chef says the ticket is not coming. A
**self-revealing fault.** A fiscal device left disabled can go **unnoticed for
days**, while money keeps flowing.

## 19.2 Temporary disable — what it solves `MVP`

An integrated peripheral failing today **paralyses the whole sales flow**, even
though a manual fallback exists:

* No internet on the machine → card payment cannot reach the terminal, **but a standalone terminal is available.**
* Cable break / broken fiscal printer → **every receipt aborts**, even though a standalone cash register could be used.

**Scope: per machine** (following the integration's natural scope). If one till's
terminal is dead, the others work unaffected.

## 19.3 What disabling means per integration

| Integration | Meaning | What is lost |
|-------------|---------|--------------|
| **Card terminal** | The "Card" payment method **switches to manual** | **Terminal authorisation data** (approval code, masked PAN, terminal ID). Day-close reconciliation **becomes manual**. The document must be marked **"manual card payment"** |
| **Fiscal device** | **The legal document is issued by a device we do not control.** The fiscal number field stays empty; whatever we print is marked **"NEM ADÓÜGYI BIZONYLAT"** | **Double entry** — staff must key into both systems; we cannot verify that the amounts match |
| **Non-fiscal printer / KDS** | Redirect or skip | The kitchen ticket |
| **NTAK** | **NEVER disableable** | — |
| **Audit log** | **NEVER disableable** | — |

**NTAK is exempt because it has no manual fallback** — reporting queues and
tolerates offline time. Disabling it would not be a workaround; it would simply
be non-reporting.

## 19.4 Disable rules `MVP`

**The failure mode of this feature is that every "temporary" bypass becomes
permanent (A7).** Therefore:

| # | Rule |
|---|------|
| a | **Mandatory expiry: 1 hour.** Never "until someone turns it back on" |
| b | **Mandatory reason** (code + free text), in the **security** audit stream |
| c | **A persistent, non-dismissible banner** on the affected machine while active. Not an icon, not a dismissible toast |
| d | **The banner must state the ACTION, not just the state:** *"Fiscal integration temporarily disabled — issue the receipt on the standalone cash register."* |
| e | **The banner shows since when it has been off and when it expires** |
| f | **The manager and cloud overviews** show every disabled integration across all sites and machines in one place |
| g | **Mandatory acknowledgement at day close** if any **protected** integration was disabled. **Aggregated** — one entry per device and integration with cycle count and total time, not one entry per cycle |

**Escalation ladder:**

| Level | Who | Duration | What happens |
|-------|-----|----------|--------------|
| **1. Temporary** | site manager (if Siduri delegated) | **1 hour**, repeatable | reason, audit, persistent banner |
| **2. Repetition** | — | **after 3 repeats** | **automatic notification to us** — this is now a real fault |
| **3. Persistent** | **Siduri only** | no expiry | documented; for fiscal, tied to the **risk acceptance form** |

**At expiry we TEST FIRST, and only then re-enable:**

1. **Run the self-test** — after in-flight transactions complete, **never during one**.
2. **Success** → **re-enable silently**, banner clears.
3. **Failure** → the integration **returns to enabled state**, **but the banner immediately switches to "DECISION REQUIRED"**, and the manager is notified.

**Why the test is required:** blind re-enabling means **once per hour somebody
eats a failed payment or an aborted receipt** — six times in an evening shift.
The friction (having to disable again) is preserved, but the cashier does not pay
for it.

**State and expiry are stored server-side, per device** — a POS restart must not
silently re-enable onto a broken device, nor silently extend the disable.

## 19.5 Never offer the disable `BASE`

> **Offering the bypass teaches the bypass** (principle A8).

* **A dedicated button in settings.** No pop-up offer, ever.
* **The error message guides but offers no lever:** *"The card terminal is unreachable. Notify the site manager."*
* **Repeated failures must reach the AUTHORISED PERSON, not the counter** — on the manager and cloud alerting surfaces, never as a pop-up on the till.

**Stricter rules for the fiscal integration**, because **disabling it is exactly
the lever for running a shift without issuing receipts**:

| # | Rule |
|---|------|
| a | The disable right is **NOT delegable by default** — we enable it explicitly, per site |
| b | **Immediate cloud notification**, not at day close |
| c | **A dedicated report:** how much turnover occurred while it was disabled |
| d | Delegation is **tied to the risk acceptance form** |

*The situation itself is lawful — a receipt issued on a standalone cash register
is a valid receipt. The risk is not legal; it is abuse.*

## 19.6 Print redirection to another machine's fiscal device `v1`

**Feasible**, because communication with the fiscal device is **IP:port based**.
**Only a Siduri system administrator may configure it**, as it is a source of
problems.

| # | Constraint |
|---|-----------|
| a | **HARD-limited to within the site, enforced server-side** — not left to admin discipline. Printing on another site's device would mean **a different NTAK registration number and possibly a different taxpayer**: a serious violation |
| b | **The document must store WHICH fiscal device printed it** (§8.3) |
| c | **Configuring the redirect and every redirected print are audited** |
| d | **The user must see** that printing happens elsewhere — otherwise they wait at the wrong counter |

## 19.7 Integration and feature registry `BASE`

For every integration, record: **name · CLASS (A or B) · enableable at this site ·
temporarily disableable · by whom · fallback behaviour · what is lost · maximum
duration · scope (per machine or per site).**

**This is not a configuration detail but a product-capability catalogue** — and
the same registry drives **paid tiers and licence levels** (§2.1).

## 19.8 Hardware and peripherals `MVP`

* NAV-approved fiscal cash registers via vendor software.
* Conventional card terminals (alongside SoftPOS) — **same principle: integrate, never write our own.**
* Broad **thermal printer (ESC/POS)** support.
* Barcode scanner, RFID/NFC reader, scale.

## 19.9 External API `v2`

* **Foodora / Wolt** native KDS and POS integration.
* **CRM and loyalty API.**
* Public REST API.

---

# 20. Printing and routing

* **Print routing:** which product type goes to which printer or KDS.
* **After proforma printing, "awaiting payment" status**; adding a new line reverts it automatically.
* **Whatever appears as a modifier on the line is ALWAYS printed and ALWAYS sent to the KDS** (§13.1).
* **Unpriced modifiers are text lines under the product**, not line items.
* **A menu appears as a header text line with its components beneath** (§13.4).
* **The fiscal receipt is in Hungarian** — a statutory constraint (§25).

---

# 21. Clients

## 21.1 POS (thick client) `MVP`

* Full-screen kiosk mode, immediate login (§18.3).
* **Table map view:** visual editor — drawable background, table placement, shapes, customisation.
* **Assignable to a table:** dedicated waiter, regular-guest profile, table-level discount.
* **Order taking:** to a table or a specific guest; default guest count offered automatically.
* **Right-hand panel views:** entry order / per guest / per course (with a merged view).
* **Sales view:** quick sale and table view.
* **Single-machine mode without table management** — the free entry tier (§2.1).
* **Concurrency protection:** optimistic locking with version numbers on table edits.
* **Reconnection:** exponential backoff, **with a shutoff limit**.

## 21.2 Thin client (PDA) `MVP`

* Order taking and management.
* **In v1 it does NOT take payment and does NOT issue receipts.**
* **The payment capability IS BUILT, but disabled.** **Not a compile-time flag** but a **server-side permission not exposed in the admin UI**, which the client queries on every payment attempt — so it cannot be unlocked by editing a local file, and **enabling it is auditable**.
* **Automatic shutdown on server failure** — protection against double entry.
* **Minimal archive:** only what it sent, with **shorter retention** — for data protection, since phones are the most frequently lost device.
* **The device-number space is SHARED** with all device types (§8.2).

## 21.3 KDS `MVP`

Touch-screen (Android / Windows) display with **drag-and-drop status changes**,
which **trigger the order ready board**.
**Every modifier is displayed** (§13.1).

## 21.4 Order Ready Board `v1`

Separate, **brandable** application (Smart TV / Android), **WebSocket**
communication: "Preparing" / "Ready".

## 21.5 Customer Facing Display `v1`

Order and tip surface; **idle video/image playback** with automatic conversion
(720p / 1024×768).
`[MEASURE]` Non-trivial on a Bay Trail iGPU (`MERESEK.md` M3).

## 21.6 Kiosk `v2`

Self-service ordering and payment terminal.

## 21.7 Inventory app `v1`

PDA module with barcode scanning; **printable count sheets** generated on the web
and entered afterwards.

## 21.8 QR table ordering `v2`

Guest-side ordering **directly against the local server**.

---

# 22. Cloud

## 22.1 Role of the cloud `BASE`

**A full management platform, not an add-on.** This is the largest scope change
in the project and **a product track of its own in the phase plan.**

| # | Area |
|---|------|
| a | **Setting parity with the POS** — the cloud must know EVERY POS setting |
| b | **Warehouse, ingredient movements, recipes** — identical to the site admin |
| c | **Reports, charts, analytics** |
| d | **Stocktake** — a dedicated function that may overwrite stock (as a correction movement, §17.4) |
| e | **Lockable settings** (price, visibility) — the chain/franchise centre can lock values |
| f | **Chain / franchise level central values**, with inheritance |
| g | **Feedback on whether a change actually reached the machines** |
| h | **Device visibility** — which machine is alive, when it last reported |
| i | **Bidirectional, specially protected synchronisation** |

## 22.2 One admin UI, served from two places `BASE`

> **There is ONE web admin application, served from TWO places:** from the cloud,
> and — when offline — **from the site's own server**.

**This eliminates silent divergence at the root** — two separate admin surfaces
would eventually know different things, and nobody would notice.

**The cloud warehouse/recipe module is the same as the site one.**

`[MEASURE]` The site server also serving a web admin — measure the load on J1900
(`MERESEK.md` M14).

**Offline limitation:** site-served admin **cannot show data older than 30 days**
(local retention, §24.2). The UI must state this rather than silently returning
an empty result.

## 22.3 Multi-site `BASE`

**A base model, not a franchise feature.** Every report must work for:

* one site,
* several selected sites,
* the whole group.

Non-franchise owners may also have multiple sites.

## 22.4 Cloud availability `MVP`

* **Two physical servers**, primary + secondary, with **automatic rerouting** and load sharing.
* **The site's "manual switchover" rationale does NOT transfer:** on site it is manual because we do not own the infrastructure and cannot know the network's state. **In the cloud we own it** — automation is justified there.
* **Active-passive write, active-active read.**

## 22.5 The cloud as archive `BASE`

**The cloud is the legal archive** (8 years). The local purge (30 days) is only
permissible because the cloud retains. **It follows that a "purely local"
topology is not sufficient on its own** at an NTAK-liable site.

## 22.6 The cloud as NTAK sender during closure `MVP`

See §11.7/e.

---

# 23. Licensing (DRM)

* **Cloud-managed, hardware-fingerprint based** licensing.
* **Heartbeat: 10-day offline grace period.**
* **The licence grace period and the client archive retention are DELIBERATELY not the same value** — two different things that must not be coupled.
* **Two fingerprints on one identifier → both blocked** until a human resolves it (§8.2).
* **Licence levels / paid tiers:** described by the integration and feature registry (§19.7).

> **The former rule "NTAK SLA warning after 18 hours offline, because of the
> 24-hour limit" is INVALID** — reporting is every 15 minutes (§11.2). The warning
> logic must be rewritten: bind it not to a 24-hour limit but to **the number and
> age of accumulated unsent 15-minute batches**.

---

# 24. Security, data protection, operations

## 24.1 Physical risk `BASE`

**The server is typically a working cash register** — the whole database sits on
the counter, not in a locked server room.

**Software cannot fully defend against physical theft; this must be stated.**
What can be done:

| # | Countermeasure |
|---|----------------|
| a | **Data minimisation** — a design rule: do not store what is not needed |
| b | **Disk encryption where TPM exists.** `[OPEN]` Whether the installed base has TPM — **prepare for both branches**; encryption is a configuration capability, and the admin UI states which branch is active |
| c | **Physical anchoring** — an installation item |
| d | **The cloud backup is the ONLY recovery path after theft** |

## 24.2 Client-side archive `MVP`

* **20 BUSY business days** of retention — **not 20 calendar days.** A day spent closed neither counts nor ages anything out.
* **Retention NEVER deletes unacknowledged data.**
* **Shorter on thin clients** (§21.2).
* **A client may request its own history back from the server** → after a machine swap the new machine repopulates itself. Three conditions: the restored archive **may be incomplete** (must be flagged), it travels over an **authenticated, audited data-release channel**, and **machine replacement is an explicit, authorised operation.**
* `[MEASURE]` Write load on cheap storage and actual size (`MERESEK.md` M8, M9).

## 24.3 Network `BASE`

* **Separating guest WiFi from the operational network is a MANDATORY INSTALLATION PRECONDITION** (§10.6).
* **Client↔server communication must be encrypted and authenticated** — the original spec did not address this at all.
* Firewall rules on the fiscal service port.

## 24.4 Risk acceptance form `MVP`

An in-application form with **touch-screen signature**, saved **AND forwarded to
the primary cloud server**, retrievable, timestamped, protected.

**Four conditions:**

| # | Condition |
|---|-----------|
| a | **The TEXT VERSION must also be stored**, not just the fact of signing |
| b | **TWO timestamps**, and **the cloud's is authoritative** — the local clock belongs to the customer's machine |
| c | **An offline path is required**, because fresh installations often have no internet — and until the cloud confirms, that must be displayed |
| d | **A configuration change requires a NEW form**, otherwise we hold a signature for a setup that no longer exists |
| e | **Cryptographic sealing:** the **full text + date + the CONFIGURATION STATE** concatenated, with a **SHA-256 digest**, sent to the cloud together with the signature. This proves not only which text was signed but that **exactly that bundle was not altered afterwards**, and it **cryptographically binds the signature to the specific configuration** that was declined. ⚠️ **Honest limitation: a touch-screen signature plus SHA-256 is NOT a qualified electronic signature.** It is evidence, not eIDAS compliance — and must not be presented as such |

**When required:** when the customer knowingly declines the backup server, the
second fiscal device, or network separation; and for delegating the temporary
disable of the fiscal integration.

## 24.5 Updates `MVP`

* Standalone offline patcher (`siduri-updater`) working around Windows file locks.
* **Update ORDER is a hard requirement:** role-carrying machines (main and backup server) must not update simultaneously.
* **New permissions arriving with an update are denied by default, with a prominent notification** (§18.1).

## 24.6 Windows Update on a role-carrying machine `BASE`

> **We built the entire HA system against server HARDWARE FAILURE. Meanwhile the
> far more likely event is Windows Update rebooting the cash register acting as
> the server at 20:00 on a Saturday — and that is entirely preventable.**

Worse: our failover is **manual** (a human presses the button after 5 minutes).
So a Windows reboot causes **5+ minutes of reduced operation and a human
decision**, at peak, for no reason at all.

| # | Item |
|---|------|
| a | **Installation must disable automatic restarts** — achievable on Windows 10 IoT Enterprise LTSC via policy/settings (deferral + active hours + no auto-restart) |
| b | **A MANDATORY INSTALLATION CHECKLIST ITEM**, in the same class as guest WiFi separation (§10.6) |
| c | **The updater VERIFIES the setting**, and if someone reverted it, **reports — to the cloud as well** |
| d | The hard requirement on update ordering (§5.2) **extends to the operating system**, not only our software |

## 24.7 Erasure of guest data (GDPR) `v1`

| # | Rule |
|---|------|
| a | **One-click anonymisation** of the regular-guest profile. Statistics stay intact (consumption data is bound to the profile identifier, not the name) |
| b | **Renaming is not enough.** It must cover **phone number, email, address, loyalty card number**, and — the riskiest — **free-text notes.** That is where staff write "the guy with the red car", which re-identifies on its own |
| c | **It must NOT touch DOCUMENTS.** An invoice carries name and address and is **retained for 8 years by law** — **the right to erasure does not override a statutory retention obligation.** Erasure applies to the **CRM profile**, not to accounting documents |

---

# 25. Languages and localisation

**Hungarian + English + German are MANDATORY**; neighbouring languages (Slovak,
Romanian, Serbian, Croatian) later.

> **Two separate tasks that must not be conflated:**

| | **(1) Software strings** | **(2) Content** |
|---|---|---|
| What | button labels, error messages, report headers | product names, category names, modifier names, allergen text |
| Whose | **ours** | **the CUSTOMER's data**, per site, again and again |
| How | **complete**, all three languages | **optional per field, with HUNGARIAN fallback** |

**Content translation must never be forced** — otherwise they will not populate
the product master at all.

**The fiscal receipt is in HUNGARIAN** — a statutory constraint. Multilingual
output lives on the non-fiscal copy, the QR guest page, the e-receipt display and
the customer displays.

> **The POS UI must be tested with GERMAN strings, not Hungarian.** German is on
> average 25–35% longer and English shorter — on the low-resolution touchscreens
> of J1900 machines, German wraps. **An acceptance criterion in the UI/UX pass.**

With (1) and (2) properly structured, a new language is **translation cost only**,
not development cost.

---

# 26. Reporting and analytics

* **Dynamic charts in the cloud.**
* **True margin:** on the purchase **moving average**, **net-based** (§12.7), **split by fulfilment mode** (§12.3).
* **Dynamic "calculated waste %" slider** for modelling true profit.
* **Cost of the takeaway share** — what takeaway costs the owner (§12.3).
* **DRS EXCLUDED from turnover figures** — a pass-through item, not revenue (§14.4/e).
* **Turnover generated while an integration was disabled** — a dedicated report (§19.5/c).
* **Table history and user history** — curated visual views from the operational audit stream (§18.4).
* Franchise/chain level: one site, several selected, whole group (§22.3).

---

# 27. MVP and scheduling

## 27.1 MVP core

Offline-first site operation · server-authoritative model · **full degraded
mode** · **HA with a backup server** · two-layer document numbering · fiscal
integration (mode 2) · **full NTAK reporting** · product catalogue with modifiers
and menus · stock and recipes · permissions and audit log · base cloud (licence,
archive, admin).

## 27.2 What the schedule cannot compress `BASE`

**Team size is not the constraint. External gates are:**

| Gate | What it blocks |
|------|----------------|
| **MTÜ certificate + NTAK validation test** | Going live |
| **Vendor contact + physical test device** | Finalising the fiscal layer |
| **Physical J1900 reference machines** (2, plus the full reference installation) | Measurements M1–M9, M12–M14 |

**These are lead times, not development tasks.** The phase plan must be built
around them, not the other way round.

## 27.3 First item of week one

**Where the API contract lives** (`B8`) — how it is versioned, who owns it. Not
optional even for a small team.

---

# 28. Open questions and unverified premises

## 28.1 Unverified premises — nothing may be built on these without a source

| # | The unverified claim | What collapses if false |
|---|----------------------|-------------------------|
| **P1** | On an AEE device the fiscal device itself issues and numbers the legal receipt → server outage does not block receipt issuance | **The entire degraded mode** (§6.2) |
| **P2** | "An entirely new negative fiscal receipt" for storno | The whole storno flow (§10.5) |
| **P3** | The e-receipt direction can be ignored for now | The shape of the document model |
| **P4** | Staff consumption and waste are outside NTAK reporting | The 24-hour order limit would apply to them (§11.4) |

*(The former "24-hour NTAK limit" premise is VERIFIED FALSE — it is 15 minutes,
§11.2. The "accounting retention period" premise is resolved: 8 years, with the
cloud archive.)*

## 28.2 Open questions — external parties

| # | Question | To whom |
|---|----------|---------|
| **K1** | Does the firmware accept a **zero-amount line item**? (working assumption: no) | vendor |
| **K2** | **Which department may carry the DRS deposit?** Can the **AJT** slot be reallocated? | vendor / NAV |
| **K3** | Does the vendor service have **any authentication, IP restriction, or listen-address** setting? | vendor |
| **K4** | Does NTAK accept an **order summary AFTER the day close** for the same tárgynap? (daily occurrence at 24/7 sites) | NTAK / MTÜ |
| **K5** | **Are staff consumption and waste NTAK-reportable?** | NTAK / MTÜ |
| **K6** | Does NTAK accept a **backdated close timestamp** (last recorded activity) when the server was dead for more than 24 hours? | NTAK / MTÜ |

## 28.3 Open questions — internal

| # | Question |
|---|----------|
| **B1** | Does the installed base have TPM (§24.1/b) — prepare for both |
| **B2** | Concrete implementation of the "message queue" |
| **B3** | Multi-tenancy model in the cloud |
| **B4** | SoftPOS is a PSP decision, not a development decision |

---

# 29. Measurement obligations

**At the first live test, MEASURE EVERYTHING.** Full list: `MERESEK.md`.

| # | Measurement | Why critical |
|---|-------------|--------------|
| **M1** | Combined server + cash register on ONE J1900 | The tightest case — **and the default** |
| **M4** | Synchronous vs. asynchronous replication write latency on a J1900 pair | The "synchronous is impossible" claim is unproven |
| **M5** | Transactions lost at failover | The magnitude of orphan transactions |
| **M12** | **THE MOST CRITICAL: the backup POS takes over service** under peak load | The entire HA design rests on this |
| **M13** | Backup POS load in normal operation (replica only) | If even this destroys response time, M12 is moot |
| **M14** | Site server also serving the web admin | §22.2 |
| **M15** | **Does the device accept a zero-amount line?** | §10.4 — blocking |
| **M16** | Which department may carry DRS | §14.4 |
| **M17** | Print response time and full document cycle time | Above how many lines does it slow noticeably |
| **M18** | Actual size of both audit streams | §18.4 |

**Physical hardware required:** M1–M9 need one J1900; M4/M5/M7/M13 need **two**;
**M12 needs the FULL reference installation** (3 Windows POS + 2 tablets +
4 phones + KDS + order board).

---

# 30. Architecture and Git repositories

| # | Repository | Content |
|---|-----------|---------|
| 1 | `siduri-backend-server` | Java / Spring Boot / GraalVM — site main and backup server, PostgreSQL |
| 2 | `siduri-pos-client` | C# / WPF — POS client, fiscal and hardware integrations |
| 3 | `siduri-flutter-clients` | Flutter workspace — PDA, KDS, order board, inventory app |
| 4 | `siduri-updater` | C# — standalone offline patcher |
| 5 | `siduri-cloud-api` | Cloud: licensing, archive, web admin, NTAK backup |
| 6 | `siduri-docs` | **Documentation — code NEVER goes here** |

**The repositories always stay private** (§10.2).

---

# 31. Working method

Full detail in `MERNOKISAROKKOVEK.md`. The essentials:

| # | Rule |
|---|------|
| 1 | **One source of truth**; everything else is a pointer, and must say so |
| 2 | **Never soften.** Information withheld out of comfort does more harm than brutal reality |
| 3 | **Every decision carries its COST**, not only its benefit |
| 4 | **No opaque references** — always spell out what a thing is about |
| 5 | **Rejected alternatives are struck through, not deleted**, with their reasoning |
| 6 | **Own mistakes are corrected, not concealed** |
| 7 | **No AI attribution in any artifact** |

---

# 32. Invariant summary — the rules that must never be broken

For quick machine reference. Violating any of these is a defect, not a trade-off.

| # | Invariant |
|---|-----------|
| I1 | Floating point is never used for money |
| I2 | Whole forints for all prices and totals; high-precision decimals only for unit costs |
| I3 | VAT is back-calculated per VAT-rate group at document level, never per line |
| I4 | The two VAT fields on a product are copies, never references |
| I5 | A product cannot be saved with incomplete VAT or a missing NTAK category |
| I6 | Only five VAT categories exist: 5 / 18 / 27 / TAM(0) / AJT |
| I7 | Service charge is a separate line, split by VAT rate, never folded into products |
| I8 | A mixed-VAT menu is always exploded into components |
| I9 | Menu component unit prices are whole forints and sum exactly to the menu price |
| I10 | An unpriced modifier is a text line, never a line item |
| I11 | A subtractive modifier is never sent as a negative-price sale line |
| I12 | Every modifier on a line is printed and shown on the KDS |
| I13 | The SIDURI document number is issued from a per-device disjoint range |
| I14 | The fiscal number is never used as our identifier and is nullable |
| I15 | Business-day length is computed on an absolute (UTC) basis, using the more conservative of monotonic and wall clock |
| I16 | The clock is never moved while a business day is open |
| I17 | Ordering never depends on the wall clock |
| I18 | `ADOTT_NAPON_ZARVA` is never sent before the tárgynap has definitively ended |
| I19 | The NTAK outbound queue is durable, ordered and non-overlapping |
| I20 | Every NTAK submission's processing acknowledgement is retrieved and stored |
| I21 | NTAK and the audit log can never be disabled |
| I22 | Every temporary integration disable has a 1-hour enforced expiry |
| I23 | The system never proactively offers a bypass |
| I24 | The audit log is append-only, enforced at database level |
| I25 | Not even the Siduri admin account can delete audit records |
| I26 | Print intent is recorded locally before the fiscal device is called |
| I27 | Print redirection is hard-limited to within the site, enforced server-side |
| I28 | The software never rejects a customer's chosen configuration |
| I29 | Errors are never silently swallowed |
| I30 | No AI attribution in any artifact |
| I31 | In invoice mode, calling the fiscal adapter is structurally impossible; a later invoice request requires storno of the receipt first |
| I32 | Selling a multi-purpose voucher is outside VAT scope; redemption is a payment method, not a product |
| I33 | The allergen list is LIVE-derived from the recipe, never a copy — the sole exception to principles A3/A4 |
| I34 | Stock never blocks a sale; only the manual "sold out" flag greys out a button |
| I35 | An audit record references the user by UUID, never by plain-text name; the role is a snapshot |
| I36 | A card tip is never an untracked drawer withdrawal |
| I37 | A split bill allocates per VAT rate, never on the grand total |
| I38 | Only Siduri may resolve an orphan transaction — but the customer can see that unresolved items exist |
| I39 | Replication-slot WAL retention is disk-capped, and reaching the cap is loud |
| I40 | Automatic Windows restarts are disabled on role-carrying machines, and this is verified |
| I41 | GDPR erasure touches the CRM profile; never an accounting document |
