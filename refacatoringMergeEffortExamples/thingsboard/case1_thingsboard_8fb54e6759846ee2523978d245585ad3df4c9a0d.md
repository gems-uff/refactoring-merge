# Case 1 — Project: thingsboard — Merge commit SHA1: 8fb54e6759846ee2523978d245585ad3df4c9a0d

---

## Modified file(s):
`application/src/main/java/org/thingsboard/server/service/subscription/TbSubscriptionUtils.java`
`application/src/main/java/org/thingsboard/server/service/queue/DefaultTbCoreConsumerService.java`

---

## Class(es) modified in the merge:
`TbSubscriptionUtils`, `DefaultTbCoreConsumerService`

---

## Merge effort lines in the combined diff

In `TbSubscriptionUtils.java` — removal of private methods and utility methods now moved to `KvProtoUtil`:
```diff
-- private static TsKvProto.Builder toKeyValueProto(long ts, KvEntry attr) { ... }
-- private static TransportProtos.TsValueProto toTsValueProto(long ts, KvEntry attr) { ... }
-- public static List<TsKvEntry> toTsKvEntityList(List<TsKvProto> dataList) { ... }
-- public static List<AttributeKvEntry> toAttributeKvList(List<TsKvProto> dataList) { ... }
-- private static KvEntry getKvEntry(KeyValueProto proto) { ... }
-- public static List<TsKvEntry> toTsKvEntityList(String key, List<TransportProtos.TsValueProto> dataList) { ... }
```

Import removals reflecting the move:
```diff
-- import org.thingsboard.server.common.data.kv.BaseAttributeKvEntry;
-- import org.thingsboard.server.common.data.kv.DataType;
-- import org.thingsboard.server.gen.transport.TransportProtos.KeyValueProto;
-- import org.thingsboard.server.gen.transport.TransportProtos.TsKvProto;
```

New static imports referencing the destination class:
```diff
++ import static org.thingsboard.server.common.util.KvProtoUtil.fromKeyValueTypeProto;
++ import static org.thingsboard.server.common.util.KvProtoUtil.toKeyValueTypeProto;
```

Call site updates in `TbSubscriptionUtils`:
```diff
-- ts.forEach(v -> builder.addData(toKeyValueProto(v.getTs(), v).build()));
++ ts.forEach(v -> builder.addData(toTsKvProtoBuilder(v.getTs(), v).build()));

-- attributes.forEach(v -> builder.addData(toKeyValueProto(v.getLastUpdateTs(), v).build()));
++ attributes.forEach(v -> builder.addData(toTsKvProtoBuilder(v.getLastUpdateTs(), v).build()));
```

In `DefaultTbCoreConsumerService.java`:
```diff
-- KvProtoUtil.toTsKvEntityList(proto.getDataList()), callback);
++ KvProtoUtil.fromTsKvProtoList(proto.getDataList()), callback);
```

Also removed — static initializer block no longer needed in `TbSubscriptionUtils`:
```diff
-- private static final DataType[] dataTypeByProtoNumber;
-- static {
--     int arraySize = Arrays.stream(DataType.values()).mapToInt(DataType::getProtoNumber).max().orElse(0);
--     dataTypeByProtoNumber = new DataType[arraySize + 1];
--     Arrays.stream(DataType.values()).forEach(dataType -> dataTypeByProtoNumber[dataType.getProtoNumber()] = dataType);
-- }
```

---

## Relevant final code in the merge

```java
// TbSubscriptionUtils.java — after merge
// private methods gone; now delegating to KvProtoUtil
import static org.thingsboard.server.common.util.KvProtoUtil.fromKeyValueTypeProto;
import static org.thingsboard.server.common.util.KvProtoUtil.toKeyValueTypeProto;

// call sites updated:
ts.forEach(v -> builder.addData(toTsKvProtoBuilder(v.getTs(), v).build()));
attributes.forEach(v -> builder.addData(toTsKvProtoBuilder(v.getLastUpdateTs(), v).build()));

// DefaultTbCoreConsumerService.java
KvProtoUtil.fromTsKvProtoList(proto.getDataList()), callback);
```

---

## Number of merge-effort lines (`++` and `--`) associated with the refactoring types under analysis:
**~55 lines**

---

## What each side had

**Parent 1** had `TbSubscriptionUtils` containing the proto conversion methods (`toKeyValueProto`, `toTsValueProto`, `toTsKvEntityList`, `toAttributeKvList`, `getKvEntry`) as private/public static methods, with call sites using `toKeyValueProto(...)` and `KvProtoUtil.toTsKvEntityList(...)`.

**Parent 2** had already performed a **Move_Method** refactoring: the proto conversion logic was moved from `TbSubscriptionUtils` to `KvProtoUtil` (a dedicated utility class), and the methods were renamed accordingly (`toTsKvProtoBuilder`, `fromTsKvProtoList`). P2 also renamed `toTsKvEntityList` → `fromTsKvProtoList` in `KvProtoUtil`.

The merge had to reconcile the two parents: P1 still had the methods in `TbSubscriptionUtils`, P2 had removed them and delegated to `KvProtoUtil`.

---

## Interpretation

The conflict was triggered by a **Move_Method** refactoring performed in P2: multiple static utility methods were moved from `TbSubscriptionUtils` to `KvProtoUtil`, and simultaneously **renamed** (`toKeyValueProto` → `toTsKvProtoBuilder`, `toTsKvEntityList` → `fromTsKvProtoList`).

The merge resolved this by:

1. **Removing all `--` methods from `TbSubscriptionUtils`** — the six private/public static methods that P2 had already moved to `KvProtoUtil` are eliminated from `TbSubscriptionUtils` via `--` lines.

2. **Removing the `--` static initializer** `dataTypeByProtoNumber` — an attribute that existed only to support the now-moved methods; its removal is a direct consequence of the **Push_Down_Attribute** / **Move_Attribute** performed in P2.

3. **Updating `++` call sites** to reference the new method names in `KvProtoUtil` (`toTsKvProtoBuilder`, `fromTsKvProtoList`), reconciling P1's old call sites with P2's renamed API.

4. **Adding `++` static imports** for `KvProtoUtil.fromKeyValueTypeProto` and `KvProtoUtil.toKeyValueTypeProto`, reflecting that the type-conversion logic now lives in `KvProtoUtil`.

This is a well-defensible example of:
- **Move_Method**: `toKeyValueProto`, `toTsKvEntityList`, `toAttributeKvList`, `getKvEntry` moved from `TbSubscriptionUtils` to `KvProtoUtil` in P2; the merge reconciles P1's still-present versions via `--` lines.
- **Rename_Method**: `toKeyValueProto` → `toTsKvProtoBuilder` and `toTsKvEntityList` → `fromTsKvProtoList` — the `++`/`--` at call sites confirm the rename conflict.
- **Move_Attribute**: the `dataTypeByProtoNumber` static field is removed (`--`) as a consequence of the method move.
