# Project: ctma-src — Merge commit SHA1: ca58dc27432b96c182cbe6ad08eed797de17e5d2

## Modified file(s)
- `aplicacao/monorepo/rfb/apps/ctma/src/app/relatorios-contabeis/shared/relatorios-contabeis.service.ts`

## Class(es) affected by the merge effort
- `RelatoriosContabeisService` (TypeScript service class)

## Merge effort lines in the combined diff

**(A) The newly extracted helper `gerarRelatorio` introduced by Parent 2 — its signature was rewritten by the merge:**

```diff
 -    gerarRelatorio(uri: string, parametrosEntrada: ParametrosEntradaRelatorio): Observable<void> {
++    gerarRelatorio(
++        uri: string,
++        parametrosEntrada: ParametrosEntradaRelatorio
++    ): Observable<void> {
+         this.spinnerService.show();
+         return this.http.post(uri, parametrosEntrada).pipe(
+             map(FileSaverService.saveAsPdf),
+             finalize(() => this.spinnerService.hide())
+         );
      }
```

**(B) `emitirMovimentacoesDiariasSiafi` — Parent 1 had the inline pattern that Parent 2 extracted, and the merge had to reconcile the two; the `++` lines replace Parent 1's inline implementation with a call to the extracted method:**

```diff
-     public emitirMovimentacoesDiariasSiafi(
-     ): Observable<void> {
-         this.spinnerService.show();
- 
-             .post(
-                 `${this.serviceUrl}/emitir-movimentacoes-diarias-siafi`,
-                 map(FileSaverService.saveAsPdf),
-                 finalize(() => this.spinnerService.hide())
 -    public emitirMovimentacoesDiariasSiafi(parametrosEntrada: ParametrosEntradaRelatorio): Observable<void> {
 -        return this.gerarRelatorio(`${this.serviceUrl}/emitir-movimentacoes-diarias-siafi`, parametrosEntrada);
++    public emitirMovimentacoesDiariasSiafi(
++        parametrosEntrada: ParametrosEntradaRelatorio
++    ): Observable<void> {
++        return this.gerarRelatorio(
++            `${this.serviceUrl}/emitir-movimentacoes-diarias-siafi`,
++            parametrosEntrada
++        );
+     }
```

**(C) `emitirProcessosPorUaContaRecinto` — same pattern; Parent 1's inline implementation was discarded in favor of a call to the extracted helper:**

```diff
 +    public emitirProcessosPorUaContaRecinto(
 +        parametrosEntrada: ParametrosEntradaRelatorio
 +    ): Observable<void> {
-         this.spinnerService.show();
-         this.mensagensGlobaisService.clear();
++        return this.gerarRelatorio(
++            `${this.serviceUrl}/emitir-processos-por-ua-conta-recinto`,
++            parametrosEntrada
++        );
+     }
-         return this.http
-             .post(
-                 `${this.serviceUrl}/emitir-processos-por-ua-conta-recinto`,
-                 parametrosEntrada
-             )
-             .pipe(
-                 map(FileSaverService.saveAsPdf),
-                 finalize(() => this.spinnerService.hide())
-             );
```

## Relevant final code in the merge

```typescript
public emitirMovimentacoesDiariasSiafi(
    parametrosEntrada: ParametrosEntradaRelatorio
): Observable<void> {
    return this.gerarRelatorio(
        `${this.serviceUrl}/emitir-movimentacoes-diarias-siafi`,
        parametrosEntrada
    );
}

public emitirProcessosPorUaContaRecinto(
    parametrosEntrada: ParametrosEntradaRelatorio
): Observable<void> {
    return this.gerarRelatorio(
        `${this.serviceUrl}/emitir-processos-por-ua-conta-recinto`,
        parametrosEntrada
    );
}

gerarRelatorio(
    uri: string,
    parametrosEntrada: ParametrosEntradaRelatorio
): Observable<void> {
    this.spinnerService.show();
    return this.http.post(uri, parametrosEntrada).pipe(
        map(FileSaverService.saveAsPdf),
        finalize(() => this.spinnerService.hide())
    );
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis
- **15 `++` lines** directly associated with **Extract_Method** conflict resolution:
  - 7 lines in `emitirMovimentacoesDiariasSiafi` (lines 110–116 of the combined diff)
  - 4 lines in `emitirProcessosPorUaContaRecinto` body (lines 158–161)
  - 4 lines in the new `gerarRelatorio` signature (lines 174–177)
- **0 `--` lines** associated with this refactoring.

## What each side had

- **Parent 1** kept the original *inline* implementation pattern in multiple methods, e.g. `emitirMovimentacoesDiariasSiafi` and `emitirProcessosPorUaContaRecinto`:
  ```typescript
  // Parent 1 (Pre-merge)
  public emitirMovimentacoesDiariasSiafi(
      parametrosEntrada: ParametrosEntradaRelatorio
  ): Observable<void> {
      this.spinnerService.show();
      return this.http.post(
          `${this.serviceUrl}/emitir-movimentacoes-diarias-siafi`,
          parametrosEntrada
      ).pipe(
          map(FileSaverService.saveAsPdf),
          finalize(() => this.spinnerService.hide())
      );
  }
  ```
  Parent 1 did **not** contain `gerarRelatorio`.

- **Parent 2 contains the evidence of the refactoring.** It introduced the new helper method `gerarRelatorio(uri, parametrosEntrada)` whose body is exactly the `spinnerService.show + http.post + pipe(map(saveAsPdf), finalize(hide))` pattern, and it rewrote the callers to delegate to it:
  ```typescript
  // Parent 2 (Pre-merge)
  public emitirMovimentacoesDiariasSiafi(parametrosEntrada: ParametrosEntradaRelatorio): Observable<void> {
      return this.gerarRelatorio(`${this.serviceUrl}/emitir-movimentacoes-diarias-siafi`, parametrosEntrada);
  }

  gerarRelatorio(uri: string, parametrosEntrada: ParametrosEntradaRelatorio): Observable<void> {
      this.spinnerService.show();
      return this.http.post(uri, parametrosEntrada).pipe(
          map(FileSaverService.saveAsPdf),
          finalize(() => this.spinnerService.hide())
      );
  }
  ```

## Interpretation

The refactoring is **Extract_Method**, introduced **in Parent 2**, and it is unambiguously evidenced by the combined diff:

- The new method `gerarRelatorio(uri, parametrosEntrada)` appears as `+` lines (in Parent 2 and the merge but not in Parent 1) — lines 178–183 of the diff carry the extracted body.
- The body of `gerarRelatorio` is exactly the `spinnerService.show() → http.post(...) → pipe(map(FileSaverService.saveAsPdf), finalize(hide))` sequence that appears as `-` lines (Parent 1 only) inside `emitirMovimentacoesDiariasSiafi` and `emitirProcessosPorUaContaRecinto`. The structural correspondence between the discarded Parent 1 fragments and the new helper body is the hallmark of Extract_Method.
- In Parent 2, the callers (`emitirMovimentacoesDiariasSiafi`, `emitirProcessosPorUaContaRecinto`) were already rewritten to a one-line `return this.gerarRelatorio(uri, parametrosEntrada);`, also visible as ` -` lines in the diff (the single-line versions that Parent 2 held).

The `++` lines are the **merge effort to resolve the conflict** the refactoring caused: Parent 1 still held the long inline body that Parent 2 had already extracted away. The merge could not simply pick one side because Parent 1 had reformatted the surrounding signatures to a multi-line style. The result is a freshly written multi-line invocation of `gerarRelatorio` for each affected caller (the 7 + 4 lines), plus a freshly written multi-line signature for the newly introduced `gerarRelatorio` method (the 4 lines), so the integration of Parent 2's extracted helper fits Parent 1's formatting conventions.

The refactoring was **not** performed during the merge: `gerarRelatorio` and the rewritten one-line callers already existed in Parent 2 as ` -`/` +` (i.e. Parent 2-side) content, which is the diff's evidence that the extraction happened *before* the merge. The merge only paid the cost of integrating it.
