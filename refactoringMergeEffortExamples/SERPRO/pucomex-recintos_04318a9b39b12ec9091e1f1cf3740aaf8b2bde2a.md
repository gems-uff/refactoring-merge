# Project: pucomex-recintos — Merge commit SHA1: 04318a9b39b12ec9091e1f1cf3740aaf8b2bde2a

## Modified file(s):
- `pucomex-recintos-despachante/src/main/java/br/gov/serpro/pucomex/recintos/despachante/infra/delegate/DespachoServiceDelegate.java`

(Parent blobs differ: `index cbbe63e5,f45644d1..835c86a6`, confirming a genuine two-sided conflict.)

## Class(es) affected by the merge effort:
- `DespachoServiceDelegate`

## Merge effort lines in the combined diff

Both parents edited `montaEventoInformativo`. **Parent 1** renamed the accessor `getDtHrTransmissao()` → `getDataHoraTransmissao()` (keeping the method as a single `return`). **Parent 2** restructured the method body into an `if/else` (adding a `dtoEventoAlvo` parameter and branch) but still called the **old** accessor `getDtHrTransmissao()`. The merge kept Parent 2's two-branch structure and rewrote each branch's accessor call to Parent 1's new name — two `++` lines:

```diff
  		return new EventoInformativoDTO(EventosInfoRcnt.get(/**/
  				this.getTipoEventoRecinto(tipoEventoRecinto), /**/
  				this.getTipoOperacaoEvento(tipoOperacao)).getIdentificacao(), /**/
 -				dtoFiltrado.getDadosTransmissao().getDtHrTransmissao(), /**/      // Parent 2 (discarded)
++				dtoFiltrado.getDadosTransmissao().getDataHoraTransmissao(), /**/  // created in the merge
  				dtoFiltrado.getDadosTransmissao().getProtocolo(), null, /**/
```
(The same `getDtHrTransmissao` → `getDataHoraTransmissao` rewrite occurs in the second `else` branch — the other `++` line.)

Parent 1's pre-restructure version (discarded, `- `) shows it already used the new name:

```diff
- 				dtoFiltrado.getDadosTransmissao().getDataHoraTransmissao(), /**/  // Parent 1 (discarded)
```

## Relevant final code in the merge

```java
public EventoInformativoDTO montaEventoInformativo(EventoRecintoDTO dtoFiltrado,
		TipoEventoRecinto tipoEventoRecinto, TipoOperacaoEventoRecinto tipoOperacao,
		EventoRecintoDTO dtoEventoAlvo) {

	if (TipoOperacaoEventoRecinto.INCLUSAO.equals(tipoOperacao)) {
		return new EventoInformativoDTO(EventosInfoRcnt.get(
				this.getTipoEventoRecinto(tipoEventoRecinto),
				this.getTipoOperacaoEvento(tipoOperacao)).getIdentificacao(),
				dtoFiltrado.getDadosTransmissao().getDataHoraTransmissao(),
				dtoFiltrado.getDadosTransmissao().getProtocolo(), null,
				JsonConverter.toJson(dtoFiltrado));
	} else { // Retificacao ou Exclusao
		return new EventoInformativoDTO(EventosInfoRcnt.get(
				this.getTipoEventoRecinto(tipoEventoRecinto),
				this.getTipoOperacaoEvento(tipoOperacao)).getIdentificacao(),
				dtoFiltrado.getDadosTransmissao().getDataHoraTransmissao(),
				dtoFiltrado.getDadosTransmissao().getProtocolo(), null,
				JsonConverter.toJson(dtoFiltrado), JsonConverter.toJson(dtoEventoAlvo));
	}
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**2 lines** — 2 `++` (created in the merge), 0 `--`.

(A third `++` line elsewhere in the file adds an unrelated test-data JSON constant `JSON_CONTROLE_ACESSO_VEICULOS` and is not counted.)

## What each side had

- **Parent 1** (`- ` discarded) — **contains the evidence of the rename**: a single-`return` `montaEventoInformativo` that already calls `dtoFiltrado.getDadosTransmissao().getDataHoraTransmissao()` (the new accessor name).
- **Parent 2** (` -` discarded call lines; `+ ` inherited structure) — restructured the method into an `if/else` with a new `dtoEventoAlvo` parameter, but still called the **old** accessor `getDtHrTransmissao()`.

## Interpretation

The refactoring evidenced by the `++` lines is **Rename_Method**, introduced in **Parent 1**: the accessor `getDtHrTransmissao()` was renamed to `getDataHoraTransmissao()` on the object returned by `dtoFiltrado.getDadosTransmissao()` (the abbreviation `DtHr` expanded to the full words `DataHora`).

**Why the `++` lines confirm it.** Each `++` line is one of Parent 2's two restructured branches with its accessor call swapped from the old name to Parent 1's new name. The lines exist in neither parent verbatim: Parent 1 had the new name but only one `return`; Parent 2 had two branches but the old name. A clean text merge was impossible because Parent 2's branch bodies referenced a method that Parent 1 had renamed away, so the integrator had to combine Parent 2's `if/else` structure with Parent 1's renamed accessor by hand. That manual substitution is the merge effort.

**Why the refactoring belongs to a parent, not the merge.** The new accessor name appears in Parent 1's discarded line (`- `) and the old name in Parent 2's discarded lines (` -`); the merge merely propagated Parent 1's already-completed rename into Parent 2's new control flow. The rename was therefore introduced in a parent, and the `++` effort is the downstream cost of reconciling it — matching rule 7's evidence standard. (This is the same conflict shape as merge `4e58cc4d`, where a parent-side accessor rename forced rewriting of the other parent's call sites.)
