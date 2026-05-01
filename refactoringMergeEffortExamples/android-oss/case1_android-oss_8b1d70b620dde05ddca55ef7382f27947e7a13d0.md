# Case 1 [Very Strong] — Project: android-oss — Merge commit SHA1: 8b1d70b620dde05ddca55ef7382f27947e7a13d0

## Modified file(s):
- `app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationChildFilterViewHolder.java`
- `app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationHeaderLoggedInViewHolder.java`
- `app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationHeaderLoggedOutViewHolder.java`
- `app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationRootFilterViewHolder.java`
- `app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationTopFilterViewHolder.java`

## Class(es) modified in the merge:
- `HamburgerNavigationChildFilterViewHolder`
- `HamburgerNavigationHeaderLoggedInViewHolder`
- `HamburgerNavigationHeaderLoggedOutViewHolder`
- `HamburgerNavigationRootFilterViewHolder`
- `HamburgerNavigationTopFilterViewHolder`

## Merge effort lines in the combined diff

The pattern below repeats across all five ViewHolder files. Shown here for three representative cases:

```diff
// HamburgerNavigationChildFilterViewHolder.java
 +import android.support.annotation.NonNull;
++import android.support.annotation.Nullable;
++import com.kickstarter.libs.utils.ObjectUtils;
++import static com.kickstarter.libs.utils.ObjectUtils.*;
++
 +  @Override
-   public void onBind(final @NonNull Object datum) {
-     this.item = (NavigationDrawerData.Section.Row) datum;
++  public void bindData(final @Nullable Object data) throws Exception {
++    item = requireNonNull((NavigationDrawerData.Section.Row) data, NavigationDrawerData.Section.Row.class);
++  }
++
++  @Override
++  public void onBind() {
 +    final Context context = view.getContext();
```

```diff
// HamburgerNavigationHeaderLoggedInViewHolder.java
++import android.support.annotation.Nullable;
++import com.kickstarter.libs.utils.ObjectUtils;
++import static com.kickstarter.libs.utils.ObjectUtils.*;
++
 +  @Override
-   public void onBind(final @NonNull Object datum) {
-     this.user = (User) datum;
++  public void bindData(final @Nullable Object data) throws Exception {
++    user = requireNonNull((User) data, User.class);
++  }
++
++  @Override
++  public void onBind() {
 +    final Context context = view.getContext();
```

```diff
// HamburgerNavigationHeaderLoggedOutViewHolder.java
++import android.support.annotation.Nullable;

 +  @Override
-   public void onBind(final @NonNull Object datum) {
++  public void bindData(final @Nullable Object data) throws Exception {
++  }
++
++  @Override
++  public void onBind() {
 +  }
```

The same `--`/`++` pattern applies identically to `HamburgerNavigationRootFilterViewHolder` and `HamburgerNavigationTopFilterViewHolder`.

## Relevant final code in the merge

```java
// Representative: HamburgerNavigationChildFilterViewHolder
@Override
public void bindData(final @Nullable Object data) throws Exception {
  item = requireNonNull((NavigationDrawerData.Section.Row) data, NavigationDrawerData.Section.Row.class);
}

@Override
public void onBind() {
  final Context context = view.getContext();
  final Category category = item.params().category();
  // ... UI binding logic ...
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
28 lines (all `++`; the `-` lines are P2 discards, not merge-produced `--`)

## What each side had

**Parent 1 (P1)** refactored `KSViewHolder`, splitting `onBind(@NonNull Object datum)` into two lifecycle methods: `bindData(@Nullable Object data) throws Exception` for data assignment, and a no-arg `onBind()` for UI rendering. This new API propagated to all existing ViewHolder subclasses in P1's branch.

**Parent 2 (P2)** introduced five new Hamburger ViewHolder classes still using the old single-method contract:
```java
// P2 (old API, discarded):
- public void onBind(final @NonNull Object datum) {
-   this.item = (NavigationDrawerData.Section.Row) datum;
  // ... UI binding mixed into the same method body ...
```

## Interpretation

This is a **Rename_Method** conflict (with method split on the base class). P1 renamed and split `onBind(@NonNull Object datum)` into `bindData(@Nullable Object data)` + `onBind()` on `KSViewHolder`. P2 simultaneously added five new ViewHolder subclasses against the old API. The merge had to write the full two-method body for all five classes (28 `++` lines), conforming to P1's new contract.

The evidence is unambiguous: the `-` lines (P2 discards) show the old `onBind(@NonNull Object datum)` signature; the `++` lines produce `bindData` + `onBind()` in its place. The pattern repeats identically across five independent files, confirming a systematic refactoring conflict. The case is defensible for IEEE TSE: the rename changes the lifecycle contract of a base class, the parent attribution is directly readable from the combined-diff notation, and the `++` lines are behaviorally non-trivial.

## Complete diff

```diff
diff --cc app/src/main/java/com/kickstarter/ui/adapters/DiscoveryAdapter.java
index cfaebe728,ad9da54db..faa2e38c9
--- a/app/src/main/java/com/kickstarter/ui/adapters/DiscoveryAdapter.java
+++ b/app/src/main/java/com/kickstarter/ui/adapters/DiscoveryAdapter.java
@@@ -12,20 -15,52 +15,52 @@@ import java.util.Collections
  import java.util.List;
  
  public final class DiscoveryAdapter extends KSAdapter {
+   private static final int SECTION_ONBOARDING_VIEW = 0;
+   private static final int SECTION_PROJECT_CARD_VIEW = 1;
+ 
    private final Delegate delegate;
  
-   public interface Delegate extends ProjectCardViewHolder.Delegate {}
+   public interface Delegate extends ProjectCardViewHolder.Delegate, DiscoveryOnboardingViewHolder.Delegate {}
  
-   public DiscoveryAdapter(@NonNull final List<Project> projects, @NonNull final Delegate delegate) {
-     addSection(projects);
+   public DiscoveryAdapter(final @NonNull Delegate delegate) {
      this.delegate = delegate;
+ 
 -    this.data().add(SECTION_ONBOARDING_VIEW, Collections.emptyList());
 -    this.data().add(SECTION_PROJECT_CARD_VIEW, Collections.emptyList());
++    insertSection(SECTION_ONBOARDING_VIEW, Collections.emptyList());
++    insertSection(SECTION_PROJECT_CARD_VIEW, Collections.emptyList());
+   }
+ 
+   public void setShouldShowOnboardingView(final boolean shouldShowOnboardingView) {
+     if (shouldShowOnboardingView) {
 -      data().set(SECTION_ONBOARDING_VIEW, Collections.singletonList(null));
++      setSection(SECTION_ONBOARDING_VIEW, Collections.singletonList(null));
+     } else {
 -      data().set(SECTION_ONBOARDING_VIEW, Collections.emptyList());
++      setSection(SECTION_ONBOARDING_VIEW, Collections.emptyList());
+     }
+     notifyDataSetChanged();
+   }
+ 
+   public void takeProjects(final @NonNull List<Project> projects) {
 -    data().set(SECTION_PROJECT_CARD_VIEW, projects);
++    setSection(SECTION_PROJECT_CARD_VIEW, projects);
+     notifyDataSetChanged();
    }
  
-   protected @LayoutRes int layout(@NonNull final SectionRow sectionRow) {
-     return R.layout.project_card_view;
+   @Override
+   protected @LayoutRes int layout(final @NonNull SectionRow sectionRow) {
+     if (sectionRow.section() == SECTION_ONBOARDING_VIEW) {
+         return R.layout.discovery_onboarding_view;
+     } else {
+       return R.layout.project_card_view;
+     }
    }
  
-   protected @NonNull KSViewHolder viewHolder(@LayoutRes final int layout, @NonNull final View view) {
-     return new ProjectCardViewHolder(view, delegate);
+   @Override
+   protected KSViewHolder viewHolder(final @LayoutRes int layout, final @NonNull View view) {
+     switch (layout) {
+       case R.layout.discovery_onboarding_view:
+         return new DiscoveryOnboardingViewHolder(view, delegate);
+       case R.layout.project_card_view:
+         return new ProjectCardViewHolder(view, delegate);
+       default:
+         return new EmptyViewHolder(view);
+     }
    }
  }
diff --cc app/src/main/java/com/kickstarter/ui/toolbars/DiscoveryToolbar.java
index 9f526f8d8,b8bad8c58..91d286c6f
--- a/app/src/main/java/com/kickstarter/ui/toolbars/DiscoveryToolbar.java
+++ b/app/src/main/java/com/kickstarter/ui/toolbars/DiscoveryToolbar.java
@@@ -75,15 -73,9 +75,15 @@@ public final class DiscoveryToolbar ext
    @OnClick(R.id.filter_button)
    public void filterButtonClick(@NonNull final View view) {
      final DiscoveryActivity activity = (DiscoveryActivity) getContext();
-     activity.viewModel().filterButtonClick();
+     activity.viewModel().inputs.filterButtonClicked();
    }
  
 +  @OnClick(R.id.hamburger_button)
 +  public void hamburgerButtonClick(@NonNull final View view) {
 +    final Context context = getContext();
 +    context.startActivity(new Intent(context, HamburgerActivity.class));
 +  }
 +
    public void loadParams(@NonNull final DiscoveryParams params) {
      final Context context = getContext();
  
diff --cc app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationChildFilterViewHolder.java
index 7902dc7d3,000000000..246469426
mode 100644,000000..100644
--- a/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationChildFilterViewHolder.java
+++ b/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationChildFilterViewHolder.java
@@@ -1,69 -1,0 +1,77 @@@
 +package com.kickstarter.ui.viewholders;
 +
 +import android.content.Context;
 +import android.support.annotation.NonNull;
++import android.support.annotation.Nullable;
 +import android.view.View;
 +import android.widget.TextView;
 +
 +import com.kickstarter.KSApplication;
 +import com.kickstarter.R;
 +import com.kickstarter.libs.KSString;
++import com.kickstarter.libs.utils.ObjectUtils;
 +import com.kickstarter.models.Category;
 +import com.kickstarter.ui.adapters.data.NavigationDrawerData;
 +
 +import javax.inject.Inject;
 +
 +import butterknife.Bind;
 +import butterknife.BindColor;
 +import butterknife.ButterKnife;
 +import butterknife.OnClick;
 +import timber.log.Timber;
 +
++import static com.kickstarter.libs.utils.ObjectUtils.*;
++
 +public final class HamburgerNavigationChildFilterViewHolder extends KSViewHolder {
 +  protected @Bind(R.id.filter_text_view) TextView filterTextView;
 +  protected @BindColor(R.color.black) int blackColor;
 +  protected @BindColor(R.color.dark_gray) int darkGrayColor;
 +
 +  protected @Inject KSString ksString;
 +
 +  private NavigationDrawerData.Section.Row item;
 +  private Delegate delegate;
 +
 +  public interface Delegate {
 +    void rowClick(final @NonNull HamburgerNavigationChildFilterViewHolder viewHolder, final @NonNull NavigationDrawerData.Section.Row row);
 +  }
 +
 +  public HamburgerNavigationChildFilterViewHolder(final @NonNull View view, final @NonNull Delegate delegate) {
 +    super(view);
 +    this.delegate = delegate;
 +    ((KSApplication) view.getContext().getApplicationContext()).component().inject(this);
 +    ButterKnife.bind(this, view);
 +  }
 +
 +  @Override
-   public void onBind(final @NonNull Object datum) {
-     this.item = (NavigationDrawerData.Section.Row) datum;
++  public void bindData(final @Nullable Object data) throws Exception {
++    item = requireNonNull((NavigationDrawerData.Section.Row) data, NavigationDrawerData.Section.Row.class);
++  }
++
++  @Override
++  public void onBind() {
 +    final Context context = view.getContext();
 +
 +    final Category category = item.params().category();
 +    if (category != null && category.isRoot()) {
 +      filterTextView.setText(ksString.format(context.getString(R.string.discovery_filters_all_of_category), "category_name", item.params().filterString(context)));
 +    } else {
 +      filterTextView.setText(item.params().filterString(context));
 +    }
 +    if (item.selected()) {
 +      filterTextView.setTextAppearance(context, R.style.SubheadPrimaryMedium);
 +      filterTextView.setTextColor(blackColor);
 +    } else {
 +      filterTextView.setTextAppearance(context, R.style.SubheadPrimary);
 +      filterTextView.setTextColor(darkGrayColor);
 +    }
 +  }
 +
 +  @OnClick(R.id.filter_text_view)
 +  protected void textViewClick() {
 +    Timber.d("HamburgerNavigationChildFilterViewHolder rowClick");
 +    delegate.rowClick(this, item);
 +  }
 +}
 +
diff --cc app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationHeaderLoggedInViewHolder.java
index 3725f2385,000000000..d21027711
mode 100644,000000..100644
--- a/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationHeaderLoggedInViewHolder.java
+++ b/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationHeaderLoggedInViewHolder.java
@@@ -1,48 -1,0 +1,56 @@@
 +package com.kickstarter.ui.viewholders;
 +
 +import android.content.Context;
 +import android.support.annotation.NonNull;
++import android.support.annotation.Nullable;
 +import android.view.View;
 +import android.widget.ImageView;
 +import android.widget.TextView;
 +
 +import com.kickstarter.R;
 +import com.kickstarter.libs.transformations.CircleTransformation;
++import com.kickstarter.libs.utils.ObjectUtils;
 +import com.kickstarter.models.User;
 +import com.squareup.picasso.Picasso;
 +
 +import butterknife.Bind;
 +import butterknife.ButterKnife;
 +import butterknife.OnClick;
 +
++import static com.kickstarter.libs.utils.ObjectUtils.*;
++
 +public final class HamburgerNavigationHeaderLoggedInViewHolder extends KSViewHolder {
 +  private User user;
 +
 +  protected @Bind(R.id.user_image_view) ImageView userImageView;
 +  protected @Bind(R.id.user_name_text_view) TextView userNameTextView;
 +
 +  public HamburgerNavigationHeaderLoggedInViewHolder(final @NonNull View view) {
 +    super(view);
 +    ButterKnife.bind(this, view);
 +  }
 +
 +  @Override
-   public void onBind(final @NonNull Object datum) {
-     this.user = (User) datum;
++  public void bindData(final @Nullable Object data) throws Exception {
++    user = requireNonNull((User) data, User.class);
++  }
++
++  @Override
++  public void onBind() {
 +    final Context context = view.getContext();
 +
 +    userNameTextView.setText(user.name());
 +    Picasso.with(context)
 +      .load(user.avatar().medium())
 +      .transform(new CircleTransformation())
 +      .into(userImageView);
 +  }
 +
 +  @OnClick(R.id.user_container)
 +  public void userClick() {
 +  }
 +
 +  @OnClick(R.id.settings_icon_button)
 +  public void settingsClick() {
 +  }
 +}
diff --cc app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationHeaderLoggedOutViewHolder.java
index 835614cd9,000000000..1da0ed9a2
mode 100644,000000..100644
--- a/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationHeaderLoggedOutViewHolder.java
+++ b/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationHeaderLoggedOutViewHolder.java
@@@ -1,24 -1,0 +1,29 @@@
 +package com.kickstarter.ui.viewholders;
 +
 +import android.support.annotation.NonNull;
++import android.support.annotation.Nullable;
 +import android.view.View;
 +
 +import com.kickstarter.R;
 +
 +import butterknife.ButterKnife;
 +import butterknife.OnClick;
 +
 +public final class HamburgerNavigationHeaderLoggedOutViewHolder extends KSViewHolder {
 +  public HamburgerNavigationHeaderLoggedOutViewHolder(final @NonNull View view) {
 +    super(view);
 +    ButterKnife.bind(this, view);
 +  }
 +
 +  @Override
-   public void onBind(final @NonNull Object datum) {
++  public void bindData(final @Nullable Object data) throws Exception {
++  }
++
++  @Override
++  public void onBind() {
 +  }
 +
 +  @OnClick(R.id.logged_out_container)
 +  public void loggedOutClick() {
 +  }
 +}
diff --cc app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationRootFilterViewHolder.java
index 6301a2917,000000000..67a8033cd
mode 100644,000000..100644
--- a/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationRootFilterViewHolder.java
+++ b/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationRootFilterViewHolder.java
@@@ -1,56 -1,0 +1,64 @@@
 +package com.kickstarter.ui.viewholders;
 +
 +import android.content.Context;
 +import android.support.annotation.NonNull;
++import android.support.annotation.Nullable;
 +import android.view.View;
 +import android.widget.TextView;
 +
 +import com.kickstarter.R;
++import com.kickstarter.libs.utils.ObjectUtils;
 +import com.kickstarter.ui.adapters.data.NavigationDrawerData;
 +import com.kickstarter.ui.views.IconButton;
 +
 +import butterknife.Bind;
 +import butterknife.ButterKnife;
 +import butterknife.OnClick;
 +import timber.log.Timber;
 +
++import static com.kickstarter.libs.utils.ObjectUtils.*;
++
 +public final class HamburgerNavigationRootFilterViewHolder extends KSViewHolder {
 +  protected @Bind(R.id.filter_text_view) TextView filterTextView;
 +  protected @Bind(R.id.expand_button) IconButton expandButton;
 +  protected @Bind(R.id.collapse_button) IconButton collapseButton;
 +  private NavigationDrawerData.Section.Row item;
 +  private Delegate delegate;
 +
 +  public interface Delegate {
 +    void rowClick(final @NonNull HamburgerNavigationRootFilterViewHolder viewHolder, final @NonNull NavigationDrawerData.Section.Row row);
 +  }
 +
 +  public HamburgerNavigationRootFilterViewHolder(final @NonNull View view, final @NonNull Delegate delegate) {
 +    super(view);
 +    this.delegate = delegate;
 +    ButterKnife.bind(this, view);
 +  }
 +
 +  @Override
-   public void onBind(final @NonNull Object datum) {
-     this.item = (NavigationDrawerData.Section.Row) datum;
++  public void bindData(final @Nullable Object data) throws Exception {
++    item = requireNonNull((NavigationDrawerData.Section.Row) data, NavigationDrawerData.Section.Row.class);
++  }
++
++  @Override
++  public void onBind() {
 +    final Context context = view.getContext();
 +    filterTextView.setText(item.params().filterString(context));
 +    if (item.rootIsExpanded()) {
 +      expandButton.setVisibility(View.GONE);
 +      collapseButton.setVisibility(View.VISIBLE);
 +    } else {
 +      expandButton.setVisibility(View.VISIBLE);
 +      collapseButton.setVisibility(View.GONE);
 +    }
 +  }
 +
 +  @OnClick(R.id.filter_text_view)
 +  protected void textViewClick() {
 +    Timber.d("HamburgerNavigationRootFilterViewHolder rowClick");
 +    delegate.rowClick(this, item);
 +  }
 +}
 +
diff --cc app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationTopFilterViewHolder.java
index 50272e188,000000000..215a4c76a
mode 100644,000000..100644
--- a/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationTopFilterViewHolder.java
+++ b/app/src/main/java/com/kickstarter/ui/viewholders/HamburgerNavigationTopFilterViewHolder.java
@@@ -1,53 -1,0 +1,61 @@@
 +package com.kickstarter.ui.viewholders;
 +
 +import android.content.Context;
 +import android.support.annotation.NonNull;
++import android.support.annotation.Nullable;
 +import android.view.View;
 +import android.widget.LinearLayout;
 +import android.widget.TextView;
 +
 +import com.kickstarter.R;
++import com.kickstarter.libs.utils.ObjectUtils;
 +import com.kickstarter.ui.adapters.data.NavigationDrawerData;
 +
 +import butterknife.Bind;
 +import butterknife.BindColor;
 +import butterknife.ButterKnife;
 +import butterknife.OnClick;
 +import timber.log.Timber;
 +
++import static com.kickstarter.libs.utils.ObjectUtils.*;
++
 +public final class HamburgerNavigationTopFilterViewHolder extends KSViewHolder {
 +  protected @Bind(R.id.filter_view) LinearLayout filterView;
 +  protected @Bind(R.id.filter_text_view) TextView filterTextView;
 +  protected @BindColor(R.color.hamburger_navigation_item_selected) int filterSelectedColor;
 +  protected @BindColor(R.color.transparent) int filterUnselectedColor;
 +  private NavigationDrawerData.Section.Row item;
 +  private Delegate delegate;
 +
 +  public interface Delegate {
 +    void rowClick(final @NonNull HamburgerNavigationTopFilterViewHolder viewHolder, final @NonNull NavigationDrawerData.Section.Row row);
 +  }
 +
 +  public HamburgerNavigationTopFilterViewHolder(final @NonNull View view, final @NonNull Delegate delegate) {
 +    super(view);
 +    this.delegate = delegate;
 +    ButterKnife.bind(this, view);
 +  }
 +
 +  @Override
-   public void onBind(final @NonNull Object datum) {
-     this.item = (NavigationDrawerData.Section.Row) datum;
++  public void bindData(final @Nullable Object data) throws Exception {
++    item = requireNonNull((NavigationDrawerData.Section.Row) data, NavigationDrawerData.Section.Row.class);
++  }
++
++  @Override
++  public void onBind() {
 +    final Context context = view.getContext();
 +    filterTextView.setText(item.params().filterString(context));
 +    filterTextView.setTextAppearance(context, item.selected() ? R.style.SubheadPrimaryMedium : R.style.SubheadPrimary);
 +    filterView.setBackgroundColor(item.selected() ? filterSelectedColor : filterUnselectedColor);
 +  }
 +
 +  @OnClick(R.id.filter_text_view)
 +  protected void textViewClick() {
 +    Timber.d("HamburgerNavigationTopFilterViewHolder rowClick");
 +    delegate.rowClick(this, item);
 +  }
 +}
 +
diff --cc app/src/main/res/layout/horizontal_line_1dp_view.xml
index fed80f990,f1a457feb..2a4286854
--- a/app/src/main/res/layout/horizontal_line_1dp_view.xml
+++ b/app/src/main/res/layout/horizontal_line_1dp_view.xml
@@@ -1,8 -1,8 +1,8 @@@
  <?xml version="1.0" encoding="utf-8"?>
  <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:orientation="vertical"
-   android:layout_width="fill_parent"
+   android:layout_width="match_parent"
 -  android:layout_height="wrap_content" >
 +  android:layout_height="wrap_content">
  
    <View
      android:id="@+id/horizontal_line_thin_view"
diff --cc app/src/main/res/layout/settings_layout.xml
index fefdeecc9,17b89539c..b9c7faef7
--- a/app/src/main/res/layout/settings_layout.xml
+++ b/app/src/main/res/layout/settings_layout.xml
@@@ -438,6 -418,8 +418,8 @@@
  
          </RelativeLayout>
  
 -        <include layout="@layout/horizontal_line_thin_view"/>
++        <include layout="@layout/horizontal_line_1dp_view" />
+ 
          <Button
            style="@style/BorderButton"
            android:id="@+id/log_out_button"
diff --cc app/src/main/res/values/dimens.xml
index ca64bc4ab,a31e9066a..3de7d3c30
--- a/app/src/main/res/values/dimens.xml
+++ b/app/src/main/res/values/dimens.xml
@@@ -54,10 -51,8 +55,11 @@@
    <dimen name="card_padding_action_half">@dimen/grid_1_half</dimen>
    <dimen name="profile_card_height">@dimen/grid_26</dimen>
  
 +  <!-- Hamburger -->
 +  <dimen name="hamburger_drawer_item_padding_y">14dp</dimen>
 +
    <!-- Layout padding -->
+   <dimen name="activity_padding_x">0dp</dimen>
    <dimen name="feed_padding_y">@dimen/grid_5_half</dimen>
    <dimen name="feed_padding_x">@dimen/grid_3</dimen>
    <dimen name="form_margin_x">@dimen/grid_3</dimen>
diff --cc app/src/main/res/values/styles.xml
index a47f4c997,35307f624..7caf59034
--- a/app/src/main/res/values/styles.xml
+++ b/app/src/main/res/values/styles.xml
@@@ -224,18 -210,17 +224,17 @@@
      <item name="android:maxWidth">@dimen/button_icon_fixed_width</item>
      <item name="android:gravity">center</item>
      <item name="android:textColor">@color/primary_dark</item>
 -    <item name="android:textSize">22sp</item>
 +    <item name="android:textSize">@dimen/icon</item>
    </style>
  
-   <style name="ToolbarTitle" parent="SubheadPrimary">
+   <style name="ToolbarTitle" parent="Headline">
+     <item name="android:layout_height">wrap_content</item>
+     <item name="android:layout_width">wrap_content</item>
+     <item name="android:layout_centerVertical">true</item>
      <item name="android:color">@color/black</item>
      <item name="android:textColorHint">@color/dark_gray</item>
-   </style>
- 
-   <!-- Reduce margin size for < v21 devices, due to different FAB shadow rendering -->
-   <style name="StarFab">
-     <item name="android:layout_marginRight">@dimen/grid_1</item>
-     <item name="android:layout_marginBottom">@dimen/grid_1</item>
+     <item name="android:layout_marginLeft">@dimen/grid_3_half</item>
+     <item name="android:layout_marginStart">@dimen/grid_3_half</item>
    </style>
  
    <!-- Typography -->
```
