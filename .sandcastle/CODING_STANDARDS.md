# Project-specific overrides — Ousterhout / TDD principles supplied by skills.

<!-- The reviewer runs the `/improve-codebase-architecture` skill first (deep
     modules, narrow interfaces) and the implementer runs `/tdd`. This file is
     for rules those skills do NOT already cover — adopter-specific style,
     naming, or domain conventions.

     Keep this file short. If a rule fits inside the skills' remit, do not
     duplicate it here. Three examples (commented out) below: -->

<!--
- Public exports use named exports only; default exports are reserved for
  React component files that ship a single component.
- Database access goes through the repository layer in `src/db/repos/*`; route
  handlers must not import the ORM directly.
- All user-facing strings live in `src/i18n/en.ts`; never inline literals in
  components.
-->
