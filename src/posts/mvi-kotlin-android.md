---
title: MVI and Why Android Finally Got Easy
description: Kotlin, MVI, RxKotlin, and Room made Android development actually enjoyable. Here's why I think MVI is the way forward.
date: 2019-11-20
layout: post.njk
tags:
  - post
  - android
  - kotlin
  - mvi
  - architecture
---

I've been doing this for a while now. Started with Java, survived the AsyncTask era, lived through MVP, watched MVVM become the religion it is today. And honestly? I'm bored.

Not bored with coding — bored because Android finally got easy. Really easy. And it happened so quietly that nobody noticed.

Kotlin fixed the language. MVI fixed the architecture. RxKotlin fixed the async mess. [Room](https://developer.android.com/training/data-storage/room) fixed the database. That's it. That's the entire stack. Everything else is details.

## The Problem With What Came Before

### MVC — The Wild West

Remember MVC in Android? Activity is the controller. View is the layout. Model is your data. Sounds clean. It's not.

The Activity does everything. UI logic, business logic, navigation, lifecycle management. It's a 2000-line god object that nobody wants to touch because nobody understands it.

### MVP — Better, But Fragile

Presenter holds a reference to the View. View is an interface. Presenter does the work. Sounds reasonable until you realize:

- View can be null (activity destroyed)
- Presenter survives rotation
- You spend half your time managing null checks
- Contract files multiply like rabbits

It works. It just requires discipline. And discipline is hard.

### MVVM — The Current Religion

DataBinding. LiveData. ViewModels. It's the standard now. And it's good. I won't argue with that.

But here's my issue: MVVM is ambiguous. Where does the business logic go? ViewModel? Repository? Some other layer? I've seen ViewModels with 500 lines of code. I've seen Repositories that do UI work. The boundaries are fuzzy.

Also, LiveData is... fine. But it's not reactive. It's observable, sure. But it's not a stream. If you're used to RxJava or Kotlin Flow, LiveData feels like going back to 2015.

## Enter MVI

Model-View-Intent. Three things. That's it.

- **Intent** — User actions (clicks, swipes, typing)
- **Model** — State of the screen (what you show)
- **View** — Renders the state (Activity, Fragment, Composable)

There's no ambiguity. There's no "where does this logic go?" The Intent produces a new Model. The View renders the Model. Always. No exceptions.

## The Code

Here's a login screen in MVI:

```kotlin
// State
data class LoginState(
    val email: String = "",
    val password: String = "",
    val isLoading: Boolean = false,
    val error: String? = null,
    val isLoggedIn: Boolean = false
)

// Intent (user actions)
sealed class LoginIntent {
    data class EmailChanged(val email: String) : LoginIntent()
    data class PasswordChanged(val password: String) : LoginIntent()
    object LoginClicked : LoginIntent()
}

// ViewModel
class LoginViewModel(
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _state = MutableStateFlow(LoginState())
    val state: StateFlow<LoginState> = _state

    fun processIntent(intent: LoginIntent) {
        when (intent) {
            is LoginIntent.EmailChanged -> {
                _state.update { it.copy(email = intent.email, error = null) }
            }
            is LoginIntent.PasswordChanged -> {
                _state.update { it.copy(password = intent.password, error = null) }
            }
            is LoginIntent.LoginClicked -> login()
        }
    }

    private fun login() {
        val currentState = _state.value
        if (currentState.email.isBlank() || currentState.password.isBlank()) {
            _state.update { it.copy(error = "Fill everything in") }
            return
        }

        _state.update { it.copy(isLoading = true) }

        authRepository.login(currentState.email, currentState.password)
            .subscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
            .subscribe(
                { _state.update { it.copy(isLoading = false, isLoggedIn = true) } },
                { error -> _state.update { it.copy(isLoading = false, error = error.message) } }
            )
            .addTo(disposables)
    }
}
```

And the View:

```kotlin
class LoginActivity : AppCompatActivity() {

    private val viewModel: LoginViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        // Render state
        lifecycleScope.launch {
            viewModel.state.collect { state ->
                progressBar.visibility = if (state.isLoading) View.VISIBLE else View.GONE
                loginButton.isEnabled = !state.isLoading
                emailInput.setText(state.email)
                passwordInput.setText(state.password)
                errorText.text = state.error ?: ""
                errorText.visibility = if (state.error != null) View.VISIBLE else View.GONE

                if (state.isLoggedIn) {
                    startActivity(Intent(this, MainActivity::class.java))
                    finish()
                }
            }
        }

        // Send intents
        emailInput.addTextChangedListener { text ->
            viewModel.processIntent(LoginIntent.EmailChanged(text.toString()))
        }
        passwordInput.addTextChangedListener { text ->
            viewModel.processIntent(LoginIntent.PasswordChanged(text.toString()))
        }
        loginButton.setOnClickListener {
            viewModel.processIntent(LoginIntent.LoginClicked)
        }
    }
}
```

Look at that. No callbacks. No interfaces. No contracts. The state is single source of truth. The View just renders. The ViewModel just processes intents.

## Why It's Harder To Mess Up

Here's the thing about MVI: there's only one way to do it.

In MVVM, you can put logic in the ViewModel. Or the Repository. Or a UseCase. Or the Activity. The architecture is flexible, which means it's also ambiguous.

In MVI, the Intent produces State. That's the only rule. If you follow it, the code is predictable. If you don't, it doesn't compile or the state doesn't update.

Also, because state is immutable (data class), you can't have race conditions. You can't have concurrent modifications. The state is what it is at any given moment.

Debugging? Easy. `Log.d("STATE", state.toString())` — you see every single state change. No hunting through callbacks.

Testing? Easy. Just pass an Intent, check the resulting State. No mocking views or presenters.

## But What About...

### Composable?

MVI works perfectly with Compose. [`StateFlow`](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow) into a `collectAsState()` and you're done. The ViewModel doesn't even need to change.

### Navigation?

Single Activity. Fragments or Composables. The state contains navigation state too if you want.

```kotlin
data class HomeState(
    val items: List<Item> = emptyList(),
    val navigation: Navigation? = null
)

sealed class HomeIntent {
    data class ItemClicked(val item: Item) : HomeIntent()
}

sealed class Navigation {
    object ToDetail : Navigation()
}
```

### Large Screens?

Break it down. Each screen has its own MVI. Compose them together. Simple.

## The Stack

Here's the entire modern Android stack:

- **Language**: Kotlin — null safety, extensions, coroutines
- **Architecture**: MVI — unidirectional data flow, single state
- **Async**: Kotlin Coroutines + Flow — streams, not callbacks
- **Database**: Room — reactive, type-safe, compile-time verified
- **DI**: Hilt or Koin — pick your poison

That's it. That's everything. No Retrofit vs Volley debates. No RxJava vs LiveData arguments. No MVP vs MVVM flame wars.

## The Take

I'm not saying MVI is perfect. I'm not saying it's the only way. I'm saying it's the easiest way to write bug-free Android code in 2019.

The combination of Kotlin's safety, MVI's predictability, coroutines' simplicity, and Room's robustness — it just works. I've been doing this for years and I've never been more productive.

Android got easy. Don't let anyone tell you otherwise.
