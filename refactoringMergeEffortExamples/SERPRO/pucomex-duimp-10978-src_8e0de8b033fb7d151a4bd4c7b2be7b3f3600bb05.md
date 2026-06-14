# pucomex-duimp-10978-src_8e0de8b033fb7d151a4bd4c7b2be7b3f3600bb05

## Modified file(s):
- `pucomex-ccta-frontend/src/app/carga/gerenciar-associacao/components/dialog-incluir-associacao/dialog-incluir-associacao.component.html`
- `pucomex-ccta-frontend/src/app/carga/gerenciar-associacao/components/dialog-incluir-associacao/dialog-incluir-associacao.component.ts`

## Class(es) affected by the merge effort:
- `DialogIncluirAssociacaoComponent` (the `.ts` component class and its `.html` template)
- Renamed method: `preencherRazaoSocial()` → `preencherNomeResponsavel()`

## Merge effort lines in the combined diff

One side renamed the component method `preencherRazaoSocial()` to `preencherNomeResponsavel()`
(and rewrote its body). The template's `(onBlur)` binding existed in **both** parents pointing at
the old name, so the merge had to remove the old binding from both sides and create a new one
pointing at the renamed method.

### Template call site (`.html`)

```diff
@@@ -61,7 -70,7 +62,7 @@@
  						tipo="cnpj"
  						formControlName="cnpjResponsavel"
  						id="cnpjResponsavel"
--						(onBlur)="preencherRazaoSocial()"
++						(onBlur)="preencherNomeResponsavel()"
  					></pucx-cpf-cnpj>
```

### Method declaration (`.ts`)

```diff
 -    preencherRazaoSocial() {        // Parent 1 / HEAD: old name + old body (discarded)
++  preencherNomeResponsavel() {     // merge: renamed declaration adopted
++    console.log("Cnpj is valid=" + this.formAssociacao.controls['cnpjResponsavel'].valid);
+     if (this.formAssociacao.controls['cnpjResponsavel'].valid) {
```

## Relevant final code in the merge

```html
<pucx-cpf-cnpj
    tipo="cnpj"
    formControlName="cnpjResponsavel"
    id="cnpjResponsavel"
    (onBlur)="preencherNomeResponsavel()"
></pucx-cpf-cnpj>
```

```typescript
preencherNomeResponsavel() {
    console.log("Cnpj is valid=" + this.formAssociacao.controls['cnpjResponsavel'].valid);
    if (this.formAssociacao.controls['cnpjResponsavel'].valid) {
        this.associacoesService.retornarRazaoPessoaJuridica(
            // ...
        ).subscribe(/* ... */);
    } else {
        this.nomeResponsavel = "";
        // ...
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**3 lines** — the `--`/`++` pair on the `.html` `(onBlur)` binding (2 lines) plus the `++`
renamed method declaration in the `.ts` file (1 line).

## What each side had

- **Parent 1 / HEAD**: declared the method under its **old** name `preencherRazaoSocial()`
  (shown as the ` -` discarded declaration in the `.ts` hunk) and bound the template
  `(onBlur)="preencherRazaoSocial()"`.
- **Parent 2**: rewrote the method, **renaming** it to `preencherNomeResponsavel()` and changing
  its body (the surrounding `+ ` context lines in the `.ts` file are Parent 2's new
  implementation). Parent 2 carries the evidence of the rename.

Because the old `(onBlur)="preencherRazaoSocial()"` binding existed in **both** parents, it is
removed from both (`--`) and the renamed binding is created by the merge (`++`).

## Interpretation

The refactoring type evidenced is **Rename_Method**: `preencherRazaoSocial()` →
`preencherNomeResponsavel()`.

The `--` / `++` lines confirm it: the template binding that referenced the old method name had to
be deleted (`--`, since both parents still carried the literal `preencherRazaoSocial()` text) and
re-created (`++`) referencing the renamed method so the template would still resolve against the
component after the rename. The `++` declaration line in the `.ts` shows the renamed method being
adopted into the merged class.

The rename was introduced in a **parent** (Parent 2, which both renames the declaration and
supplies the new body), not by the merge itself: the merge only had to carry the rename through to
the call site that the other parent still expressed with the old name. The case is well supported
because the conflict is visible simultaneously at the declaration site (`.ts`) and the call site
(`.html`), and the resolution consistently adopts the new name in both places.

> Note: the file is a frontend TypeScript/HTML component — it is application source code, not an
> excluded artifact type (SQL/YAML/CI/CD/build/auto-generated), so it is in scope.
