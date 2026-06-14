# Project: pucomex-catprodutos_6cc9c808ff558d53a910e2dbe1bb3afc19e70cc5

## Modified file(s):
`pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/infrastructure/persistence/jpa/JPAViagemRepository.java`

## Class(es) affected by the merge effort:
`JPAViagemRepository`

## Merge effort lines in the combined diff

```diff
 +  public boolean existeViagem(ChegadaViagemQuery param) {
 +      StringBuilder sb = new StringBuilder();
 +      sb.append("SELECT count(viagem)");
 -      montarConsultaViagem(sb);
++      this.montarConsultaViagem(sb);
 +      TypedQuery<Long> query = this.getEntityManager().createQuery(sb.toString(), Long.class);
 +  }

-- (blank line removed)

 -  private void montarConsultaViagem(StringBuilder sb) {
 -      sb.append("  FROM Viagem viagem");
 -      sb.append(" WHERE viagem.situacao = :situacao");
 -      sb.append("   AND viagem.numeroVoo = :numeroVoo");
 -      sb.append("   AND viagem.localOrigem.codigo = :aeroportoPartida");
 -      sb.append("   AND function('TO_CHAR', viagem.dataPartidaPrevista,'DD/MM/YYYY') = :dataPartidaPrevista");
 -  }

++  private void montarConsultaViagem(StringBuilder sb) {
++      sb.append("  FROM Viagem viagem");
++      sb.append(" WHERE viagem.situacao = :situacao");
++      sb.append("   AND viagem.numeroVoo = :numeroVoo");
++      sb.append("   AND viagem.localOrigem.codigo = :aeroportoPartida");
++      sb.append("   AND function('TO_CHAR', viagem.dataPartidaPrevista,'DD/MM/YYYY') = :dataPartidaPrevista");
++  }

  public Viagem obterViagem(ChegadaViagemQuery param) {
      StringBuilder sb = new StringBuilder();
      sb.append("SELECT viagem");
 -    sb.append("  FROM Viagem viagem");
 -    sb.append(" WHERE viagem.situacao = :situacao");
 -    sb.append("   AND viagem.numeroVoo = :numeroVoo");
 -    sb.append("   AND viagem.localOrigem.codigo = :aeroportoPartida");
 -    sb.append("   AND function('TO_CHAR', viagem.dataPartidaPrevista,'DD/MM/YYYY') = :dataPartidaPrevista");
 -  montarConsultaViagem(sb);
++      this.montarConsultaViagem(sb);
```

## Relevant final code in the merge

```java
public boolean existeViagem(ChegadaViagemQuery param) {
    StringBuilder sb = new StringBuilder();
    sb.append("SELECT count(viagem)");
    this.montarConsultaViagem(sb);  // extracted call
    TypedQuery<Long> query = this.getEntityManager().createQuery(sb.toString(), Long.class);
    ...
}

private void montarConsultaViagem(StringBuilder sb) {
    sb.append("  FROM Viagem viagem");
    sb.append(" WHERE viagem.situacao = :situacao");
    sb.append("   AND viagem.numeroVoo = :numeroVoo");
    sb.append("   AND viagem.localOrigem.codigo = :aeroportoPartida");
    sb.append("   AND function('TO_CHAR', viagem.dataPartidaPrevista,'DD/MM/YYYY') = :dataPartidaPrevista");
}

public Viagem obterViagem(ChegadaViagemQuery param) {
    StringBuilder sb = new StringBuilder();
    sb.append("SELECT viagem");
    this.montarConsultaViagem(sb);  // extracted call replacing 5 inline appends
    ...
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**10 lines** (1 `++` for `this.montarConsultaViagem(sb)` in `existeViagem`, 7 `++` for the extracted method body declaration, 1 `++` for `this.montarConsultaViagem(sb)` in `obterViagem`, 1 `--` blank line separator removed as part of method repositioning)

## What each side had

**Parent 1** had (evidenced by `" -"` lines):
```java
// obterViagem had 5 inline sb.append calls — not using montarConsultaViagem:
- sb.append("  FROM Viagem viagem");
- sb.append(" WHERE viagem.situacao = :situacao");
- sb.append("   AND viagem.numeroVoo = :numeroVoo");
- sb.append("   AND viagem.localOrigem.codigo = :aeroportoPartida");
- sb.append("   AND function('TO_CHAR', ...) = :dataPartidaPrevista");
// montarConsultaViagem was declared BEFORE getNuviSequence (different location in file)
- private void montarConsultaViagem(StringBuilder sb) { ... }
```

**Parent 2** had (evidenced by `"- "` lines):
```java
// existeViagem called montarConsultaViagem without `this.`:
- montarConsultaViagem(sb);
// obterViagem also called montarConsultaViagem without `this.`:
- montarConsultaViagem(sb);
// montarConsultaViagem was at a different file position (before getNuviSequence in P2)
```

Parent 2 introduced the **Extract_Method** refactoring: the 5 repeated `sb.append` statements in `obterViagem` were extracted into `montarConsultaViagem`, and P2 also used that method in the newly added `existeViagem`. Parent 1 still had the 5 inline appends in `obterViagem`.

## Interpretation

**Refactoring type**: **Extract_Method**.

Parent 2 extracted the repeated JPQL query fragment (5 `sb.append` statements for the `FROM`/`WHERE` clause of the viagem query) into the private helper method `montarConsultaViagem`. This same method was then reused in both `existeViagem` (new method added by P2) and `obterViagem` (existing method refactored by P2).

The conflict arose at two points:
1. **In `obterViagem`**: P1 still had 5 inline `sb.append` calls; P2 had already replaced them with `montarConsultaViagem(sb)`. The merge produced `this.montarConsultaViagem(sb)` (`++`).
2. **Method declaration position**: P1 had `montarConsultaViagem` in a different position (before `getNuviSequence`). P2 placed it after `getNuviSequence`. The merge repositioned it after `getNuviSequence` and added the `this.` qualifier at both call sites.

The refactoring was introduced in Parent 2 (not by the merge itself), as evidenced by P2's call sites already using `montarConsultaViagem(sb)` while P1 still carried the 5 inline append calls. The `++` lines are the necessary merge effort to reconcile P1's inline code with P2's extracted method.
