# Project: pucomex-tabx-backend — Merge commit SHA1: 030b60ce5f9b2b02fb52760a256789308edcc2fe

## Modified file(s):
- `src/main/java/br/gov/serpro/pucomex/tabx/application/service/ExtracaoMoedaSuce.java`

(Parent blobs differ: `index 0c38f995,8536f738..3fffe95c`, confirming a genuine two-sided conflict.)

## Class(es) affected by the merge effort:
- `ExtracaoMoedaSuce`

## Merge effort lines in the combined diff

Parent 1 renamed `tabelaRepository.obterPorNome(...)` to `tabelaRepository.obterPorNomeAtiva(...)`. Parent 2 introduced two new repository lookups (`tabelaMoeda`, `tabelaTaxaCambio`) that still called the **old** name. The merge kept Parent 2's two new lookups but rewrote them with Parent 1's renamed method — the two `++` lines:

```diff
 -		this.tabela = this.tabelaRepository.obterPorNomeAtiva(NOME_TABELA);                // Parent 1 (discarded; already used new name)
  -		this.tabelaMoeda = this.tabelaRepository.obterPorNome(NOME_TABELA_MOEDA);          // Parent 2 (discarded; old name)
  -		this.tabelaTaxaCambio = this.tabelaRepository.obterPorNome(NOME_TABELA_TAXA_CAMBIO); // Parent 2 (discarded; old name)
++		this.tabelaMoeda = this.tabelaRepository.obterPorNomeAtiva(NOME_TABELA_MOEDA);        // created in the merge
++		this.tabelaTaxaCambio = this.tabelaRepository.obterPorNomeAtiva(NOME_TABELA_TAXA_CAMBIO); // created in the merge
```

## Relevant final code in the merge

```java
public String executar() {
    try {
        this.tabelaMoeda = this.tabelaRepository.obterPorNomeAtiva(NOME_TABELA_MOEDA);
        this.tabelaTaxaCambio = this.tabelaRepository.obterPorNomeAtiva(NOME_TABELA_TAXA_CAMBIO);
        ResultadoExtracao resultadoConsultaDados = this.consultarDados();
        List<String> filtrosMoeda = new ArrayList<>();
        filtrosMoeda.add(this.tabelaMoeda.getCampoNegocio().getNome());
        /* ... Parent 2's restructured body using two-table approach ... */
    } catch (Exception e) {
        return TabxMessages.getInstance().get(TabxMessages.TABX_ER0017, this.tabelaMoeda.getRotulo());
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**2 lines** — 2 `++` (created in the merge), 0 `--`.

## What each side had

- **Parent 1** (`- ` discarded) — **contains the evidence of the rename**: a single-table lookup that already calls `tabelaRepository.obterPorNomeAtiva(NOME_TABELA)`.
- **Parent 2** (` -` discarded, `+ ` inherited) — restructured `executar()` to look up two tables (`tabelaMoeda`, `tabelaTaxaCambio`) and process them separately, but still called the **old** `obterPorNome(...)` on both.

## Interpretation

The refactoring evidenced by the `++` lines is **Rename_Method**, introduced in **Parent 1**: the repository accessor `obterPorNome(String)` was renamed to `obterPorNomeAtiva(String)` (qualifying the lookup as "active").

**Why the `++` lines confirm it.** Each `++` line is one of Parent 2's two new repository-lookup statements, re-expressed with Parent 1's renamed accessor. Neither parent contained these lines verbatim: Parent 1 had the new name but only one lookup (for a single `tabela`); Parent 2 had two lookups but used the old name on both. A clean text merge was impossible — the integrator had to combine Parent 2's two-table structure with Parent 1's renamed accessor, producing the two `++` lines.

**Why the refactoring belongs to a parent, not the merge.** The new name appears in Parent 1's discarded line (`- `) and the old name in Parent 2's discarded lines (` -`). The merge merely propagated Parent 1's already-completed rename into the new code Parent 2 introduced. This is the same conflict shape as merges `4e58cc4d` and `04318a9b`, where a parent-side accessor rename forced rewriting of the other parent's call sites.
