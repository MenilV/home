---
title: Aesthetic
description: A fast, easy-to-use, plug-and-play theme engine for Android apps.
year: 2018
role: Creator
tags:
  - project
  - android
  - kotlin
  - opensource
url: https://github.com/MenilV/aesthetic
---

Aesthetic is a theme engine for Android apps I built to solve a common problem: dynamic theming that actually works.

## The Problem

Most Android apps either:
- Use static themes defined in XML
- Have complex, fragile dynamic theming systems
- Require massive architectural changes to support themes

## The Solution

Aesthetic provides:

- **Rx-based reactivity** - Themes update automatically when changed
- **Minimal setup** - Drop-in solution with sensible defaults
- **Material Design compliance** - Works with Google's design system
- **Performance** - Efficient color calculations and caching

## Usage

```kotlin
// Set primary color
Aesthetic.get()
  .colorPrimary(Res.color(R.color.md_indigo_500))
  .colorAccent(Res.color(R.color.md_pink_500))
  .apply()

// Subscribe to theme changes
Aesthetic.get()
  .colorPrimary()
  .subscribe { color ->
    // Update UI
  }
```

## Impact

- 500+ stars on GitHub
- Used in production apps
- Inspired similar libraries

## Open Source

Available on [GitHub](https://github.com/MenilV/aesthetic) under MIT license.
