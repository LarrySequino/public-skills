# Context Profiles

Classify the screen on **three independent axes**, then apply all three. A finding's
severity shifts by axis — see the tier legend in `thresholds.md`.

Earlier versions of this file used single profiles named `mobile-app` / `web-app` /
`marketing-site`. That conflated variables that vary independently, and produced a real
defect: "mobile" resolved to Apple's 44pt and silently under-enforced Material's 48dp on
Android. It also left mobile *web* with no profile at all. Classify separately.

    Modality  →  what the finger or cursor demands   (Critical when missed)
    Platform  →  what the user expects to see        (costs familiarity)
    Surface   →  what the screen is for              (shifts emphasis)

State all three at the top of the review. If one is unknown, say so rather than
assuming — an unstated modality is how the wrong target minimum gets applied.

---

## Axis 1 — Modality (how it is operated)

The strongest axis. It sets hard minimums and it is **not** implied by the platform: a
web app on a touchscreen laptop is touch-operated; a native tablet app driven by a
trackpad is pointer-operated.

### touch
- **Targets: ≥48×48dp.** See `thresholds.md`. Do not use 44 because the platform is iOS —
  48 satisfies both and a cross-platform artifact binds to the stricter number.
- **Thumb reach:** primary actions in the bottom third; top corners are hard one-handed.
- **No hover.** Any affordance that only exists on hover is unreachable. Hover-revealed
  actions are a Critical finding here, not a Polish one.
- **Ergonomics:** destructive actions away from the natural thumb resting spot.
- Weight heavily: target size, thumb reach, state coverage, motion feel.

### pointer
- **Targets: ≥44×44px**, and never below the 24×24px universal floor.
- **Hover *and* focus states both required**, and visibly distinct from rest.
- Full keyboard navigation with a visible focus ring.
- Density is affordable; whitespace still needs rhythm.

### hybrid (both, or unknown)
Take the stricter of the two on every rule: 48dp targets **and** full hover/focus/keyboard
support. Most modern web falls here. When modality is genuinely unknown, this is the
correct default — it is the only one that cannot be wrong.

---

## Axis 2 — Platform (what the user expects)

Convention, not physics. A miss reads as foreign rather than broken, so cap severity at
Major unless it also breaks a universal or modality rule. Applies only to the platform
actually declared.

### iOS
Bottom sheets over centered modals; left-edge swipe returns; system back gesture must not
be trapped; respect notch/Dynamic Island and home-indicator insets; Dynamic Type must not
clip the layout.

### Android / Material
System back (gesture or button) must be honored; navigation bar and cutout insets
respected; FAB placement follows Material if a FAB is used at all.

### web
Real `<a>` elements for navigation so modifier-click and middle-click work; URL reflects
state (filters, tabs, pagination) so views are shareable and restorable; browser back
must not break the view; `env(safe-area-inset-*)` on full-bleed layouts, since mobile
browsers have insets too.

### cross-platform
Take the union of maxima on every numeric rule. Where two conventions genuinely conflict —
iOS left-edge-back against Android system-back — satisfy both if the affordances can
coexist, and if they cannot, say so explicitly as a stated trade-off rather than silently
picking one. An unstated choice here is the finding.

---

## Axis 3 — Surface (what the screen is for)

Shifts which dimensions carry weight. Changes emphasis, not minimums.

### product / app screen
Task completion is the job. Weight: hierarchy, state coverage (empty, loading, error),
consistency with the rest of the product, motion feel.

### dense / data tool
Dashboards, admin, tables. Information density is a feature. Weight: consistency and
tokens, hierarchy inside dense layouts, keyboard access, empty and error states,
responsive strategy for tables.

### marketing / landing
Conversion is the job. Value proposition and primary action land without scrolling; one
dominant call to action, competing actions are findings; image weight and load feel are
UX. Weight: hierarchy, type, color composition, brand feeling. Relax app-pattern and
state checks — they mostly do not apply.

---

## Domain modifiers

A domain modifier layers product-specific criteria on top of all three axes. None is
active by default — write one for the product under review and name it when invoking.

A modifier should say three things:

- **Which qualities become criteria rather than niceties.** If a product lives or dies on
  emotional tone, "cold but correct" is a finding — see Group D. If it lives on precision,
  warmth is noise.
- **Which affordances must be present and findable**, so their absence is a finding rather
  than an omission. Consent, reporting, undo, audit trails, disclosure — whichever the
  domain demands.
- **Which moments carry disproportionate weight.** Every product has a handful of screens
  that are its signature. Those earn extra scrutiny on motion, hierarchy and copy tone;
  they cannot feel generic, and a merely-adequate result on one is a finding.

Keep a modifier to a handful of lines. If it grows into a second rubric, it is a surface,
not a modifier.
