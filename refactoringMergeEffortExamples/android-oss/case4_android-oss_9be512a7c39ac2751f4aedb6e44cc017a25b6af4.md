# Case 4 — Project: android-oss — Merge commit SHA1: 9be512a7c39ac2751f4aedb6e44cc017a25b6af4

## Modified file(s):
- `app/src/main/java/com/kickstarter/viewmodels/outputs/DiscoveryViewModelOutputs.java`
- `app/src/main/java/com/kickstarter/viewmodels/DiscoveryViewModel.java`

## Class(es) modified in the merge:
- `DiscoveryViewModelOutputs` (interface)
- `DiscoveryViewModel`

## Merge effort lines in the combined diff

```diff
// DiscoveryViewModelOutputs.java — interface method return type
    Observable<Boolean> shouldShowOnboarding();
    Observable<DiscoveryParams> showFilters();
-   Observable<Project> showProject();
+   Observable<Pair<Project, RefTag>> showProject();

// DiscoveryViewModel.java — implementation body
 +  private final PublishSubject<Project> showProject = PublishSubject.create();
 +  @Override
-   public Observable<Project> showProject() {
-     return showProject;
+   public Observable<Pair<Project, RefTag>> showProject() {
 -    return params.compose(Transformers.takePairWhen(projectClicked))
++    return params.compose(Transformers.takePairWhen(showProject))
+       .map(pp -> DiscoveryViewModel.projectAndRefTagFromParamsAndProject(pp.first, pp.second));
    }
```

## Relevant final code in the merge

```java
// DiscoveryViewModelOutputs.java
public interface DiscoveryViewModelOutputs {
  // ...
  Observable<Pair<Project, RefTag>> showProject();
  // ...
}

// DiscoveryViewModel.java
@Override
public Observable<Pair<Project, RefTag>> showProject() {
  return params.compose(Transformers.takePairWhen(showProject))
    .map(pp -> DiscoveryViewModel.projectAndRefTagFromParamsAndProject(pp.first, pp.second));
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
6 lines (2 `++`, 2 `-` discards from each parent confirming conflicting implementations, and 1 `-` on the interface)

## What each side had

**Parent 1 (P1)** changed the return type of `showProject()` in `DiscoveryViewModelOutputs` from `Observable<Project>` to `Observable<Pair<Project, RefTag>>`, and rewired the implementation to use `params.compose(Transformers.takePairWhen(projectClicked)).map(...)`. This is a **Change_Return_Type** refactoring on an interface method.

**Parent 2 (P2)** kept the old return type `Observable<Project>` and provided its own implementation using a new `showProject` subject directly:
```java
// P2 (old return type + old implementation, discarded):
-  public Observable<Project> showProject() {
-    return showProject;   // direct subject return, no Pair wrapping
```

P1 (discarded implementation):
```java
// P1 (new return type but different internal wiring, discarded):
 -  return params.compose(Transformers.takePairWhen(projectClicked))
```

## Interpretation

This is a **Change_Return_Type** conflict. P1 changed the return type of `showProject()` from `Observable<Project>` to `Observable<Pair<Project, RefTag>>` across the interface and implementation. P2 independently provided a new `showProject` `PublishSubject` and returned it directly with the old return type. The merge had to:

1. Adopt P1's new return type `Observable<Pair<Project, RefTag>>` on the interface
2. Write the implementation body combining P2's `showProject` subject (as the trigger source) with P1's `params + map(...)` transformation (`++` lines)

The `++` lines on the implementation body are the merge's reconciliation work: using P2's subject name (`showProject`) inside P1's transformation pipeline. This cross-parent synthesis is the core of the merge effort. 

## Complete diff

```diff
diff --cc app/src/main/java/com/kickstarter/viewmodels/outputs/DiscoveryViewModelOutputs.java
index 6f0614afe,8c3ced53f..854702230
--- a/app/src/main/java/com/kickstarter/viewmodels/outputs/DiscoveryViewModelOutputs.java
+++ b/app/src/main/java/com/kickstarter/viewmodels/outputs/DiscoveryViewModelOutputs.java
@@@ -11,11 -13,7 +14,11 @@@ import rx.Observable
  public interface DiscoveryViewModelOutputs {
    Observable<List<Project>> projects();
    Observable<DiscoveryParams> params();
 +  Observable<List<Activity>> activities();
    Observable<Boolean> shouldShowOnboarding();
    Observable<DiscoveryParams> showFilters();
-   Observable<Project> showProject();
+   Observable<Pair<Project, RefTag>> showProject();
 +  Observable<Void> showSignupLogin();
 +  Observable<Void> showActivityFeed();
 +  Observable<Activity> showActivityUpdate();
  }

diff --cc app/src/main/java/com/kickstarter/viewmodels/DiscoveryViewModel.java
index 9f3786f0f,213c4f081..248cac2bb
--- a/app/src/main/java/com/kickstarter/viewmodels/DiscoveryViewModel.java
+++ b/app/src/main/java/com/kickstarter/viewmodels/DiscoveryViewModel.java
@@@ -67,44 -68,17 +73,42 @@@
    public Observable<DiscoveryParams> params() {
      return params;
    }
 +  private final PublishSubject<Project> showProject = PublishSubject.create();
 +  @Override
-   public Observable<Project> showProject() {
-     return showProject;
+   public Observable<Pair<Project, RefTag>> showProject() {
 -    return params.compose(Transformers.takePairWhen(projectClicked))
++    return params.compose(Transformers.takePairWhen(showProject))
+       .map(pp -> DiscoveryViewModel.projectAndRefTagFromParamsAndProject(pp.first, pp.second));
    }
```
