# Project: ctma-src_1a1a006c458d7beab141a4de5209cf5fb06b4a86

## Modified file(s):
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/validation/CommonValidation.java`
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/validation/FlightManifestValidation.java`
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/application/service/ViagemService.java`
- `pucomex-ccta-commons/src/main/java/br/gov/serpro/pucomex/ccta/commons/infrastructure/exception/CctaBusinessException.java`

## Class(es) affected by the merge effort:
`CommonValidation`, `FlightManifestValidation`, `CctaBusinessException`

## Merge effort lines in the combined diff

### CommonValidation.java — new renamed method declarations

```diff
 -  public static CctaBusinessException businessException(String codigo, CCTAPucomexField campo, Notificacao notificacao) {
 +  public static CctaBusinessException businessException(String codigo, CCTAPucomexField campo) {
        ...
++  public static CctaBusinessException businessExceptionNotificacao(String codigo, CCTAPucomexField campo, Notificacao notificacao) {
++      String message = new CCTAMessage().get(codigo, campo.label());
++      return new CctaBusinessException(codigo, message, campo, notificacao);
++  }
++
 -  public static CctaBusinessException businessException(String codigo, CCTAPucomexField campo, Notificacao notificacao, Object... params) {
++  public static CctaBusinessException businessExceptionNotificacao(String codigo, CCTAPucomexField campo, Notificacao notificacao, Object... params) {

++  public static CctaBusinessException businessExceptionNotificacao(boolean invisivel, String codigo, CCTAPucomexField campo, Notificacao notificacao,
++          Object... params) {
++      String message = new CCTAMessage().get(codigo, params);
++      return new CctaBusinessException(codigo, message, campo, invisivel, notificacao);
++  }
++
 -  public static void evaluateException(MultiBusinessException mbe, String codigo, CCTAPucomexField campo, Notificacao notificacao,
++  public static void evaluateExceptionNotificacao(MultiBusinessException mbe, String codigo, CCTAPucomexField campo, Notificacao notificacao,
 +          Object... params) {
++      mbe.addException(businessExceptionNotificacao(codigo, campo, notificacao, params));
++  }
++
++  public static void evaluateExceptionNotificacao(boolean invisivel, MultiBusinessException mbe, String codigo,
++          CCTAPucomexField campo, Notificacao notificacao, Object... params) {
++      ...
++      mbe.addException(businessExceptionNotificacao(invisivel, codigo, campo, notificacao, params));
++  }
```

### FlightManifestValidation.java — call sites updated to renamed method

```diff
 -  CommonValidation.evaluateException(mbe,
 +  CommonValidation.evaluateExceptionNotificacao(mbe,
++  CommonValidation.evaluateExceptionNotificacao(mbe,          // (×4 visible occurrences)
++  CommonValidation.evaluateExceptionNotificacao(true, mbe,    // (×4 visible occurrences)
```

### CctaBusinessException.java — new constructor introduced by merge

```diff
++
++  public CctaBusinessException(String code, String message, CCTAPucomexField field, Boolean invisivel, Notificacao notificacao) {
++      super(code, message, field);
++      this.cctaPucomexField = field;
++      this.invisivel = invisivel;
++      this.notificacao = notificacao;
++  }
```

## Relevant final code in the merge

```java
// CommonValidation.java (merged result)
public static CctaBusinessException businessException(String codigo, CCTAPucomexField campo) { ... }

public static CctaBusinessException businessExceptionNotificacao(String codigo, CCTAPucomexField campo, Notificacao notificacao) {
    String message = new CCTAMessage().get(codigo, campo.label());
    return new CctaBusinessException(codigo, message, campo, notificacao);
}

public static void evaluateExceptionNotificacao(MultiBusinessException mbe, String codigo, CCTAPucomexField campo, Notificacao notificacao,
        Object... params) {
    if (!Optional.ofNullable(mbe).isPresent()) {
        throwError(codigo, campo, params);
    }
    mbe.addException(businessExceptionNotificacao(codigo, campo, notificacao, params));
}

// FlightManifestValidation.java (merged result, excerpt)
CommonValidation.evaluateExceptionNotificacao(mbe,
        CCTAMessage.ERRO_RETIFICACAO_PRE_MANIFESTO_HOUSE_COM_BLOQUEIO_CARREGAMENTO_VISIVEL,
        CCTAXFFMField.FM_ARR_ATC_IMC_TCD_ID, notificacao, conhecimento.getNumeroAWB(), ...);
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**26 lines** (method declaration `++` lines for `businessExceptionNotificacao` × 3 overloads + `evaluateExceptionNotificacao` × 2 overloads + `CctaBusinessException` constructor + call-site `++` lines in `FlightManifestValidation` × 8 occurrences)

## What each side had

**Parent 1** had (evidenced by `" +"` lines):
```java
// Methods with "Notificacao" parameter using the OLD name "businessException" / "evaluateException"
+ public static CctaBusinessException businessException(String codigo, CCTAPucomexField campo, Notificacao notificacao) { ... }
+ public static void evaluateException(MultiBusinessException mbe, String codigo, CCTAPucomexField campo, Notificacao notificacao, Object... params) { ... }

// FlightManifestValidation calling the old name:
+ CommonValidation.evaluateException(mbe, ...)
+ CommonValidation.evaluateException(true, mbe, ...)
```

**Parent 2** had (evidenced by `"+ "` lines):
```java
// Methods WITHOUT the Notificacao parameter overload — the Notificacao-carrying overload had been
// removed/renamed in P2, leaving only the base signatures:
+ public static CctaBusinessException businessException(String codigo, CCTAPucomexField campo) { ... }
// Call sites in FlightManifestValidation were already updated by P2 to pass Notificacao objects,
// but using the renamed method name "evaluateExceptionNotificacao":
+ CommonValidation.evaluateExceptionNotificacao(mbe, ...)
```

Parent 2 contains the evidence of the **Rename_Method** refactoring: it renamed `businessException(..., Notificacao)` → `businessExceptionNotificacao(...)` and `evaluateException(..., Notificacao)` → `evaluateExceptionNotificacao(...)`, separating the notification-carrying overloads from the plain ones. P1 still used the old names. The merge had to introduce the new named methods (`++` declarations) and update the call sites in `FlightManifestValidation` to the new name.

## Interpretation

**Refactoring type**: **Rename_Method** (and **Extract_Method** for the separated overloads).

Parent 2 introduced a systematic renaming of all `CommonValidation` methods that carry a `Notificacao` parameter: the overloads `businessException(…, Notificacao)` and `evaluateException(…, Notificacao)` were renamed to `businessExceptionNotificacao(…)` and `evaluateExceptionNotificacao(…)` respectively, making it explicit that these variants carry notification side-effects. This is confirmed by the `" +"` lines (P1) still showing the old names and the `"+ "` lines (P2) already using the new names in call sites within `FlightManifestValidation`.

Parent 1 still had the old `evaluateException(…, Notificacao)` overloads and called them in `FlightManifestValidation`. When merged, the conflict arose because P1's call sites used old names while P2 expected the new names. The merge effort (`++` lines) resolved this by:

1. Creating the renamed method declarations (`businessExceptionNotificacao`, `evaluateExceptionNotificacao`).
2. Updating all call sites in `FlightManifestValidation` to the new names.
3. Adding the missing `CctaBusinessException` constructor accepting `Boolean invisivel` and `Notificacao notificacao`.

The refactoring was unambiguously in Parent 2 (not introduced by the merge itself), as evidenced by P2 already having updated call sites with the new name that conflicted with P1's unchanged usage of the old name.
