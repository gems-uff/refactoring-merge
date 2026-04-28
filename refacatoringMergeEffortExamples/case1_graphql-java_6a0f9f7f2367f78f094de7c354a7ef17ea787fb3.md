# Case 1 — Project: graphql-java — Merge commit SHA1: 6a0f9f7f2367f78f094de7c354a7ef17ea787fb3
---

## Modified file(s):
`src/main/java/graphql/normalized/ExecutableNormalizedOperationFactory.java`

---

## Class(es) modified in the merge:
`ExecutableNormalizedOperationFactory`, `ExecutableNormalizedOperationFactoryImpl` (new inner class)

---

## Merge effort lines in the combined diff

**Fields promoted to `static final` in the outer class:**
```diff
-- private final ConditionalNodes conditionalNodes = new ConditionalNodes();
-- private final IncrementalNodes incrementalNodes = new IncrementalNodes();
++ private static final ConditionalNodes conditionalNodes = new ConditionalNodes();
++ private static final IncrementalNodes incrementalNodes = new IncrementalNodes();
```

**`buildFieldWithChildren` signature — `deferSupport` parameter reconciliation:**
```diff
-- int maxLevel) {
++ int maxLevel,
++ boolean deferSupport) {
```

At recursive call site:
```diff
-- maxLevel);
++ maxLevel,
++ deferSupport);
```

**`ENFMerger.merge` call — `deferSupport` parameter:**
```diff
-- ENFMerger.merge(possibleMerger.parent, childrenWithSameResultKey, graphQLSchema);
++ ENFMerger.merge(possibleMerger.parent, childrenWithSameResultKey, graphQLSchema, options.deferSupport);
```

**`buildFieldWithChildren` call from `createNormalizedQueryImpl`:**
```diff
-- options.getMaxChildrenDepth());
++ options.getMaxChildrenDepth(),
++ options.deferSupport);
```

**In test file — static call reconciliation:**
```diff
-- }
++
```
(closing brace conflict resolved by merge, plus multiple call site reconciliations in test)

---

## Relevant final code in the merge

```java
// Outer class — static fields
private static final ConditionalNodes conditionalNodes = new ConditionalNodes();
private static final IncrementalNodes incrementalNodes = new IncrementalNodes();

// New private inner class encapsulating per-execution state
private static class ExecutableNormalizedOperationFactoryImpl {
    private final GraphQLSchema graphQLSchema;
    private final OperationDefinition operationDefinition;
    private final Map<String, FragmentDefinition> fragments;
    private final CoercedVariables coercedVariableValues;
    private final @Nullable Map<String, NormalizedInputValue> normalizedVariableValues;
    private final Options options;
    // ... builders and lists as instance fields ...

    private ExecutableNormalizedOperation createNormalizedQueryImpl() { ... }

    private void buildFieldWithChildren(ExecutableNormalizedField executableNormalizedField,
                                        ImmutableList<FieldAndAstParent> fieldAndAstParents,
                                        int curLevel,
                                        int maxLevel,
                                        boolean deferSupport) { ... }

    // Other previously-static or previously-parameter-passing methods now as instance methods
}
```

---

## Number of merge-effort lines (`++` and `--`) associated with the refactoring types under analysis:
**14 lines**

---

## What each side had

**Parent 1** had `ExecutableNormalizedOperationFactory` as a stateful class where `createNormalizedQueryImpl` was an instance method, with `conditionalNodes` and `incrementalNodes` as **instance fields** (`private final`). The `buildFieldWithChildren` method had no `deferSupport` parameter — it was passed through `FieldCollectorNormalizedQueryParams`. `ENFMerger.merge` was called without a `deferSupport` argument.

**Parent 2** had already begun refactoring the class: `conditionalNodes` was promoted to `static final`, and `buildFieldWithChildren` received `deferSupport` as an explicit `boolean` parameter. However, `incrementalNodes` remained an instance field, and the inner class `ExecutableNormalizedOperationFactoryImpl` did not yet exist — the logic was still spread across the outer class with accumulated parameters.

The merge had to reconcile both structural directions simultaneously.

---

## Interpretation

This is a multi-refactoring merge effort case with strong `++`/`--` evidence:

### 1. Extract_Class
The most significant refactoring: the private per-execution logic of `createNormalizedQueryImpl` and its supporting methods (`buildFieldWithChildren`, `updateFieldToNFMap`, `updateCoordinatedToNFMap`, `captureMergedField`, `collectFromMergedField`) was extracted from the outer `ExecutableNormalizedOperationFactory` into a new private inner class `ExecutableNormalizedOperationFactoryImpl`. This extraction eliminated the need to pass accumulated state (builders, maps, callbacks) as parameters across method calls — instead, the inner class holds them as instance fields. The `--` lines remove the multi-parameter signatures; the `" +"` lines introduce the inner class body (inherited from P2); but the `++` lines specifically reconcile the conflict between the two parents' structural approaches.

### 2. Pull_Up_Attribute / Split_Attribute
The `++` lines:
```java
++ private static final ConditionalNodes conditionalNodes = new ConditionalNodes();
++ private static final IncrementalNodes incrementalNodes = new IncrementalNodes();
```
represent a conflict between P1 (both as instance fields) and P2 (only `conditionalNodes` promoted to `static`). The merge synthesized the fully promoted `static final` version for **both** fields — a `Pull_Up_Attribute` pattern where instance state is elevated to class-level static state, applicable to both fields simultaneously.

### 3. Split_Parameter / Merge_Parameter
The `++` lines adding `boolean deferSupport` to `buildFieldWithChildren` and its recursive call, and adding `options.deferSupport` to `ENFMerger.merge`, represent a **Split_Parameter** conflict: P1 had no such parameter (it was accessed via `FieldCollectorNormalizedQueryParams`), P2 had introduced it explicitly. The merge had to create `++` lines that thread `deferSupport` correctly through the new inner class structure.

The merge did not simply pick one parent's architecture — it synthesized the `static final` promotion of both fields and the `deferSupport` parameter threading, which neither parent had in a fully consistent form.
