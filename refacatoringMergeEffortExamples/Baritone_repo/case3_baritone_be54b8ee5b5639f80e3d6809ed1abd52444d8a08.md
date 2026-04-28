# Case 3 — Project: baritone — Merge commit SHA1: be54b8ee5b5639f80e3d6809ed1abd52444d8a08

---

## Modified file(s):
`src/launch/java/baritone/launch/mixins/MixinBlockStateContainer.java`

---

## Class(es) modified in the merge:
`MixinBlockStateContainer` → `MixinBlockStateContainer<T>`

---

## Merge effort lines in the combined diff

```diff
-- public abstract class MixinBlockStateContainer implements IBlockStateContainer {
++ public abstract class MixinBlockStateContainer<T> implements IBlockStateContainer<T> {

-  protected IBlockStatePalette<IBlockState> palette;
-- protected IBlockStatePalette palette;
++ protected IBlockStatePalette<T> palette;

-- public IBlockStatePalette getPalette() {
++ public IBlockStatePalette<T> getPalette() {

-- public IBlockState getAtPalette(int index) {
++ public T getAtPalette(int index) {
```

---

## Relevant final code in the merge

```java
@Mixin(BlockStateContainer.class)
public abstract class MixinBlockStateContainer<T> implements IBlockStateContainer<T> {

    @Shadow
    protected BitArray storage;

    @Shadow
    protected IBlockStatePalette<T> palette;

    @Override
    public IBlockStatePalette<T> getPalette() {
        return palette;
    }

    @Override
    public BitArray getStorage() {
        return storage;
    }

    @Override
    public T getAtPalette(int index) {
        return palette.get(index);
    }
}
```

---

## Number of merge-effort lines (`++` and `--`) associated with the refactoring types under analysis:
**8 lines**

---

## What each side had

**Parent 1** had `MixinBlockStateContainer` as a non-generic class implementing the raw `IBlockStateContainer` interface. The `palette` field was typed as `IBlockStatePalette<IBlockState>` (concrete type parameter), and `getAtPalette` returned `IBlockState`.

**Parent 2** had introduced generics: the class became `MixinBlockStateContainer<T>` implementing `IBlockStateContainer<T>`. The `palette` field changed to `IBlockStatePalette<T>` (raw type in P2's version, but intended to be generic), and `getAtPalette` was updated to return `T`. Additionally, `getPalette()` return type changed to `IBlockStatePalette<T>`.

---

## Interpretation

P2 performed a **Change_Return_Type** and **Change_Parameter_Type** refactoring on `MixinBlockStateContainer` by introducing a type parameter `<T>` that propagates through:

1. **Class declaration**: raw `implements IBlockStateContainer` → generic `implements IBlockStateContainer<T>` (lines `--`/`++`)
2. **Field type**: `IBlockStatePalette` (raw) → `IBlockStatePalette<T>` (lines `--`/`++`) — **Replace_Attribute** / **Change_Parameter_Type** on the field
3. **`getPalette()` return type**: raw `IBlockStatePalette` → `IBlockStatePalette<T>` (lines `--`/`++`) — **Change_Return_Type**
4. **`getAtPalette()` return type**: `IBlockState` → `T` (lines `--`/`++`) — **Change_Return_Type**

The merge had to reconcile P1's concrete `IBlockState`-typed version with P2's generic `<T>`-parameterized version, producing `++`/`--` lines at all four declaration sites. This is a clear, defensible example of **Change_Return_Type** applied to two methods simultaneously, driven by the introduction of a type parameter in the class declaration.
