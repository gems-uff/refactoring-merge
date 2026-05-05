# Case 4 — Project: keycloak — Merge commit SHA1: 97d5f4aafc0caa573557bd18cf88e5906bee85e1

## Modified file(s):
- `broker/core/src/main/java/org/keycloak/broker/provider/IdentityProvider.java`
- `broker/core/src/main/java/org/keycloak/broker/provider/AbstractIdentityProvider.java`
- `broker/core/src/main/java/org/keycloak/broker/provider/AuthenticationResponse.java` (deleted)

## Class(es) modified in the merge:
- `IdentityProvider` (interface)
- `AbstractIdentityProvider`

## Merge effort lines in the combined diff

### 1. `IdentityProvider` — nested interface `Callback` renamed to `AuthenticationCallback` (P2 Rename_Class)

```diff
-     public interface Callback {
++    public interface AuthenticationCallback {
++        /**
++         * This method should be called by provider after the JAXRS callback endpoint has finished authentication
++         * with the remote IDP
++         * ...
++         */
 +        public Response authenticated(Map<String, String> userNotes, IdentityProviderModel identityProviderConfig,
 +                                       FederatedIdentity federatedIdentity, String code);
      }
...
-     Object callback(RealmModel realm, Callback callback);
++    Object callback(RealmModel realm, AuthenticationCallback callback);
```

### 2. `IdentityProvider` — `handleRequest` signature changed, `AuthenticationResponse` return type replaced (P2 Change_Return_Type + Rename_Method)

```diff
--    AuthenticationResponse handleRequest(AuthenticationRequest request);
...
++    Response handleRequest(AuthenticationRequest request);
```

### 3. `AbstractIdentityProvider` — `logout` method renamed to `keycloakInitiatedBrowserLogout` (P2 Rename_Method)

```diff
-     public Response logout(UserSessionModel userSession, UriInfo uriInfo, RealmModel realm) {
++    public Response keycloakInitiatedBrowserLogout(UserSessionModel userSession, UriInfo uriInfo, RealmModel realm) {
          return null;
      }
```

### 4. `AbstractIdentityProvider` — `callback` parameter type updated to `AuthenticationCallback` (merge effort from Rename_Class)

```diff
-     public Object callback(RealmModel realm, Callback callback) {
++    public Object callback(RealmModel realm, AuthenticationCallback callback) {
          return null;
      }
```

## Relevant final code in the merge

```java
// IdentityProvider.java
public interface IdentityProvider<C extends IdentityProviderModel> extends Provider {

    public interface AuthenticationCallback {
        public Response authenticated(Map<String, String> userNotes,
                                      IdentityProviderModel identityProviderConfig,
                                      FederatedIdentity federatedIdentity,
                                      String code);
    }

    Object callback(RealmModel realm, AuthenticationCallback callback);

    Response handleRequest(AuthenticationRequest request);
}

// AbstractIdentityProvider.java
@Override
public Object callback(RealmModel realm, AuthenticationCallback callback) {
    return null;
}

@Override
public Response keycloakInitiatedBrowserLogout(UserSessionModel userSession, UriInfo uriInfo, RealmModel realm) {
    return null;
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**22 lines**

## What each side had

**Parent 1 (P1):**
- `IdentityProvider.Callback` — nested interface named `Callback`.
- `Object callback(RealmModel realm, Callback callback)` in the interface and abstract implementation.
- `AuthenticationResponse handleRequest(AuthenticationRequest request)` — return type was the custom `AuthenticationResponse` class.
- `AbstractIdentityProvider.logout(UserSessionModel, UriInfo, RealmModel)` — method named `logout`.

**Parent 2 (P2):**
- Renamed nested interface `Callback` to `AuthenticationCallback`, expanding its documentation.
- Changed `handleRequest` return type from `AuthenticationResponse` to `Response` (JAX-RS), and deleted `AuthenticationResponse.java`.
- Renamed `logout` to `keycloakInitiatedBrowserLogout` in `AbstractIdentityProvider` and updated the interface.
- Updated `callback` parameter type accordingly.

## Interpretation

Three refactoring types are evidenced:

1. **Rename_Class** (`Callback` → `AuthenticationCallback`): P2 renamed the nested inner interface in `IdentityProvider`. The `--` line on `public interface Callback` and the `++` line on `public interface AuthenticationCallback` are merge-effort lines. The propagated rename in the `callback` method signature (`--  Object callback(RealmModel realm, Callback callback)` / `++  Object callback(RealmModel realm, AuthenticationCallback callback)`) is further merge effort in both the interface and the abstract implementation.

2. **Change_Return_Type** (`handleRequest`): P2 changed the return type of `handleRequest` from the project-specific `AuthenticationResponse` to JAX-RS `Response`, accompanied by deleting `AuthenticationResponse.java`. The `--` line on `AuthenticationResponse handleRequest(...)` and the `++` line on `Response handleRequest(...)` are direct merge-effort.

3. **Rename_Method** (`logout` → `keycloakInitiatedBrowserLogout`): P2 renamed this method in `AbstractIdentityProvider`. The `--`/`++` lines on the method signature in `AbstractIdentityProvider` are merge-effort resolving the conflict between P1 (which did not have this rename) and P2.

All three cases are strongly supported by the `--` (removed) and `++` (created in merge) markers in the combined diff.

## Complete diff

<details>
<summary>Click to expand full combined diff</summary>

See uploaded file: `keycloak_97d5f4aafc0caa573557bd18cf88e5906bee85e1.diff`

</details>
