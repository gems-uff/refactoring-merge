# Project: pucomex-duex-backend — Merge commit SHA1: b8f170420c726a8180bfff2122ba8f0f05dcbe0c

## Modified file(s):
- `pucomex-duex-business/src/main/java/br/gov/serpro/pucomex/due/utils/Util.java` (constant declaration)
- `pucomex-duex-business/src/test/java/br/gov/serpro/pucomex/due/business/core/validators/due/DUEBCCoreEmElaboracaoDUEValidaTest.java` (call sites where the magic literal was replaced by the symbolic constant)

## Class(es) affected by the merge effort:
- `Util` (declares the extracted constant `ANO_MUDANCA_SEQUENCE_2021`)
- `DUEBCCoreEmElaboracaoDUEValidaTest` (consumer whose `2021` literal was replaced by the constant)

## Merge effort lines in the combined diff
Declaration site (`Util.java`):
```diff
  	protected static final int[] PESOS_PERDCOMP_2 = new int[] { 8, 7, 6, 5, 4, 3, 2, 9, ... };

++<<<<<<< HEAD
 +	public static final int ANO_MUDANCA_SEQUENCE_2021 = 2021;
++=======
+ 	static final int ANO_MUDANCA_SEQUENCE_2021 = 2021;
++>>>>>>> refs/remotes/origin/master
```

Call sites (`DUEBCCoreEmElaboracaoDUEValidaTest.java`):
```diff
  	public void testObterNomeSequenceFinalAno() {

++<<<<<<< HEAD
 +		String sequenceDue = ...Util.getNomeSequenceVigente("duev_nr_seq",
 +				...Util.ANO_MUDANCA_SEQUENCE_2021);
 +		String sequenceRascunho = ...Util.getNomeSequenceVigente("duer_seq",
 +				...Util.ANO_MUDANCA_SEQUENCE_2021);
++=======
+ 		String sequenceDue = ...Util.getNomeSequenceVigente("duev_nr_seq", 2021);
+ 		String sequenceRascunho = ...Util.getNomeSequenceVigente("duer_seq", 2021);
++>>>>>>> refs/remotes/origin/master
  		Assert.assertEquals("duev_nr_seq", sequenceDue);
```

Notation recap:
- `" +"` → present in **Parent 1 (HEAD)**: the call sites use the **extracted symbolic constant** `Util.ANO_MUDANCA_SEQUENCE_2021`; the constant is declared `public static final`.
- `"+ "` → present in **Parent 2 (origin/master)**: the call sites use the **inline magic literal** `2021`; the constant is declared with default (package) visibility `static final`.
- `"++"` → created in the merge: the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) at both the declaration and the two call sites — the textual merge effort produced because the two parents disagreed on literal-vs-constant (and on the declaration's visibility).

## Relevant final code in the merge
The merge was committed with the conflict materialized (markers retained) at both the declaration and the call sites:
```java
// Util.java
<<<<<<< HEAD
public static final int ANO_MUDANCA_SEQUENCE_2021 = 2021;
=======
static final int ANO_MUDANCA_SEQUENCE_2021 = 2021;
>>>>>>> refs/remotes/origin/master

// DUEBCCoreEmElaboracaoDUEValidaTest.java
<<<<<<< HEAD
String sequenceDue = Util.getNomeSequenceVigente("duev_nr_seq", Util.ANO_MUDANCA_SEQUENCE_2021);
String sequenceRascunho = Util.getNomeSequenceVigente("duer_seq", Util.ANO_MUDANCA_SEQUENCE_2021);
=======
String sequenceDue = Util.getNomeSequenceVigente("duev_nr_seq", 2021);
String sequenceRascunho = Util.getNomeSequenceVigente("duer_seq", 2021);
>>>>>>> refs/remotes/origin/master
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**6 lines** (6 `++`, 0 `--`):
- `Util.java` — 3 `++` conflict-marker lines at the declaration.
- `DUEBCCoreEmElaboracaoDUEValidaTest.java` — 3 `++` conflict-marker lines at the call sites.

## What each side had
- **Parent 1 (HEAD)** — contains the refactoring evidence:
  ```diff
  + public static final int ANO_MUDANCA_SEQUENCE_2021 = 2021;        // declares the named constant
  + ...Util.getNomeSequenceVigente("duev_nr_seq", ...Util.ANO_MUDANCA_SEQUENCE_2021);   // uses it
  + ...Util.getNomeSequenceVigente("duer_seq",  ...Util.ANO_MUDANCA_SEQUENCE_2021);     // uses it
  ```
  Parent 1 replaced the inline literal `2021` at the call sites with the symbolic constant `Util.ANO_MUDANCA_SEQUENCE_2021`.

- **Parent 2 (origin/master)** — retained the inline magic literal:
  ```diff
  + static final int ANO_MUDANCA_SEQUENCE_2021 = 2021;              // package-visible declaration
  + ...Util.getNomeSequenceVigente("duev_nr_seq", 2021);            // literal 2021 inline
  + ...Util.getNomeSequenceVigente("duer_seq",  2021);             // literal 2021 inline
  ```

## Interpretation
- **Refactoring type evidenced:** `Extract_Variable` (extraction of the magic number `2021` into the symbolic constant `ANO_MUDANCA_SEQUENCE_2021`, then replacing the literal with the constant at the usage sites). The decisive evidence is the call-site hunk, where Parent 1 uses `Util.ANO_MUDANCA_SEQUENCE_2021` exactly where Parent 2 still passes the literal `2021`.
- **Why the `++` lines confirm it:** at both the declaration and the two call sites the only difference between the parents is literal-`2021` (Parent 2) versus the extracted-constant reference (Parent 1). Git could not auto-reconcile the extracted-constant form with the inline-literal form, so it emitted conflict markers (`++`) at each location. Those marker lines are merge effort that exists solely because of the extract-constant refactoring.
- **Why the refactoring was introduced in a parent, not by the merge:** the symbolic-constant usage `Util.ANO_MUDANCA_SEQUENCE_2021` is carried by Parent 1 (HEAD) as `" +"` lines that already existed on that side, while Parent 2 independently kept the literal `2021` (`"+ "`). The merge did not perform the extraction; it only failed to auto-merge Parent 1's extracted form against Parent 2's literal form and recorded the conflict.
- **Why the case is well-supported:** the same extract-constant divergence appears consistently at three coordinated locations (one declaration + two call sites) across two files, each variant is attributable to a specific parent via the combined-diff prefixes, and the literal-vs-constant pairing is the textbook signature of `Extract_Variable`. (The accompanying `public` vs package-default visibility difference on the declaration is secondary and on its own would not be a listed refactoring; the reportable signal is the magic-number extraction at the call sites.)
