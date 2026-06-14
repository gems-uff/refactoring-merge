# Project: pucomex-tabx-backend — Merge commit SHA1: c49c8b683ba8d32fc312d9c06f7e6d8e45fa1350

## Modified file(s):
- `src/main/java/br/gov/serpro/pucomex/tabx/infrastructure/persistence/sqlbuilder/consulta/Where.java`

(Parent blobs differ: `index d424906a,975728ca..815114e3`, confirming a genuine two-sided conflict. Parent 1's blob `d424906a` is the *result* of merge `598b1f96`, so this commit is a downstream merge of the same file with a divergent branch that still carried the pre-rename API.)

## Class(es) affected by the merge effort:
- `Where`

## Merge effort lines in the combined diff

In Parent 1 the rename `getValor()` → `getValorQuery()` has already been applied (inherited from the upstream merge `598b1f96`). Parent 2 contains a divergent rewrite of the same `addTabelaEstrangeira(...)` call — different line wrapping, and still calling the **old** `filtro.getValor()`. The merge kept Parent 2's new line wrapping but rewrote each `getValor()` to Parent 1's `getValorQuery()`:

```diff
  		} else {
 -			this.addTabelaEstrangeira(filtro.getCampo().formatoQuery(), filtro.getCampo().getTipoPesquisa().getOperador(),  // Parent 1: one-line operator group
 -					filtro.getValorQuery(), tipo, parenteseInicial, parenteseFinal);                                       // Parent 1: already uses new name
 +			this.addTabelaEstrangeira(filtro.getCampo().formatoQuery(),                                                    // Parent 2: split wrapping
  -					filtro.getCampo().getTipoPesquisa().getOperador(), filtro.getValor(), tipo, parenteseInicial,          // Parent 2: old name
  -					parenteseFinal);                                                                                       // Parent 2 (discarded)
++					filtro.getCampo().getTipoPesquisa().getOperador(), filtro.getValorQuery(), tipo,                       // merge: P2 wrapping + new name
++					parenteseInicial, parenteseFinal);                                                                     // merge: continuation
```

## Relevant final code in the merge

```java
} else {
    this.addTabelaEstrangeira(filtro.getCampo().formatoQuery(),
            filtro.getCampo().getTipoPesquisa().getOperador(), filtro.getValorQuery(), tipo,
            parenteseInicial, parenteseFinal);
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**2 lines** — 2 `++` (created in the merge), 0 `--`.

## What each side had

- **Parent 1** (`- ` discarded) — **contains the evidence of the rename**: the `addTabelaEstrangeira` call already uses `filtro.getValorQuery()`, with the operator-group fitting on one line.
- **Parent 2** (` -` discarded, ` +` inherited) — split the same call across more lines and still calls `filtro.getValor()` (the old name).

## Interpretation

The refactoring evidenced by the `++` lines is **Rename_Method** `getValor()` → `getValorQuery()` on `CampoValor` — the same rename evidenced by merge `598b1f96`, now propagating into a second branch that had diverged before the rename landed in mainline. **Parent 1** carries the rename (it inherited the rename via the prior merge); **Parent 2** carries the old-name version on the divergent branch.

**Why the `++` lines confirm it.** The two `++` lines reproduce Parent 2's multi-line wrapping of `addTabelaEstrangeira(...)` but substitute Parent 1's `getValorQuery()` for Parent 2's `getValor()`. Selecting either parent verbatim would either drop Parent 2's restructured wrapping (taking Parent 1) or regress the rename (taking Parent 2); the integrator had to hand-author the combined form.

**Why the refactoring belongs to a parent, not the merge.** The new name is present in Parent 1's discarded line and inherited continuations; the old name in Parent 2's discarded lines. The rename was not authored by this merge — it pre-existed in Parent 1's history (introduced upstream of merge `598b1f96`) — and the `++` effort here is the cost of carrying that rename across to a divergent branch that hadn't received it. Same Rename_Method pattern as `4e58cc4d`, `04318a9b`, `030b60ce`, and `598b1f96`.
