Project: elasticsearch — Merge commit SHA1: 3d0cedbabbedca4649f8778cb3e6329717db4b7a

## Modified file(s):
- `core/src/main/java/org/elasticsearch/action/support/replication/BasicReplicationRequest.java`
- `core/src/main/java/org/elasticsearch/action/support/replication/TransportReplicationAction.java`
- `core/src/main/java/org/elasticsearch/cluster/action/shard/ShardStateAction.java`
- `core/src/test/java/org/elasticsearch/action/support/replication/TransportReplicationActionTests.java`
- `core/src/test/java/org/elasticsearch/cluster/action/shard/ShardStateActionTests.java`
- `core/src/test/java/org/elasticsearch/index/mapper/DynamicMappingDisabledTests.java`

## Class(es) modified in the merge:
- `BasicReplicationRequest`
- `ShardStateAction`
- `TransportReplicationAction`

## Merge effort lines in the combined diff

```diff
# BasicReplicationRequest.java — constructor signature conflict
 -    public BasicReplicationRequest(ActionRequest<?> request, ShardId shardId) {
 -        super(request, shardId);
++    public BasicReplicationRequest(ShardId shardId) {
++        super(shardId);

# TransportRefreshAction.java — call-site conflict
-      protected BasicReplicationRequest newShardRequest(RefreshRequest request, ShardId shardId) {
-          return new BasicReplicationRequest(shardId);
 -        return new BasicReplicationRequest(request, shardId);
++        return new BasicReplicationRequest(shardId);

# ShardStateAction.java — constructor parameter addition conflict
  public ShardStateAction(Settings settings, ClusterService clusterService, TransportService transportService,
--                        AllocationService allocationService, RoutingService routingService) {
++                        AllocationService allocationService, RoutingService routingService, ThreadPool threadPool) {
  ...
++        this.threadPool = threadPool;

 -        ClusterStateObserver observer = new ClusterStateObserver(clusterService, null, logger);
++        ClusterStateObserver observer = new ClusterStateObserver(clusterService, null, logger, threadPool.getThreadContext());

# ShardStateActionTests.java — test constructor conflict
 -            super(settings, clusterService, transportService, allocationService, routingService);
++            super(settings, clusterService, transportService, allocationService, routingService, THREAD_POOL);

# TransportReplicationActionTests.java — constructor conflict
--                    new ShardStateAction(settings, clusterService, transportService, null, null), null,
++                    new ShardStateAction(settings, clusterService, transportService, null, null, threadPool), null,

# DynamicMappingDisabledTests.java — constructor conflict
--        shardStateAction = new ShardStateAction(settings, clusterService, transportService, null, null);
++        shardStateAction = new ShardStateAction(settings, clusterService, transportService, null, null, THREAD_POOL);
```

## Relevant final code in the merge

```java
// BasicReplicationRequest.java
public BasicReplicationRequest(ShardId shardId) {
    super(shardId);
}

// ShardStateAction.java
public ShardStateAction(Settings settings, ClusterService clusterService, TransportService transportService,
                        AllocationService allocationService, RoutingService routingService, ThreadPool threadPool) {
    ...
    this.threadPool = threadPool;
    ...
    ClusterStateObserver observer = new ClusterStateObserver(clusterService, null, logger, threadPool.getThreadContext());
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
12 lines (4 `--` lines and 8 `++` lines)

## What each side had

**Parent 1** had `BasicReplicationRequest(ShardId shardId)` (without an `ActionRequest<?> request` parameter) and `ShardStateAction` without a `ThreadPool` parameter.

**Parent 2** had `BasicReplicationRequest(ActionRequest<?> request, ShardId shardId)` (with the extra `request` parameter) and `ShardStateAction` with a `ThreadPool threadPool` parameter added.

## Interpretation

Two independent **Change_Parameter_Type** / parameter-list refactorings conflict here:

1. **`BasicReplicationRequest` constructor**: P2 had added an `ActionRequest<?> request` first parameter; P1 had removed it. The merge reconciled by adopting P1's simpler constructor (just `ShardId`), removing the `request` argument (`--`) and keeping the single-parameter form (`++`). All call sites in `TransportRefreshAction` required corresponding updates.

2. **`ShardStateAction` constructor**: P2 added a `ThreadPool threadPool` parameter. P1 had not. The merge incorporated the new parameter (`++`) and updated every construction site across tests (`++` in test files, `--` for the old calls missing the parameter). The added `threadPool.getThreadContext()` call inside `shardFailed` and `shardStarted` is the direct consequence — P2 needed thread context access, which required injecting `ThreadPool`.

Both are well-evidenced by the `--`/`++` pairs directly in the constructor declarations and all downstream call sites.

## Complete diff

```diff
diff --cc core/src/main/java/org/elasticsearch/action/admin/indices/refresh/TransportRefreshAction.java
@@@ -53,8 -53,8 +53,8 @@@
-      protected BasicReplicationRequest newShardRequest(RefreshRequest request, ShardId shardId) {
-          return new BasicReplicationRequest(shardId);
 -        return new BasicReplicationRequest(request, shardId);
++        return new BasicReplicationRequest(shardId);

diff --cc core/src/main/java/org/elasticsearch/action/support/replication/BasicReplicationRequest.java
@@@ (constructor) @@@
 -    public BasicReplicationRequest(ActionRequest<?> request, ShardId shardId) {
 -        super(request, shardId);
++    public BasicReplicationRequest(ShardId shardId) {
++        super(shardId);

diff --cc core/src/main/java/org/elasticsearch/cluster/action/shard/ShardStateAction.java
@@@ (constructor signature) @@@
  public ShardStateAction(...,
--                        AllocationService allocationService, RoutingService routingService) {
++                        AllocationService allocationService, RoutingService routingService, ThreadPool threadPool) {
++        this.threadPool = threadPool;

 -        ClusterStateObserver observer = new ClusterStateObserver(clusterService, null, logger);
++        ClusterStateObserver observer = new ClusterStateObserver(clusterService, null, logger, threadPool.getThreadContext());

diff --cc core/src/test/java/org/elasticsearch/cluster/action/shard/ShardStateActionTests.java
 -            super(settings, clusterService, transportService, allocationService, routingService);
++            super(settings, clusterService, transportService, allocationService, routingService, THREAD_POOL);

diff --cc core/src/test/java/org/elasticsearch/action/support/replication/TransportReplicationActionTests.java
--                    new ShardStateAction(settings, clusterService, transportService, null, null), null,
++                    new ShardStateAction(settings, clusterService, transportService, null, null, threadPool), null,

diff --cc core/src/test/java/org/elasticsearch/index/mapper/DynamicMappingDisabledTests.java
--        shardStateAction = new ShardStateAction(settings, clusterService, transportService, null, null);
++        shardStateAction = new ShardStateAction(settings, clusterService, transportService, null, null, THREAD_POOL);
```
