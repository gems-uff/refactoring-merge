# Project: pucomex-duimp-10978-src_36e726f2d1fefbf321ff8af72ca6a963099f6550

## Modified file(s):
- `pucomex-ccta-manifestacao/src/main/java/br/gov/serpro/pucomex/ccta/manifestacao/application/service/ViagemService.java`
- `pucomex-ccta-manifestacao/src/main/java/br/gov/serpro/pucomex/ccta/manifestacao/application/service/RecepcaoCargaService.java`
- `pucomex-ccta-manifestacao/src/main/java/br/gov/serpro/pucomex/ccta/manifestacao/application/service/ChegadaVooService.java`
- `pucomex-ccta-manifestacao/src/main/java/br/gov/serpro/pucomex/ccta/manifestacao/application/mapper/CargaDetalheMapper.java`
- (plus several other mappers/services that consume the renamed accessors)

## Class(es) affected by the merge effort:
- `ViagemService`
- `RecepcaoCargaService`
- `ChegadaVooService`
- `CargaDetalheMapper`
- Domain accessor owner: `Viagem` / `ViagemConhecimento` (collection accessors)

## Merge effort lines in the combined diff

Two method renames performed on one side had to be propagated by the merge to the
call sites that the *other* side still expressed with the old names.

### Rename A — `getViagemConhecimentos()` → `getViagensConhecimento()`

```diff
@@@ -43,102 -43,33 +45,31 @@@ public class ViagemService
+ 	private void associarConhecimentos(Viagem viagem) {
 -		if (viagem.getViagemConhecimentos() != null) {
++		if (CollectionUtils.isNotEmpty(viagem.getViagensConhecimento())) {
+ 			List<ViagemConhecimento> listaViagemConhecimentos = new ArrayList<>();
 -
 -			for (ViagemConhecimento viagemConhecimento : viagem.getViagemConhecimentos()) {
++			for (ViagemConhecimento viagemConhecimento : viagem.getViagensConhecimento()) {
```

```diff
@@@ -182,43 -131,101 +128,92 @@@
+ 	private void atualizarViagemConhecimento(Viagem viagem, Viagem viagemJaRegistrada) {
 -		if (viagem.getViagemConhecimentos() != null) {
++		if (CollectionUtils.isNotEmpty(viagem.getViagensConhecimento())) {
 -			for (ViagemConhecimento viagemConhecimento : viagem.getViagemConhecimentos()) {
++			for (ViagemConhecimento viagemConhecimento : viagem.getViagensConhecimento()) {
```

Other files reconciled by the merge with the same rename:

```diff
--		builder.conhecimentos(ViagemConhecimentoMapper.get(param.getViagemConhecimentos()));
++		builder.conhecimentos(ViagemConhecimentoMapper.get(param.getViagensConhecimento()));
--		builder.cargas(CargaDetalhadaSemTipoOuAwbOuMawbMapper.get(param.getViagemConhecimentos()));
++		builder.cargas(CargaDetalhadaSemTipoOuAwbOuMawbMapper.get(param.getViagensConhecimento()));
--		Optional.ofNullable(viagem.getViagemConhecimentos())
++		Optional.ofNullable(viagem.getViagensConhecimento())
--		for (ViagemConhecimento vc : viagem.getViagemConhecimentos()) {
++		for (ViagemConhecimento vc : viagem.getViagensConhecimento()) {
```

### Rename B — `getTratamentoEspecialCarga()` → `getTratamentosEspeciaisCarga()`

```diff
@@@ -182,43 -131,101 +128,92 @@@
+ 	private void atualizarTratamentoEspecialCarga(ViagemConhecimento viagemConhecimento) {
 -		if (viagemConhecimento.getTratamentoEspecialCarga() != null) {
 -			for (TratamentoEspecialCarga tratamentoEspecialCarga : viagemConhecimento.getTratamentoEspecialCarga()) {
++		if (CollectionUtils.isNotEmpty(viagemConhecimento.getTratamentosEspeciaisCarga())) {
++			for (TratamentoEspecialCarga tratamentoEspecialCarga : viagemConhecimento.getTratamentosEspeciaisCarga()) {
 -			viagemConhecimento.getTratamentoEspecialCarga().addAll(viagemConhecimento.getTratamentoEspecialCarga());
++			viagemConhecimento.getTratamentosEspeciaisCarga().addAll(viagemConhecimento.getTratamentosEspeciaisCarga());
```

## Relevant final code in the merge

```java
private void atualizarViagemConhecimento(Viagem viagem, Viagem viagemJaRegistrada) {
    if (CollectionUtils.isNotEmpty(viagem.getViagensConhecimento())) {
        this.atualizarEquipamentoTransporte(viagem, viagemJaRegistrada);
        for (ViagemConhecimento viagemConhecimento : viagem.getViagensConhecimento()) {
            this.atualizarClassificacaoMercadoria(viagemConhecimento);
            this.atualizarManuseioCarga(viagemConhecimento);
            this.atualizarObservacaoEmbarqueCarga(viagemConhecimento);
            this.atualizarTratamentoEspecialCarga(viagemConhecimento);
        }
    }
}

private void atualizarTratamentoEspecialCarga(ViagemConhecimento viagemConhecimento) {
    if (CollectionUtils.isNotEmpty(viagemConhecimento.getTratamentosEspeciaisCarga())) {
        for (TratamentoEspecialCarga tratamentoEspecialCarga : viagemConhecimento.getTratamentosEspeciaisCarga()) {
            tratamentoEspecialCarga.setViagemConhecimento(viagemConhecimento);
        }
        viagemConhecimento.getTratamentosEspeciaisCarga()
            .addAll(viagemConhecimento.getTratamentosEspeciaisCarga());
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**45 lines** — 42 `++`/`--` lines carrying the `getViagemConhecimentos → getViagensConhecimento`
rename, and 3 `++` lines carrying the `getTratamentoEspecialCarga → getTratamentosEspeciaisCarga`
rename.

## What each side had

- **Parent 2** (the `-131,101` / `-` side of the combined diff) still used the **old**
  accessor names throughout: `viagem.getViagemConhecimentos()` and
  `viagemConhecimento.getTratamentoEspecialCarga()`. These appear as single `-` (` -`)
  context lines that were discarded from Parent 2.
- **Parent 1 / HEAD** (the `+` side) had already **renamed** the accessors to
  `getViagensConhecimento()` and `getTratamentosEspeciaisCarga()`; the surrounding
  `+ ` context lines (the bodies of `associarConhecimentos`, `atualizarViagemConhecimento`,
  `atualizarTratamentoEspecialCarga`) belong to Parent 1's renamed code.

The evidence of the refactoring is therefore located in **Parent 1**: it carries the renamed
method declarations and their consistent usage, while Parent 2 carries the pre-rename usage.

## Interpretation

The refactoring type evidenced is **Rename_Method** (collection accessor renames):
`getViagemConhecimentos()` → `getViagensConhecimento()` and
`getTratamentoEspecialCarga()` → `getTratamentosEspeciaisCarga()`.

The `++` / `--` lines confirm it because, on the exact lines where the two parents overlapped,
the combined diff removes the old-name invocation (`--` / discards the ` -` Parent-2 form) and
creates a new line invoking the renamed accessor (`++`). The merge could not simply take one
side verbatim: Parent 2's surrounding logic (the loop bodies, the `final`/null guards) had to be
preserved while substituting the renamed accessor that Parent 1 introduced. That substitution is
the merge effort.

The refactoring was introduced in **Parent 1**, not by the merge: the renamed identifiers exist
as Parent-1 context (`+ `) across many already-converted call sites, and Parent 2 uniformly shows
the pre-rename names. The merge's role was purely to reconcile Parent 2's still-old call sites with
Parent 1's rename — a textbook rename-induced merge conflict. The case is well supported by the
high count (45) of mutually consistent rename-bearing merge-effort lines spread across multiple
independent files.
