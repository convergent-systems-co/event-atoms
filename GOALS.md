# event-atoms — Goals

> Event primitives — types, schemas, channels, subscription patterns, delivery semantics — paired with Service Atoms to cover the request/response and async halves of distributed systems.

*This document is derived from `aish/ARCHITECTURE.md` (now `xdao/xdao/ARCHITECTURE.md` §The *-Atoms Catalogs). Sections marked **Generated** are pattern-based and are intended as a starting point for revision, not as decided plan.*

---

## What this catalog makes civilization-grade

Event-driven architectures reinvent the wheel for every message bus. Kafka schemas live in one registry, NATS subjects in another, RabbitMQ exchanges nowhere portable. Cross-system event flows are bespoke. Schema evolution rules are tribal knowledge.

By cataloging the primitives, `event-atoms` turns this domain from opaque-and-ephemeral to typed, versioned, composable, machine-readable, and open — the civilization-grade properties the ecosystem requires.

## What it catalogs

### Atom types

- **`event-type`** — Canonical event names with semantic meaning (OrderPlaced, UserCreated, SignalReceived).
- **`schema`** — Event payload schema, versioned and forward-compatible.
- **`channel`** — Where events flow (topic, subject, exchange, queue).
- **`subscription-pattern`** — How subscribers express interest (exact, wildcard, content-filtered).
- **`delivery-semantics`** — At-least-once, at-most-once, exactly-once, ordered, unordered.

### Compositions: `streams`

A stream composition assembles event types + schemas + channels + subscriptions + delivery semantics into a complete event-driven flow. Multi-stream compositions describe event-driven architectures.

### Rule types

- **`schema-evolution`** — What schema changes are backwards-compatible (adding optional field = OK; removing = breaking).
- **`delivery-guarantee`** — Which delivery semantics a channel supports.
- **`ordering-constraint`** — Per-partition ordering, global ordering, none.

## Runtime consumers

- **universal-bus** — Future service-layer runtime needs event vocabulary to route async messages.

## Status & priority

**Current status:** `proposed`

**Priority tier:** Tier 4 — Build when companion runtime exists

**Trigger / activation condition:** Universal Bus exists. Pairs with service-atoms — together they cover the request/response and async halves of distributed systems.

## Roadmap *(Generated — milestone shapes mirror aish's roadmap pattern; revise as actual work begins)*

### v0.1 — Bootstrap & spec acceptance

**Goal:** Schema accepted. Paired with service-atoms for unified service/event vocabulary.

**Success criterion:** Three real event flows cataloged and routable via Universal Bus.

**Kill criterion:** Universal Bus design indicates events should be modeled as a special case of services — pivot to merging event-atoms into service-atoms.

**Work:**

- [ ] XAIP: stream composition schema
- [ ] Define 5 atom type schemas with delivery-semantic constraints
- [ ] Catalog 3 internal event flows as seed
- [ ] Verify against Kafka, NATS, RabbitMQ implementations

### v0.2 — Adoption & expansion

**Goal:** Universal Bus routes events via event-atoms.

**Work:**

- [ ] Universal Bus event-routing integration
- [ ] Schema-evolution validator
- [ ] Cross-system event flow examples

### v1.0 — Operational

**Goal:** Default event vocabulary for ecosystem-internal async messaging.

## Concrete atom example *(Generated — illustrative, not seed content)*

```yaml
streams/order-placed-flow/definition.yml
---
id: order-placed-flow
type: composition
version: 1.0.0
event_type: { ref: atoms/event-type/order-placed }
schema: { ref: atoms/schema/order-placed-v2 }
channel: { ref: atoms/channel/orders-topic }
subscription_pattern: { ref: atoms/subscription-pattern/wildcard-region }
delivery: { ref: atoms/delivery-semantics/at-least-once-ordered }
```

## Adoption strategy *(Generated)*

Adoption follows Universal Bus. Pre-bus, event-atoms is the spec everyone agrees to.

## Civilization-grade property checklist

Every catalog must satisfy these before v1.0. Failing any blocks a release.

| Property | Mechanism in this catalog |
|---|---|
| Typed | JSON Schema in `schemas/` validates every atom, composition, rule |
| Versioned | Every atom has a semver `version` field; compositions reference atoms by version-pinned ID |
| Machine-readable | `exports/catalog.json` published on every release |
| Composable | Compositions reference atoms by ID; CI verifies references resolve and no circular dependencies |
| Open | Apache-2.0 licensed; LICENSE file present |
| Durable | No external dependencies for primary content (no remote image URLs, no vendor APIs in the hot path) |

## Related

- **Spec:** [atoms-spec](https://github.com/convergent-systems-co/atoms-spec) — the canonical structure every catalog conforms to
- **Tools:** [atoms-tools](https://github.com/convergent-systems-co/atoms-tools) — CLI for validate / export / bootstrap / resolve
- **Federation:** [xdao](https://github.com/convergent-systems-co/xdao) — ecosystem directory and discovery
- **Umbrella:** [atoms](https://github.com/convergent-systems-co/atoms) — every catalog as a git submodule
- **Manifest:** [`ATOMS.yml`](./ATOMS.yml) — this catalog's machine-readable manifest
- **Standard:** [`README.md`](./README.md) — catalog overview and contribution flow
