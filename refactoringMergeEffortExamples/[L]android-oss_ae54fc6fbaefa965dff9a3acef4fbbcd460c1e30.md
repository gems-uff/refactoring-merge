# Project: android-oss — Merge commit SHA1: ae54fc6fbaefa965dff9a3acef4fbbcd460c1e30

## Modified file(s):
- `app/src/main/java/com/kickstarter/models/User.java`

## Class(es) modified in the merge:
- `User`
- `User.Builder`

## Merge effort lines in the combined diff

```diff
// User.java — abstract accessor
 +  public abstract @Nullable Integer backedProjectsCount();
++  public abstract @Nullable Integer createdProjectsCount();
 +  public abstract boolean happeningNewsletter();
    public abstract long id();
-   public abstract @Nullable Integer launchedProjectsCount();
    public abstract String name();
 -  @Nullable public abstract Integer backedProjectsCount();
 -  @Nullable public abstract Integer createdProjectsCount();
 -  @Nullable public abstract Integer starredProjectsCount();

// User.Builder — builder setter
      public abstract Builder backedProjectsCount(Integer __);
+     public abstract Builder createdProjectsCount(Integer __);
 +   public abstract Builder happeningNewsletter(boolean __);
 +   public abstract Builder id(long __);
-    public abstract Builder launchedProjectsCount(Integer __);
 +   public abstract Builder name(String __);
```

## Relevant final code in the merge

```java
@AutoParcel
public abstract class User implements Parcelable {
  public abstract Avatar avatar();
  public abstract @Nullable Integer backedProjectsCount();
  public abstract @Nullable Integer createdProjectsCount(); // renamed from launchedProjectsCount
  public abstract boolean happeningNewsletter();
  public abstract long id();
  // ...

  @AutoParcel.Builder
  public abstract static class Builder {
    public abstract Builder backedProjectsCount(Integer __);
    public abstract Builder createdProjectsCount(Integer __); // renamed from launchedProjectsCount
    public abstract Builder happeningNewsletter(boolean __);
    // ...
  }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
2 lines (2 `++`; the `-` lines are P1/P2 discards confirming the conflicting declarations)

## What each side had

**Parent 1 (P1)** renamed the attribute `launchedProjectsCount` → `createdProjectsCount` in the `User` model class, updating both the abstract accessor method and its `Builder` counterpart. The `-` line `public abstract @Nullable Integer launchedProjectsCount()` and `-` `public abstract Builder launchedProjectsCount(Integer __)` are P1's removals.

**Parent 2 (P2)** kept `launchedProjectsCount` under its old name and also had `createdProjectsCount` declared separately (in a different style and position), while adding a large set of new notification/newsletter attributes to `User`. The ` -` lines showing `@Nullable public abstract Integer createdProjectsCount()` and `@Nullable public abstract Integer backedProjectsCount()` are P2's declarations in its old position/style, which conflicted with P1's restructured layout.

```java
// P1 removed (old name):
-  public abstract @Nullable Integer launchedProjectsCount();
-  public abstract Builder launchedProjectsCount(Integer __);

// P2 had (old position/style, discarded):
 -  @Nullable public abstract Integer createdProjectsCount();
 -  @Nullable public abstract Integer backedProjectsCount();
```

## Interpretation

This is a **Rename_Attribute** conflict. P1 renamed `launchedProjectsCount` → `createdProjectsCount` in the `User` model. P2 was simultaneously adding new attributes to `User` without awareness of P1's rename. The merge had to write `createdProjectsCount` in the new canonical position and style (`++` lines), after the old `launchedProjectsCount` was removed (`-` line from P1) and P2's conflicting declarations were discarded (` -` lines).

The evidence is clear: the `-` line removes `launchedProjectsCount`; the `++` line places `createdProjectsCount` in its final form. The same rename is confirmed symmetrically in `Builder`. 

## Complete diff

```diff
diff --cc app/src/main/java/com/kickstarter/models/User.java
index 66c28e47c,cf2b0b982..15293dee3
--- a/app/src/main/java/com/kickstarter/models/User.java
+++ b/app/src/main/java/com/kickstarter/models/User.java
@@@ -11,46 -11,20 +11,46 @@@ import auto.parcel.AutoParcel
  @AutoParcel
  public abstract class User implements Parcelable {
    public abstract Avatar avatar();
 +  public abstract @Nullable Integer backedProjectsCount();
++  public abstract @Nullable Integer createdProjectsCount();
 +  public abstract boolean happeningNewsletter();
    public abstract long id();
-   public abstract @Nullable Integer launchedProjectsCount();
    public abstract String name();
 -  @Nullable public abstract Integer backedProjectsCount();
 -  @Nullable public abstract Integer createdProjectsCount();
 -  @Nullable public abstract Integer starredProjectsCount();
 +  public abstract boolean notifyMobileOfBackings();
 +  public abstract boolean notifyMobileOfComments();
 +  public abstract boolean notifyMobileOfFollower();
 +  public abstract boolean notifyMobileOfFriendActivity();
 +  public abstract boolean notifyMobileOfUpdates();
 +  public abstract boolean notifyOfBackings();
 +  public abstract boolean notifyOfComments();
 +  public abstract boolean notifyOfFollower();
 +  public abstract boolean notifyOfFriendActivity();
 +  public abstract boolean notifyOfUpdates();
 +  public abstract boolean promoNewsletter();
 +  public abstract @Nullable Integer starredProjectsCount();
 +  public abstract boolean weeklyNewsletter();
  
    @AutoParcel.Builder
    public abstract static class Builder {
      public abstract Builder avatar(Avatar __);
 -    public abstract Builder id(long __);
 -    public abstract Builder name(String __);
      public abstract Builder backedProjectsCount(Integer __);
+     public abstract Builder createdProjectsCount(Integer __);
 +    public abstract Builder happeningNewsletter(boolean __);
 +    public abstract Builder id(long __);
-     public abstract Builder launchedProjectsCount(Integer __);
 +    public abstract Builder name(String __);
 +    public abstract Builder notifyMobileOfBackings(boolean __);
 +    public abstract Builder notifyMobileOfComments(boolean __);
 +    public abstract Builder notifyMobileOfFollower(boolean __);
 +    public abstract Builder notifyMobileOfFriendActivity(boolean __);
 +    public abstract Builder notifyMobileOfUpdates(boolean __);
 +    public abstract Builder notifyOfBackings(boolean __);
 +    public abstract Builder notifyOfComments(boolean __);
 +    public abstract Builder notifyOfFollower(boolean __);
 +    public abstract Builder notifyOfFriendActivity(boolean __);
 +    public abstract Builder notifyOfUpdates(boolean __);
 +    public abstract Builder promoNewsletter(boolean __);
      public abstract Builder starredProjectsCount(Integer __);
 +    public abstract Builder weeklyNewsletter(boolean __);
      public abstract User build();
    }
```
