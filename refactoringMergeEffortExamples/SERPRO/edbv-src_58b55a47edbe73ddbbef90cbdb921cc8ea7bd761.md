# Project: edbv-src_58b55a47edbe73ddbbef90cbdb921cc8ea7bd761

## Modified file(s):
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/domain/Conhecimento.java`
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/service/BloqueioCargaService.java`
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/service/NotificacaoBloqueioService.java`
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/mapper/ConsultaViagemCargaDetalhadoMapper.java`
- `pucomex-ccta-batch/src/main/java/br/gov/serpro/pucomex/ccta/batch/infrastructure/application/service/DesbloqueioAutomaticoService.java`

## Class(es) affected by the merge effort:
`Conhecimento`, `BloqueioCargaService`, `NotificacaoBloqueioService`, `ConsultaViagemCargaDetalhadoMapper`, `DesbloqueioAutomaticoService`

## Merge effort lines in the combined diff

### Conhecimento.java — method removed and all internal call sites updated

```diff
--  public boolean isHAWB() {
--      return TipoConhecimento.HOUSE_WAYBILL.equals(TipoConhecimento.get(this.tipoAWB));
--  }

--      if (this.isHAWB()) {
++      if (getTipoConhecimento().isHAWB()) {

--          if (!this.isHAWB()) {
++          if (!getTipoConhecimento().isHAWB()) {

--          if (!this.isHAWB()) {
++          if (!getTipoConhecimento().isHAWB()) {

--          if (!this.isHAWB()) {
++          if (!getTipoConhecimento().isHAWB()) {

--          if (!this.isHAWB()) {
++          if (!getTipoConhecimento().isHAWB()) {
```

### DesbloqueioAutomaticoService.java

```diff
--      if (!conhecimento.isHAWB()) {
++      if (!conhecimento.getTipoConhecimento().isHAWB()) {
```

### ConsultaViagemCargaDetalhadoMapper.java

```diff
--          if (Objects.nonNull(conhecimento.getIdentificacaoConsignatario()) && conhecimento.isHAWB()) {
++          if (Objects.nonNull(conhecimento.getIdentificacaoConsignatario()) && conhecimento.getTipoConhecimento().isHAWB()) {

--          if (conhecimento.isHAWB())
++          if (conhecimento.getTipoConhecimento().isHAWB())
```

### BloqueioCargaService.java

```diff
--      if (conh.isHAWB()) {
++      if (conh.getTipoConhecimento().isHAWB()) {
```

### NotificacaoBloqueioService.java

```diff
--                          conhecimentoManaged.isHAWB());
++                          conhecimentoManaged.getTipoConhecimento().isHAWB());

--          if (conhecimentoManaged.isHAWB()) {
++          if (conhecimentoManaged.getTipoConhecimento().isHAWB()) {
```

## Relevant final code in the merge

```java
// Conhecimento.java — isHAWB() method is GONE; internal uses replaced:
public BigDecimal getValorTotalFrete() {
    if (getTipoConhecimento().isHAWB()) { ... }
}
public boolean hasAlgumaChegadaCarga() {
    if (!getTipoConhecimento().isHAWB()) { ... }
}

// Call sites in other classes:
if (!conhecimento.getTipoConhecimento().isHAWB()) { ... }   // DesbloqueioAutomaticoService
if (conh.getTipoConhecimento().isHAWB()) { ... }            // BloqueioCargaService
if (conhecimentoManaged.getTipoConhecimento().isHAWB()) { } // NotificacaoBloqueioService
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**22 lines** (11 `--` lines removing `isHAWB()` occurrences + 11 `++` lines replacing them with `getTipoConhecimento().isHAWB()` across all affected classes, including the method declaration removal itself)

## What each side had

Both P1 and P2 had the same base code for `Conhecimento.isHAWB()` before the merge (the diff index shows identical parent SHAs: `fc55f0398a,fc55f0398a`), confirming both parents had the same version of `Conhecimento`. The `--`/`++` lines therefore represent the merge's own effort to:

- **Remove** the `isHAWB()` convenience method from `Conhecimento` (the `--` on the method declaration).
- **Replace** all 10 call sites across 5 classes with the inlined expression `getTipoConhecimento().isHAWB()`.

Wait — the identical index hashes mean this is a one-sided change: only one parent contributed all changes to `Conhecimento.java` while the other had the old version. The `--`/`++` pairs confirm both the removal of the method and the updates at every call site were merge effort.

**Parent 1** had:
```java
// In Conhecimento.java — isHAWB() still present:
- public boolean isHAWB() {
-     return TipoConhecimento.HOUSE_WAYBILL.equals(TipoConhecimento.get(this.tipoAWB));
- }
// All call sites using the old shorthand:
- if (conhecimento.isHAWB()) { ... }
- if (conh.isHAWB()) { ... }
```

**Parent 2** had (the same as P1, based on identical index hash for Conhecimento):
The diff structure (`fc55f0398a,fc55f0398a..146a702526`) confirms P2 had the same version of `Conhecimento` as P1. The refactoring was introduced during the merge commit itself only if both parents were identical — however, the other files touched (BloqueioCargaService, ConsultaViagemCargaDetalhadoMapper, NotificacaoBloqueioService, DesbloqueioAutomaticoService) each show `--`/`++` pairs where their parents apparently had `conhecimento.isHAWB()`, and the merge replaced all of them uniformly with `getTipoConhecimento().isHAWB()`.

The evidence of the refactoring in the parent side is present in `BloqueioCargaService` and `ConsultaViagemCargaDetalhadoMapper`, where their index hashes differ between P1 and P2 (`e194fadfe9,86762c6c44` and `c8b0760ffc,c8b0760ffc`), and the `--`/`++` pairs show the old `isHAWB()` being removed. The merge had to consistently apply the removal across all files.

## Interpretation

**Refactoring type**: **Inline_Method**.

The `isHAWB()` convenience method on `Conhecimento` was inlined: every call site `x.isHAWB()` was replaced with the inline expression `x.getTipoConhecimento().isHAWB()`. The method declaration itself was then deleted.

This is a textbook **Inline_Method** refactoring: a short delegating method is removed and its body is substituted at each call site. The merge effort (`--`/`++` lines) spans 5 files and eliminates both the method definition and all 10 external call sites, replacing each with the equivalent direct expression.

The refactoring was introduced by a parent branch (evidenced by `BloqueioCargaService` having different parent hashes and showing the `--` removal of `conh.isHAWB()` paired with `++` insertion of `conh.getTipoConhecimento().isHAWB()`). The merge had to propagate this change to all remaining call sites that the branch had not yet updated, hence the large number of `--`/`++` merge effort lines across multiple files.
