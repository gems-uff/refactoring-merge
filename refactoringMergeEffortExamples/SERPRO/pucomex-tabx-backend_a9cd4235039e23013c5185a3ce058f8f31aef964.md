# Project: pucomex-tabx-backend — Merge commit SHA1: a9cd4235039e23013c5185a3ce058f8f31aef964

## Modified file(s):
- `src/main/java/br/gov/serpro/pucomex/tabx/application/service/DadoService.java`
- `src/main/java/br/gov/serpro/pucomex/tabx/application/service/TabelaService.java`

(Parent blobs differ on both files: `5a304f27,f9a1111a` and `00eb454a,b3205541` respectively — confirming genuine two-sided conflicts.)

## Class(es) affected by the merge effort:
- `DadoService`
- `TabelaService`

## Merge effort lines in the combined diff

Parent 1 renamed the repository accessors `tabelaRepository.obterPorNome(...)` → `obterPorNomeAtiva(...)` and `tabelaRepository.listarOrderByNome()` → `listarOrderByNomeAtiva()`. Parent 2 added new methods (`incluir`, `alterar`, `excluir` overloads in `DadoService`; `listarTabelasExterno` in `TabelaService`) whose bodies called the **old** names. The merge kept Parent 2's new methods but rewrote each call site with Parent 1's renamed accessor — five `++` lines:

### `DadoService.java` — `obterPorNome` → `obterPorNomeAtiva` (4 ++ lines)

```diff
   	public void incluir(TabelaInclusaoCommand comando) {
  -		Tabela tabela = this.tabelaRepository.obterPorNome(comando.getNomeTabela());   // Parent 2 (discarded; old name)
++		Tabela tabela = this.tabelaRepository.obterPorNomeAtiva(comando.getNomeTabela());  // created in the merge
   		if (tabela == null) { ... }
   	}

   	public void alterar(TabelaAlteracaoCommand comando) {
  -		Tabela tabela = this.tabelaRepository.obterPorNome(comando.getNomeTabela());
++		Tabela tabela = this.tabelaRepository.obterPorNomeAtiva(comando.getNomeTabela());
   	}

   	public void excluir(TabelaAlteracaoCommand comando) {
  -		Tabela tabela = this.tabelaRepository.obterPorNome(comando.getNomeTabela());
++		Tabela tabela = this.tabelaRepository.obterPorNomeAtiva(comando.getNomeTabela());
   	}

   	public void incluir(String nomeTabela, List<...> campos) {
  -		Tabela tabela = this.tabelaRepository.obterPorNome(nomeTabela);
++		Tabela tabela = this.tabelaRepository.obterPorNomeAtiva(nomeTabela);
   	}
```

### `TabelaService.java` — `listarOrderByNome` → `listarOrderByNomeAtiva` (1 ++ line)

```diff
   	public List<TabelaApiRepresentation> listarTabelasExterno() {                       // Parent 2: new method
   		List<Tabela> tabelas = null;
   		if (this.usuarioAutenticado.isIntervenientePrivado()) {
   			tabelas = this.permissaoOrgaoRepository.listarTabelasPorPermissaoSemOrgaoIntervenientePrivadoOrderByNome(
   					TabxGeneralConstants.SIM.getValor());
   		} else {
  -			tabelas = this.tabelaRepository.listarOrderByNome();          // Parent 2 (discarded; old name)
++			tabelas = this.tabelaRepository.listarOrderByNomeAtiva();     // created in the merge
   		}
   	}
```

## Relevant final code in the merge

```java
// DadoService.java
@Transactional
public void incluir(TabelaInclusaoCommand comando) {
    Tabela tabela = this.tabelaRepository.obterPorNomeAtiva(comando.getNomeTabela());
    if (tabela == null) { /* ... */ }
    /* ... */
}
// Same pattern for alterar(), excluir(), and incluir(String, List)

// TabelaService.java
public List<TabelaApiRepresentation> listarTabelasExterno() {
    List<Tabela> tabelas = null;
    if (this.usuarioAutenticado.isIntervenientePrivado()) {
        tabelas = this.permissaoOrgaoRepository.listarTabelasPorPermissaoSemOrgaoIntervenientePrivadoOrderByNome(
                TabxGeneralConstants.SIM.getValor());
    } else {
        tabelas = this.tabelaRepository.listarOrderByNomeAtiva();
    }
    /* ... */
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**5 lines** — 5 `++` (created in the merge), 0 `--`.

(The diff contains additional `++` lines in `PermissaoOrgaoRepository.java`, `JPAPermissaoOrgaoRepository.java`, `SpringDataJPAPermissaoOrgaoRepository.java`, and the tests, but those are merge-authored declarations of *new* repository methods, not Rename_Method evidence — they are excluded from the count under the conservative interpretation of rule 7.)

## What each side had

- **Parent 1** (` -` / `- ` discarded across the file) — **contains the evidence of the rename**: every call site uses `obterPorNomeAtiva(...)` / `listarOrderByNomeAtiva()` (the new names). Parent 1 also had the renamed declarations on the repository interfaces.

  Example of Parent 1's contribution (` +` clean lines on existing methods elsewhere in the file):
  ```diff
  +		Tabela tabela = this.tabelaRepository.obterPorNomeAtiva(nomeTabela);
  +		List<Tabela> tabelas = this.tabelaRepository.listarOrderByNomeAtiva();
  ```

- **Parent 2** (` -` discarded; `+ ` inherited) — added several new service methods (`incluir`, `alterar`, `excluir` and a non-DTO overload of `incluir`; `listarTabelasExterno`) whose bodies still called the **old** `obterPorNome(...)` / `listarOrderByNome()`.

## Interpretation

Two `Rename_Method` refactorings are evidenced, **both introduced in Parent 1**:

1. `TabelaRepository.obterPorNome(String)` → `obterPorNomeAtiva(String)` (qualifying the lookup as "active").
2. `TabelaRepository.listarOrderByNome()` → `listarOrderByNomeAtiva()` (same qualification).

**Why the `++` lines confirm it.** Each `++` line is a method body Parent 2 newly authored, with its repository call swapped from the old name to Parent 1's new name. Neither parent contained these lines verbatim: Parent 1 had the new names but not Parent 2's new service methods; Parent 2 had the new service methods but called the old names. A clean text merge could not produce the result — the integrator had to combine Parent 2's new method bodies with Parent 1's renamed API, four times for `obterPorNome` and once for `listarOrderByNome`.

**Why the refactoring belongs to a parent, not the merge.** The new names appear in Parent 1's clean ` +` lines (where Parent 1 already used the renamed API in pre-existing methods) and in its discarded ` -` lines for places the merge dropped. The old names appear in Parent 2's discarded ` -` lines, inside method bodies that the merge otherwise adopted from Parent 2. The merge did not invent the rename; it carried Parent 1's already-completed rename into the new code Parent 2 had written against the old API. This is the same conflict shape as merges `4e58cc4d`, `04318a9b`, `030b60ce`, `598b1f96`, and `c49c8b683` in this campaign.

**Why the case is well-supported.** Five `++` lines, distributed across two files and two renamed methods, all sharing one consistent pattern (Parent 2 body + Parent 1 renamed accessor). The naming convention is uniform (each affected method gains an `Ativa` suffix), and the renamed declarations appear on Parent 1's clean lines, providing structural confirmation independent of the call-site evidence.
