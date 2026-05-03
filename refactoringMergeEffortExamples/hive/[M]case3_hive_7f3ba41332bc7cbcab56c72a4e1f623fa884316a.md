# Case 3 — Project: hive — Merge commit SHA1: 7f3ba41332bc7cbcab56c72a4e1f623fa884316a

## Modified file(s):
- `ql/src/java/org/apache/hadoop/hive/ql/exec/Operator.java`
- `ql/src/java/org/apache/hadoop/hive/ql/exec/SparkHashTableSinkOperator.java`
- `ql/src/java/org/apache/hadoop/hive/ql/exec/vector/VectorSparkHashTableSinkOperator.java`
- `ql/src/java/org/apache/hadoop/hive/ql/exec/vector/VectorSparkPartitionPruningSinkOperator.java`
- `ql/src/java/org/apache/hadoop/hive/ql/parse/spark/SparkPartitionPruningSinkOperator.java`

## Class(es) modified in the merge:
- `Operator` (base class — inner `DefaultEdge` class)
- `SparkHashTableSinkOperator`
- `VectorSparkHashTableSinkOperator`
- `VectorSparkPartitionPruningSinkOperator`
- `SparkPartitionPruningSinkOperator`

## Merge effort lines in the combined diff

### Operator.java — base class `Change_Return_Type`: `Collection<Future<?>>` → `void` in `DefaultEdge.initializeOp()`

```diff
     @Override
 -    protected Collection<Future<?>> initializeOp(Configuration conf) {
 -      return childOperators;
 +    protected void initializeOp(Configuration conf) {
     }
```

### SparkHashTableSinkOperator.java — `Change_Return_Type` in override

```diff
   @Override
 -  protected Collection<Future<?>> initializeOp(Configuration hconf) throws HiveException {
 -    Collection<Future<?>> result = super.initializeOp(hconf);
 +  protected void initializeOp(Configuration hconf) throws HiveException {
 +    super.initializeOp(hconf);
     ObjectInspector[] inputOIs = new ObjectInspector[conf.getTagLength()];
+    byte tag = conf.getTag();
     inputOIs[tag] = inputObjInspectors[0];
     conf.setTagOrder(new Byte[]{ tag });
     htsOperator.setConf(conf);
```

### VectorSparkHashTableSinkOperator.java — `Change_Return_Type` in override (new file from P2)

```diff
   @Override
 -  protected Collection<Future<?>> initializeOp(Configuration hconf) throws HiveException {
 -    Collection<Future<?>> result = super.initializeOp(hconf);
 -    assert result.isEmpty();
++  protected void initializeOp(Configuration hconf) throws HiveException {
     inputObjInspectors[0] =
         VectorizedBatchUtil.convertToStandardStructObjectInspector((StructObjectInspector) inputObjInspectors[0]);
++    super.initializeOp(hconf);
     firstBatch = true;
 -    return result;
   }
```

### VectorSparkPartitionPruningSinkOperator.java — `Change_Return_Type` in override (new file from P2)

```diff
   @Override
 -  public Collection<Future<?>> initializeOp(Configuration hconf) throws HiveException {
 -    Collection<Future<?>> result = super.initializeOp(hconf);
 -    assert result.isEmpty();
++  public void initializeOp(Configuration hconf) throws HiveException {
     inputObjInspectors[0] =
         VectorizedBatchUtil.convertToStandardStructObjectInspector(
             (StructObjectInspector) inputObjInspectors[0]);
++    super.initializeOp(hconf);
     firstBatch = true;
 -    return result;
   }
```

### SparkPartitionPruningSinkOperator.java — `Change_Return_Type` in override (new file from P2)

```diff
   @SuppressWarnings("deprecation")
 -  public Collection<Future<?>> initializeOp(Configuration hconf) throws HiveException {
 -    Collection<Future<?>> result = super.initializeOp(hconf);
++  public void initializeOp(Configuration hconf) throws HiveException {
++    super.initializeOp(hconf);
     serializer = (Serializer) ReflectionUtils.newInstance(
         conf.getTable().getDeserializerClass(), null);
     buffer = new DataOutputBuffer();
 -    return result;
   }
```

## Relevant final code in the merge

```java
// Operator.java - base DefaultEdge inner class
@Override
protected void initializeOp(Configuration conf) {
    // void: no return
}

// SparkHashTableSinkOperator.java
@Override
protected void initializeOp(Configuration hconf) throws HiveException {
    super.initializeOp(hconf);
    // ... rest of initialization
}

// VectorSparkHashTableSinkOperator.java
@Override
protected void initializeOp(Configuration hconf) throws HiveException {
    inputObjInspectors[0] =
        VectorizedBatchUtil.convertToStandardStructObjectInspector(
            (StructObjectInspector) inputObjInspectors[0]);
    super.initializeOp(hconf);
    firstBatch = true;
}

// VectorSparkPartitionPruningSinkOperator.java / SparkPartitionPruningSinkOperator.java
@Override
public void initializeOp(Configuration hconf) throws HiveException {
    super.initializeOp(hconf);
    // ... class-specific initialization
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
**~18 lines** (++ for the new `void` signatures replacing `Collection<Future<?>>` return types, and removal of `return result` statements across all 5 classes)

## What each side had

**Parent 1 (P1)** had the Spark-specific operator classes (`SparkHashTableSinkOperator`, `SparkPartitionPruningSinkOperator`, and their vectorized variants) with `initializeOp()` returning `Collection<Future<?>>`. The P1 pattern was:
```java
protected Collection<Future<?>> initializeOp(Configuration hconf) throws HiveException {
    Collection<Future<?>> result = super.initializeOp(hconf);
    // ... class-specific setup ...
    return result;
}
```

**Parent 2 (P2)** changed `initializeOp()` from returning `Collection<Future<?>>` to `void` in the base `Operator` class hierarchy. P2's change eliminated the future collection return mechanism, simplifying the API. However, P2's versions of the Spark operator classes (new files) still had the old `Collection<Future<?>>` signature with `assert result.isEmpty()` guards before removing the return.

## Interpretation

This is a clear **Change_Return_Type** refactoring. P1 introduced `initializeOp()` returning `Collection<Future<?>>` as the method signature across the Spark operator hierarchy. P2 changed the base class `Operator.DefaultEdge.initializeOp()` to return `void` instead.

The evidence is unambiguous:
- The `--` lines show P2's old `Collection<Future<?>>` return type with `return result` statements.
- The `++` lines show the merged `void` return type with `super.initializeOp(hconf)` calls replacing the `Collection<Future<?>> result = super.initializeOp(hconf)` pattern.
- The removal of `assert result.isEmpty()` guards (also `--` lines) confirms that the entire result-collection mechanism was discarded.
- The change is consistent across all 5 operator classes: `Operator.DefaultEdge`, `SparkHashTableSinkOperator`, `VectorSparkHashTableSinkOperator`, `VectorSparkPartitionPruningSinkOperator`, and `SparkPartitionPruningSinkOperator`.

This represents a systematic API simplification where P1's mechanism of returning asynchronous futures from operator initialization was abolished in favor of a void method, requiring conflict resolution across the entire operator hierarchy.

## Complete diff

```diff
diff --cc ql/src/java/org/apache/hadoop/hive/ql/exec/Operator.java
index 861f53604f2,0f02737b8c5..9f1b20aae1d
--- a/ql/src/java/org/apache/hadoop/hive/ql/exec/Operator.java
+++ b/ql/src/java/org/apache/hadoop/hive/ql/exec/Operator.java
@@@ -1385,7 -1350,14 +1385,13 @@@
     @Override
 -    protected Collection<Future<?>> initializeOp(Configuration conf) {
 -      return childOperators;
 +    protected void initializeOp(Configuration conf) {
     }
   }
+
+   public void removeParents() { ... }
 }

diff --cc ql/src/java/org/apache/hadoop/hive/ql/exec/SparkHashTableSinkOperator.java
index 4a5f0b981a9,aa8808ac905..8dbe45ca8b4
--- a/ql/src/java/org/apache/hadoop/hive/ql/exec/SparkHashTableSinkOperator.java
+++ b/ql/src/java/org/apache/hadoop/hive/ql/exec/SparkHashTableSinkOperator.java
@@@ -61,9 -58,10 +58,10 @@@
   @Override
 -  protected Collection<Future<?>> initializeOp(Configuration hconf) throws HiveException {
 -    Collection<Future<?>> result = super.initializeOp(hconf);
 +  protected void initializeOp(Configuration hconf) throws HiveException {
 +    super.initializeOp(hconf);
     ObjectInspector[] inputOIs = new ObjectInspector[conf.getTagLength()];
+    byte tag = conf.getTag();
     inputOIs[tag] = inputObjInspectors[0];
     conf.setTagOrder(new Byte[]{ tag });
     htsOperator.setConf(conf);

diff --cc ql/src/java/org/apache/hadoop/hive/ql/exec/vector/VectorSparkHashTableSinkOperator.java
index 00000000000,6b9ac263715..8486d12d21e
@@@ -1,0 -1,104 +1,101 @@@
 + [new file from P2 — all + lines except key signature changes:]
   @Override
 -  protected Collection<Future<?>> initializeOp(Configuration hconf) throws HiveException {
 -    Collection<Future<?>> result = super.initializeOp(hconf);
 -    assert result.isEmpty();
++  protected void initializeOp(Configuration hconf) throws HiveException {
     inputObjInspectors[0] =
         VectorizedBatchUtil.convertToStandardStructObjectInspector(...);
++    super.initializeOp(hconf);
     firstBatch = true;
 -    return result;
   }

diff --cc ql/src/java/org/apache/hadoop/hive/ql/exec/vector/VectorSparkPartitionPruningSinkOperator.java
index 00000000000,3bce49d603a..eb0b408370a
@@@ -1,0 -1,99 +1,96 @@@
 + [new file from P2 — all + lines except key signature changes:]
   @Override
 -  public Collection<Future<?>> initializeOp(Configuration hconf) throws HiveException {
 -    Collection<Future<?>> result = super.initializeOp(hconf);
 -    assert result.isEmpty();
++  public void initializeOp(Configuration hconf) throws HiveException {
     inputObjInspectors[0] =
         VectorizedBatchUtil.convertToStandardStructObjectInspector(...);
++    super.initializeOp(hconf);
     firstBatch = true;
 -    return result;
   }

diff --cc ql/src/java/org/apache/hadoop/hive/ql/parse/spark/SparkPartitionPruningSinkOperator.java
index 00000000000,20432c771ce..cd1301d5fa7
@@@ -1,0 -1,142 +1,141 @@@
 + [new file from P2 — all + lines except key signature changes:]
   @SuppressWarnings("deprecation")
 -  public Collection<Future<?>> initializeOp(Configuration hconf) throws HiveException {
 -    Collection<Future<?>> result = super.initializeOp(hconf);
++  public void initializeOp(Configuration hconf) throws HiveException {
++    super.initializeOp(hconf);
     serializer = (Serializer) ReflectionUtils.newInstance(...);
     buffer = new DataOutputBuffer();
 -    return result;
   }

diff --cc ql/src/java/org/apache/hadoop/hive/ql/io/AcidUtils.java ...
[other files — no refactoring relevance]
```
