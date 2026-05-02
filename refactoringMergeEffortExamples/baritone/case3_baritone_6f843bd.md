# Case 3 — Project: baritone — Merge commit SHA1: 6f843bd24da1a9ea62f653b216d6e25012392133

## Modified file(s):
- `src/main/java/baritone/pathing/movement/MovementHelper.java`
- `src/main/java/baritone/pathing/movement/movements/MovementPillar.java`

## Class(es) modified in the merge:
`MovementHelper`

## Merge effort lines in the combined diff

```diff
@@@ MovementHelper.java -346,9 -337,11 +345,11 @@@

-     static boolean canPlaceAgainst(IBlockState state) {
-         // TODO isBlockNormalCube isn't the best check for whether or not we can place a block against it.
-         return state.isBlockNormalCube();
+     static boolean canPlaceAgainst(BlockStateInterface bsi, int x, int y, int z, IBlockState state) {
 -        return state.isBlockNormalCube() || state.isFullBlock() || state.getBlock() == Blocks.GLASS || state.getBlock() == Blocks.STAINED_GLASS;
++        return state.isBlockNormalCube() || state.isFullCube() || state.getBlock() == Blocks.GLASS || state.getBlock() instanceof BlockStainedGlass;

@@@ MovementPillar.java -77,10 -77,18 +78,18 @@@

-         if ((MovementHelper.isLiquid(fromState) && !MovementHelper.canPlaceAgainst(fromDown)) || ...
 -        if (from instanceof BlockLiquid || (fromDown.getBlock() instanceof BlockLiquid && context.assumeWalkOnWater)) {
++        if ((MovementHelper.isLiquid(fromState) && !MovementHelper.canPlaceAgainst(context.bsi, x, y - 1, z, fromDown)) || ...
```

## Relevant final code in the merge

```java
// MovementHelper.java
static boolean canPlaceAgainst(BlockStateInterface bsi, int x, int y, int z, IBlockState state) {
    // can we look at the center of a side face of this block and likely be able to place?
    return state.isBlockNormalCube() || state.isFullCube()
        || state.getBlock() == Blocks.GLASS
        || state.getBlock() instanceof BlockStainedGlass;
}
```

```java
// MovementPillar.java
if ((MovementHelper.isLiquid(fromState)
        && !MovementHelper.canPlaceAgainst(context.bsi, x, y - 1, z, fromDown))
        || (MovementHelper.isLiquid(fromDown) && context.assumeWalkOnWater)) {
    // cannot pillar
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
2 lines (2 `++`, 0 `--`)

## What each side had

**Parent 1 (refactoring branch):**
Introduced a richer version of `canPlaceAgainst` that takes `BlockStateInterface bsi, int x, int y, int z` as additional parameters, enabling more context-aware placement checks. Existing call sites in `MovementPillar` were updated to pass `context.bsi` and coordinates:
```
+ static boolean canPlaceAgainst(BlockStateInterface bsi, int x, int y, int z, IBlockState state) {
+     return state.isBlockNormalCube() || state.isFullBlock() || ...
```

**Parent 2 (MC update branch):**
Kept the original single-parameter `canPlaceAgainst(IBlockState state)` signature but updated it with a richer return condition (adding `isFullBlock()` and glass checks), and updated call sites with a different condition check for liquid:
```
- static boolean canPlaceAgainst(IBlockState state) {
-     return state.isBlockNormalCube();
- if (from instanceof BlockLiquid || (fromDown.getBlock() instanceof BlockLiquid && context.assumeWalkOnWater)) {
```

## Interpretation

This case evidences a **Split_Parameter** / **Add_Parameter** refactoring on `canPlaceAgainst` in `MovementHelper`. P1 extended the method signature from `(IBlockState state)` to `(BlockStateInterface bsi, int x, int y, int z, IBlockState state)`, splitting the context information that was previously implicit into explicit parameters. P2 independently improved the return logic of the single-parameter version. The merge had to reconcile both: the `++` on the method body takes the richer return condition from P2 (adding `isFullCube()` and `instanceof BlockStainedGlass`) while the method signature and call site update come from P1. In `MovementPillar`, the `++` line replaces P2's `instanceof BlockLiquid` check (old MC API) with P1's fluid API call that also passes `context.bsi, x, y-1, z` to the new overload. The two `++` lines are directly traceable to the parameter addition refactoring: one in the method body and one at a call site that now passes the additional parameters.

## Complete diff

```diff
diff --cc src/main/java/baritone/pathing/movement/MovementHelper.java
@@@ -346,9 -337,11 +345,11 @@@

-     static boolean canPlaceAgainst(IBlockState state) {
-         // TODO isBlockNormalCube isn't the best check...
-         return state.isBlockNormalCube();
+     static boolean canPlaceAgainst(BlockStateInterface bsi, int x, int y, int z, IBlockState state) {
 -        return state.isBlockNormalCube() || state.isFullBlock() || state.getBlock() == Blocks.GLASS || state.getBlock() == Blocks.STAINED_GLASS;
++        return state.isBlockNormalCube() || state.isFullCube() || state.getBlock() == Blocks.GLASS || state.getBlock() instanceof BlockStainedGlass;
      }

diff --cc src/main/java/baritone/pathing/movement/movements/MovementPillar.java
@@@ -77,10 -77,18 +78,18 @@@

-         if ((MovementHelper.isLiquid(fromState) && !MovementHelper.canPlaceAgainst(fromDown)) || (MovementHelper.isLiquid(fromDown) && context.assumeWalkOnWater)) {
 -        if (from instanceof BlockLiquid || (fromDown.getBlock() instanceof BlockLiquid && context.assumeWalkOnWater)) {
++        if ((MovementHelper.isLiquid(fromState) && !MovementHelper.canPlaceAgainst(context.bsi, x, y - 1, z, fromDown)) || (MovementHelper.isLiquid(fromDown) && context.assumeWalkOnWater)) {
```
