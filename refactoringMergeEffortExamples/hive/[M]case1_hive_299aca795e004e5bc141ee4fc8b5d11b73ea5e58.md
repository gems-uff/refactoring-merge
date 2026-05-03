# Case 1 — Project: hive — Merge commit SHA1: 299aca795e004e5bc141ee4fc8b5d11b73ea5e58

## Modified file(s):
- `hbase-handler/src/java/org/apache/hadoop/hive/hbase/HBaseStatsAggregator.java`
- `itests/util/src/main/java/org/apache/hadoop/hive/ql/stats/DummyStatsAggregator.java`
- `itests/util/src/main/java/org/apache/hadoop/hive/ql/stats/KeyVerifyingStatsAggregator.java`

## Class(es) modified in the merge:
- `HBaseStatsAggregator`
- `DummyStatsAggregator`
- `KeyVerifyingStatsAggregator`

## Merge effort lines in the combined diff

### HBaseStatsAggregator.java — `Change_Parameter_Type`: `MapRedTask` → `Task<?>` in `connect()`

```diff
 import org.apache.hadoop.hbase.filter.PrefixFilter;
 import org.apache.hadoop.hbase.util.Bytes;
 -import org.apache.hadoop.hive.ql.exec.mr.MapRedTask;
++import org.apache.hadoop.hive.ql.exec.Task;
 import org.apache.hadoop.hive.ql.stats.StatsAggregator;

 ...
-  public boolean connect(Configuration hiveconf) {
 -  public boolean connect(Configuration hiveconf, MapRedTask sourceTask) {
++  public boolean connect(Configuration hiveconf, Task<?> sourceTask) {
```

### DummyStatsAggregator.java — same `Change_Parameter_Type`

```diff
 import org.apache.hadoop.conf.Configuration;
 -import org.apache.hadoop.hive.ql.exec.mr.MapRedTask;
++import org.apache.hadoop.hive.ql.exec.Task;

 ...
-  public boolean connect(Configuration hconf) {
 -  public boolean connect(Configuration hconf, MapRedTask sourceTask) {
++  public boolean connect(Configuration hconf, Task<?> sourceTask) {
```

### KeyVerifyingStatsAggregator.java — same `Change_Parameter_Type`

```diff
 import org.apache.hadoop.conf.Configuration;
 -import org.apache.hadoop.hive.ql.exec.mr.MapRedTask;
++import org.apache.hadoop.hive.ql.exec.Task;
 import org.apache.hadoop.hive.ql.session.SessionState;

 ...
-  public boolean connect(Configuration hconf) {
 -  public boolean connect(Configuration hconf, MapRedTask sourceTask) {
++  public boolean connect(Configuration hconf, Task<?> sourceTask) {
```

## Relevant final code in the merge

```java
// HBaseStatsAggregator.java (and analogously in DummyStatsAggregator, KeyVerifyingStatsAggregator)
import org.apache.hadoop.hive.ql.exec.Task;
...
public boolean connect(Configuration hiveconf, Task<?> sourceTask) {
    // implementation unchanged, only parameter type widened
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**6 lines** (3 `++` import lines replacing `MapRedTask` with `Task`, and 3 `++` method signature lines introducing `Task<?> sourceTask`)

## What each side had

**Parent 1 (P1)** had `StatsAggregator.connect(Configuration)` — a single-parameter signature with no `sourceTask` parameter at all. The import for `MapRedTask` was not present.

**Parent 2 (P2)** had `StatsAggregator.connect(Configuration, MapRedTask sourceTask)` — a two-parameter signature using the concrete `MapRedTask` type, and the import `org.apache.hadoop.hive.ql.exec.mr.MapRedTask`.

## Interpretation

This is a clear **Change_Parameter_Type** refactoring. P2 had already introduced a second parameter `sourceTask` of type `MapRedTask` (a concrete subclass specific to MapReduce tasks) to the `connect()` interface method. P1 still had the original single-parameter version. The merge reconciled these by adopting P2's two-parameter signature but widening the parameter type from the concrete `MapRedTask` to the generic `Task<?>` — allowing any type of task (including Tez, Spark, etc.) to be passed.

The `--` lines confirm P2's narrow `MapRedTask sourceTask` type and the corresponding import. The `++` lines confirm the merged resolution adopted `Task<?> sourceTask` with the more general import `org.apache.hadoop.hive.ql.exec.Task`. This is consistent across all three implementing classes (`HBaseStatsAggregator`, `DummyStatsAggregator`, `KeyVerifyingStatsAggregator`), confirming the refactoring was systematic and originated in P2 before the merge.

## Complete diff

```diff
diff --cc hbase-handler/src/java/org/apache/hadoop/hive/hbase/HBaseStatsAggregator.java
index fafd68bc480,8fa5c3e88d8..39dbf8c4712
--- a/hbase-handler/src/java/org/apache/hadoop/hive/hbase/HBaseStatsAggregator.java
+++ b/hbase-handler/src/java/org/apache/hadoop/hive/hbase/HBaseStatsAggregator.java
@@@ -32,6 -32,7 +32,7 @@@
  import org.apache.hadoop.hbase.filter.PrefixFilter;
  import org.apache.hadoop.hbase.util.Bytes;
 -import org.apache.hadoop.hive.ql.exec.mr.MapRedTask;
++import org.apache.hadoop.hive.ql.exec.Task;
  import org.apache.hadoop.hive.ql.stats.StatsAggregator;

 @@@ -46,7 -47,7 +47,7 @@@
    /**
     * Does the necessary HBase initializations.
     */
-   public boolean connect(Configuration hiveconf) {
 -  public boolean connect(Configuration hiveconf, MapRedTask sourceTask) {
++  public boolean connect(Configuration hiveconf, Task<?> sourceTask) {
    // ...

diff --cc itests/util/src/main/java/org/apache/hadoop/hive/ql/stats/DummyStatsAggregator.java
index fafd68bc480,8fa5c3e88d8..39dbf8c4712
--- a/itests/util/src/main/java/org/apache/hadoop/hive/ql/stats/DummyStatsAggregator.java
+++ b/itests/util/src/main/java/org/apache/hadoop/hive/ql/stats/DummyStatsAggregator.java
@@@ -19,6 -19,7 +19,7 @@@
  package org.apache.hadoop.hive.ql.stats;
  import org.apache.hadoop.conf.Configuration;
 -import org.apache.hadoop.hive.ql.exec.mr.MapRedTask;
++import org.apache.hadoop.hive.ql.exec.Task;
 @@@ -32,7 -33,7 +33,7 @@@
-   public boolean connect(Configuration hconf) {
 -  public boolean connect(Configuration hconf, MapRedTask sourceTask) {
++  public boolean connect(Configuration hconf, Task<?> sourceTask) {

diff --cc itests/util/src/main/java/org/apache/hadoop/hive/ql/stats/KeyVerifyingStatsAggregator.java
index fafd68bc480,8fa5c3e88d8..39dbf8c4712
--- a/itests/util/src/main/java/org/apache/hadoop/hive/ql/stats/KeyVerifyingStatsAggregator.java
+++ b/itests/util/src/main/java/org/apache/hadoop/hive/ql/stats/KeyVerifyingStatsAggregator.java
@@@ -19,6 -19,7 +19,7 @@@
  import org.apache.hadoop.conf.Configuration;
 -import org.apache.hadoop.hive.ql.exec.mr.MapRedTask;
++import org.apache.hadoop.hive.ql.exec.Task;
  import org.apache.hadoop.hive.ql.session.SessionState;
 @@@ -29,7 -30,7 +30,7 @@@
-   public boolean connect(Configuration hconf) {
 -  public boolean connect(Configuration hconf, MapRedTask sourceTask) {
++  public boolean connect(Configuration hconf, Task<?> sourceTask) {
      return true;
    }
```
