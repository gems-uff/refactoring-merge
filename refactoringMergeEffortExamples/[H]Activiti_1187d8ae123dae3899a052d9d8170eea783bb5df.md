# Project: Activiti — Merge commit SHA1: 1187d8ae123dae3899a052d9d8170eea783bb5df

## Modified file(s):
- `modules/activiti-engine/src/main/java/org/activiti/engine/compatibility/Activiti5CompatibilityHandler.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/AsyncExecutor.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/DefaultAsyncJobExecutor.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/ExecuteAsyncRunnable.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/ExecuteAsyncRunnableFactory.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/multitenant/ExecutorPerTenantAsyncExecutor.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/multitenant/SharedExecutorServiceAsyncExecutor.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/multitenant/TenantAwareExecuteAsyncRunnable.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/multitenant/TenantAwareExecuteAsyncRunnableFactory.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/cmd/LockExclusiveJobCmd.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/cmd/UnlockExclusiveJobCmd.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/jobexecutor/AsyncJobAddedNotification.java`
- `modules/activiti-spring/src/main/java/org/activiti/spring/SpringAsyncExecutor.java`
- `modules/activiti-spring/src/main/java/org/activiti/spring/SpringCallerRunsRejectedJobsHandler.java`
- `modules/activiti-spring/src/main/java/org/activiti/spring/SpringRejectedJobsHandler.java`

## Class(es) modified in the merge:
- `Activiti5CompatibilityHandler` (interface)
- `AsyncExecutor` (interface)
- `DefaultAsyncJobExecutor`
- `ExecuteAsyncRunnable`
- `ExecuteAsyncRunnableFactory` (interface)
- `ExecutorPerTenantAsyncExecutor`
- `SharedExecutorServiceAsyncExecutor`
- `TenantAwareExecuteAsyncRunnable`
- `TenantAwareExecuteAsyncRunnableFactory`
- `LockExclusiveJobCmd`
- `UnlockExclusiveJobCmd`
- `AsyncJobAddedNotification`
- `SpringAsyncExecutor`, `SpringCallerRunsRejectedJobsHandler`, `SpringRejectedJobsHandler`

## Merge effort lines in the combined diff

The pattern below repeats across all affected files. Shown for the most representative cases:

```diff
// Activiti5CompatibilityHandler.java — interface method signatures
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;

--  void executeJobWithLockAndRetry(JobEntity job);
++  void executeJobWithLockAndRetry(Job job);

--  void handleFailedJob(JobEntity job, Throwable exception);
++  void handleFailedJob(Job job, Throwable exception);

// AsyncExecutor.java — interface method
--  boolean executeAsyncJob(JobEntity job);
++  boolean executeAsyncJob(Job job);

// DefaultAsyncJobExecutor.java — field, constructor, methods
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;

--  protected LinkedList<JobEntity> temporaryJobQueue = new LinkedList<JobEntity>();
++  protected LinkedList<Job> temporaryJobQueue = new LinkedList<Job>();

--  public boolean executeAsyncJob(final JobEntity job) {
++  public boolean executeAsyncJob(final Job job) {

--  protected Runnable createRunnableForJob(final JobEntity job) {
++  protected Runnable createRunnableForJob(final Job job) {

--  protected void unacquireJob(final JobEntity job, CommandContext commandContext) {
++  protected void unacquireJob(final Job job, CommandContext commandContext) {

--      JobEntity job = temporaryJobQueue.pop();
++      Job job = temporaryJobQueue.pop();

// ExecuteAsyncRunnable.java — field and constructor
--  protected JobEntity job;
++  protected Job job;

--  public ExecuteAsyncRunnable(JobEntity job, CommandExecutor commandExecutor) {
++  public ExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor) {

// ExecuteAsyncRunnableFactory.java — interface method
--  Runnable createExecuteAsyncRunnable(JobEntity jobEntity, CommandExecutor commandExecutor);
++  Runnable createExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor);

// SharedExecutorServiceAsyncExecutor.java — anonymous class method + usage
--      public Runnable createExecuteAsyncRunnable(JobEntity jobEntity, CommandExecutor commandExecutor) {
++      public Runnable createExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor) {

--        return new TenantAwareExecuteAsyncRunnable(jobEntity, commandExecutor,
++        return new TenantAwareExecuteAsyncRunnable(job, commandExecutor,

// TenantAwareExecuteAsyncRunnable.java — constructor
--  public TenantAwareExecuteAsyncRunnable(JobEntity job, CommandExecutor commandExecutor, TenantInfoHolder tenantInfoHolder, String tenantId) {
++  public TenantAwareExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor, TenantInfoHolder tenantInfoHolder, String tenantId) {

// TenantAwareExecuteAsyncRunnableFactory.java — method + usage
--  public Runnable createExecuteAsyncRunnable(JobEntity jobEntity, CommandExecutor commandExecutor) {
--    return new TenantAwareExecuteAsyncRunnable(jobEntity, commandExecutor, tenantInfoHolder, tenantId);
++  public Runnable createExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor) {
++    return new TenantAwareExecuteAsyncRunnable(job, commandExecutor, tenantInfoHolder, tenantId);

// LockExclusiveJobCmd.java / UnlockExclusiveJobCmd.java / AsyncJobAddedNotification.java
--  protected JobEntity job;
++  protected Job job;
--  public LockExclusiveJobCmd(JobEntity job) {
++  public LockExclusiveJobCmd(Job job) {
```

## Relevant final code in the merge

```java
// AsyncExecutor.java (interface)
boolean executeAsyncJob(Job job);

// DefaultAsyncJobExecutor.java
protected LinkedList<Job> temporaryJobQueue = new LinkedList<Job>();

public boolean executeAsyncJob(final Job job) { ... }
protected Runnable createRunnableForJob(final Job job) { ... }
protected void unacquireJob(final Job job, CommandContext commandContext) { ... }

// ExecuteAsyncRunnableFactory.java (interface)
Runnable createExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor);
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
More than 60 lines (30+ `++` and 30+ `--`), spread across 15 files

## What each side had

**Parent 1 (P1)** changed the parameter type of all async job executor methods, interfaces, and fields from the concrete implementation class `JobEntity` to the interface `Job` (defined in `org.activiti.engine.runtime.Job`). This is a **Change_Parameter_Type** refactoring applied systematically across the entire async execution subsystem — interface methods, implementations, constructors, fields, and factory methods. P1 also renamed the parameter name `jobEntity` → `job` in factory methods as part of the change.

**Parent 2 (P2)** was working in the same files (e.g., adding `JobManager` injection to `DefaultAsyncJobExecutor`, restructuring `JobEntityManagerImpl`) but kept all method signatures and field types using the old `JobEntity` concrete class:
```java
// P2 (old type, discarded):
- boolean executeAsyncJob(JobEntity job);
- protected JobEntity job;
- public ExecuteAsyncRunnable(JobEntity job, CommandExecutor commandExecutor)
- public Runnable createExecuteAsyncRunnable(JobEntity jobEntity, CommandExecutor commandExecutor)
```

## Interpretation

This is a **Change_Parameter_Type** . P1 changed the parameter type of every method in the async executor subsystem from the concrete `JobEntity` to the `Job` interface, reflecting an abstraction-layer-widening refactoring. P2 simultaneously modified the same files without knowledge of P1's type change.

The evidence is unambiguous: every `--` line removes `JobEntity` and every `++` line introduces `Job` in its place — across interfaces, concrete classes, anonymous classes, fields, constructors, and local variables in 15 files. The parameter name change `jobEntity` → `job` in factory methods is also a **Rename_Parameter** refactoring applied as part of the same effort.

This case is Very Strong: more than 60 `++`/`--` lines directly traceable to the type change, the conflict spans the entire async executor module and its Spring integration, and the pattern is perfectly systematic and unambiguous.

## Complete diff

```diff
diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/compatibility/Activiti5CompatibilityHandler.java
index 8f424cb7c5,8f424cb7c5..f9e2af19dc
--- a/modules/activiti-engine/src/main/java/org/activiti/engine/compatibility/Activiti5CompatibilityHandler.java
+++ b/modules/activiti-engine/src/main/java/org/activiti/engine/compatibility/Activiti5CompatibilityHandler.java
@@@ -22,7 -22,7 +22,6 @@@
  import org.activiti.bpmn.model.MapExceptionEntry;
  import org.activiti.engine.delegate.BpmnError;
  import org.activiti.engine.delegate.DelegateExecution;
--import org.activiti.engine.impl.persistence.entity.JobEntity;
  import org.activiti.engine.impl.persistence.entity.SignalEventSubscriptionEntity;
  import org.activiti.engine.impl.persistence.entity.TaskEntity;
  import org.activiti.engine.impl.persistence.entity.VariableInstance;
@@@ -153,9 -153,9 +152,9 @@@
  
    void executeJob(Job job);
    
--  void executeJobWithLockAndRetry(JobEntity job);
++  void executeJobWithLockAndRetry(Job job);
    
--  void handleFailedJob(JobEntity job, Throwable exception);
++  void handleFailedJob(Job job, Throwable exception);
    
    void deleteJob(String jobId);

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/AsyncExecutor.java
index 093a833c0c,1a8f53f307..c8ebae8f24
--- a/modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/AsyncExecutor.java
+++ b/modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/AsyncExecutor.java
@@@ -14,6 -14,6 +14,7 @@@
  
  import org.activiti.engine.impl.interceptor.CommandExecutor;
  import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;
  
@@@ -36,7 -36,7 +37,7 @@@
--  boolean executeAsyncJob(JobEntity job);
++  boolean executeAsyncJob(Job job);

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/DefaultAsyncJobExecutor.java
index eea6f6b90a,b247eb4340..c2e9d3e7ba
--- a/modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/DefaultAsyncJobExecutor.java
+++ b/modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/DefaultAsyncJobExecutor.java
@@@ -13,7 -13,7 +13,7 @@@
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;

--  protected LinkedList<JobEntity> temporaryJobQueue = new LinkedList<JobEntity>();
++  protected LinkedList<Job> temporaryJobQueue = new LinkedList<Job>();

--  public boolean executeAsyncJob(final JobEntity job) {
++  public boolean executeAsyncJob(final Job job) {

--  protected Runnable createRunnableForJob(final JobEntity job) {
++  protected Runnable createRunnableForJob(final Job job) {

--  protected void unacquireJob(final JobEntity job, CommandContext commandContext) {
++  protected void unacquireJob(final Job job, CommandContext commandContext) {

--      JobEntity job = temporaryJobQueue.pop();
++      Job job = temporaryJobQueue.pop();

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/ExecuteAsyncRunnable.java
index 9c30b669f3,7b73cadd2b..86e987b755
--- a/modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/ExecuteAsyncRunnable.java
+++ b/modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/ExecuteAsyncRunnable.java
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;

--  protected JobEntity job;
++  protected Job job;

--  public ExecuteAsyncRunnable(JobEntity job, CommandExecutor commandExecutor) {
++  public ExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor) {

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/ExecuteAsyncRunnableFactory.java
index fc78078e37,fc78078e37..56869abdb5
--- a/modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/ExecuteAsyncRunnableFactory.java
+++ b/modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/ExecuteAsyncRunnableFactory.java
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;

--  Runnable createExecuteAsyncRunnable(JobEntity jobEntity, CommandExecutor commandExecutor);
++  Runnable createExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor);

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/multitenant/ExecutorPerTenantAsyncExecutor.java
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;

--  public boolean executeAsyncJob(JobEntity job) {
++  public boolean executeAsyncJob(Job job) {

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/multitenant/SharedExecutorServiceAsyncExecutor.java
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;

--      public Runnable createExecuteAsyncRunnable(JobEntity jobEntity, CommandExecutor commandExecutor) {
++      public Runnable createExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor) {

--        return new TenantAwareExecuteAsyncRunnable(jobEntity, commandExecutor,
++        return new TenantAwareExecuteAsyncRunnable(job, commandExecutor,

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/multitenant/TenantAwareExecuteAsyncRunnable.java
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;

--  public TenantAwareExecuteAsyncRunnable(JobEntity job, CommandExecutor commandExecutor, TenantInfoHolder tenantInfoHolder, String tenantId) {
++  public TenantAwareExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor, TenantInfoHolder tenantInfoHolder, String tenantId) {

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/asyncexecutor/multitenant/TenantAwareExecuteAsyncRunnableFactory.java
--  public Runnable createExecuteAsyncRunnable(JobEntity jobEntity, CommandExecutor commandExecutor) {
--    return new TenantAwareExecuteAsyncRunnable(jobEntity, commandExecutor, tenantInfoHolder, tenantId);
++  public Runnable createExecuteAsyncRunnable(Job job, CommandExecutor commandExecutor) {
++    return new TenantAwareExecuteAsyncRunnable(job, commandExecutor, tenantInfoHolder, tenantId);

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/cmd/LockExclusiveJobCmd.java
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;
--  protected JobEntity job;
++  protected Job job;
--  public LockExclusiveJobCmd(JobEntity job) {
++  public LockExclusiveJobCmd(Job job) {

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/cmd/UnlockExclusiveJobCmd.java
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;
--  protected JobEntity job;
++  protected Job job;
--  public UnlockExclusiveJobCmd(JobEntity job) {
++  public UnlockExclusiveJobCmd(Job job) {

diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/jobexecutor/AsyncJobAddedNotification.java
--import org.activiti.engine.impl.persistence.entity.JobEntity;
++import org.activiti.engine.runtime.Job;
--  protected JobEntity job;
++  protected Job job;
--  public AsyncJobAddedNotification(JobEntity job, AsyncExecutor asyncExecutor) {
++  public AsyncJobAddedNotification(Job job, AsyncExecutor asyncExecutor) {
```
