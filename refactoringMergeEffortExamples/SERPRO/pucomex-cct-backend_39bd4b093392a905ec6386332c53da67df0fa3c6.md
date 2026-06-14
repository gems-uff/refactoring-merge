# Project: pucomex-cct-backend — Merge commit SHA1: 39bd4b093392a905ec6386332c53da67df0fa3c6

## Modified file(s):
- `pucomex-cct-business/src/main/java/br/gov/serpro/pucomex/cct/manifestacao/internacional/ManifestacaoInternacionalBC.java`
- `pucomex-cct-business/src/main/java/br/gov/serpro/pucomex/cct/operacao/business/DocumentoTransporteBC.java`
- `pucomex-cct-service-int/src/main/java/br/gov/serpro/pucomex/cct/interno/util/RepresentacaoCoverEmpresas.java`
- (Corroborating, no merge-effort lines: `FactoryImprimirMic.java`)

## Class(es) affected by the merge effort:
- `IntegracaoCNPJBC` (the integration class whose method `obterCNPJ(...)` was renamed to `obterCNPJComEndereco(...)`)
- `ManifestacaoInternacionalBC`, `DocumentoTransporteBC`, `RepresentacaoCoverEmpresas` (callers whose call sites were reconciled)

## Merge effort lines in the combined diff
`ManifestacaoInternacionalBC.java` (representative — same pattern x3 in this file):
```diff
 -				: integracaoCNPJBC.get().obterCNPJComEndereco(localCompleto.getCpfCnpjResponsavelChave())
- 				: this.integracaoCNPJBC.get().obterCNPJ(localCompleto.getCpfCnpjResponsavelChave())
++				: this.integracaoCNPJBC.get().obterCNPJComEndereco(localCompleto.getCpfCnpjResponsavelChave())
  				.getNomeEmpresarial());
```

`DocumentoTransporteBC.java` (x2):
```diff
- 				: this.getIntegracaoCNPJBC().obterCNPJ(dados.getCpfCnpjManifestadorChave()).getNomeEmpresarial());
 -				: this.getIntegracaoCNPJBC().obterCNPJComEndereco(dados.getCpfCnpjManifestadorChave()).getNomeEmpresarial());
++				: this.getIntegracaoCNPJBC().obterCNPJComEndereco(dados.getCpfCnpjManifestadorChave()).getNomeEmpresarial());
```

`RepresentacaoCoverEmpresas.java` (x2 — a Parent-1-only new file the merge had to patch):
```diff
- 		return new RepresentacaoCover(this.integracaoCnpjBC.obterCNPJ(identificacao).getNomeEmpresarial(),
++		return new RepresentacaoCover(this.integracaoCnpjBC.obterCNPJComEndereco(identificacao).getNomeEmpresarial(),
  				isTransportador, depositario);
```

Notation recap:
- `"- "` → discarded from **Parent 1**: the call used the **old** name `obterCNPJ(...)`.
- `" -"` → discarded from **Parent 2**: the call used the **new** name `obterCNPJComEndereco(...)`.
- `"++"` → created in the merge: the reconciled call uses the **new** name `obterCNPJComEndereco(...)` (combined with Parent 1's `this.`/`get()` receiver form where the two parents also differed on the qualifier).

## Relevant final code in the merge
```java
// ManifestacaoInternacionalBC
localCompleto.setCpfCnpjResponsavelValor(Util.isCPF(localCompleto.getCpfCnpjResponsavelChave())
        ? this.integracaoCPFBC.get().obterCPF(localCompleto.getCpfCnpjResponsavelChave()).getNome()
        : this.integracaoCNPJBC.get().obterCNPJComEndereco(localCompleto.getCpfCnpjResponsavelChave())
                .getNomeEmpresarial());

// RepresentacaoCoverEmpresas
return new RepresentacaoCover(this.integracaoCnpjBC.obterCNPJComEndereco(identificacao).getNomeEmpresarial(),
        isTransportador, depositario);
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**7 lines** (7 `++`, 0 `--`):
- `ManifestacaoInternacionalBC.java` — 3 `++` lines
- `DocumentoTransporteBC.java` — 2 `++` lines
- `RepresentacaoCoverEmpresas.java` — 2 `++` lines

(The 2 `++` lines in `CNPJDelegate.java` and the 1 `++` in `CPFDelegate.java` are not counted here: they reconcile a separate dependency-injection change — `Beans.getReference(...).call(...)` → injected `this.delegate.cnpjL003ConsultarCnpj(...)` — and a closing brace, neither of which is one of the refactoring types under analysis.)

## What each side had
- **Parent 1** — used the **old** method name at every call site:
  ```diff
  - this.integracaoCNPJBC.get().obterCNPJ(localCompleto.getCpfCnpjResponsavelChave())
  - this.getIntegracaoCNPJBC().obterCNPJ(dados.getCpfCnpjManifestadorChave()).getNomeEmpresarial())
  - this.integracaoCnpjBC.obterCNPJ(identificacao).getNomeEmpresarial()
  ```

- **Parent 2** — contains the refactoring evidence (the **renamed** method):
  ```diff
  + integracaoCNPJBC.get().obterCNPJComEndereco(localCompleto.getCpfCnpjResponsavelChave())
  + this.getIntegracaoCNPJBC().obterCNPJComEndereco(dados.getCpfCnpjManifestadorChave()).getNomeEmpresarial())
  ```
  In `FactoryImprimirMic.java` (corroborating, no `++`/`--`), the same one-directional change appears as pure Parent-2 adoption (`obterCNPJ` discarded, `obterCNPJComEndereco` kept), confirming the rename belongs to Parent 2 and was applied uniformly across the integration's call sites.

## Interpretation
- **Refactoring type evidenced:** `Rename_Method`. `IntegracaoCNPJBC.obterCNPJ(String)` was renamed to `obterCNPJComEndereco(String)` in Parent 2.
- **Why the `++` lines confirm it:** at each call site the two parents differ only by the method identifier (`obterCNPJ` vs `obterCNPJComEndereco`) — same receiver, same argument, same `.getNomeEmpresarial()` continuation. Git could not auto-merge Parent 1's old-name calls with Parent 2's renamed calls (the lines also diverged on the `this.` qualifier), so the merge re-emitted each call as a `++` line carrying Parent 2's new name. These `++` lines are pure conflict-resolution effort caused by the rename.
- **Why the refactoring was introduced in a parent, not by the merge:** the new name `obterCNPJComEndereco` is carried by Parent 2 (`" -"` lines that already existed on that side, plus the uniform Parent-2 adoption in `FactoryImprimirMic`), while Parent 1 uniformly retained `obterCNPJ` (`"- "` lines). The merge did not coin the new name; it propagated Parent 2's existing rename into the call sites Parent 1 still wrote with the old name — including patching a Parent-1-only new file (`RepresentacaoCoverEmpresas`), which is exactly the maintenance burden a rename imposes on a merge.
- **Why the case is well-supported:** the same rename surfaces as conflict effort across three independent files and seven call sites, every occurrence is attributable to a specific parent via the combined-diff prefixes, and the direction is corroborated by a fourth file's one-sided Parent-2 adoption. The uniform, mechanical nature of the change (and the need to fix even a file absent from Parent 2) is far more consistent with a method rename in Parent 2 than with any per-site behavioral choice.
