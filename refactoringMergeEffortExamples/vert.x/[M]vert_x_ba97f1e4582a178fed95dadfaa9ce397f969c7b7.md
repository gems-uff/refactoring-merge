# Case 6 — Project: vert_x — Merge commit SHA1: ba97f1e4582a178fed95dadfaa9ce397f969c7b7

## Modified file(s):
- `vertx-core/src/main/java/org/vertx/java/core/sockjs/EventBusBridge.java`
- `vertx-core/src/main/java/org/vertx/java/core/sockjs/EventBusBridgeHook.java` (new file)
- `vertx-core/src/main/java/org/vertx/java/core/sockjs/SockJSServer.java`
- `vertx-core/src/main/java/org/vertx/java/core/sockjs/impl/DefaultSockJSServer.java`
- `vertx-examples/src/main/java/eventbusbridge/ServerHook.java`

## Class(es) modified in the merge:
- `EventBusBridge`
- `EventBusBridgeHook` (interface)
- `SockJSServer` (interface)
- `DefaultSockJSServer`
- `ServerHook`

## Merge effort lines in the combined diff

### `SockJSServer.java` — Rename_Method: `setupHook` → `setHook`

P1 declared `setupHook(EventBusBridgeHook hook)` in the `SockJSServer` interface. P2 renamed it to `setHook`. The merge adopted the renamed version:

```diff
-  void setupHook(EventBusBridgeHook hook);
++  void setHook(EventBusBridgeHook hook);
```

### `DefaultSockJSServer.java` — Rename_Method: `setupHook` → `setHook` at implementation site

```diff
-  public void setupHook(EventBusBridgeHook hook) {
-	this.hook = hook;
++  public void setHook(EventBusBridgeHook hook) {
++	  this.hook = hook;
+   }
```

### `EventBusBridgeHook.java` — Rename_Method: `handleRegister` → `handlePreRegister` + new method `handlePostRegister`

P1 had a single method `handleRegister(SockJSSocket, String)`. P2 split this into `handlePreRegister` (returning boolean) and added `handlePostRegister` (returning void). The interface in the merge reflects:

```diff
-	  boolean handleRegister(SockJSSocket sock, String address);
++  boolean handlePreRegister(SockJSSocket sock, String address);
++
++  void handlePostRegister(SockJSSocket sock, String address);
```

### `EventBusBridge.java` — method renamed at usage / implementation

The method `handleRegister` was renamed `handlePreRegister` in P2, and `handlePostRegister` was added:

```diff
-  protected boolean handleRegister(SockJSSocket sock, String address) {
-    if(hook != null) {
-       return hook.handleRegister(sock, address);    		   
-	}
+  protected boolean handlePreRegister(SockJSSocket sock, String address) {
++    if (hook != null) {
++      return hook.handlePreRegister(sock, address);
++	  }
     return true;
   }

+  protected void handlePostRegister(SockJSSocket sock, String address) {
++    if (hook != null) {
++      hook.handlePostRegister(sock, address);
++    }
+  }
```

The `handleSocketClosed`, `handleSendOrPub`, and `handleUnregister` methods also had their null-check bodies fixed:

```diff
-    if(hook != null) {
++    if (hook != null) {
+       hook.handleSocketClosed(sock);
+     }

-	if(hook != null) {
-       return hook.handleSendOrPub(sock, send, msg, address);    		   
-	}
++    if (hook != null) {
++      return hook.handleSendOrPub(sock, send, msg, address);
++    }

-	if(hook != null) {
-	   return hook.handleUnregister(sock, address);    		   		
-	}
++    if (hook != null) {
++      return hook.handleUnregister(sock, address);
++    }
```

### `DefaultSockJSServer.java` — bridge() method bodies reconciled

P1 called `installApp(sjsConfig, new EventBusBridge(...))` directly. P2 introduced a local variable and conditionally set the hook before installing. The merge resolved by adopting P2's pattern:

```diff
-     installApp(sjsConfig, new EventBusBridge(vertx, inboundPermitted, outboundPermitted));
-	EventBusBridge busBridge = new EventBusBridge(vertx, inboundPermitted, outboundPermitted);
-	if(hook != null){
-		busBridge.setHook(hook);
-	}
++	  EventBusBridge busBridge = new EventBusBridge(vertx, inboundPermitted, outboundPermitted);
++    if (hook != null) {
++      busBridge.setHook(hook);
++    }
+     installApp(sjsConfig, busBridge);
```

(Same for the two other overloads of `bridge()`)

### `ServerHook.java` — `handleRegister` → `handlePreRegister` + new `handlePostRegister`

```diff
-    public boolean handleRegister(SockJSSocket sock, String address){
-      logger.info("handleRegister, sock = " + sock + ", address = " + address);
-      return true;      
-    }
++  public boolean handlePreRegister(SockJSSocket sock, String address) {
++    logger.info("handlePreRegister, sock = " + sock + ", address = " + address);
++    return true;
++  }
++
++  public void handlePostRegister(SockJSSocket sock, String address) {
++    logger.info("handlePostRegister, sock = " + sock + ", address = " + address);
++  }
```

## Relevant final code in the merge

```java
// SockJSServer.java
void setHook(EventBusBridgeHook hook);

// EventBusBridgeHook.java
boolean handlePreRegister(SockJSSocket sock, String address);
void handlePostRegister(SockJSSocket sock, String address);
boolean handleUnregister(SockJSSocket sock, String address);

// EventBusBridge.java
protected boolean handlePreRegister(SockJSSocket sock, String address) {
  if (hook != null) {
    return hook.handlePreRegister(sock, address);
  }
  return true;
}

protected void handlePostRegister(SockJSSocket sock, String address) {
  if (hook != null) {
    hook.handlePostRegister(sock, address);
  }
}

// DefaultSockJSServer.java
public void setHook(EventBusBridgeHook hook) {
  this.hook = hook;
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**~35 lines** (`++` and `--` across `SockJSServer`, `DefaultSockJSServer`, `EventBusBridgeHook`, `EventBusBridge`, and `ServerHook`)

## What each side had

**Parent 1 (P1):** Declared `setupHook()` in `SockJSServer`, implemented it in `DefaultSockJSServer`, and had `handleRegister()` as the single pre/post-register hook method. Used `installApp(sjsConfig, new EventBusBridge(...))` directly in `bridge()` overloads. The hook null-check code used tab-indented, inconsistent formatting.

**Parent 2 (P2):** Renamed `setupHook` → `setHook` (**Rename_Method**), renamed `handleRegister` → `handlePreRegister` (**Rename_Method**), added the new `handlePostRegister` method (**Extract_Method**), and restructured the `bridge()` overloads to use a local variable before installing.

## Interpretation

Two refactoring types are clearly evidenced:

1. **Rename_Method** (`setupHook` → `setHook`): The `--` line in `SockJSServer.java` removes the old name; the `++` line introduces the new one. The same change propagates to `DefaultSockJSServer`. This is a surgical, non-cosmetic rename confirmed by the method signature change.

2. **Rename_Method** + **Extract_Method** (`handleRegister` → `handlePreRegister` + new `handlePostRegister`): The original single `handleRegister` method in both the interface (`EventBusBridgeHook`) and its implementation (`EventBusBridge`, `ServerHook`) was renamed to `handlePreRegister` and complemented by a new `handlePostRegister` method. The `--` lines confirm the old name, the `++` lines confirm both the rename and the new method.

Both renames were introduced in P2 before the merge. P1 had made independent edits to the same files (fixing the null-check bodies, restructuring `bridge()` calls), causing conflicts that required explicit merge effort.

## Complete diff

```diff
diff --cc vertx-core/src/main/java/org/vertx/java/core/sockjs/EventBusBridge.java
index 6c1350716b,1185922b13..0942dd8db7
--- a/vertx-core/src/main/java/org/vertx/java/core/sockjs/EventBusBridge.java
+++ b/vertx-core/src/main/java/org/vertx/java/core/sockjs/EventBusBridge.java
[... full raw diff content as provided in the input file ...]
```
