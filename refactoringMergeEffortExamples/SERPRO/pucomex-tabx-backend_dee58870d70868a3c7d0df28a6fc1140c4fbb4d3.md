# Project: pucomex-tabx-backend_598b1f96464cdb0c71dccf0b94f30c951f8e501c

## Modified file(s):
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/service/ConsultarCargaDetalheService.java`

## Class(es) affected by the merge effort:
- `ConsultarCargaDetalheService`

## Merge effort lines in the combined diff

The `adicionarDominioCNPJ` / CPF logic that used to be **inline** in Parent 1 was
**extracted into dedicated private methods** in Parent 2. The merge had to drop Parent 1's
inline bodies and call the extracted methods, adopting the `this.` qualification:

```diff
@@@ adicionarDominioCNPJ(...) @@@
 -		adicionarDominioCNPJInterveniente(representation, cnpjs);
 -
 -		adicionarDominioCNPJDesconsolidacao(representation, cnpjs);
 -
++		this.adicionarDominioCNPJInterveniente(representation, cnpjs);
++
++		this.adicionarDominioCNPJDesconsolidacao(representation, cnpjs);
+ 		if (representation.getInformacaoGeral().getInfoArquivo() != null) {
+ 			...
+ 	private void adicionarDominioCNPJDesconsolidacao(CargaDetalheRepresentation representation, Set<String> cnpjs) {
```

```diff
@@@ adicionarDominioCNPJDesconsolidacao(...) @@@
 -				adicionarDominioCNPJDesconsolidacaoHouses(representation, cnpjs);
 -
++				this.adicionarDominioCNPJDesconsolidacaoHouses(representation, cnpjs);
```

```diff
@@@ adicionarDominioCPF(...) — Parent 1 inline block discarded, replaced by extracted call @@@
- 		if (representation.getInterveniente() != null) {
- 			if ((representation.getInterveniente().getConsignatario() != null)
- 					&& (representation.getInterveniente().getConsignatario().getDocumento() != null)
- 					&& representation.getInterveniente().getConsignatario().getDocumento().getTipo()
- 					.equals(TipoDocumentoId.CPF.getChaveValor())) {
- 				cpfs.add(representation.getInterveniente().getConsignatario().getDocumento().getNumero());
- 			}
- 			...
- 		}
 -		adicionarDominioCPFInterveniente(representation, cpfs);
++		this.adicionarDominioCPFInterveniente(representation, cpfs);
+ 	private void adicionarDominioCPFInterveniente(CargaDetalheRepresentation representation, Set<String> cpfs) {
```

## Relevant final code in the merge

```java
private void adicionarDominioCNPJ(CargaDetalheRepresentation representation, Set<String> cnpjs) {
    this.adicionarDominioCNPJInterveniente(representation, cnpjs);
    this.adicionarDominioCNPJDesconsolidacao(representation, cnpjs);
    ...
}

// extracted methods (defined in Parent 2, inherited with `+ ` prefix):
private void adicionarDominioCNPJDesconsolidacao(CargaDetalheRepresentation representation, Set<String> cnpjs) { ... }
private void adicionarDominioCNPJDesconsolidacaoHouses(CargaDetalheRepresentation representation, Set<String> cnpjs) { ... }
private void adicionarDominioCNPJInterveniente(CargaDetalheRepresentation representation, Set<String> cnpjs) { ... }
private void adicionarDominioCPFInterveniente(CargaDetalheRepresentation representation, Set<String> cpfs) { ... }
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
4 lines (`++`) — the four extracted-method call sites:
`this.adicionarDominioCNPJInterveniente(...)`, `this.adicionarDominioCNPJDesconsolidacao(...)`,
`this.adicionarDominioCNPJDesconsolidacaoHouses(...)`, `this.adicionarDominioCPFInterveniente(...)`.

## What each side had
- **Parent 1** kept the domain-collection logic **inline** inside `adicionarDominioCNPJ` /
  the CPF method (the long `if (representation.getInterveniente() != null) { ... }` blocks,
  shown as `- ` discarded-from-Parent-1 lines), and where it did call helpers it used the
  **unqualified** form `adicionarDominioCNPJInterveniente(...)` (the ` -` discarded-from
  -Parent-1 call lines).
- **Parent 2** is where the **refactoring lives**: it introduced the extracted private
  methods `adicionarDominioCNPJDesconsolidacao`, `adicionarDominioCNPJDesconsolidacaoHouses`,
  `adicionarDominioCNPJInterveniente`, and `adicionarDominioCPFInterveniente` (their bodies
  appear with the `+ ` prefix, inherited from Parent 2).

## Interpretation
The refactoring is **Extract_Method**, introduced in **Parent 2**: blocks of inline
CNPJ/CPF domain-collection logic were pulled out into the named private helper methods.
Parent 1 still carried the equivalent code inline (and called the pre-existing helpers
without the `this.` qualifier). The two branches conflicted because the same regions of
`ConsultarCargaDetalheService` were both rewritten — one branch extracting the logic, the
other leaving it inline with a different call convention. The merge resolved the conflict
by discarding Parent 1's inline bodies and emitting `++` calls to Parent 2's extracted
methods, normalized to the `this.`-qualified style. The presence of the extracted method
*definitions* on the Parent‑2 side (`+ `) confirms the extraction happened before the
merge, so the `++` lines are conflict-resolution merge effort rather than an extraction
performed by the merge itself.
