# Case 2 — Project: android-oss — Merge commit SHA1: 8b1d70b620dde05ddca55ef7382f27947e7a13d0

## Modified file(s):
- `app/src/main/java/com/kickstarter/ui/adapters/DiscoveryAdapter.java`

## Class(es) modified in the merge:
- `DiscoveryAdapter`

## Merge effort lines in the combined diff

```diff
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
```

## Relevant final code in the merge

```java
public DiscoveryAdapter(final @NonNull Delegate delegate) {
  this.delegate = delegate;
  insertSection(SECTION_ONBOARDING_VIEW, Collections.emptyList());
  insertSection(SECTION_PROJECT_CARD_VIEW, Collections.emptyList());
}

public void setShouldShowOnboardingView(final boolean shouldShowOnboardingView) {
  if (shouldShowOnboardingView) {
    setSection(SECTION_ONBOARDING_VIEW, Collections.singletonList(null));
  } else {
    setSection(SECTION_ONBOARDING_VIEW, Collections.emptyList());
  }
  notifyDataSetChanged();
}

public void takeProjects(final @NonNull List<Project> projects) {
  setSection(SECTION_PROJECT_CARD_VIEW, projects);
  notifyDataSetChanged();
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
10 lines (5 `++` and 5 ` -` discards, with the ` -` lines confirming what P2 had; true `--` count is 0, as no lines were actively removed by the merge itself — all old lines appear as ` -` discards from P2)

> **Note on notation:** In this diff, the old `data().add(...)` and `data().set(...)` calls appear with the ` -` prefix (discarded from P2), not `--`. The `++` lines are the merge-created replacements. This is consistent with a case where P1 renamed the API and P2 wrote new code against the old API — the merge discards P2's old calls and writes P1's new names.

## What each side had

**Parent 1 (P1)** renamed methods in the `KSAdapter` base class, replacing the raw `data().add(...)` call with the named helper `insertSection(...)`, and `data().set(...)` with `setSection(...)`. This **Rename_Method** refactoring encapsulated direct list manipulation behind intentionally named API methods.

**Parent 2 (P2)** introduced the new `DiscoveryAdapter` with multi-section support (onboarding + project card), calling the old raw API directly:
```java
// P2 (old API, discarded):
 -  this.data().add(SECTION_ONBOARDING_VIEW, Collections.emptyList());
 -  this.data().add(SECTION_PROJECT_CARD_VIEW, Collections.emptyList());
 -  data().set(SECTION_ONBOARDING_VIEW, Collections.singletonList(null));
 -  data().set(SECTION_ONBOARDING_VIEW, Collections.emptyList());
 -  data().set(SECTION_PROJECT_CARD_VIEW, projects);
```

## Interpretation

This is a **Rename_Method** conflict. P1 renamed `data().add(...)` → `insertSection(...)` and `data().set(...)` → `setSection(...)` in the `KSAdapter` base class. P2 simultaneously wrote `DiscoveryAdapter` using the old raw calls. The merge had to write the new method names (5 `++` lines) across all five call sites, replacing the P2-discarded old calls (5 ` -` lines).

The evidence is direct and unambiguous: each ` -` line shows the old raw-API call; each `++` line shows the exact renamed replacement. There are no logic changes — only the method name differs. The pattern repeats five times within a single file. The case is defensible for IEEE TSE: it is a clean surgical rename of base-class API methods, with clear parent attribution from the combined-diff notation.

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
```
