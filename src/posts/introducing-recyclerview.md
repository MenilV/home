---
title: Introducing RecyclerView
description: A new way to display lists in Android that's efficient, flexible, and actually pleasant to use.
date: 2016-06-06
layout: post.njk
tags:
  - post
  - android
  - recyclerview
---

If you've used `ListView` for any serious amount of time, you know the pain. View holders are optional (so everyone forgets them), layouts are limited to vertical lists, and animations feel tacked on. It's worked for years, but it never felt right.

A new widget landed in the support library recently that fixes all of this. It's called [`RecyclerView`](https://developer.android.com/develop/ui/views/layout/recyclerview).
## The Problem with ListView

ListView has served us well for years. But it has some fundamental limitations:

- View holders weren't enforced, leading to repeated `findViewById` calls
- No built-in support for horizontal lists, grids, or staggered layouts
- Limited animation capabilities
- Poor decoupling between data and display

## Enter RecyclerView

RecyclerView is a brand new widget that addresses all of these issues. It's part of the support library, so it works all the way back to API 7.

### ViewHolder Pattern — Built In

The ViewHolder pattern is now mandatory. This means better performance out of the box:

```java
public class MyAdapter extends RecyclerView.Adapter<MyAdapter.ViewHolder> {

    private List<MyItem> items = new ArrayList<>();

    public MyAdapter(List<MyItem> items) {
        this.items = items;
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView titleText;
        TextView subtitleText;

        public ViewHolder(View itemView) {
            super(itemView);
            titleText = (TextView) itemView.findViewById(R.id.title);
            subtitleText = (TextView) itemView.findViewById(R.id.subtitle);
        }
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
            .inflate(R.layout.item_layout, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        MyItem item = items.get(position);
        holder.titleText.setText(item.getTitle());
        holder.subtitleText.setText(item.getSubtitle());
    }

    @Override
    public int getItemCount() {
        return items.size();
    }
}
```

Notice how the ViewHolder caches the views. No more repetitive `findViewById` in `getView`.

### LayoutManagers — One Widget, Multiple Layouts

This is the game-changer. RecyclerView delegates layout to a `LayoutManager`, so one widget handles everything:

```java
// Vertical list (like ListView)
recyclerView.setLayoutManager(new LinearLayoutManager(context));

// Horizontal list
recyclerView.setLayoutManager(
    new LinearLayoutManager(context, LinearLayoutManager.HORIZONTAL, false));

// Grid layout
recyclerView.setLayoutManager(new GridLayoutManager(context, 2));

// Staggered grid (Pinterest-style)
recyclerView.setLayoutManager(
    new StaggeredGridLayoutManager(2, StaggeredGridLayoutManager.VERTICAL));
```

Same adapter, completely different layouts. That's the power of proper abstraction.

Same adapter, completely different layouts. That's the power of proper abstraction.

### ItemDecoration — Clean Separation

Want dividers between items? Want custom spacing? Use `ItemDecoration`:

```java
public class SpacingDecoration extends RecyclerView.ItemDecoration {

    private int spacing;

    public SpacingDecoration(int spacing) {
        this.spacing = spacing;
    }

    @Override
    public void getItemOffsets(Rect outRect, View view, 
            RecyclerView parent, RecyclerView.State state) {
        outRect.bottom = spacing;
    }
}

recyclerView.addItemDecoration(new SpacingDecoration(16));
```

No more messing with margins in your item layout. Clean separation of concerns.

No more messing with margins in your item layout. Clean separation of concerns.

### Animations — First Class Support

RecyclerView makes animations easy:

```java
// Default animations (add, remove, move)
recyclerView.setItemAnimator(new DefaultItemAnimator());

// Or configure specific animations
SimpleItemAnimator animator = (SimpleItemAnimator) recyclerView.getItemAnimator();
animator.setSupportsChangeAnimations(false);
animator.setAddDuration(200);
animator.setRemoveDuration(200);
```

You can also set `initialLayoutPrefetchCount` on the LayoutManager for initial load performance.

You can also animate the initial layout with `layoutManager.initialLayoutPrefetchCount`.

## Putting It All Together

Here's a complete example:

```java
public class MainActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private MyAdapter adapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recyclerView = (RecyclerView) findViewById(R.id.recycler_view);

        // Set up layout manager
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        // Set up adapter
        adapter = new MyAdapter(generateItems());
        recyclerView.setAdapter(adapter);

        // Add spacing
        recyclerView.addItemDecoration(new SpacingDecoration(dpToPx(16)));

        // Optimize performance
        recyclerView.setHasFixedSize(true);
    }

    private List<MyItem> generateItems() {
        List<MyItem> items = new ArrayList<>();
        for (int i = 1; i <= 50; i++) {
            items.add(new MyItem("Item " + i, "Description for item " + i));
        }
        return items;
    }

    private int dpToPx(int dp) {
        return (int) (dp * Resources.getSystem().getDisplayMetrics().density);
    }
}
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<android.support.v7.widget.RecyclerView
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/recycler_view"
    android:scrollbars="vertical"
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:id="@+id/title"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textSize="18sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/subtitle"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textSize="14sp"
        android:textColor="#666666" />

</LinearLayout>
```

## Adding the Dependency

In your `build.gradle`:

```groovy
dependencies {
    compile 'com.android.support:recyclerview-v7:23.2.0'
}
```

> Note: The version should match your support library version.

## Why This Matters

RecyclerView represents a shift in how Android thinks about lists:

1. **Performance** — Mandatory view recycling with ViewHolder
2. **Flexibility** — Swappable LayoutManagers for any arrangement
3. **Decoupling** — Clean separation between data, display, and layout
4. **Animations** — Built-in support for smooth transitions

It's not just an improved ListView — it's a fundamentally better architecture for list-based UIs.

Give it a try. Once you go RecyclerView, you won't look back.
