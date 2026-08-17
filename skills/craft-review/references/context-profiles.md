# Context Profiles

Classify the screen, then apply that profile's emphasis on top of the base dimensions. A finding's
severity can shift by profile (e.g., tap-target size is Critical on mobile, N/A on a marketing hero).

## mobile-app (default)

Native iOS/Android app screens.

- **Targets:** ≥44×44pt (Apple HIG); Material ≥48×48dp. This is Critical, not Polish.
- **Thumb reach:** primary actions in the bottom third; top corners are hard to reach one-handed.
- **Safe areas:** respect notch/Dynamic Island top inset and the home-indicator bottom inset; content
  and CTAs must not collide with them.
- **Patterns:** bottom sheets for secondary flows, not center modals; swipe/drag as first-class;
  system back/gesture respected.
- **Dynamic Type:** layout must survive larger text sizes without clipping.
- **One-hand ergonomics:** destructive actions away from the natural thumb resting spot.
- Weight heavily: symmetry, tap targets, thumb reach, state coverage, motion feel.

## web-app

SaaS dashboards, admin, dense data tools.

- **Density:** information density is a feature; whitespace still needs rhythm.
- **Input:** hover AND focus states required; full keyboard navigation and visible focus rings.
- **Responsive:** define behavior at breakpoints; tables need a responsive strategy.
- **Targets:** ≥24×24px (WCAG 2.5.8) minimum, 44 preferred for touch-capable.
- Weight heavily: consistency/tokens, hierarchy in dense layouts, keyboard a11y, empty/error states.

## marketing-site

Landing pages, homepages, conversion surfaces.

- **Above the fold:** the value prop and primary CTA must land without scrolling.
- **Conversion:** one dominant CTA; friction and competing actions are findings.
- **Performance:** image weight and load feel are UX; flag heavy hero media.
- **Less chrome:** editorial hierarchy and rhythm matter more than app-pattern consistency.
- Weight heavily: hierarchy, type, color composition, brand feeling; relax app-pattern/state checks.

## Domain modifiers

A domain modifier layers product-specific criteria on top of a profile. None is active by default —
write one for the product under review and name it when invoking.

A modifier should say three things:

- **Which qualities become criteria rather than niceties.** If a product lives or dies on emotional
  tone, "cold but correct" is a finding — see Group D. If it lives on precision, warmth is noise.
- **Which affordances must be present and findable**, so their absence is a finding rather than an
  omission. Consent, reporting, undo, audit trails, disclosure — whichever the domain demands.
- **Which moments carry disproportionate weight.** Every product has a handful of screens that are
  its signature. Those earn extra scrutiny on motion, hierarchy and copy tone; they cannot feel
  generic, and a merely-adequate result on one is a finding.

Keep a modifier to a handful of lines. If it grows into a second rubric, it is a profile, not a
modifier.
