# Project: DependencyCheck — Merge commit SHA1: cf2f2dc62d2d38e3c5e1be299a877c977a1c15ea

## Modified file(s):
- `dependency-check-core/src/main/java/org/owasp/dependencycheck/analyzer/NodePackageAnalyzer.java`

## Class(es) modified in the merge:
`NodePackageAnalyzer`

## Merge effort lines in the combined diff

```diff
diff --cc dependency-check-core/src/main/java/org/owasp/dependencycheck/analyzer/NodePackageAnalyzer.java
index 6f737a2b2,ae4ed6057..f318269d4

@@@ -120,60 -124,67 +124,65 @@@

      // call site — version capture conflict
-             addToEvidence(dependency, EvidenceType.VERSION, json, "version");
-             dependency.setDisplayFileName(String.format("%s/%s", file.getParentFile().getName(), file.getName()));
++            final String version = addToEvidence(dependency, EvidenceType.VERSION, json, "version");
++            dependency.setVersion(version);

      // method declaration conflict
-     private void addToEvidence(Dependency dep, EvidenceType t, JsonObject json, String key) {
 -    private String addToEvidence(JsonObject json, EvidenceCollection collection, String key) {
++    private String addToEvidence(Dependency dep, EvidenceType t, JsonObject json, String key) {
+         String evidenceStr = null;

      // body — first branch (JsonString)
-                 dep.addEvidence(t, PACKAGE_JSON, key, ((JsonString) value).getString(), Confidence.HIGHEST);
-
 -            	    evidenceStr = ((JsonString) value).getString();
 -                collection.addEvidence(PACKAGE_JSON, key, evidenceStr, Confidence.HIGHEST);
++                evidenceStr = ((JsonString) value).getString();
++                dep.addEvidence(t, PACKAGE_JSON, key, evidenceStr, Confidence.HIGHEST);

      // body — nested JsonObject branch
 -                    evidenceStr = ((JsonString) subValue).getString();
 -                collection.addEvidence(PACKAGE_JSON,
++                        evidenceStr = ((JsonString) subValue).getString();
 +                        dep.addEvidence(t, PACKAGE_JSON,

      // closing return
 -		}
 -		return evidenceStr;
 -	}
++        return evidenceStr;
 +    }
```

## Relevant final code in the merge

```java
private String addToEvidence(Dependency dep, EvidenceType t, JsonObject json, String key) {
    String evidenceStr = null;
    if (json.containsKey(key)) {
        final JsonValue value = json.get(key);
        if (value instanceof JsonString) {
            evidenceStr = ((JsonString) value).getString();
            dep.addEvidence(t, PACKAGE_JSON, key, evidenceStr, Confidence.HIGHEST);
        } else if (value instanceof JsonObject) {
            final JsonObject jsonObject = (JsonObject) value;
            for (final Map.Entry<String, JsonValue> entry : jsonObject.entrySet()) {
                final String property = entry.getKey();
                final JsonValue subValue = entry.getValue();
                if (subValue instanceof JsonString) {
                    evidenceStr = ((JsonString) subValue).getString();
                    dep.addEvidence(t, PACKAGE_JSON,
                            String.format("%s.%s", key, property),
                            evidenceStr, Confidence.HIGHEST);
                } else {
                    LOGGER.warn("JSON sub-value not string as expected: {}", subValue);
                }
            }
        } else {
            LOGGER.warn("JSON value not string or JSON object as expected: {}", value);
        }
    }
    return evidenceStr;
}
```

And at the call site:
```java
final String version = addToEvidence(dependency, EvidenceType.VERSION, json, "version");
dependency.setVersion(version);
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
8 lines (1 `--` at the call site removing `void` usage; 1 `++` capturing the `String` return; 1 `++` for `dependency.setVersion(version)`; 1 `--` removing `void` signature; 1 `++` replacing with `String` return signature; 2 `++` in the body replacing `collection.addEvidence` calls with the merged pattern using `evidenceStr`; 1 `++` for `return evidenceStr`)

## What each side had

- **Parent 1 (P1):** `addToEvidence` was refactored to accept `(Dependency dep, EvidenceType t, JsonObject json, String key)` and return **`void`** — it added evidence directly onto the `Dependency`. The call site used it as a statement with no return value captured. The version was set separately via `dependency.setDisplayFileName(...)`.
- **Parent 2 (P2):** `addToEvidence` had the original signature `(JsonObject json, EvidenceCollection collection, String key)` returning **`String`** (the evidence string found). The return value was used at the call site: `final String version = addToEvidence(json, dependency.getVersionEvidence(), "version")`.

## Interpretation

This case evidences **Change_Return_Type** (from `String` to `void` in P1's refactoring) and **Change_Parameter_Type** (from `EvidenceCollection collection` to `Dependency dep, EvidenceType t` in P1's refactoring) on the private helper method `addToEvidence`. One parent restructured the method to pass `Dependency` + `EvidenceType` directly (eliminating the `EvidenceCollection` intermediary), but made it `void`. The other parent retained the old `EvidenceCollection` parameter and `String` return type. The merge had to resolve both dimensions at once: adopt the new parameter types AND restore the `String` return type and `return evidenceStr` statement (needed for the call site to capture the version string). The `++` lines on the declaration, body, and return statement — together with the `--` lines on both the old `void` declaration and the old `collection.addEvidence` calls — directly confirm that the conflict was caused by this two-dimensional parameter and return type change introduced in one of the parents.

## Complete diff

```diff
diff --cc dependency-check-core/src/main/java/org/owasp/dependencycheck/analyzer/NodePackageAnalyzer.java
index 6f737a2b2,ae4ed6057..f318269d4
--- a/dependency-check-core/src/main/java/org/owasp/dependencycheck/analyzer/NodePackageAnalyzer.java
+++ b/dependency-check-core/src/main/java/org/owasp/dependencycheck/analyzer/NodePackageAnalyzer.java
@@@ -55,7 -58,7 +55,11 @@@
++    public static final String DEPENDENCY_ECOSYSTEM = "npm";

@@@ -120,60 -124,67 +124,65 @@@
 -	@Override
 -	protected void analyzeDependency(Dependency dependency, Engine engine) throws AnalysisException {
 -		dependency.setEcosystem(DEPENDENCY_ECOSYSTEM);
 -		final File file = dependency.getActualFile();
 -		...
 -		final EvidenceCollection productEvidence = dependency.getProductEvidence();
 -		final EvidenceCollection vendorEvidence = dependency.getVendorEvidence();
 -		...
 -		addToEvidence(json, productEvidence, "description");
 -		addToEvidence(json, vendorEvidence, "author");
 -		final String version = addToEvidence(json, dependency.getVersionEvidence(), "version");
 -		dependency.setVersion(version);
 -	}
 +    @Override
 +    protected void analyzeDependency(Dependency dependency, Engine engine) throws AnalysisException {
++        dependency.setEcosystem(DEPENDENCY_ECOSYSTEM);
 +        ...
 +        addToEvidence(dependency, EvidenceType.PRODUCT, json, "description");
 +        addToEvidence(dependency, EvidenceType.VENDOR, json, "author");
-             addToEvidence(dependency, EvidenceType.VERSION, json, "version");
-             dependency.setDisplayFileName(String.format(...));
++            final String version = addToEvidence(dependency, EvidenceType.VERSION, json, "version");
++            dependency.setVersion(version);
 +    }

     /**
      * @param dep the dependency to add the evidence
      * @param t the type of evidence to add
      * @param json information from node.js
 -    * @param collection a set of evidence about a dependency
      * @param key the key to obtain the data from the json information
+      * @return the actual string set into evidence
      */
-     private void addToEvidence(Dependency dep, EvidenceType t, JsonObject json, String key) {
 -    private String addToEvidence(JsonObject json, EvidenceCollection collection, String key) {
++    private String addToEvidence(Dependency dep, EvidenceType t, JsonObject json, String key) {
+         String evidenceStr = null;
 -    		if (json.containsKey(key)) {
 +        if (json.containsKey(key)) {
              final JsonValue value = json.get(key);
              if (value instanceof JsonString) {
-                 dep.addEvidence(t, PACKAGE_JSON, key, ((JsonString) value).getString(), Confidence.HIGHEST);
 -            		evidenceStr = ((JsonString) value).getString();
 -                collection.addEvidence(PACKAGE_JSON, key, evidenceStr, Confidence.HIGHEST);
++                evidenceStr = ((JsonString) value).getString();
++                dep.addEvidence(t, PACKAGE_JSON, key, evidenceStr, Confidence.HIGHEST);
              } else if (value instanceof JsonObject) {
                  ...
                  if (subValue instanceof JsonString) {
 -                    	evidenceStr = ((JsonString) subValue).getString();
 -                    collection.addEvidence(PACKAGE_JSON, ...);
++                        evidenceStr = ((JsonString) subValue).getString();
 +                        dep.addEvidence(t, PACKAGE_JSON, ...);
                  }
              }
 -		}
 -		return evidenceStr;
 -	}
 +        }
++        return evidenceStr;
 +    }
```
