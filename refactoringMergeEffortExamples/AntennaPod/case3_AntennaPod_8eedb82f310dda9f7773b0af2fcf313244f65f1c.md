# Case 3 — Project: AntennaPod — Merge commit SHA1: 8eedb82f310dda9f7773b0af2fcf313244f65f1c

## Modified file(s):
- `core/src/main/java/de/danoeh/antennapod/core/service/download/DownloadServiceNotification.java`

## Class(es) modified in the merge:
- `DownloadServiceNotification`

## Merge effort lines in the combined diff

```diff
              sb.append("• ").append(statuses.get(i).getTitle());
-             sb.append(": ").append(context.getString(DownloadErrorLabel.from(statuses.get(i).getReason())));
+             if (statuses.get(i).getReason() != null) {
 -                sb.append(": ").append(statuses.get(i).getReason().getErrorString(context));
++                sb.append(": ").append(context.getString(DownloadErrorLabel.from(statuses.get(i).getReason())));
+             }
```

## Relevant final code in the merge

```java
sb.append("• ").append(statuses.get(i).getTitle());
if (statuses.get(i).getReason() != null) {
    sb.append(": ").append(context.getString(DownloadErrorLabel.from(statuses.get(i).getReason())));
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
1 line (`++` on the `DownloadErrorLabel.from(...)` call inside the null-guard block)

## What each side had

**Parent 1 (P1)** replaced the instance method call `statuses.get(i).getReason().getErrorString(context)` — where `getErrorString` was a method on the `DownloadError` enum — with a static lookup via a new label class: `context.getString(DownloadErrorLabel.from(statuses.get(i).getReason()))`. This is a **Rename_Method** / **Extract_Class** refactoring: the error-to-string mapping was extracted from `DownloadError.getErrorString()` into a separate `DownloadErrorLabel` utility class with a `from()` factory method. P1 had the new expression without any null guard.

**Parent 2 (P2)** added a null-safety guard `if (statuses.get(i).getReason() != null)` around the old expression, keeping the old `getErrorString(context)` call:
```java
// P2 (old API with null guard, discarded):
 -  if (statuses.get(i).getReason() != null) {
 -      sb.append(": ").append(statuses.get(i).getReason().getErrorString(context));
 -  }
```

## Interpretation

This is a **Rename_Method** conflict: P1 renamed `DownloadError.getErrorString(context)` into a separate static lookup `DownloadErrorLabel.from(reason)` + `context.getString(...)`. P2 simultaneously added a null-guard around the old API call. The merge had to place the new `DownloadErrorLabel.from(...)` expression inside P2's null-guard block — the `++` line is the merge's reconciliation of P1's new API with P2's null-safety addition.

The evidence is clear: the ` -` line shows the old `getErrorString(context)` call from P2; the `++` line writes the new `DownloadErrorLabel.from(...)` expression in its place, inside the null-check that P2 contributed. This is a Medium case (only 1 `++` line), but it is defensible for IEEE TSE because the method name change is directly evidenced and the parent attribution is unambiguous.

## Complete diff

```diff
diff --cc core/src/main/java/de/danoeh/antennapod/core/service/download/DownloadServiceNotification.java
index f5677433f,44a30da81..96ac08c6d
--- a/core/src/main/java/de/danoeh/antennapod/core/service/download/DownloadServiceNotification.java
+++ b/core/src/main/java/de/danoeh/antennapod/core/service/download/DownloadServiceNotification.java
@@@ -136,7 -117,9 +136,9 @@@
                 continue;
             }
             sb.append("• ").append(statuses.get(i).getTitle());
-            sb.append(": ").append(context.getString(DownloadErrorLabel.from(statuses.get(i).getReason())));
+            if (statuses.get(i).getReason() != null) {
 -               sb.append(": ").append(statuses.get(i).getReason().getErrorString(context));
++               sb.append(": ").append(context.getString(DownloadErrorLabel.from(statuses.get(i).getReason())));
+            }
             if (i != statuses.size() - 1) {
                 sb.append("\n");
             }
```
