# pucomex-cct-backend_3c705a1f7860e085d214f254ba0b73687a91e1c5

## Modified file(s):
- `pucomex-ccta-manifestacao/src/main/java/br/gov/serpro/pucomex/ccta/manifestacao/application/validation/HouseWayBillValidation.java` (conflicting call sites — where the merge effort occurs)
- `pucomex-ccta-manifestacao/src/main/java/br/gov/serpro/pucomex/ccta/manifestacao/application/validation/ConhecimentoValidation.java` (where the renamed method definitions originate, in Parent 2)

## Class(es) affected by the merge effort:
- `HouseWayBillValidation`
- `ConhecimentoValidation`

## Merge effort lines in the combined diff

The conflict is the propagation of a method rename (`rngDataEmissaoTransportadorAnterior` → `rngRestritivaDataEmissaoTransportadorAnterior`, and the `Posterior` variant) into call sites that the other branch had concurrently modified.

Renamed method **definitions** contributed by Parent 2 (`+ ` = present only in Parent 2), inside `ConhecimentoValidation`:

```diff
+ 	public void rngRestritivaDataEmissaoTransportadorAnterior(Conhecimento conh, int dias, MultiBusinessException mbe) {
+ 	public void rngRestritivaDataEmissaoTransportadorPosterior(Conhecimento conh, int dias,
```

Conflicting **call sites** in `HouseWayBillValidation.validarCreation(...)`:

```diff
- 		this.conhecimentoValidation.get().rngDataEmissaoTransportadorAnterior(conhecimentoHouse, 360, mbe);
- 		this.conhecimentoValidation.get().rngDataEmissaoTransportadorPosterior(conhecimentoHouse, 90, mbe);
++		this.conhecimentoValidation.get().rngRestritivaDataEmissaoTransportadorAnterior(conhecimentoHouse, 360, mbe);
++		this.conhecimentoValidation.get().rngRestritivaDataEmissaoTransportadorPosterior(conhecimentoHouse, 90, mbe);
```

Notation:
- `- ` = line present in **Parent 1**, discarded by the merge (the old-named calls).
- `+ ` = line present only in **Parent 2** (the renamed method definitions).
- `++` = line **created in the merge** (the merge effort — the renamed call sites).

A corroborating rename in the same hunk, `isHouseAwb` → `isHAWB`, also shows the same shape:

```diff
- 		if (conhecimentosVigentes.stream().filter(Conhecimento::isHouseAwb)
++		if (conhecimentosVigentes.stream().filter(Conhecimento::isHAWB)
```

## Relevant final code in the merge

```java
public void validarCreation(Conhecimento conhecimentoHouse, MultiBusinessException mbe) {
	this.conhecimentoValidation.get().rngLeiFormacaoNumeroAWBXFZB(conhecimentoHouse, mbe);
	this.conhecimentoValidation.get().rngRestritivaDataEmissaoTransportadorAnterior(conhecimentoHouse, 360, mbe);
	this.conhecimentoValidation.get().rngRestritivaDataEmissaoTransportadorPosterior(conhecimentoHouse, 90, mbe);
	this.validarHAWB(conhecimentoHouse, mbe);
	this.validarOrigemDestino(conhecimentoHouse, mbe);
	this.validarRUC(conhecimentoHouse, mbe);
}
```

The merged `validarCreation` invokes the **renamed** validation methods (`rngRestritivaDataEmissaoTransportadorAnterior` / `...Posterior`) defined by Parent 2.

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**2 lines** (the two `++` renamed call sites in `validarCreation`).

> The two `isHouseAwb → isHAWB` `++` reconciliations (lines 266 and 279 of the combined diff) are supporting evidence of the same rename pattern; counting them as well would raise the figure to 4 `++` lines. The primary, cleanest, fully parent-attributable case is the 2-line `rngRestritivaDataEmissaoTransportador*` rename, so the headline count is reported conservatively as 2.

## What each side had

The combined diff is `git diff <merge>^1 <merge>^2 <merge>`; the `HouseWayBillValidation` blobs differ between parents (`index a02baa7046,b9f37f8228..00b32bc233`), and so do the `ConhecimentoValidation` blobs (`index b9a3454483,b56806369b..bd4cde3ae2`), so both files were genuinely modified on both branches.

- **Parent 1** retained the **old method names** and invoked them from `validarCreation`:
  ```diff
  -		this.conhecimentoValidation.get().rngDataEmissaoTransportadorAnterior(conhecimentoHouse, 360, mbe);
  -		this.conhecimentoValidation.get().rngDataEmissaoTransportadorPosterior(conhecimentoHouse, 90, mbe);
  -		... Conhecimento::isHouseAwb ...
  ```
- **Parent 2** introduced the **renamed methods** (the evidence of the refactoring lives here):
  ```diff
  +	public void rngRestritivaDataEmissaoTransportadorAnterior(Conhecimento conh, int dias, MultiBusinessException mbe) { ... }
  +	public void rngRestritivaDataEmissaoTransportadorPosterior(Conhecimento conh, int dias, MultiBusinessException mbe) { ... }
  ```

**The refactoring (Rename_Method) was introduced in Parent 2.** Parent 1 had no knowledge of the new names and kept calling the old ones while independently restructuring `validarCreation`.

## Interpretation

**Refactoring type evidenced: `Rename_Method`** — `rngDataEmissaoTransportadorAnterior` → `rngRestritivaDataEmissaoTransportadorAnterior` and `rngDataEmissaoTransportadorPosterior` → `rngRestritivaDataEmissaoTransportadorPosterior`, on `ConhecimentoValidation`. (A second, corroborating Rename_Method `isHouseAwb` → `isHAWB` appears in the same hunk.)

- **Why it is a parent-side refactoring, not a merge-introduced one:** the renamed method *definitions* are present on the Parent 2 side as `+ ` lines (they exist in Parent 2's blob independently of the merge resolution), while Parent 1's blob still contains the old-named call sites as ` -` lines. The rename therefore pre-existed in Parent 2 before the merge; the merge did not invent it.

- **Why the `++` lines confirm the merge effort:** `validarCreation` was concurrently edited on both branches — Parent 1 changed surrounding statements while still calling the old names; Parent 2 renamed the API. Because the two edits overlap on the same lines, Git could not auto-merge them. The integrator manually reconciled the block by **discarding Parent 1's old-named calls** (` -`) and **emitting the renamed calls** (`++`). Those two `++` lines are exactly the human work required to carry Parent 2's Rename_Method into the region that Parent 1 had also touched.

- **Why the case is well-supported:** the rename is corroborated by (a) Parent 2's renamed method definitions, (b) the matching old→new call-site substitution at the conflict point, and (c) a second independent rename (`isHouseAwb → isHAWB`) resolved with the same old→new shape in the very same hunk. The merge-effort lines sit precisely where Parent 1's and Parent 2's edits collide, making the causal link between the parent-side Rename_Method and the merge effort unambiguous.

- **Classification caveats honored:** this is a rename of existing methods (same parameters, same semantics, new names), classified as `Rename_Method`. The separate addition of a `tiposAWB` parameter to `obterVigente(...)` seen elsewhere in this diff is an *Add Parameter* change, which is **not** among the refactoring types under analysis (it is neither `Split_Parameter`, `Merge_Parameter`, `Change_Parameter_Type`, nor `Rename_Parameter`), and is therefore deliberately excluded from this report.
