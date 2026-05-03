# Case 4 — Project: elasticsearch — Merge commit SHA1: 4bb5b4100d0687f29d758ce5a329c831c563ebe5

## Modified file(s):
- `core/src/main/java/org/elasticsearch/action/support/replication/TransportReplicationAction.java`

## Class(es) modified in the merge:
- `TransportReplicationAction`
- `TransportReplicationAction.IndexShardReferenceImpl` (inner class)

## Merge effort lines in the combined diff

```diff
# getIndexShardReferenceOnPrimary — method rename conflict
-      protected IndexShardReference getIndexShardOperationsCounterOnPrimary(ShardId shardId) {
-          ...
-          return new IndexShardReferenceImpl(indexShard);
 -        return new IndexShardReferenceImpl(indexShard, true);
++        return IndexShardReferenceImpl.createOnPrimary(indexShard);

# getIndexShardReferenceOnReplica — rename + signature change conflict
-      protected IndexShardReference getIndexShardOperationsCounterOnReplica(ShardId shardId, long opPrimaryTerm) {
-          ...
-          return new IndexShardReferenceImpl(indexShard, opPrimaryTerm);
 -    protected IndexShardReference getIndexShardReferenceOnReplica(ShardId shardId) {
 -        ...
 -        return new IndexShardReferenceImpl(indexShard, false);
++    protected IndexShardReference getIndexShardReferenceOnReplica(ShardId shardId, long primaryTerm) {
++        ...
++        return IndexShardReferenceImpl.createOnReplica(indexShard, primaryTerm);

# IndexShardReferenceImpl — constructor conflict
 -    IndexShardReferenceImpl(IndexShard indexShard, boolean primaryAction) {
++    private IndexShardReferenceImpl(IndexShard indexShard, long primaryTerm) {
         this.indexShard = indexShard;
 -        if (primaryAction) {
++        if (primaryTerm < 0) {
             operationLock = indexShard.acquirePrimaryOperationLock();
         } else {
 -            operationLock = indexShard.acquireReplicaOperationLock();
++            operationLock = indexShard.acquireReplicaOperationLock(primaryTerm);
         }

++    static IndexShardReferenceImpl createOnPrimary(IndexShard indexShard) {
++        return new IndexShardReferenceImpl(indexShard, -1);
++    }
++
++    static IndexShardReferenceImpl createOnReplica(IndexShard indexShard, long primaryTerm) {
++        return new IndexShardReferenceImpl(indexShard, primaryTerm);
++    }
```

## Relevant final code in the merge

```java
protected IndexShardReference getIndexShardReferenceOnPrimary(ShardId shardId) {
    IndexService indexService = indicesService.indexServiceSafe(shardId.getIndex());
    IndexShard indexShard = indexService.getShard(shardId.id());
    return IndexShardReferenceImpl.createOnPrimary(indexShard);
}

protected IndexShardReference getIndexShardReferenceOnReplica(ShardId shardId, long primaryTerm) {
    IndexService indexService = indicesService.indexServiceSafe(shardId.getIndex());
    IndexShard indexShard = indexService.getShard(shardId.id());
    return IndexShardReferenceImpl.createOnReplica(indexShard, primaryTerm);
}

private IndexShardReferenceImpl(IndexShard indexShard, long primaryTerm) {
    this.indexShard = indexShard;
    if (primaryTerm < 0) {
        operationLock = indexShard.acquirePrimaryOperationLock();
    } else {
        operationLock = indexShard.acquireReplicaOperationLock(primaryTerm);
    }
}

static IndexShardReferenceImpl createOnPrimary(IndexShard indexShard) {
    return new IndexShardReferenceImpl(indexShard, -1);
}

static IndexShardReferenceImpl createOnReplica(IndexShard indexShard, long primaryTerm) {
    return new IndexShardReferenceImpl(indexShard, primaryTerm);
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
16 lines (4 `--` lines and 12 `++` lines)

## What each side had

**Parent 1** had methods named `getIndexShardOperationsCounterOnPrimary` and `getIndexShardOperationsCounterOnReplica(ShardId, long opPrimaryTerm)`, and `IndexShardReferenceImpl` had separate constructors `(IndexShard)` (for primary) and `(IndexShard, long opPrimaryTerm)` (for replica).

**Parent 2** had renamed these methods to `getIndexShardReferenceOnPrimary` and `getIndexShardReferenceOnReplica(ShardId)` (without the `long` parameter), and the `IndexShardReferenceImpl` constructor used a `boolean primaryAction` to distinguish primary vs. replica.

## Interpretation

This is a compound **Rename_Method** + **Change_Parameter_Type** refactoring conflict. One parent renamed both getter methods and changed the replica method to carry a `long primaryTerm` parameter (instead of encoding it in a boolean). The other parent renamed the same methods but used a `boolean primaryAction` parameter. The merge had to reconcile both by:
- Adopting the `long primaryTerm` approach for the unified constructor (`Change_Parameter_Type`: `boolean primaryAction` → `long primaryTerm`, where `< 0` means primary)
- **Extract_Method**: introducing `createOnPrimary` and `createOnReplica` factory methods to replace the multi-overload constructor pattern
- Keeping the `getIndexShardReferenceOnReplica(ShardId, long primaryTerm)` name+signature

The `--` lines show the old `boolean primaryAction`-based dispatch and the old method name `getIndexShardReferenceOnReplica(ShardId)`, while `++` lines introduce the new unified `long primaryTerm`-based approach and the factory static methods.

## Complete diff

```diff
diff --cc core/src/main/java/org/elasticsearch/action/support/replication/TransportReplicationAction.java
@@@ -709,16 -780,24 +781,24 @@@
-      protected IndexShardReference getIndexShardOperationsCounterOnReplica(ShardId shardId, long opPrimaryTerm) {
-          ...
-          return new IndexShardReferenceImpl(indexShard, opPrimaryTerm);
 -    protected IndexShardReference getIndexShardReferenceOnReplica(ShardId shardId) {
 -        ...
 -        return new IndexShardReferenceImpl(indexShard, false);
++    protected IndexShardReference getIndexShardReferenceOnReplica(ShardId shardId, long primaryTerm) {
++        ...
++        return IndexShardReferenceImpl.createOnReplica(indexShard, primaryTerm);

-      protected IndexShardReference getIndexShardOperationsCounterOnPrimary(ShardId shardId) {
-          ...
-          return new IndexShardReferenceImpl(indexShard);
 -        return new IndexShardReferenceImpl(indexShard, true);
++        return IndexShardReferenceImpl.createOnPrimary(indexShard);

@@@ -1082,44 +1085,59 @@@
 -    IndexShardReferenceImpl(IndexShard indexShard, boolean primaryAction) {
++    private IndexShardReferenceImpl(IndexShard indexShard, long primaryTerm) {
         this.indexShard = indexShard;
 -        if (primaryAction) {
++        if (primaryTerm < 0) {
             operationLock = indexShard.acquirePrimaryOperationLock();
         } else {
 -            operationLock = indexShard.acquireReplicaOperationLock();
++            operationLock = indexShard.acquireReplicaOperationLock(primaryTerm);
         }

++    static IndexShardReferenceImpl createOnPrimary(IndexShard indexShard) {
++        return new IndexShardReferenceImpl(indexShard, -1);
++    }

++    static IndexShardReferenceImpl createOnReplica(IndexShard indexShard, long primaryTerm) {
++        return new IndexShardReferenceImpl(indexShard, primaryTerm);
++    }
```
