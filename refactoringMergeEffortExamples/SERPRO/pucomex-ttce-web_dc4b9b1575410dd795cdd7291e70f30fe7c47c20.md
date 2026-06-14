# Project: pucomex-ttce-web_dc4b9b1575410dd795cdd7291e70f30fe7c47c20

## Modified file(s):
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/service/HistoricoEventoService.java`
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/domain/EntregaCargaImportador.java`
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/service/EntregaCargaService.java`

## Class(es) affected by the merge effort:
- `HistoricoEventoService` (method rename)
- `EntregaCargaImportador` (attribute rename)
- `EntregaCargaService` (call sites of both)

## Merge effort lines in the combined diff

### A) Rename_Method: `ListarHistoricoConhecimento` → `listarHistoricoConhecimento`, `ListarHistoricoDsic` → `listarHistoricoDsic`

```diff
@@@ HistoricoEventoService.java — method definitions @@@
- 	public List<HistoricoEventoRepresentation> listarHistoricoDsic(Long idDsic) {     // Parent 1 already renamed
 -	public List<HistoricoEventoRepresentation> ListarHistoricoConhecimento(Long idConhecimento) {  // Parent 2 old name
++	public List<HistoricoEventoRepresentation> listarHistoricoConhecimento(Long idConhecimento) {  // merge result
...
 -	public List<HistoricoEventoRepresentation> ListarHistoricoDsic(Long idDsic)      // Parent 2 old name
++	public List<HistoricoEventoRepresentation> listarHistoricoDsic(Long idDsic) {     // merge result
```

```diff
@@@ HistoricoEventoService.java — internal call site @@@
--				.ListarHistoricoConhecimento(id);
++				.listarHistoricoConhecimento(id);
```

### B) Rename_Attribute: `tipoEntregador` → `tipoIntervenienteEntregador` (+ accessor renames)

```diff
@@@ EntregaCargaImportador.java — field declaration @@@
- 	@Column(name = "OPCI_IN_TP_INTERVE")
- 	private Integer tipoEntregador;
++	@Column(name = "OPCI_IN_TP_INTERVE_ENTR")
++	private Integer tipoIntervenienteEntregador;
```

```diff
@@@ EntregaCargaService.java — accessor call sites @@@
- 		entrega.setTipoEntregador(this.historicoEventoService.getCodigoTipoInterveniente());
++		entrega.setTipoIntervenienteEntregador(this.historicoEventoService.getCodigoTipoInterveniente());
...
- 					entrega.getTipoEntradaDadosEnum(), auditoria, conhecimento, null, entrega.getTipoEntregador());
++					entrega.getTipoEntradaDadosEnum(), auditoria, conhecimento, null,
++					entrega.getTipoIntervenienteEntregador());
- 					entrega.getTipoEntradaDadosEnum(), auditoria, dsic, null, entrega.getTipoEntregador());
++					entrega.getTipoEntradaDadosEnum(), auditoria, dsic, null, entrega.getTipoIntervenienteEntregador());
```

## Relevant final code in the merge

```java
// HistoricoEventoService
public List<HistoricoEventoRepresentation> listarHistoricoConhecimento(Long idConhecimento) { ... }
public List<HistoricoEventoRepresentation> listarHistoricoDsic(Long idDsic) { ... }
// ... caller:
... .listarHistoricoConhecimento(id);

// EntregaCargaImportador
@Column(name = "OPCI_IN_TP_INTERVE_ENTR")
private Integer tipoIntervenienteEntregador;

// EntregaCargaService
entrega.setTipoIntervenienteEntregador(this.historicoEventoService.getCodigoTipoInterveniente());
... entrega.getTipoIntervenienteEntregador());
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
8 lines
- Rename_Method (`ListarHistorico*` → `listarHistorico*`): 3 `++` (two definitions + one call site) and 1 `--` (the old-name call site) = 4 lines.
- Rename_Attribute (`tipoEntregador` → `tipoIntervenienteEntregador`): 4 `++` lines (the field declaration and three accessor call sites).

## What each side had
- **Rename_Method (introduced in Parent 1):** Parent 1's side already used the corrected
  lower-case name — e.g. `listarHistoricoDsic` appears as a `- ` (discarded-from-Parent-1)
  context line, showing Parent 1 had renamed `Listar… → listar…`. **Parent 2** still
  declared `ListarHistoricoConhecimento` / `ListarHistoricoDsic` with the capital `L`
  (the ` -` discarded-from-Parent-2 lines). The merge emitted `++` definitions and a `--`/`++`
  call-site swap to settle on the lower-case name.
- **Rename_Attribute (introduced in Parent 2):** the old field `tipoEntregador` with
  `@Column("OPCI_IN_TP_INTERVE")` is on the `- ` (discarded-from-Parent-1) side, whereas
  the renamed field `tipoIntervenienteEntregador` with the new column `OPCI_IN_TP_INTERVE_ENTR`
  is the form the merge adopts (`++`). Parent 1 contributed new callers
  (`registrarHistoricoEvento`, the `setTipoEntregador(...)` call) still using the **old**
  accessor names, so the merge had to retarget them onto the renamed accessors.

Both production files carry **distinct parent blobs** — `HistoricoEventoService.java`
(`5a608c345a,e8d191f803..`), `EntregaCargaImportador.java` (`54ea2455e3,091a7722a2..`),
`EntregaCargaService.java` (`03a232b9fc,18ca5777bf..`) — confirming genuine two-sided conflicts.

## Interpretation
Two refactorings from the list are evidenced, each introduced in a parent (not the merge):
1. **Rename_Method** — `ListarHistoricoConhecimento`/`ListarHistoricoDsic` renamed to the
   lower-cased `listarHistoricoConhecimento`/`listarHistoricoDsic` (done in Parent 1).
   The merge effort consists of emitting the renamed definitions and updating the stale
   caller (`--` old → `++` new) that Parent 2 still referenced under the old casing.
2. **Rename_Attribute** — `tipoEntregador` renamed to `tipoIntervenienteEntregador` (with
   the JPA column and the get/set accessors renamed too; done in Parent 2). Parent 1 added
   code calling the old `getTipoEntregador()`/`setTipoEntregador()`, so the merge produced
   `++` lines retargeting every reference onto the renamed attribute and its accessors.

In both cases the old identifiers come from the non-refactoring parent while the new ones
match the refactoring parent's form; the `++`/`--` lines are the work required to make the
two branches agree on the new names, i.e. genuine conflict-resolution merge effort caused
by parent refactorings — not renames performed by the merge itself.

> Note: changes in `CargaResource.java` (index `e26f373b13,e26f373b13..`, identical parent
> blobs) and the field-injection rearrangements were **not** counted, as the former is
> merge-introduced and the latter is not one of the target refactoring types.
