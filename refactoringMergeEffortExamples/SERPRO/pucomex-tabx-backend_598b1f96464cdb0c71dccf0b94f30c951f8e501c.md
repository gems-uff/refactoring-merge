# Project: pucomex-tabx-backend — Merge commit SHA1: 598b1f96464cdb0c71dccf0b94f30c951f8e501c

## Modified file(s):
- `src/main/java/br/gov/serpro/pucomex/tabx/infrastructure/persistence/sqlbuilder/consulta/Where.java`

(Parent blobs differ: `index 7fe8ebde,4d25a144..d424906a`, confirming a genuine two-sided conflict.)

## Class(es) affected by the merge effort:
- `Where`

## Merge effort lines in the combined diff

Parent 1 renamed `filtro.getValor()` to `filtro.getValorQuery()` on the iterated filter object. Parent 2 restructured the same loop body into an `if/else` discriminating local vs foreign-table filters, but its two new branches still called the **old** `filtro.getValor()`. The merge kept Parent 2's two-branch structure and rewrote each branch's accessor call to Parent 1's new name:

```diff
  		for (CampoValor filtro : filtros) {
 -			this.add(filtro.getCampo().formatoQuery(), filtro.getCampo().getTipoPesquisa().getOperador(),  // Parent 1: single call
 -					filtro.getValorQuery(), tipo, parenteseInicial, parenteseFinal);                       // Parent 1: already uses new name
 +			if (filtro.getCampo().getTabela().getCodigo().equals(tabelaCorrente.getCodigo())) {           // Parent 2: new local branch
 +				this.add(filtro.getCampo().formatoQuery(), filtro.getCampo().getTipoPesquisa().getOperador(),
  -					filtro.getValor(), tipo, parenteseInicial, parenteseFinal);                            // Parent 2: old name
++						filtro.getValorQuery(), tipo, parenteseInicial, parenteseFinal);                  // merge: rewritten with new name
 +			} else {
 +				this.addTabelaEstrangeira(filtro.getCampo().formatoQuery(), filtro.getCampo().getTipoPesquisa().getOperador(),
  -					filtro.getValor(), tipo, parenteseInicial, parenteseFinal);                            // Parent 2: old name
++						filtro.getValorQuery(), tipo, parenteseInicial, parenteseFinal);                  // merge: rewritten with new name
 +			}
  		}
```

## Relevant final code in the merge

```java
for (CampoValor filtro : filtros) {
    if (filtro.getCampo().getTabela().getCodigo().equals(tabelaCorrente.getCodigo())) {
        this.add(filtro.getCampo().formatoQuery(), filtro.getCampo().getTipoPesquisa().getOperador(),
                filtro.getValorQuery(), tipo, parenteseInicial, parenteseFinal);
    } else {
        this.addTabelaEstrangeira(filtro.getCampo().formatoQuery(), filtro.getCampo().getTipoPesquisa().getOperador(),
                filtro.getValorQuery(), tipo, parenteseInicial, parenteseFinal);
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**2 lines** — 2 `++` (created in the merge), 0 `--`.

## What each side had

- **Parent 1** (`- ` discarded) — **contains the evidence of the rename**: a single, unbranched call to `this.add(...)` that already passes `filtro.getValorQuery()` (the new accessor).
- **Parent 2** (` -` discarded, `+ ` inherited) — restructured the loop body into an `if/else` (local vs `addTabelaEstrangeira` foreign-table branch), but its two new branches still pass `filtro.getValor()` (the old accessor).

## Interpretation

The refactoring evidenced by the `++` lines is **Rename_Method**, introduced in **Parent 1**: the accessor `getValor()` on `CampoValor` was renamed to `getValorQuery()` (qualifying its purpose as the SQL-query value).

**Why the `++` lines confirm it.** Each `++` line is one of Parent 2's two restructured branches with its accessor call swapped from `getValor()` to `getValorQuery()`. Neither parent contained these lines verbatim: Parent 1 had the new name but no `if/else` branching; Parent 2 had the branching but the old name. The integrator had to combine Parent 2's two-branch structure with Parent 1's renamed accessor by hand — the two `++` lines.

**Why the refactoring belongs to a parent, not the merge.** The new name appears in Parent 1's discarded line (`- `) and the old name in Parent 2's discarded lines (` -`); the merge merely propagated Parent 1's rename into Parent 2's new control flow. Same conflict shape as merges `04318a9b` and `030b60ce` in this campaign — a parent-side accessor rename forces rewriting of the other parent's call sites.
