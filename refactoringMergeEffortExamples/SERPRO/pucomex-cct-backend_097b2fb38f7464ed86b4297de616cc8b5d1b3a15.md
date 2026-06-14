# Project: pucomex-cct-backend — Merge commit SHA1: 097b2fb38f7464ed86b4297de616cc8b5d1b3a15

## Modified file(s):
- `pucomex-cct-business/src/main/java/br/gov/serpro/pucomex/cct/manifestacao/internacional/factory/FactoryConhecimentoV2.java` (site of the merge effort)
- `pucomex-cct-business/src/main/java/br/gov/serpro/pucomex/cct/manifestacao/internacional/factory/FactoryDocAnexo.java` (corroborating context — no merge-effort lines)

## Class(es) affected by the merge effort:
- `FactoryConhecimentoV2` (caller)
- the `cover` DTO whose accessor was renamed (`getDocsAnexo()` → `getDocumentosEmAnexo()`)

## Merge effort lines in the combined diff
```diff
  		this.getEntidadeAtual().setRegiaoFiscalRemetente(cover.getRegiaoFiscalRemetente());
- 		if (cover.getDocsAnexo() != null) {
 -		this.getEntidadeAtual().getListaDocAnexo().addAll(this.parserDocAnexo.getListaEntidade(cover.getDocumentosEmAnexo()));
++
++		if (cover.getDocumentosEmAnexo() != null) {
 +			this.getEntidadeAtual().setListaDocAnexo(new HashSet<>());
 +			this.getEntidadeAtual().getListaDocAnexo()
- 					.addAll(this.parserDocAnexo.getListaEntidade(cover.getDocsAnexo()));
++					.addAll(this.parserDocAnexo.getListaEntidade(cover.getDocumentosEmAnexo()));
 +		}
```

Notation recap:
- `"- "` → discarded from **Parent 1**: Parent 1 used the **old** accessor `cover.getDocsAnexo()` (both in the `if` guard and in the `addAll(...)` argument).
- `" -"` → discarded from **Parent 2**: Parent 2's single-line variant used the **new** accessor `cover.getDocumentosEmAnexo()`.
- `" +"` → present in **Parent 1**: the structural block (`setListaDocAnexo(new HashSet<>())` + `getListaDocAnexo()`).
- `"++"` → created in the merge: the merge kept Parent 1's structural block but rewrote both accessor calls to Parent 2's **new** name `getDocumentosEmAnexo()`.

## Relevant final code in the merge
```java
this.getEntidadeAtual().setRegiaoFiscalRemetente(cover.getRegiaoFiscalRemetente());

if (cover.getDocumentosEmAnexo() != null) {
    this.getEntidadeAtual().setListaDocAnexo(new HashSet<>());
    this.getEntidadeAtual().getListaDocAnexo()
            .addAll(this.parserDocAnexo.getListaEntidade(cover.getDocumentosEmAnexo()));
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**2 lines** (2 `++`, 0 `--`) — the rewritten `if (cover.getDocumentosEmAnexo() != null)` guard and the `.addAll(... cover.getDocumentosEmAnexo())` argument, both created in the merge using the renamed accessor. (A third `++` line is an inserted blank line and is not counted.)

## What each side had
- **Parent 1** — used the **pre-rename** accessor:
  ```diff
  - if (cover.getDocsAnexo() != null) {
  - 		.addAll(this.parserDocAnexo.getListaEntidade(cover.getDocsAnexo()));
  ```
  Parent 1 also contributed the surrounding null-check + `new HashSet<>()` block structure.

- **Parent 2** — contains the refactoring evidence (the **renamed** accessor):
  ```diff
  + this.getEntidadeAtual().getListaDocAnexo().addAll(this.parserDocAnexo.getListaEntidade(cover.getDocumentosEmAnexo()));
  ```
  Parent 2 invokes `cover.getDocumentosEmAnexo()`.

  Corroborating context in the same combined diff (`FactoryDocAnexo.java`, **no `++`/`--` lines** — pure Parent-2 adoption) shows Parent 2 renamed the DTO type and its accessors as a family:
  ```diff
  - public DocAnexo getEntidade(DocAnexoDTO cover) {            // Parent 1
  + public DocAnexo getEntidade(DocumentoAnexoDTO cover) {      // Parent 2
  - this.docAnexo.setNumeroDocAnexo(cover.getNumeroDocAnexo()); // Parent 1
  + this.docAnexo.setNumeroDocAnexo(cover.getNumero());         // Parent 2
  ```

## Interpretation
- **Refactoring type evidenced:** `Rename_Method`. The accessor `cover.getDocsAnexo()` was renamed to `cover.getDocumentosEmAnexo()`. (The corroborating `FactoryDocAnexo` hunk additionally evidences a `Rename_Class`/`Change_Parameter_Type` of `DocAnexoDTO` → `DocumentoAnexoDTO` in the same parent, but that hunk produced no merge-effort lines, so the reportable effort is the getter rename in `FactoryConhecimentoV2`.)
- **Why the `++` lines confirm it:** the two parents differ on the same call site only by the accessor name (`getDocsAnexo` vs `getDocumentosEmAnexo`). Git could not auto-merge Parent 1's structural block (which referenced the old name) with Parent 2's renamed accessor, so the merge re-emitted the guard and the `addAll(...)` argument as `++` lines carrying Parent 2's new name inside Parent 1's structure. Those `++` lines exist solely to reconcile the rename.
- **Why the refactoring was introduced in a parent, not by the merge:** the renamed accessor `getDocumentosEmAnexo()` is carried by Parent 2 as a `" -"` line (it already existed on the Parent 2 side before the merge), and Parent 1 independently kept the old `getDocsAnexo()` (a `"- "` line). The merge did not invent the new name; it only propagated Parent 2's existing rename into the conflicting block.
- **Why the case is well-supported:** the conflict is contained in one call site with both accessor variants visible and attributed to specific parents, and the rename is corroborated by an independent, parallel rename of the same DTO family in `FactoryDocAnexo`. This is a clean rename-induced merge conflict.
