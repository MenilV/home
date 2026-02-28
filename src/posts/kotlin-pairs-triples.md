---
title: Pairs and Triples in Kotlin (and why you shouldn't use them)
description: Why Kotlin's Pair and Triple classes are an anti-pattern that can hurt your codebase's readability and maintainability.
date: 2024-12-26
layout: post.njk
tags:
  - post
  - kotlin
  - android
  - best-practices
---

_This post was originally published on the [Nutrient blog](https://www.nutrient.io/blog/pairs-and-triples-in-kotlin-and-why-you-shouldnt-use-them/)._

Kotlin's [`Pair`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-pair/) and [`Triple`](https://kotlinlang.org/api/latest/jvm/stdlib/kotlin/-triple/) classes seem convenient at first glance. Need to return two values from a function? Just use a `Pair`. Three values? `Triple` has you covered.

But this convenience comes at a cost. Let me explain why I think you should avoid them in production code.

## The Problem with Pairs

Here's a typical example of `Pair` usage:

```kotlin
fun getUserLocation(): Pair<Double, Double> {
    return Pair(latitude, longitude)
}

// Usage
val location = getUserLocation()
val lat = location.first
val lon = location.second
```

Looks harmless, right? But look at the call site again. Do you know which is latitude and which is longitude just by reading the code? You have to check the function definition to be sure.

Compare this to a data class:

```kotlin
data class Location(val latitude: Double, val longitude: Double)

fun getUserLocation(): Location {
    return Location(latitude, longitude)
}

// Usage
val location = getUserLocation()
val lat = location.latitude  // Clear and explicit
val lon = location.longitude // No ambiguity
```

## The Triple Problem

Triples make things even worse:

```kotlin
fun getUserData(): Triple<String, String, Int> {
    return Triple(name, email, age)
}

// Usage - what does .third represent again?
val data = getUserData()
println("${data.first}, ${data.second}, ${data.third}")
```

The type signature `Triple<String, String, Int>` tells you nothing semantically. Three strings would be completely indistinguishable.

## When Are They Okay?

I'll admit there are valid use cases:

1. **Temporary transformations** - mapping operations where the pair is immediately destructured
2. **Private helper functions** - internal implementation details that don't leak out
3. **Interacting with functional APIs** - some libraries expect pairs

```kotlin
// This is fine - internal and immediately destructured
val (min, max) = numbers.minMax()
```

## Better Alternatives

### Data Classes

For domain concepts, always prefer data classes:

```kotlin
data class Coordinates(val latitude: Double, val longitude: Double)
data class Dimensions(val width: Int, val height: Int)
data class DateRange(val start: Date, val end: Date)
```

### Type Aliases

For simple cases, type aliases can help:

```kotlin
typealias Coordinates = Pair<Double, Double>

// Still has .first/.second problem but documents intent better
```

### Inline Classes

For type safety without overhead:

```kotlin
@JvmInline
value class Latitude(val value: Double)

@JvmInline
value class Longitude(val value: Double)

fun getLocation(): Pair<Latitude, Longitude>
```

## The Bottom Line

Pairs and Triples are convenient but opaque. They sacrifice clarity for brevity. In a team setting, explicit data classes make your intent obvious and your code maintainable.

Reserve `Pair` and `Triple` for truly generic operations, not domain modeling. Your future self (and your teammates) will thank you.
