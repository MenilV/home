---
title: RxJava and RxAndroid
description: Reactive extensions bring a new way to handle asynchronous data streams in Android.
date: 2017-03-15
layout: post.njk
tags:
  - post
  - android
  - rxjava
  - rxandroid
---

I've been building Android apps for a few years now. You learn to cope. Background thread for the database. Another one for the API. Callbacks everywhere. AsyncTasks that weren't actually async. Handlers and Looper. Loaders that were too rigid and died with the activity.

Every project ended up with its own ad-hoc solution. It worked, mostly, but it never felt right.

## The Problem

Here's what a typical data fetch looked like:

```java
new AsyncTask<Void, Void, User>() {
    @Override
    protected User doInBackground(Void... params) {
        return userApi.getUser(userId);
    }

    @Override
    protected void onPostExecute(User user) {
        nameText.setText(user.getName());
        emailText.setText(user.getEmail());
    }
}.execute();
```

Seems fine. Except:

- No way to chain operations cleanly
- Error handling is manual and easy to forget
- Good luck canceling mid-flight
- Rotate the device and hope the Activity is still alive
- Need database first, then API? Enjoy the callback hell

## Enter Observables

[RxJava](https://github.com/ReactiveX/RxJava) gives you `Observable`. A stream of data that you can transform, combine, and subscribe to:

```java
Observable<User> userObservable = api.getUser(userId);
```

The chaining is where it gets useful.

## Database → Network → UI

Say you need to check local cache, fetch from API if stale, save to DB, then show in UI:

```java
Observable<User> cachedUser = database.getUser(userId);
Observable<User> freshUser = api.getUser(userId)
    .doOnNext(user -> database.saveUser(user))
    .onErrorResumeNext(throwable -> cachedUser);

Observable.concat(cachedUser, freshUser)
    .first()
    .subscribeOn(Schedulers.io())
    .observeOn(AndroidSchedulers.mainThread())
    .subscribe(this::displayUser, this::showError);
```

That chain does four things — cache, network, save, UI — in one readable stream. No callbacks inside callbacks.

Here's what each part does:

- `cachedUser` emits from local database
- `freshUser` hits the API and saves to DB on success
- `onErrorResumeNext` falls back to cache if network fails
- `concat` runs them in order — cache first, then network
- `first()` takes only the first successful emission

## Operators

### map — transform

```java
api.getUser(userId)
    .map(user -> user.getName())
    .subscribe(name -> textView.setText(name));
```

### flatMap — chain operations

```java
api.getUser(userId)
    .flatMap(user -> api.getPosts(user.getId()))
    .subscribe(posts -> adapter.setPosts(posts));
```

### filter — skip items

```java
api.getAllUsers()
    .filter(user -> user.getAge() >= 18)
    .subscribe(this::displayUser);
```

### zip — combine sources

```java
Observable<User> user = api.getUser(userId);
Observable<List<Post>> posts = api.getPosts(userId);

Observable.zip(user, posts, (u, p) -> new UserWithPosts(u, p))
    .subscribe(this::displayUserWithPosts);
```

## Android Lifecycle

RxAndroid gives you `AndroidSchedulers.mainThread()`. That's the main thing it adds — a scheduler that runs on the UI thread.

The real problem is memory leaks. If your Observable is still emitting after the Activity is destroyed, boom. `CompositeDisposable` fixes this:

```java
public class UserActivity extends AppCompatActivity {

    private CompositeDisposable disposables = new CompositeDisposable();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Disposable d = api.getUser(userId)
            .subscribeOn(Schedulers.io())
            .observeOn(AndroidSchedulers.mainThread())
            .subscribe(this::displayUser, this::showError);

        disposables.add(d);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        disposables.clear();
    }
}
```

Clear the disposables in `onDestroy` and you're safe.

## Thoughts

Is it verbose? Sometimes. Does it beat the alternative? For anything beyond a single API call, yes. Once you start thinking in streams, it clicks.

There's also [RxBinding from Jake Wharton](https://github.com/JakeWharton/RxBinding) if you want to treat UI events as streams:

```java
RxView.clicks(button)
    .flatMap(v -> api.getData())
    .subscribe(this::updateUI);
```

It's a different way to think about UI. Not better or worse — just different. RxJava 2 is in the works with Flow, which might change things further. But these ideas — streams, operators, threading — they're worth understanding regardless of which reactive library you end up using.
