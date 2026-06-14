# Project: pucomex-catprodutos_613879ba1a6b4695a44b26c4df3e6f6cc4f3abbb

## Modified file(s):
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/service/BloqueioCargaService.java`

## Class(es) affected by the merge effort:
- `BloqueioCargaService`

## Merge effort lines in the combined diff

The conflict and its resolution occur inside the method `gerarBloqueioCargaAutomatico(...)`. The relevant region of the combined diff is:

```diff
 -	 * @param dataRecebimento
 +	 * @param conh
 +	 * @param dataBloqueio
  	 * @param motivo
  	 */
 -	private void gerarBloqueioCargaAutomatico(Conhecimento conhecimento, ZonedDateTime dataRecebimento,
 +	private void gerarBloqueioCargaAutomatico(Conhecimento conh, ZonedDateTime dataBloqueio,
  			MotivoBloqueioAutomatico motivo) {
  		List<MotivoTipoBloqueioCarga> listaMotivoTipo = this.motivoRepository.get().listar(motivo,
 -				conhecimento.getCategoriaCargaEnum(), true);
 +				conh.getCategoriaCargaEnum(), true);
  		Set<Long> idsMotivoTipo = new HashSet<>();
  		listaMotivoTipo.stream().forEach(mt -> idsMotivoTipo.add(mt.getId()));
 -		if (this.hasBloqueioAtivoMotivo(conhecimento, idsMotivoTipo)) {
 +		if (this.hasBloqueioAtivoMotivo(conh, idsMotivoTipo)) {
  			return;
  		}
  		for (MotivoTipoBloqueioCarga item : listaMotivoTipo) {
 -			BloqueioCarga bloqueio = BloqueioCargaMapper.getBloqueioAutomatico(conhecimento, dataRecebimento, item,
 +			BloqueioCarga bloqueio = BloqueioCargaMapper.getBloqueioAutomatico(conh, dataBloqueio, item,
  					BLOQUEIO_AUTOMATICO);
  			this.rngInclusaoPrazoDesbloqueioAutomatico(bloqueio, item);
 +			conh.addBloqueioCarga(bloqueio);
+ 			bloqueio.setBloqueioDesbloqueioDeveSerInformadoENotificado(true);
 -			conhecimento.addBloqueioCarga(bloqueio);
++			conh.addBloqueioCarga(bloqueio);
  		}
  	}
```

The two lines that constitute the actual **merge effort** are the final pair:

```diff
--			conhecimento.addBloqueioCarga(bloqueio);
++			conh.addBloqueioCarga(bloqueio);
```

(The ` -` / ` +` / `+ ` lines above are parent-side context shown only to make the conflict and its resolution self-evident.)

## Relevant final code in the merge

```java
private void gerarBloqueioCargaAutomatico(Conhecimento conh, ZonedDateTime dataBloqueio,
		MotivoBloqueioAutomatico motivo) {
	List<MotivoTipoBloqueioCarga> listaMotivoTipo = this.motivoRepository.get().listar(motivo,
			conh.getCategoriaCargaEnum(), true);
	Set<Long> idsMotivoTipo = new HashSet<>();
	listaMotivoTipo.stream().forEach(mt -> idsMotivoTipo.add(mt.getId()));
	if (this.hasBloqueioAtivoMotivo(conh, idsMotivoTipo)) {
		return;
	}
	for (MotivoTipoBloqueioCarga item : listaMotivoTipo) {
		BloqueioCarga bloqueio = BloqueioCargaMapper.getBloqueioAutomatico(conh, dataBloqueio, item,
				BLOQUEIO_AUTOMATICO);
		this.rngInclusaoPrazoDesbloqueioAutomatico(bloqueio, item);
		bloqueio.setBloqueioDesbloqueioDeveSerInformadoENotificado(true);
		conh.addBloqueioCarga(bloqueio);
	}
}
```

The merged method keeps the **renamed parameters** (`conh`, `dataBloqueio`) throughout, fuses Parent 2's new statement (`bloqueio.setBloqueioDesbloqueioDeveSerInformadoENotificado(true)`), and emits a single reconciled call `conh.addBloqueioCarga(bloqueio)`.

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**2 lines** (1 `--` and 1 `++`).

> Note: the remaining `--` lines elsewhere in this combined diff are blank-line / whitespace removals and comment reflow (cosmetic), and are therefore excluded from this count.

## What each side had

The combined diff is `git diff <merge>^1 <merge>^2 <merge>` and the file blob hashes differ between parents (`index 3592dea7e2,2eb7353f7a..05d26657f5`), so both parents genuinely modified this file.

- **Parent 1** (column 1, ` -` lines): kept the **original parameter names**.
  ```diff
  -	private void gerarBloqueioCargaAutomatico(Conhecimento conhecimento, ZonedDateTime dataRecebimento,
  -				conhecimento.getCategoriaCargaEnum(), true);
  -		if (this.hasBloqueioAtivoMotivo(conhecimento, idsMotivoTipo)) {
  -			BloqueioCarga bloqueio = BloqueioCargaMapper.getBloqueioAutomatico(conhecimento, dataRecebimento, item, ...
  -			conhecimento.addBloqueioCarga(bloqueio);
  ```
- **Parent 2** (column 2 / ` +` reconciled side, plus the `+ ` only-in-P2 line): **renamed** the parameters `conhecimento → conh` and `dataRecebimento → dataBloqueio` consistently across the method body and Javadoc, and additionally introduced a new statement.
  ```diff
  +	 * @param conh
  +	 * @param dataBloqueio
  +	private void gerarBloqueioCargaAutomatico(Conhecimento conh, ZonedDateTime dataBloqueio,
  +				conh.getCategoriaCargaEnum(), true);
  +		if (this.hasBloqueioAtivoMotivo(conh, idsMotivoTipo)) {
  +			BloqueioCarga bloqueio = BloqueioCargaMapper.getBloqueioAutomatico(conh, dataBloqueio, item, ...
  +			conh.addBloqueioCarga(bloqueio);
  + 			bloqueio.setBloqueioDesbloqueioDeveSerInformadoENotificado(true);   // only in Parent 2
  ```

The **evidence of the refactoring resides in Parent 2**: the parameter `conhecimento` was renamed to `conh` and `dataRecebimento` to `dataBloqueio`, updating the Javadoc `@param` tags and every usage inside the method consistently — the textbook signature of **Rename_Parameter**.

## Interpretation

**Refactoring type evidenced: `Rename_Parameter`** (`conhecimento → conh`, `dataRecebimento → dataBloqueio`) in the method `BloqueioCargaService.gerarBloqueioCargaAutomatico(...)`.

- **Why it is a parent-side refactoring, not a merge-introduced one:** the two parent blob hashes differ (`3592dea7e2` vs `2eb7353f7a`), and the rename appears on the Parent 2 side consistently across the Javadoc and all method-body usages, while Parent 1 retained the original identifiers. The rename therefore already existed in Parent 2 *before* the merge; it was not created by the merge commit.

- **Why the `++` / `--` lines confirm the merge effort:** at the last statement of the loop, Parent 1 contributed `conhecimento.addBloqueioCarga(bloqueio);` (old name) while Parent 2 contributed both the renamed call `conh.addBloqueioCarga(bloqueio);` and a new sibling statement `bloqueio.setBloqueioDesbloqueioDeveSerInformadoENotificado(true);`. Git could not auto-reconcile this overlapping region: the same logical statement existed under two different identifier names on the two sides. The integrator manually resolved it by **removing** the old-named line (`--	conhecimento.addBloqueioCarga(bloqueio);`) and **emitting** the renamed line (`++	conh.addBloqueioCarga(bloqueio);`). That `--`/`++` pair is precisely the human work required to carry Parent 2's Rename_Parameter through the conflicting block contributed by Parent 1.

- **Why the case is well-supported:** the rename is corroborated independently by (a) the Javadoc `@param` retagging, (b) the renamed method signature, and (c) multiple consistent in-body usages — none of which are speculative. The merge-effort lines sit exactly at the one spot where Parent 1's edits and Parent 2's renamed-and-extended edits overlapped, making the causal link between the parent-side Rename_Parameter and the merge effort unambiguous.

- **Classification caveats honored:** this is a genuine rename of existing parameters (same arity, same types, same semantics, new names), not a `Split_Parameter` or `Merge_Parameter`. No parameter was divided into multiple parts and none were fused, so the stricter parameter-refactoring definitions do not apply here.
