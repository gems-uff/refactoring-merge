# Case 1 — Project: antlr4 — Merge commit SHA1: 3b3fe3da579275b3a1bee91d0914a8b76b356615

## Modified file(s):
`tool/src/org/antlr/v4/codegen/Target.java`

## Class(es) modified in the merge:
`Target`

## Merge effort lines in the combined diff

```diff
@@@ -65,7 -65,7 +65,7 @@@ public abstract class Target
   	protected String[] targetCharValueEscape = new String[255];
   
-- 	private final CodeGenerator gen;
++ 	protected final CodeGenerator gen;
   	private final String language;
   	private STGroup templates;
```

## Relevant final code in the merge

```java
public abstract class Target {
    // ...
    protected String[] targetCharValueEscape = new String[255];

    protected final CodeGenerator gen;   // ← result of the merge
    private final String language;
    private STGroup templates;
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
2 lines (1 `--` + 1 `++`)

## What each side had

**Parent 1 (base branch):**
```
- private final CodeGenerator gen;
```

**Parent 2 (C++ target branch):**
Introduced `CppTarget` as a new subclass of `Target`. `CppTarget` added several overriding methods (`getRecognizerFileName`, `getListenerFileName`, `getVisitorFileName`, `getBaseListenerFileName`, `getBaseVisitorFileName`) that internally call `gen.g.getRecognizerName()` and similar. Because `gen` was declared `private` in `Target`, these methods could not compile in the subclass — the branch therefore changed `gen` to `protected` to allow subclass access. P2 had:
```
+ protected final CodeGenerator gen;
```

## Interpretation

This case evidences a **Replace_Attribute** refactoring: the visibility modifier of the field `gen` in the abstract class `Target` was changed from `private` to `protected`. The change was introduced in Parent 2 to allow the newly added `CppTarget` subclass to access `gen` directly. Parent 1 still had `private`. The merge had to choose one declaration, producing exactly one `--` (discarding the `private` version) and one `++` (inserting `protected final CodeGenerator gen`). The refactoring type is confirmed by the presence of `CppTarget` in the same merge, where `gen` is accessed without a getter — something impossible with `private` visibility. The case is surgical and specific to this single field in a single class.

## Complete diff

```diff
diff --cc tool/src/org/antlr/v4/codegen/Target.java
index b071dbd7a,ec27f5ad6..cfe963271
--- a/tool/src/org/antlr/v4/codegen/Target.java
+++ b/tool/src/org/antlr/v4/codegen/Target.java
@@@ -65,7 -65,7 +65,7 @@@ public abstract class Target 
   	 */
   	protected String[] targetCharValueEscape = new String[255];
   
--	private final CodeGenerator gen;
++	protected final CodeGenerator gen;
   	private final String language;
   	private STGroup templates;
```
