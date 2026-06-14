# Project: pucomex-tabx-backend — Merge commit SHA1: f4f5b3f364d1296228a8d714162ccebbbb0c3a94

## Modified file(s):
- `src/main/java/br/gov/serpro/pucomex/tabx/domain/validation/CampoValorValido.java`

(Parent blobs differ: `index 9cb8a8c3,b6b3ae9e..72d73682`, confirming a genuine two-sided conflict.)

## Class(es) affected by the merge effort:
- `CampoValorValido`

## Merge effort lines in the combined diff

Two private methods, `validaSeFormatoDataValido` and `validaSeTamanhoValido`, had their signature split in Parent 1 (one `CampoValor` parameter divided into a `Campo` plus a `String` value). Parent 2 kept the old wrapped-object signatures but added a new `tipoData()` clause to the type checks in both methods. The merge kept Parent 1's split signatures and re-emitted Parent 2's added `tipoData()` clause in terms of the new parameters — three `++` lines:

### Method 1 — `validaSeFormatoDataValido` signature contributed by each side
```diff
 -	private boolean validaSeFormatoDataValido(CampoValor campoValor) {            // Parent 2 (discarded)
 +	private boolean validaSeFormatoDataValido(Campo campo, String valor) {        // Parent 1 (inherited)
```

### Method 1 — body reconciled in the merge (merge effort)
```diff
- 			if (!campo.tipoDataHora()) {                                                                 // Parent 1 (discarded; only one condition)
 -			if ((!campoValor.getCampo().tipoDataHora()) && !campoValor.getCampo().tipoData()) {           // Parent 2 (discarded; old object + new tipoData clause)
++			if ((!campo.tipoDataHora()) && !campo.tipoData()) {                                          // created in the merge
```

### Method 2 — `validaSeTamanhoValido` signature contributed by each side
```diff
 -	private void validaSeTamanhoValido(CampoValor campoValor) {                   // Parent 2 (discarded)
 +	private void validaSeTamanhoValido(Campo campo, String valor) {               // Parent 1 (inherited)
```

### Method 2 — body reconciled in the merge (merge effort)
```diff
- 			&& (campo.getTamanho() < Integer.valueOf(valor.length())) && (!campo.tipoDataHora())) {     // Parent 1 (discarded; only !tipoDataHora)
 -			&& (!campoValor.getCampo().tipoDataHora()) && (!campoValor.getCampo().tipoData())) {        // Parent 2 (discarded; old object + new tipoData clause)
++			&& (campo.getTamanho() < Integer.valueOf(valor.length())) && (!campo.tipoDataHora())       // created in the merge
++			&& (!campo.tipoData())) {                                                                  // created in the merge
```

## Relevant final code in the merge

```java
private boolean validaSeFormatoDataValido(Campo campo, String valor) {
    try {
        if ((!campo.tipoDataHora()) && !campo.tipoData()) {
            return true;
        }
        if ((campo.getFormato() == null) || campo.getFormato().isBlank()) {
            return true;
        }
        DateFormat formatter = new SimpleDateFormat(campo.getFormato());
        formatter.parse(valor);
        return true;
    } catch (Exception e) {
        throw new BusinessException(TabxMessages.TABX_IN0012,
                TabxMessages.getInstance().get(TabxMessages.TABX_IN0012, campo.getNome(), campo.getFormato()));
    }
}

private void validaSeTamanhoValido(Campo campo, String valor) {
    if (((valor != null) && (!valor.isBlank())) && (campo.getTamanho() != null)
            && (campo.getTamanho() < Integer.valueOf(valor.length())) && (!campo.tipoDataHora())
            && (!campo.tipoData())) {
        throw new BusinessException(TabxMessages.TABX_IN0041,
                TabxMessages.getInstance().get(TabxMessages.TABX_IN0041, campo.getNome(), campo.getTamanho()));
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**3 lines** — 3 `++` (created in the merge), 0 `--`.

Breakdown: 1 `++` for `validaSeFormatoDataValido` (the reconciled `if`), 2 `++` for `validaSeTamanhoValido` (the multi-line reconciled `if` condition).

## What each side had

- **Parent 1** (` +` inherited / `- ` discarded) — **contains the evidence of the refactoring**. It carries the new split signatures:
  - `private boolean validaSeFormatoDataValido(Campo campo, String valor)`
  - `private void validaSeTamanhoValido(Campo campo, String valor)`

  and the method bodies already address fields directly through `campo.getFormato()`, `campo.getTamanho()`, `campo.tipoDataHora()`, etc., using the second parameter `valor` directly (no `.getValor()` indirection).

- **Parent 2** (` -` discarded, `+ ` inherited) — still carried the **old, unrefactored** API:
  - `private boolean validaSeFormatoDataValido(CampoValor campoValor)`
  - `private void validaSeTamanhoValido(CampoValor campoValor)`

  with every access mediated through `campoValor.getCampo().<...>` / `campoValor.getValor()`. Independently of the split, Parent 2 also **added a new `tipoData()` check** to both methods' type guards (`!tipoData()` joined the existing `!tipoDataHora()`).

## Interpretation

The refactoring evidenced by the `++` lines is **Split_Parameter**, introduced in **Parent 1**: each method's single `CampoValor` parameter was divided into its two semantically related parts — the metadata holder `Campo campo` and the string value `String valor`. The mapping is unambiguous and one-to-one:
- `campoValor.getCampo()` → `campo`
- `campoValor.getValor()` → `valor`

This satisfies the strict definition (one existing parameter divided into two or more semantically related parts, not the addition of an independent parameter — rule 4).

**Why the `++` lines confirm it.** Each `++` line is one of Parent 2's enriched (`tipoData`-aware) type guards re-expressed against Parent 1's split parameters. The lines exist in neither parent verbatim: Parent 1 had `campo`/`valor` but only the original one-clause guard; Parent 2 had the two-clause guard but on `campoValor.getCampo()`. The conflict could not have been resolved by a clean text merge because Parent 2's body referenced an object (`campoValor`) that no longer exists as a parameter in Parent 1's signature, forcing the integrator to manually substitute Parent 1's two split parameters into Parent 2's added clause. That manual substitution is the merge effort.

**Why the refactoring belongs to a parent, not the merge.** The new split signatures appear inherited from Parent 1 (` +`) on both methods, with corresponding ` -` discarded lines from Parent 2 showing the old wrapped-object signatures. The merge did not invent the split — it adopted Parent 1's already-completed Split_Parameter and adapted Parent 2's new clause to it. This is the same conflict shape as merge `pcce_3307f55` in this campaign (where a DTO parameter was split into three Strings), with the additional twist that Parent 2 independently expanded the conditional logic, multiplying the per-clause substitution effort.

**Why the case is well-supported.** The evidence is structural and mutually reinforcing: matching renamed headers on both methods, a consistent DTO-field-to-parameter mapping verifiable line-by-line, and merge-effort lines that exist solely to bridge Parent 1's split signatures with Parent 2's enriched bodies.
