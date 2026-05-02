# Case 4 — Project: baritone — Merge commit SHA1: 4c9689fe1949b7e0b2dae0c406ee01a3b04af5db

## Modified file(s):
`src/api/java/baritone/api/utils/Helper.java`

## Class(es) modified in the merge:
`Helper` (interface)

## Merge effort lines in the combined diff

```diff
@@@ -80,31 -112,72 +112,68 @@@

-     default void logDirect(ITextComponent... components) {
+     default void logDirect(boolean logAsToast, ITextComponent... components) {
 -        ITextComponent component = new TextComponentString("");
 -        if (!logAsToast) {
 -            component.appendSibling(getPrefix());
 -            component.appendSibling(new TextComponentString(" "));
 -        }
 +        ITextComponent component = new StringTextComponent("");
 +        component.appendSibling(getPrefix());
 +        component.appendSibling(new StringTextComponent(" "));
          Arrays.asList(components).forEach(component::appendSibling);
-         mc.execute(() -> BaritoneAPI.getSettings().logger.value.accept(component));
+         if (logAsToast) {
+             logToast(getPrefix(), component);
+         } else {
 -            mc.addScheduledTask(() -> BaritoneAPI.getSettings().logger.value.accept(component));
++            mc.execute(() -> BaritoneAPI.getSettings().logger.value.accept(component));
+         }
+     }

@@@ -106,7 -112,72 +148,10 @@@
--     * @param message The message to display in chat
--     * @param color   The color to print that message in
++     * @param message    The message to display in chat
++     * @param color      The color to print that message in
```

## Relevant final code in the merge

```java
// Helper.java
default void logDirect(boolean logAsToast, ITextComponent... components) {
    ITextComponent component = new StringTextComponent("");
    component.appendSibling(getPrefix());
    component.appendSibling(new StringTextComponent(" "));
    Arrays.asList(components).forEach(component::appendSibling);
    if (logAsToast) {
        logToast(getPrefix(), component);
    } else {
        mc.execute(() -> BaritoneAPI.getSettings().logger.value.accept(component));
    }
}

default void logDirect(ITextComponent... components) {
    logDirect(BaritoneAPI.getSettings().logAsToast.value, components);
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
3 lines (1 meaningful `++` + 2 `--` Javadoc formatting)

## What each side had

**Parent 1 (toast notification branch):**
Added a `logAsToast` boolean parameter to `logDirect`, transforming the single-signature method into an overloaded pair. P1 also used `mc.addScheduledTask(...)` (old Minecraft API). P1 had:
```
- default void logDirect(boolean logAsToast, ITextComponent... components) {
-     ...
-     if (!logAsToast) {
-         component.appendSibling(getPrefix());
-         ...
-     }
-     mc.addScheduledTask(() -> BaritoneAPI.getSettings().logger.value.accept(component));
```

**Parent 2 (MC update branch):**
Renamed `mc.addScheduledTask(...)` to `mc.execute(...)` (Minecraft 1.14+ API), and kept the original single-parameter signature of `logDirect`. P2 had:
```
+ default void logDirect(ITextComponent... components) {
+     ...
+     mc.execute(() -> BaritoneAPI.getSettings().logger.value.accept(component));
```

## Interpretation

This case evidences a **Parameterize_Variable** refactoring on `logDirect` in the `Helper` interface: P1 added a new `boolean logAsToast` parameter, transforming an implicitly unconditional method into a parameterized one that conditionally routes output to toast or chat. Simultaneously, P2 renamed `mc.addScheduledTask(...)` to `mc.execute(...)`. The merge conflict arose because both parents modified the body of `logDirect`. The `++` line `mc.execute(...)` is the merge resolution that takes the API rename from P2 while placing it inside the conditional structure introduced by P1. The `--` lines are minor Javadoc formatting changes (column alignment in parameter documentation). The `++` line is directly attributable to the conflict between P1's `addScheduledTask` in the new `else` branch and P2's `mc.execute` call, making this a well-supported case.

## Complete diff

```diff
diff --cc src/api/java/baritone/api/utils/Helper.java
@@@ -80,31 -112,72 +112,68 @@@
-     default void logDirect(ITextComponent... components) {
+     default void logDirect(boolean logAsToast, ITextComponent... components) {
 -        ITextComponent component = new TextComponentString("");
 -        if (!logAsToast) {
 -            component.appendSibling(getPrefix());
 -            component.appendSibling(new TextComponentString(" "));
 -        }
 +        ITextComponent component = new StringTextComponent("");
 +        component.appendSibling(getPrefix());
 +        component.appendSibling(new StringTextComponent(" "));
          Arrays.asList(components).forEach(component::appendSibling);
-         mc.execute(() -> BaritoneAPI.getSettings().logger.value.accept(component));
+         if (logAsToast) {
+             logToast(getPrefix(), component);
+         } else {
 -            mc.addScheduledTask(() -> BaritoneAPI.getSettings().logger.value.accept(component));
++            mc.execute(() -> BaritoneAPI.getSettings().logger.value.accept(component));
+         }
+     }

--     * @param message The message to display in chat
--     * @param color   The color to print that message in
++     * @param message    The message to display in chat
++     * @param color      The color to print that message in
```
