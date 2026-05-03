# Case 4 — Project: hadoop — Merge commit SHA1: adc651044c0cacff62a3afa1ef1f833ab47e0413

## Modified file(s):
- `hadoop-tools/hadoop-azure/src/main/java/org/apache/hadoop/fs/azure/RemoteWasbAuthorizerImpl.java`

## Class(es) modified in the merge:
- `RemoteWasbAuthorizerImpl`

## Merge effort lines in the combined diff

### `authorize` method — `Merge_Parameter`: `delegationToken` removed from signature, promoted to instance field

```diff
    @Override
-   public boolean authorize(String wasbAbsolutePath, String accessType,
-       String delegationToken) throws WasbAuthorizationException, IOException {
- 
+   public boolean authorize(String wasbAbsolutePath, String accessType)
+       throws WasbAuthorizationException, IOException {
 +    try {
 +      URIBuilder uriBuilder = new URIBuilder(remoteAuthorizerServiceUrl);
 +      uriBuilder.setPath("/" + CHECK_AUTHORIZATION_OP);
 +      uriBuilder.addParameter(WASB_ABSOLUTE_PATH_QUERY_PARAM_NAME, wasbAbsolutePath);
 +      uriBuilder.addParameter(ACCESS_OPERATION_QUERY_PARAM_NAME, accessType);
-       uriBuilder.addParameter(DELEGATION_TOKEN_QUERY_PARAM_NAME, delegationToken);
++      if (isSecurityEnabled && StringUtils.isNotEmpty(delegationToken)) {
++        uriBuilder.addParameter(DELEGATION_TOKEN_QUERY_PARAM_NAME, delegationToken);
++      }
++
-       String responseBody = remoteCallHelper.makeRemoteGetRequest(new HttpGet(uriBuilder.build()));
++      String responseBody = null;
++      UserGroupInformation ugi = UserGroupInformation.getCurrentUser();
++      UserGroupInformation connectUgi = ugi.getRealUser();
++      if (connectUgi == null) {
++        connectUgi = ugi;
++      } else {
++        uriBuilder.addParameter(Constants.DOAS_PARAM, ugi.getShortUserName());
++      }
++      if (isSecurityEnabled && !connectUgi.hasKerberosCredentials()) {
++        connectUgi = UserGroupInformation.getLoginUser();
++      }
++      connectUgi.checkTGTAndReloginFromKeytab();
++
+       try {
 -        URIBuilder uriBuilder = new URIBuilder(remoteAuthorizerServiceUrl);
 -        ... [P2's full UGI-based body]
 -        responseBody = connectUgi.doAs(...)
 -        ...
++        responseBody = connectUgi
++            .doAs(new PrivilegedExceptionAction<String>() {
++              @Override
++              public String run() throws Exception {
++                ...
++                return remoteCallHelper.makeRemoteGetRequest(httpGet);
++              }
++            });
++      } catch (InterruptedException e) {
++        LOG.error("Error in check authorization", e);
++        throw new WasbAuthorizationException("Error in check authorize", e);
       }
++
+       ObjectMapper objectMapper = new ObjectMapper();
+       RemoteAuthorizerResponse authorizerResponse =
-           objectMapper.readValue(responseBody, RemoteAuthorizerResponse.class);
++          objectMapper
++              .readValue(responseBody, RemoteAuthorizerResponse.class);
+
+       if (authorizerResponse == null) {
+         throw new WasbAuthorizationException("RemoteAuthorizerResponse object null...");
+       } else if (authorizerResponse.getResponseCode() == REMOTE_CALL_SUCCESS_CODE) {
+         return authorizerResponse.getAuthorizationResult();
+       } else {
+         throw new WasbAuthorizationException("Remote authorization"
-             + " service encountered an error "
++            + " serivce encountered an error "
+             + authorizerResponse.getResponseMessage());
+       }
+     } catch (URISyntaxException | WasbRemoteCallException
+         | JsonParseException | JsonMappingException ex) {
+       throw new WasbAuthorizationException(ex);
+     }
   }
```

## Relevant final code in the merge

```java
@Override
public boolean authorize(String wasbAbsolutePath, String accessType)
    throws WasbAuthorizationException, IOException {
  try {
    URIBuilder uriBuilder = new URIBuilder(remoteAuthorizerServiceUrl);
    uriBuilder.setPath("/" + CHECK_AUTHORIZATION_OP);
    uriBuilder.addParameter(WASB_ABSOLUTE_PATH_QUERY_PARAM_NAME, wasbAbsolutePath);
    uriBuilder.addParameter(ACCESS_OPERATION_QUERY_PARAM_NAME, accessType);
    if (isSecurityEnabled && StringUtils.isNotEmpty(delegationToken)) {
      uriBuilder.addParameter(DELEGATION_TOKEN_QUERY_PARAM_NAME, delegationToken);
    }
    String responseBody = null;
    UserGroupInformation ugi = UserGroupInformation.getCurrentUser();
    UserGroupInformation connectUgi = ugi.getRealUser();
    // ... UGI setup ...
    connectUgi.checkTGTAndReloginFromKeytab();
    try {
      responseBody = connectUgi.doAs(new PrivilegedExceptionAction<String>() {
        @Override
        public String run() throws Exception {
          // ... Kerberos/token auth flow ...
          return remoteCallHelper.makeRemoteGetRequest(httpGet);
        }
      });
    } catch (InterruptedException e) {
      LOG.error("Error in check authorization", e);
      throw new WasbAuthorizationException("Error in check authorize", e);
    }
    ObjectMapper objectMapper = new ObjectMapper();
    RemoteAuthorizerResponse authorizerResponse =
        objectMapper.readValue(responseBody, RemoteAuthorizerResponse.class);
    // ... response handling ...
  } catch (URISyntaxException | WasbRemoteCallException
      | JsonParseException | JsonMappingException ex) {
    throw new WasbAuthorizationException(ex);
  }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**~55 lines** (++ and -- in the `authorize` method body and signature)

## What each side had

**Parent 1 (P1)** removed `delegationToken` from the `authorize` method signature and promoted it to an instance field (fetched via `SecurityUtils.getDelegationTokenFromCredentials()` in `init()`). The method body was restructured to reference `this.delegationToken` directly, with full UGI and Kerberos support inside the `doAs` call.

**Parent 2 (P2)** kept the original three-parameter signature `authorize(String wasbAbsolutePath, String accessType, String delegationToken)` and unconditionally added the token to the URI query parameters without UGI/Kerberos handling: `uriBuilder.addParameter(DELEGATION_TOKEN_QUERY_PARAM_NAME, delegationToken)`.

## Interpretation

This is a clear **Merge_Parameter** case. P1 removed the `delegationToken` parameter from `authorize()` by promoting it to an instance field, making the signature `authorize(String wasbAbsolutePath, String accessType)`. P2 still had three parameters.

The `--` lines confirm:
- P2's three-parameter signature: `authorize(String wasbAbsolutePath, String accessType, String delegationToken)`
- P2's unconditional token addition: `uriBuilder.addParameter(DELEGATION_TOKEN_QUERY_PARAM_NAME, delegationToken)` (no null/empty check)
- P2's simpler body: a direct `makeRemoteGetRequest()` without UGI indirection

The `++` lines confirm the merge produced:
- P1's two-parameter signature (parameter removed = Merge_Parameter)
- `if (isSecurityEnabled && StringUtils.isNotEmpty(delegationToken))` guard (using the instance field)
- P1's full UGI/Kerberos `doAs` body merged into the try/catch structure from P2

The structural conflict — P1 had structured the body with an outer try/catch for URI construction and an inner try for the `doAs`, while P2's body was flat — required the merge to reconcile both structural shapes while also adopting the two-argument signature. This is a well-supported case: the `--` lines show two incompatible signatures, and the `++` lines show the unified result.

## Complete diff

```diff
diff --cc hadoop-common-project/hadoop-common/src/main/conf/log4j.properties
index 9984666e09d,b4658ae7dae..1289115e6e4
(log4j config - not refactoring relevant)
++log4j.appender.FSLOGGER.MaxBackupIndex=${hadoop.log.maxbackupindex}
++
(++ lines = formatting merge only)

diff --cc hadoop-common-project/hadoop-nfs/src/main/java/org/apache/hadoop/oncrpc/SimpleTcpServer.java
@@@ -91,7 -92,7 +92,7 @@@
--  
++
(whitespace-only, not relevant)

diff --cc hadoop-tools/hadoop-azure/src/main/java/org/apache/hadoop/fs/azure/RemoteWasbAuthorizerImpl.java
index 5f2265bc732,a2105c7f8c3..e22a3a28318
--- a/hadoop-tools/hadoop-azure/src/main/java/org/apache/hadoop/fs/azure/RemoteWasbAuthorizerImpl.java
+++ b/hadoop-tools/hadoop-azure/src/main/java/org/apache/hadoop/fs/azure/RemoteWasbAuthorizerImpl.java
@@@ -82,14 -103,24 +103,24 @@@
    @Override
    public void init(Configuration conf)
        throws WasbAuthorizationException, IOException {
+     LOG.debug("Initializing RemoteWasbAuthorizerImpl instance");
+     Iterator<Token<? extends TokenIdentifier>> tokenIterator = null;
+     try {
 -         delegationToken = SecurityUtils.getDelegationTokenFromCredentials();
++      delegationToken = SecurityUtils.getDelegationTokenFromCredentials();
+     } catch (IOException e) {
+       final String msg = "Error in fetching the WASB delegation token";
+       LOG.error(msg, e);
+       throw new IOException(msg, e);
+     }

-     remoteAuthorizerServiceUrl = conf.get(KEY_REMOTE_AUTH_SERVICE_URL);
+     remoteAuthorizerServiceUrl = SecurityUtils.getRemoteAuthServiceUrls(conf);

      if (remoteAuthorizerServiceUrl == null
--          || remoteAuthorizerServiceUrl.isEmpty()) {
++        || remoteAuthorizerServiceUrl.isEmpty()) {
        throw new WasbAuthorizationException("...");
      }
      this.remoteCallHelper = new WasbRemoteCallHelper();
@@@ -96,41 -130,86 +130,86 @@@
    }

    @Override
-   public boolean authorize(String wasbAbsolutePath, String accessType,
-       String delegationToken) throws WasbAuthorizationException, IOException {
-
+   public boolean authorize(String wasbAbsolutePath, String accessType)
+       throws WasbAuthorizationException, IOException {
+    try {
+      URIBuilder uriBuilder = new URIBuilder(remoteAuthorizerServiceUrl);
+      uriBuilder.setPath("/" + CHECK_AUTHORIZATION_OP);
+      uriBuilder.addParameter(WASB_ABSOLUTE_PATH_QUERY_PARAM_NAME, wasbAbsolutePath);
+      uriBuilder.addParameter(ACCESS_OPERATION_QUERY_PARAM_NAME, accessType);
-       uriBuilder.addParameter(DELEGATION_TOKEN_QUERY_PARAM_NAME, delegationToken);
++      if (isSecurityEnabled && StringUtils.isNotEmpty(delegationToken)) {
++        uriBuilder.addParameter(DELEGATION_TOKEN_QUERY_PARAM_NAME, delegationToken);
++      }
++
-       String responseBody = remoteCallHelper.makeRemoteGetRequest(new HttpGet(uriBuilder.build()));
++      String responseBody = null;
++      UserGroupInformation ugi = UserGroupInformation.getCurrentUser();
++      UserGroupInformation connectUgi = ugi.getRealUser();
++      if (connectUgi == null) { connectUgi = ugi; }
++      else { uriBuilder.addParameter(Constants.DOAS_PARAM, ugi.getShortUserName()); }
++      if (isSecurityEnabled && !connectUgi.hasKerberosCredentials()) {
++        connectUgi = UserGroupInformation.getLoginUser();
++      }
++      connectUgi.checkTGTAndReloginFromKeytab();
++
+       try {
 -        [P2's full UGI body with inner try/catch]
++        responseBody = connectUgi.doAs(new PrivilegedExceptionAction<String>() {
++          @Override public String run() throws Exception {
++            AuthenticatedURL.Token token = null;
++            HttpGet httpGet = new HttpGet(uriBuilder.build());
++            if (isKerberosSupportEnabled && UserGroupInformation.isSecurityEnabled()
++                && (delegationToken == null || delegationToken.isEmpty())) {
++              token = new AuthenticatedURL.Token();
++              final Authenticator kerberosAuthenticator = new KerberosDelegationTokenAuthenticator();
++              try {
++                kerberosAuthenticator.authenticate(uriBuilder.build().toURL(), token);
++                Validate.isTrue(token.isSet(), "Authenticated Token is NOT present...");
++              } catch (AuthenticationException e) {
++                throw new IOException("Authentication failed in check authorization", e);
++              }
++              if (token != null) {
++                httpGet.setHeader("Cookie", AuthenticatedURL.AUTH_COOKIE + "=" + token);
++              }
+              }
++            return remoteCallHelper.makeRemoteGetRequest(httpGet);
++          }
++        });
++      } catch (InterruptedException e) {
++        LOG.error("Error in check authorization", e);
++        throw new WasbAuthorizationException("Error in check authorize", e);
       }
+      ObjectMapper objectMapper = new ObjectMapper();
+      RemoteAuthorizerResponse authorizerResponse =
-           objectMapper.readValue(responseBody, RemoteAuthorizerResponse.class);
++          objectMapper.readValue(responseBody, RemoteAuthorizerResponse.class);
+      if (authorizerResponse == null) { throw ...; }
+      else if (authorizerResponse.getResponseCode() == REMOTE_CALL_SUCCESS_CODE) {
+        return authorizerResponse.getAuthorizationResult();
+      } else {
+        throw new WasbAuthorizationException("Remote authorization"
-             + " service encountered an error "
++            + " serivce encountered an error "
+            + authorizerResponse.getResponseMessage());
+      }
+    } catch (URISyntaxException | WasbRemoteCallException
+        | JsonParseException | JsonMappingException ex) {
+      throw new WasbAuthorizationException(ex);
+    }
  }

diff --cc hadoop-yarn-project/.../TestAMRMClient.java
(test restructuring - not refactoring relevant)
```
