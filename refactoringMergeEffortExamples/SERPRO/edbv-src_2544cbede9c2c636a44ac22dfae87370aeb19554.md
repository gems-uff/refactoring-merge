# Project: edbv-src — Merge commit SHA1: 2544cbede9c2c636a44ac22dfae87370aeb19554

## Modified file(s)
- `aplicacao/edbv-parent/edbv-viajante/src/main/java/br/gov/serpro/edbv/viajante/view/managedBean/SelecionarAcaoMB.java` (Parent 1 location, package `view.managedBean`)
- `aplicacao/edbv-parent/edbv-viajante/src/main/java/br/gov/serpro/edbv/viajante/view/managedbean/SelecionarAcaoMB.java` (Parent 2 location, package `view.managedbean`)

## Class(es) affected by the merge effort
- `SelecionarAcaoMB`
- (referenced) `AbstractEDBVManagedBean` — its package was also normalized from `view.managedBean` to `view.managedbean`

## Merge effort lines in the combined diff

**Package declaration — one parent held the class in package `...view.managedBean` (capital B); the merge consolidated it into `...view.managedbean` (lowercase b):**

```diff
-  package br.gov.serpro.edbv.viajante.view.managedBean;
++package br.gov.serpro.edbv.viajante.view.managedbean;
```

**Import of the moved superclass — same package-spelling normalization applied to the `AbstractEDBVManagedBean` import:**

```diff
-  import br.gov.serpro.edbv.dominio.view.managedBean.AbstractEDBVManagedBean;
++import br.gov.serpro.edbv.dominio.view.managedbean.AbstractEDBVManagedBean;
```

(Context: in the combined diff, one copy of the class lives at `.../view/managedBean/SelecionarAcaoMB.java` with index `ea08afa1,00000000` — **present in Parent 1, absent in Parent 2** — while a second copy of the same class lives at `.../view/managedbean/SelecionarAcaoMB.java` with index `00000000,9733ef4e` — **absent in Parent 1, present in Parent 2**. The same class body is present under both paths, evidencing the move between package spellings.)

## Relevant final code in the merge

```java
package br.gov.serpro.edbv.viajante.view.managedbean;

// ...
import br.gov.serpro.edbv.dominio.util.EdbvUtil;
import br.gov.serpro.edbv.dominio.view.managedbean.AbstractEDBVManagedBean;
import br.gov.serpro.edbv.viajante.constant.AliasNavigationRule;

@ViewController
public class SelecionarAcaoMB extends AbstractEDBVManagedBean implements Serializable {

    private static final long serialVersionUID = 1L;
    // ...
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis
- **2 `++` lines** directly associated with **Move_Class**:
  - `package br.gov.serpro.edbv.viajante.view.managedbean;`
  - `import br.gov.serpro.edbv.dominio.view.managedbean.AbstractEDBVManagedBean;`
- **0 `--` lines** associated with this refactoring.

(The remaining ~58 `++` lines in this large diff are excluded: a second `SelecionarAcaoMB` under `edbv-mobile` whose `++` lines are `this.`-qualifier and indentation cosmetics; `ErrorMessage.java` enum-constant additions (`Add Attribute`, not in the catalog) inherited from the parents; `messages_pt_BR.properties` resource entries; and `main.xhtml` markup. None carries a catalog refactoring on a `++` line.)

## What each side had

- **Parent 1 contains the evidence of the move.** It held the class under the capital-B package `br.gov.serpro.edbv.viajante.view.managedBean`, importing `AbstractEDBVManagedBean` from the capital-B `br.gov.serpro.edbv.dominio.view.managedBean` package:
  ```java
  // Parent 1 — file at .../view/managedBean/SelecionarAcaoMB.java
  package br.gov.serpro.edbv.viajante.view.managedBean;
  // ...
  import br.gov.serpro.edbv.dominio.view.managedBean.AbstractEDBVManagedBean;
  ```
  In the combined diff these two lines appear as `- ` (Parent-1-discarded) lines at the `managedBean`-path entry.

- **Parent 2** already kept the class (and its superclass import) under the lowercase package `view.managedbean`:
  ```java
  // Parent 2 — file at .../view/managedbean/SelecionarAcaoMB.java
  package br.gov.serpro.edbv.viajante.view.managedbean;
  // ...
  import br.gov.serpro.edbv.dominio.view.managedbean.AbstractEDBVManagedBean;
  ```
  Parent 2's whole class body appears as `+ ` (Parent-2-inherited) lines at the `managedbean`-path entry.

## Interpretation

The refactoring evidenced by the combined diff is **Move_Class** — `SelecionarAcaoMB` was moved from package `br.gov.serpro.edbv.viajante.view.managedBean` (capital B) to `br.gov.serpro.edbv.viajante.view.managedbean` (lowercase b). The referenced superclass `AbstractEDBVManagedBean` underwent the same package move, reflected in its import.

This is **not** a large-scale uniform namespace migration (which rule 3 says to discard). It is surgical and specific — a single class (plus the one superclass it references) relocated between two spellings of one package segment — and the move is confirmed by *structural* context rather than import lines alone:

- The same class body is present under **two distinct file paths** that differ only by the `managedBean` vs `managedbean` package-directory segment, with mutually exclusive parent presence (`ea08afa1,00000000` for the capital-B path vs `00000000,9733ef4e` for the lowercase path). One parent has the class only in the capital-B location; the other only in the lowercase location. That presence/absence pattern across two paths is the defining footprint of a class move.
- The two members of the class that *encode package identity* — the `package` declaration and the `AbstractEDBVManagedBean` import — are exactly the lines the merge had to fabricate (`++`), because the two parents disagreed on the package spelling.

The `++` lines are the **merge effort** caused by this move conflict. Because Parent 1 declared the capital-B package/import and Parent 2 declared the lowercase versions, the merge could inherit neither verbatim; it fabricated the resolved lines adopting the lowercase `managedbean` spelling. The chosen package identity is carried directly on the `++` lines.

The refactoring was **not** introduced by the merge itself: Parent 1's capital-B `package`/`import` lines are present as `- ` (Parent-1-discarded) lines and Parent 2's lowercase class body is present as `+ ` (Parent-2-inherited) lines — both parent-side artifacts predating the merge. The merge only reconciled the two package spellings, selecting the lowercase target and re-emitting the two identity lines.

(This case is structurally identical to the Move_Class reported for merge `360d190635787ba25648699fcd6eacd05f2da11f`, applied here to `SelecionarAcaoMB` rather than `CriarDeclaracaoEntradaDadosViajanteMB`.)
