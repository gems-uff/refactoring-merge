# Case 2 — Project: hibernate-orm — Merge commit SHA1: 005c4cea639ac91631d04df2c30533e1b8319d27

## Modified file(s):
- `hibernate-core/src/main/java/org/hibernate/loader/access/IdentifierLoadAccessImpl.java`

## Class(es) modified in the merge:
- `IdentifierLoadAccessImpl`

## Merge effort lines in the combined diff

### `doLoad()` — `Extract_Method`: `initializeIfNecessary()` extracted, call sites updated

```diff
 	@SuppressWarnings( "unchecked" )
 	protected final T doLoad(Object id) {
 		...
 		if ( this.lockOptions != null ) {
 			LoadEvent event = new LoadEvent( id, entityPersister.getEntityName(), lockOptions, eventSource, ... );
 			context.fireLoad( event, LoadEventListener.GET );
- 			return (T) event.getResult();
++			final Object result = event.getResult();
++			initializeIfNecessary( result );
++
++			return (T) result;
 		}

 		LoadEvent event = new LoadEvent( id, entityPersister.getEntityName(), false, eventSource, ... );
 		boolean success = false;
 		try {
 			context.fireLoad( event, LoadEventListener.GET );
 			success = true;
 		}
 		catch (ObjectNotFoundException e) { }
 		finally { context.afterOperation( success ); }
- 		return (T) event.getResult();
++
++		final Object result = event.getResult();
++		initializeIfNecessary( result );
++
++		return (T) result;
++	}
++
++	private void initializeIfNecessary(Object result) {
++		if ( result == null ) {
++			return;
++		}
++
++		if ( result instanceof HibernateProxy ) {
++			final HibernateProxy hibernateProxy = (HibernateProxy) result;
++			final LazyInitializer initializer = hibernateProxy.getHibernateLazyInitializer();
++			if ( initializer.isUninitialized() ) {
++				initializer.initialize();
++			}
++			return;
++		}
++
++		final BytecodeEnhancementMetadata enhancementMetadata = entityPersister.getEntityMetamodel().getBytecodeEnhancementMetadata();
++		if ( ! enhancementMetadata.isEnhancedForLazyLoading() ) {
++			return;
++		}
++
++		final BytecodeLazyAttributeInterceptor interceptor = enhancementMetadata.extractLazyInterceptor( result);
++		if ( interceptor instanceof EnhancementAsProxyLazinessInterceptor ) {
++			( (EnhancementAsProxyLazinessInterceptor) interceptor ).forceInitialize( result, null );
++		}
 	}
```

### New imports introduced to support the extracted method

```diff
++import org.hibernate.bytecode.enhance.spi.interceptor.BytecodeLazyAttributeInterceptor;
++import org.hibernate.bytecode.enhance.spi.interceptor.EnhancementAsProxyLazinessInterceptor;
++import org.hibernate.bytecode.spi.BytecodeEnhancementMetadata;
++import org.hibernate.proxy.HibernateProxy;
++import org.hibernate.proxy.LazyInitializer;
```

## Relevant final code in the merge

```java
// IdentifierLoadAccessImpl.java
@SuppressWarnings( "unchecked" )
protected final T doLoad(Object id) {
    final SessionImplementor session = context.getSession();
    final EventSource eventSource = (EventSource) session;
    final LoadQueryInfluencers loadQueryInfluencers = session.getLoadQueryInfluencers();

    if ( this.lockOptions != null ) {
        LoadEvent event = new LoadEvent( id, entityPersister.getEntityName(), lockOptions, eventSource,
                loadQueryInfluencers.getReadOnly() );
        context.fireLoad( event, LoadEventListener.GET );
        final Object result = event.getResult();
        initializeIfNecessary( result );
        return (T) result;
    }

    LoadEvent event = new LoadEvent( id, entityPersister.getEntityName(), false, eventSource,
            loadQueryInfluencers.getReadOnly() );
    boolean success = false;
    try {
        context.fireLoad( event, LoadEventListener.GET );
        success = true;
    }
    catch (ObjectNotFoundException e) {
        // if session cache contains proxy for non-existing object
    }
    finally {
        context.afterOperation( success );
    }

    final Object result = event.getResult();
    initializeIfNecessary( result );
    return (T) result;
}

private void initializeIfNecessary(Object result) {
    if ( result == null ) {
        return;
    }
    if ( result instanceof HibernateProxy ) {
        final HibernateProxy hibernateProxy = (HibernateProxy) result;
        final LazyInitializer initializer = hibernateProxy.getHibernateLazyInitializer();
        if ( initializer.isUninitialized() ) {
            initializer.initialize();
        }
        return;
    }
    final BytecodeEnhancementMetadata enhancementMetadata = entityPersister.getEntityMetamodel().getBytecodeEnhancementMetadata();
    if ( !enhancementMetadata.isEnhancedForLazyLoading() ) {
        return;
    }
    final BytecodeLazyAttributeInterceptor interceptor = enhancementMetadata.extractLazyInterceptor( result );
    if ( interceptor instanceof EnhancementAsProxyLazinessInterceptor ) {
        ( (EnhancementAsProxyLazinessInterceptor) interceptor ).forceInitialize( result, null );
    }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**30 lines** (++ lines for the new `initializeIfNecessary()` method body, local variable introductions at the two `return` sites, and the 5 new import lines)

## What each side had

**Parent 1 (P1)** had the original `doLoad()` implementation that returned `event.getResult()` directly without proxy/bytecode initialization logic — just `return (T) event.getResult();` in both the lock-options branch and the default path.

**Parent 2 (P2)** had `IdentifierLoadAccessImpl` as a new class (P2 introduced or rewrote this class), which included proxy-initialization logic embedded directly inside `doLoad()`, but structured differently — inline in P2's version without a separate helper method.

The merge extracted the proxy-initialization logic into a dedicated private method `initializeIfNecessary(Object result)`, replacing the two `return (T) event.getResult();` statements with a local variable capture, a call to `initializeIfNecessary()`, and then the return.

## Interpretation

This is a textbook **Extract_Method** refactoring. The `++` lines introduce a new private method `initializeIfNecessary(Object result)` that handles:
1. Null check early return
2. `HibernateProxy` initialization via `LazyInitializer`
3. Bytecode-enhanced proxy initialization via `EnhancementAsProxyLazinessInterceptor`

Before the extraction, the two `return (T) event.getResult()` statements in `doLoad()` (P1's version) were not performing this initialization. P2's version had this initialization logic but it appears to have been inline or structured differently. The merge chose to extract it into a reusable private method called at both return sites — a canonical Extract_Method outcome.

The `--` lines confirm P1 had bare `return (T) event.getResult();` at both sites without any initialization, while the `++` lines show the extracted method call replacing those bare returns. The 5 new import `++` lines further confirm that the proxy and bytecode enhancement types were not already available in the P1 version of this file.

## Complete diff

```diff
diff --cc hibernate-core/src/main/java/org/hibernate/loader/access/IdentifierLoadAccessImpl.java
index 78d78a461c8,00000000000..b206832683b
mode 100644,000000..100644
--- a/hibernate-core/src/main/java/org/hibernate/loader/access/IdentifierLoadAccessImpl.java
+++ b/hibernate-core/src/main/java/org/hibernate/loader/access/IdentifierLoadAccessImpl.java
@@@ -1,172 -1,0 +1,209 @@@
 package org.hibernate.loader.access;
 ...
++import org.hibernate.bytecode.enhance.spi.interceptor.BytecodeLazyAttributeInterceptor;
++import org.hibernate.bytecode.enhance.spi.interceptor.EnhancementAsProxyLazinessInterceptor;
++import org.hibernate.bytecode.spi.BytecodeEnhancementMetadata;
 ...
++import org.hibernate.proxy.HibernateProxy;
++import org.hibernate.proxy.LazyInitializer;
 ...
 	protected final T doLoad(Object id) {
 		...
 		if ( this.lockOptions != null ) {
 			LoadEvent event = new LoadEvent( id, entityPersister.getEntityName(), lockOptions, eventSource, ... );
 			context.fireLoad( event, LoadEventListener.GET );
- 			return (T) event.getResult();
++			final Object result = event.getResult();
++			initializeIfNecessary( result );
++
++			return (T) result;
 		}

 		LoadEvent event = new LoadEvent( ... );
 		boolean success = false;
 		try {
 			context.fireLoad( event, LoadEventListener.GET );
 			success = true;
 		}
 		catch (ObjectNotFoundException e) { }
 		finally { context.afterOperation( success ); }
- 		return (T) event.getResult();
++
++		final Object result = event.getResult();
++		initializeIfNecessary( result );
++
++		return (T) result;
++	}
++
++	private void initializeIfNecessary(Object result) {
++		if ( result == null ) {
++			return;
++		}
++		if ( result instanceof HibernateProxy ) {
++			final HibernateProxy hibernateProxy = (HibernateProxy) result;
++			final LazyInitializer initializer = hibernateProxy.getHibernateLazyInitializer();
++			if ( initializer.isUninitialized() ) {
++				initializer.initialize();
++			}
++			return;
++		}
++		final BytecodeEnhancementMetadata enhancementMetadata =
++				entityPersister.getEntityMetamodel().getBytecodeEnhancementMetadata();
++		if ( ! enhancementMetadata.isEnhancedForLazyLoading() ) {
++			return;
++		}
++		final BytecodeLazyAttributeInterceptor interceptor =
++				enhancementMetadata.extractLazyInterceptor( result);
++		if ( interceptor instanceof EnhancementAsProxyLazinessInterceptor ) {
++			( (EnhancementAsProxyLazinessInterceptor) interceptor ).forceInitialize( result, null );
++		}
 	}
 }

diff --cc hibernate-core/src/main/java/org/hibernate/mapping/ToOne.java
index 7d3e444e877,7ef8abac16f..42ba1334657
--- a/hibernate-core/src/main/java/org/hibernate/mapping/ToOne.java
+++ b/hibernate-core/src/main/java/org/hibernate/mapping/ToOne.java
@@@ -26,10 -26,20 +26,11 @@@
 	protected String referencedPropertyName;
 	private String referencedEntityName;
 	private String propertyName;
 -	private boolean embedded;
 	private boolean lazy = true;
 	protected boolean unwrapProxy;
+ 	protected boolean isUnwrapProxyImplicit;
 	protected boolean referenceToPrimaryKey = true;
```
