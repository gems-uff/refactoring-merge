# Case 3 — Project: android-oss — Merge commit SHA1: 9be512a7c39ac2751f4aedb6e44cc017a25b6af4

## Modified file(s):
- `app/src/main/java/com/kickstarter/ui/viewholders/ProfileCardViewHolder.java`
- `app/src/main/java/com/kickstarter/viewmodels/ProfileViewModel.java`

## Class(es) modified in the merge:
- `ProfileCardViewHolder` (inner interface `Delegate`)
- `ProfileViewModel`

## Merge effort lines in the combined diff

```diff
// ProfileCardViewHolder.java — Delegate interface
+   public interface Delegate {
 -    void projectCardClick(ProfileCardViewHolder viewHolder, Project project);
++    void projectCardViewHolderClicked(ProfileCardViewHolder viewHolder, Project project);
+   }

// ProfileCardViewHolder.java — onClick dispatch
+   @Override
+   public void onClick(@NonNull final View view) {
 -    delegate.projectCardClick(this, project);
++    delegate.projectCardViewHolderClicked(this, project);
+   }

// ProfileViewModel.java — method signature reconciliation
-   public void projectCardViewHolderClicked(final @NonNull ProjectCardViewHolder viewHolder, final @NonNull Project project) {
++  public void projectCardViewHolderClicked(final @NonNull ProfileCardViewHolder viewHolder, final @NonNull Project project) {
+     this.showProject.onNext(project);
+   }
```

## Relevant final code in the merge

```java
// ProfileCardViewHolder.java
public interface Delegate {
  void projectCardViewHolderClicked(ProfileCardViewHolder viewHolder, Project project);
}

@Override
public void onClick(@NonNull final View view) {
  delegate.projectCardViewHolderClicked(this, project);
}

// ProfileViewModel.java
public void projectCardViewHolderClicked(final @NonNull ProfileCardViewHolder viewHolder, final @NonNull Project project) {
  this.showProject.onNext(project);
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
6 lines (3 `++` and 1 `--`, plus 2 ` -` discards from P2 confirming the old name)

## What each side had

**Parent 1 (P1)** renamed the callback method in the `Delegate` interface pattern used by all view holders from `projectCardClick(...)` to `projectCardViewHolderClicked(...)`, applying this systematically across the codebase.

**Parent 2 (P2)** introduced the new `ProfileCardViewHolder` class with its own `Delegate` interface using the **old** method name `projectCardClick(...)`. P2 also added `projectCardViewHolderClicked(ProjectCardViewHolder ...)` to `ProfileViewModel` — using the new name but with the wrong receiver type (`ProjectCardViewHolder` instead of `ProfileCardViewHolder`):
```java
// P2 (old interface name, discarded):
 -  void projectCardClick(ProfileCardViewHolder viewHolder, Project project);
 -  delegate.projectCardClick(this, project);

// P2 (wrong parameter type, replaced by merge):
-  public void projectCardViewHolderClicked(final @NonNull ProjectCardViewHolder viewHolder, ...
```

## Interpretation

This is a **Rename_Method** conflict. P1 renamed `projectCardClick` → `projectCardViewHolderClicked` in the `Delegate` interface pattern. P2 introduced `ProfileCardViewHolder` using the old name. The merge had to:

1. Write the new method name in the `Delegate` interface (`++` line for `projectCardViewHolderClicked`)
2. Write the new dispatch call in `onClick` (`++` line replacing `projectCardClick`)
3. Fix the parameter type mismatch in `ProfileViewModel`: the `--` / `++` pair corrects `ProjectCardViewHolder` → `ProfileCardViewHolder`

The ` -` and `++` lines directly on the interface method name and call site are unambiguous evidence of a **Rename_Method** conflict. The additional `--`/`++` pair on the `ProfileViewModel` method signature represents a **Change_Parameter_Type** conflict caused by P2 using the wrong ViewHolder type. 

## Complete diff

```diff
diff --cc app/src/main/java/com/kickstarter/ui/viewholders/ProfileCardViewHolder.java
index 000000000,05ba9e460..c23deb2be
mode 000000,100644..100644
--- a/app/src/main/java/com/kickstarter/ui/viewholders/ProfileCardViewHolder.java
+++ b/app/src/main/java/com/kickstarter/ui/viewholders/ProfileCardViewHolder.java
@@@ -1,0 -1,117 +1,117 @@@
+ package com.kickstarter.ui.viewholders;
+ ...
+   public interface Delegate {
 -    void projectCardClick(ProfileCardViewHolder viewHolder, Project project);
++    void projectCardViewHolderClicked(ProfileCardViewHolder viewHolder, Project project);
+   }
+ ...
+   @Override
+   public void onClick(@NonNull final View view) {
 -    delegate.projectCardClick(this, project);
++    delegate.projectCardViewHolderClicked(this, project);
+   }

diff --cc app/src/main/java/com/kickstarter/viewmodels/ProfileViewModel.java
index 2690c2585,2edc17b7c..53dc284df
--- a/app/src/main/java/com/kickstarter/viewmodels/ProfileViewModel.java
+++ b/app/src/main/java/com/kickstarter/viewmodels/ProfileViewModel.java
@@@ -82,8 -78,4 +86,8 @@@
  
      koala.trackProfileView();
    }
+
-   public void projectCardViewHolderClicked(final @NonNull ProjectCardViewHolder viewHolder, final @NonNull Project project) {
++  public void projectCardViewHolderClicked(final @NonNull ProfileCardViewHolder viewHolder, final @NonNull Project project) {
+     this.showProject.onNext(project);
+   }
  }
```
