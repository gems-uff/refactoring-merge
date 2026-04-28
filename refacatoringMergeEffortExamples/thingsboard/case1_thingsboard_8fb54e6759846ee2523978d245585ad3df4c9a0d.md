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

## Complete diff

```diff
diff --cc application/src/main/java/org/thingsboard/server/service/queue/DefaultTbCoreConsumerService.java
index fbbb65d4ef,fd08b9da4d..cdb3f19601
--- a/application/src/main/java/org/thingsboard/server/service/queue/DefaultTbCoreConsumerService.java
+++ b/application/src/main/java/org/thingsboard/server/service/queue/DefaultTbCoreConsumerService.java
@@@ -583,7 -583,7 +583,7 @@@ public class DefaultTbCoreConsumerServi
              subscriptionManagerService.onTimeSeriesUpdate(
                      toTenantId(tenantIdMSB, tenantIdLSB),
                      TbSubscriptionUtils.toEntityId(proto.getEntityType(), proto.getEntityIdMSB(), proto.getEntityIdLSB()),
-                     KvProtoUtil.fromProtoList(proto.getDataList()), callback);
 -                    KvProtoUtil.toTsKvEntityList(proto.getDataList()), callback);
++                    KvProtoUtil.fromTsKvProtoList(proto.getDataList()), callback);
          } else if (msg.hasAttrUpdate()) {
              TbAttributeUpdateProto proto = msg.getAttrUpdate();
              subscriptionManagerService.onAttributesUpdate(
diff --cc application/src/main/java/org/thingsboard/server/service/subscription/TbSubscriptionUtils.java
index ff8b12a32f,d48851847c..243a840f51
--- a/application/src/main/java/org/thingsboard/server/service/subscription/TbSubscriptionUtils.java
+++ b/application/src/main/java/org/thingsboard/server/service/subscription/TbSubscriptionUtils.java
@@@ -23,10 -23,10 +23,8 @@@ import org.thingsboard.server.common.da
  import org.thingsboard.server.common.data.id.TenantId;
  import org.thingsboard.server.common.data.id.UserId;
  import org.thingsboard.server.common.data.kv.AttributeKvEntry;
--import org.thingsboard.server.common.data.kv.BaseAttributeKvEntry;
  import org.thingsboard.server.common.data.kv.BasicTsKvEntry;
  import org.thingsboard.server.common.data.kv.BooleanDataEntry;
--import org.thingsboard.server.common.data.kv.DataType;
  import org.thingsboard.server.common.data.kv.DoubleDataEntry;
  import org.thingsboard.server.common.data.kv.JsonDataEntry;
  import org.thingsboard.server.common.data.kv.KvEntry;
@@@ -35,8 -35,7 +33,6 @@@ import org.thingsboard.server.common.da
  import org.thingsboard.server.common.data.kv.TsKvEntry;
  import org.thingsboard.server.common.data.plugin.ComponentLifecycleEvent;
  import org.thingsboard.server.gen.transport.TransportProtos;
--import org.thingsboard.server.gen.transport.TransportProtos.KeyValueProto;
- import org.thingsboard.server.gen.transport.TransportProtos.KeyValueType;
  import org.thingsboard.server.gen.transport.TransportProtos.SubscriptionMgrMsgProto;
  import org.thingsboard.server.gen.transport.TransportProtos.TbAlarmDeleteProto;
  import org.thingsboard.server.gen.transport.TransportProtos.TbAlarmUpdateProto;
@@@ -47,7 -46,7 +43,6 @@@ import org.thingsboard.server.gen.trans
  import org.thingsboard.server.gen.transport.TransportProtos.TbTimeSeriesUpdateProto;
  import org.thingsboard.server.gen.transport.TransportProtos.ToCoreMsg;
  import org.thingsboard.server.gen.transport.TransportProtos.ToCoreNotificationMsg;
--import org.thingsboard.server.gen.transport.TransportProtos.TsKvProto;
  import org.thingsboard.server.service.ws.notification.sub.NotificationRequestUpdate;
  import org.thingsboard.server.service.ws.notification.sub.NotificationUpdate;
  import org.thingsboard.server.service.ws.notification.sub.NotificationsSubscriptionUpdate;
@@@ -60,7 -60,15 +55,10 @@@ import java.util.Map
  import java.util.TreeMap;
  import java.util.UUID;
  
 -public class TbSubscriptionUtils {
 -
 -    private static final DataType[] dataTypeByProtoNumber;
++import static org.thingsboard.server.common.util.KvProtoUtil.fromKeyValueTypeProto;
++import static org.thingsboard.server.common.util.KvProtoUtil.toKeyValueTypeProto;
+ 
 -    static {
 -        int arraySize = Arrays.stream(DataType.values()).mapToInt(DataType::getProtoNumber).max().orElse(0);
 -        dataTypeByProtoNumber = new DataType[arraySize + 1];
 -        Arrays.stream(DataType.values()).forEach(dataType -> dataTypeByProtoNumber[dataType.getProtoNumber()] = dataType);
 -    }
 +public class TbSubscriptionUtils {
  
      public static ToCoreMsg toSubEventProto(String serviceId, TbEntitySubEvent event) {
          SubscriptionMgrMsgProto.Builder msgBuilder = SubscriptionMgrMsgProto.newBuilder();
@@@ -181,7 -189,7 +179,7 @@@
          builder.setEntityIdLSB(entityId.getId().getLeastSignificantBits());
          builder.setTenantIdMSB(tenantId.getId().getMostSignificantBits());
          builder.setTenantIdLSB(tenantId.getId().getLeastSignificantBits());
--        ts.forEach(v -> builder.addData(toKeyValueProto(v.getTs(), v).build()));
++        ts.forEach(v -> builder.addData(toTsKvProtoBuilder(v.getTs(), v).build()));
          SubscriptionMgrMsgProto.Builder msgBuilder = SubscriptionMgrMsgProto.newBuilder();
          msgBuilder.setTsUpdate(builder);
          return ToCoreMsg.newBuilder().setToSubscriptionMgrMsg(msgBuilder.build()).build();
@@@ -208,7 -216,7 +206,7 @@@
          builder.setTenantIdMSB(tenantId.getId().getMostSignificantBits());
          builder.setTenantIdLSB(tenantId.getId().getLeastSignificantBits());
          builder.setScope(scope);
--        attributes.forEach(v -> builder.addData(toKeyValueProto(v.getLastUpdateTs(), v).build()));
++        attributes.forEach(v -> builder.addData(toTsKvProtoBuilder(v.getLastUpdateTs(), v).build()));
  
          SubscriptionMgrMsgProto.Builder msgBuilder = SubscriptionMgrMsgProto.newBuilder();
          msgBuilder.setAttrUpdate(builder);
@@@ -231,123 -239,121 +229,10 @@@
          return ToCoreMsg.newBuilder().setToSubscriptionMgrMsg(msgBuilder.build()).build();
      }
  
--    private static TsKvProto.Builder toKeyValueProto(long ts, KvEntry attr) {
--        KeyValueProto.Builder dataBuilder = KeyValueProto.newBuilder();
--        dataBuilder.setKey(attr.getKey());
-         dataBuilder.setType(KeyValueType.forNumber(attr.getDataType().ordinal()));
 -        dataBuilder.setType(toProto(attr.getDataType()));
--        switch (attr.getDataType()) {
--            case BOOLEAN:
--                attr.getBooleanValue().ifPresent(dataBuilder::setBoolV);
--                break;
--            case LONG:
--                attr.getLongValue().ifPresent(dataBuilder::setLongV);
--                break;
--            case DOUBLE:
--                attr.getDoubleValue().ifPresent(dataBuilder::setDoubleV);
--                break;
--            case JSON:
--                attr.getJsonValue().ifPresent(dataBuilder::setJsonV);
--                break;
--            case STRING:
--                attr.getStrValue().ifPresent(dataBuilder::setStringV);
--                break;
--        }
--        return TsKvProto.newBuilder().setTs(ts).setKv(dataBuilder);
--    }
--
--    private static TransportProtos.TsValueProto toTsValueProto(long ts, KvEntry attr) {
--        TransportProtos.TsValueProto.Builder dataBuilder = TransportProtos.TsValueProto.newBuilder();
--        dataBuilder.setTs(ts);
-         dataBuilder.setType(KeyValueType.forNumber(attr.getDataType().ordinal()));
 -        dataBuilder.setType(toProto(attr.getDataType()));
--        switch (attr.getDataType()) {
--            case BOOLEAN:
--                attr.getBooleanValue().ifPresent(dataBuilder::setBoolV);
--                break;
--            case LONG:
--                attr.getLongValue().ifPresent(dataBuilder::setLongV);
--                break;
--            case DOUBLE:
--                attr.getDoubleValue().ifPresent(dataBuilder::setDoubleV);
--                break;
--            case JSON:
--                attr.getJsonValue().ifPresent(dataBuilder::setJsonV);
--                break;
--            case STRING:
--                attr.getStrValue().ifPresent(dataBuilder::setStringV);
--                break;
--        }
--        return dataBuilder.build();
--    }
--
--
      public static EntityId toEntityId(String entityType, long entityIdMSB, long entityIdLSB) {
          return EntityIdFactory.getByTypeAndUuid(entityType, new UUID(entityIdMSB, entityIdLSB));
      }
  
--    public static List<TsKvEntry> toTsKvEntityList(List<TsKvProto> dataList) {
--        List<TsKvEntry> result = new ArrayList<>(dataList.size());
--        dataList.forEach(proto -> result.add(new BasicTsKvEntry(proto.getTs(), getKvEntry(proto.getKv()))));
--        return result;
--    }
--
--    public static List<AttributeKvEntry> toAttributeKvList(List<TsKvProto> dataList) {
--        List<AttributeKvEntry> result = new ArrayList<>(dataList.size());
--        dataList.forEach(proto -> result.add(new BaseAttributeKvEntry(getKvEntry(proto.getKv()), proto.getTs())));
--        return result;
--    }
--
--    private static KvEntry getKvEntry(KeyValueProto proto) {
--        KvEntry entry = null;
-         DataType type = DataType.values()[proto.getType().getNumber()];
-         switch (type) {
 -        switch (fromProto(proto.getType())) {
--            case BOOLEAN:
--                entry = new BooleanDataEntry(proto.getKey(), proto.getBoolV());
--                break;
--            case LONG:
--                entry = new LongDataEntry(proto.getKey(), proto.getLongV());
--                break;
--            case DOUBLE:
--                entry = new DoubleDataEntry(proto.getKey(), proto.getDoubleV());
--                break;
--            case STRING:
--                entry = new StringDataEntry(proto.getKey(), proto.getStringV());
--                break;
--            case JSON:
--                entry = new JsonDataEntry(proto.getKey(), proto.getJsonV());
--                break;
--        }
--        return entry;
--    }
--
--    public static List<TsKvEntry> toTsKvEntityList(String key, List<TransportProtos.TsValueProto> dataList) {
--        List<TsKvEntry> result = new ArrayList<>(dataList.size());
--        dataList.forEach(proto -> result.add(new BasicTsKvEntry(proto.getTs(), getKvEntry(key, proto))));
--        return result;
--    }
--
--    private static KvEntry getKvEntry(String key, TransportProtos.TsValueProto proto) {
--        KvEntry entry = null;
-         DataType type = DataType.values()[proto.getType().getNumber()];
-         switch (type) {
 -        switch (fromProto(proto.getType())) {
--            case BOOLEAN:
--                entry = new BooleanDataEntry(key, proto.getBoolV());
--                break;
--            case LONG:
--                entry = new LongDataEntry(key, proto.getLongV());
--                break;
--            case DOUBLE:
--                entry = new DoubleDataEntry(key, proto.getDoubleV());
--                break;
--            case STRING:
--                entry = new StringDataEntry(key, proto.getStringV());
--                break;
--            case JSON:
--                entry = new JsonDataEntry(key, proto.getJsonV());
--                break;
--        }
--        return entry;
--    }
--
      public static ToCoreMsg toAlarmUpdateProto(TenantId tenantId, EntityId entityId, AlarmInfo alarm) {
          TbAlarmUpdateProto.Builder builder = TbAlarmUpdateProto.newBuilder();
          builder.setEntityType(entityId.getEntityType().name());
@@@ -405,7 -411,7 +290,7 @@@
      public static List<TsKvEntry> fromProto(TransportProtos.TbSubUpdateProto proto) {
          List<TsKvEntry> result = new ArrayList<>();
          for (var p : proto.getDataList()) {
--            result.addAll(toTsKvEntityList(p.getKey(), p.getTsValueList()));
++            result.addAll(fromTsValueProtoList(p.getKey(), p.getTsValueList()));
          }
          return result;
      }
@@@ -447,4 -453,12 +332,48 @@@
          return ToCoreNotificationMsg.newBuilder().setToLocalSubscriptionServiceMsg(result).build();
      }
  
 -    public static TransportProtos.KeyValueType toProto(DataType dataType) {
 -        return TransportProtos.KeyValueType.forNumber(dataType.getProtoNumber());
++    public static TransportProtos.TsKvProto.Builder toTsKvProtoBuilder(long ts, KvEntry attr) {
++        TransportProtos.KeyValueProto.Builder dataBuilder = TransportProtos.KeyValueProto.newBuilder();
++        dataBuilder.setKey(attr.getKey());
++        dataBuilder.setType(toKeyValueTypeProto(attr.getDataType()));
++        switch (attr.getDataType()) {
++            case BOOLEAN -> attr.getBooleanValue().ifPresent(dataBuilder::setBoolV);
++            case LONG -> attr.getLongValue().ifPresent(dataBuilder::setLongV);
++            case DOUBLE -> attr.getDoubleValue().ifPresent(dataBuilder::setDoubleV);
++            case JSON -> attr.getJsonValue().ifPresent(dataBuilder::setJsonV);
++            case STRING -> attr.getStrValue().ifPresent(dataBuilder::setStringV);
++        }
++        return TransportProtos.TsKvProto.newBuilder().setTs(ts).setKv(dataBuilder);
++    }
++
++    public static TransportProtos.TsValueProto toTsValueProto(long ts, KvEntry attr) {
++        TransportProtos.TsValueProto.Builder dataBuilder = TransportProtos.TsValueProto.newBuilder();
++        dataBuilder.setTs(ts);
++        dataBuilder.setType(toKeyValueTypeProto(attr.getDataType()));
++        switch (attr.getDataType()) {
++            case BOOLEAN -> attr.getBooleanValue().ifPresent(dataBuilder::setBoolV);
++            case LONG -> attr.getLongValue().ifPresent(dataBuilder::setLongV);
++            case DOUBLE -> attr.getDoubleValue().ifPresent(dataBuilder::setDoubleV);
++            case JSON -> attr.getJsonValue().ifPresent(dataBuilder::setJsonV);
++            case STRING -> attr.getStrValue().ifPresent(dataBuilder::setStringV);
++        }
++        return dataBuilder.build();
++    }
++
++    private static List<TsKvEntry> fromTsValueProtoList(String key, List<TransportProtos.TsValueProto> dataList) {
++        List<TsKvEntry> result = new ArrayList<>(dataList.size());
++        dataList.forEach(proto -> result.add(new BasicTsKvEntry(proto.getTs(), fromTsKvProto(key, proto))));
++        return result;
+     }
+ 
 -    public static DataType fromProto(TransportProtos.KeyValueType keyValueType) {
 -        return dataTypeByProtoNumber[keyValueType.getNumber()];
++    private static KvEntry fromTsKvProto(String key, TransportProtos.TsValueProto proto) {
++        return switch (fromKeyValueTypeProto(proto.getType())) {
++            case BOOLEAN -> new BooleanDataEntry(key, proto.getBoolV());
++            case LONG -> new LongDataEntry(key, proto.getLongV());
++            case DOUBLE -> new DoubleDataEntry(key, proto.getDoubleV());
++            case STRING -> new StringDataEntry(key, proto.getStringV());
++            case JSON -> new JsonDataEntry(key, proto.getJsonV());
++        };
+     }
+ 
  }
diff --cc common/proto/src/main/java/org/thingsboard/server/common/util/KvProtoUtil.java
index 2532ce00d2,504ffe368d..14368693c5
--- a/common/proto/src/main/java/org/thingsboard/server/common/util/KvProtoUtil.java
+++ b/common/proto/src/main/java/org/thingsboard/server/common/util/KvProtoUtil.java
@@@ -35,20 -34,6 +35,20 @@@ import java.util.List
  
  public class KvProtoUtil {
  
 +    private static final DataType[] dataTypeByProtoNumber;
 +
 +    static {
 +        int arraySize = Arrays.stream(DataType.values()).mapToInt(DataType::getProtoNumber).max().orElse(0);
 +        dataTypeByProtoNumber = new DataType[arraySize + 1];
 +        Arrays.stream(DataType.values()).forEach(dataType -> dataTypeByProtoNumber[dataType.getProtoNumber()] = dataType);
 +    }
 +
 +    public static List<AttributeKvEntry> toAttributeKvList(List<TransportProtos.TsKvProto> dataList) {
 +        List<AttributeKvEntry> result = new ArrayList<>(dataList.size());
-         dataList.forEach(proto -> result.add(new BaseAttributeKvEntry(fromProto(proto.getKv()), proto.getTs())));
++        dataList.forEach(proto -> result.add(new BaseAttributeKvEntry(fromTsKvProto(proto.getKv()), proto.getTs())));
 +        return result;
 +    }
 +
      public static List<TransportProtos.TsKvProto> attrToTsKvProtos(List<AttributeKvEntry> result) {
          List<TransportProtos.TsKvProto> clientAttributes;
          if (result == null || result.isEmpty()) {
@@@ -62,7 -47,8 +62,7 @@@
          return clientAttributes;
      }
  
-     public static List<TransportProtos.TsKvProto> toProtoList(List<TsKvEntry> result) {
 -
 -    public static List<TransportProtos.TsKvProto> tsToTsKvProtos(List<TsKvEntry> result) {
++    public static List<TransportProtos.TsKvProto> toTsKvProtoList(List<TsKvEntry> result) {
          List<TransportProtos.TsKvProto> ts;
          if (result == null || result.isEmpty()) {
              ts = Collections.emptyList();
@@@ -75,51 -61,95 +75,51 @@@
          return ts;
      }
  
-     public static List<TsKvEntry> fromProtoList(List<TransportProtos.TsKvProto> dataList) {
++    public static List<TsKvEntry> fromTsKvProtoList(List<TransportProtos.TsKvProto> dataList) {
 +        List<TsKvEntry> result = new ArrayList<>(dataList.size());
-         dataList.forEach(proto -> result.add(new BasicTsKvEntry(proto.getTs(), fromProto(proto.getKv()))));
++        dataList.forEach(proto -> result.add(new BasicTsKvEntry(proto.getTs(), fromTsKvProto(proto.getKv()))));
 +        return result;
 +    }
 +
-     public static TransportProtos.TsKvProto toProto(long ts, KvEntry kvEntry) {
+     public static TransportProtos.TsKvProto toTsKvProto(long ts, KvEntry kvEntry) {
          return TransportProtos.TsKvProto.newBuilder().setTs(ts)
-                 .setKv(KvProtoUtil.toProto(kvEntry)).build();
 -                .setKv(KvProtoUtil.toKeyValueProto(kvEntry)).build();
++                .setKv(KvProtoUtil.toKeyValueTypeProto(kvEntry)).build();
 +    }
 +
-     public static TsKvEntry fromProto(TransportProtos.TsKvProto proto) {
-         return new BasicTsKvEntry(proto.getTs(), fromProto(proto.getKv()));
++    public static TsKvEntry fromTsKvProto(TransportProtos.TsKvProto proto) {
++        return new BasicTsKvEntry(proto.getTs(), fromTsKvProto(proto.getKv()));
      }
  
-     public static TransportProtos.KeyValueProto toProto(KvEntry kvEntry) {
 -    public static TransportProtos.KeyValueProto toKeyValueProto(KvEntry kvEntry) {
++    public static TransportProtos.KeyValueProto toKeyValueTypeProto(KvEntry kvEntry) {
          TransportProtos.KeyValueProto.Builder builder = TransportProtos.KeyValueProto.newBuilder();
          builder.setKey(kvEntry.getKey());
-         builder.setType(toProto(kvEntry.getDataType()));
++        builder.setType(toKeyValueTypeProto(kvEntry.getDataType()));
          switch (kvEntry.getDataType()) {
 -            case BOOLEAN:
 -                builder.setType(TransportProtos.KeyValueType.BOOLEAN_V);
 -                builder.setBoolV(kvEntry.getBooleanValue().get());
 -                break;
 -            case DOUBLE:
 -                builder.setType(TransportProtos.KeyValueType.DOUBLE_V);
 -                builder.setDoubleV(kvEntry.getDoubleValue().get());
 -                break;
 -            case LONG:
 -                builder.setType(TransportProtos.KeyValueType.LONG_V);
 -                builder.setLongV(kvEntry.getLongValue().get());
 -                break;
 -            case STRING:
 -                builder.setType(TransportProtos.KeyValueType.STRING_V);
 -                builder.setStringV(kvEntry.getStrValue().get());
 -                break;
 -            case JSON:
 -                builder.setType(TransportProtos.KeyValueType.JSON_V);
 -                builder.setJsonV(kvEntry.getJsonValue().get());
 -                break;
 +            case BOOLEAN -> kvEntry.getBooleanValue().ifPresent(builder::setBoolV);
 +            case LONG -> kvEntry.getLongValue().ifPresent(builder::setLongV);
 +            case DOUBLE -> kvEntry.getDoubleValue().ifPresent(builder::setDoubleV);
 +            case JSON -> kvEntry.getJsonValue().ifPresent(builder::setJsonV);
 +            case STRING -> kvEntry.getStrValue().ifPresent(builder::setStringV);
          }
          return builder.build();
      }
  
-     public static KvEntry fromProto(TransportProtos.KeyValueProto proto) {
-         return switch (fromProto(proto.getType())) {
 -    public static TransportProtos.TsKvProto.Builder toKeyValueProto(long ts, KvEntry attr) {
 -        TransportProtos.KeyValueProto.Builder dataBuilder = TransportProtos.KeyValueProto.newBuilder();
 -        dataBuilder.setKey(attr.getKey());
 -        dataBuilder.setType(TransportProtos.KeyValueType.forNumber(attr.getDataType().ordinal()));
 -        switch (attr.getDataType()) {
 -            case BOOLEAN:
 -                attr.getBooleanValue().ifPresent(dataBuilder::setBoolV);
 -                break;
 -            case LONG:
 -                attr.getLongValue().ifPresent(dataBuilder::setLongV);
 -                break;
 -            case DOUBLE:
 -                attr.getDoubleValue().ifPresent(dataBuilder::setDoubleV);
 -                break;
 -            case JSON:
 -                attr.getJsonValue().ifPresent(dataBuilder::setJsonV);
 -                break;
 -            case STRING:
 -                attr.getStrValue().ifPresent(dataBuilder::setStringV);
 -                break;
 -        }
 -        return TransportProtos.TsKvProto.newBuilder().setTs(ts).setKv(dataBuilder);
++    public static KvEntry fromTsKvProto(TransportProtos.KeyValueProto proto) {
++        return switch (fromKeyValueTypeProto(proto.getType())) {
 +            case BOOLEAN -> new BooleanDataEntry(proto.getKey(), proto.getBoolV());
 +            case LONG -> new LongDataEntry(proto.getKey(), proto.getLongV());
 +            case DOUBLE -> new DoubleDataEntry(proto.getKey(), proto.getDoubleV());
 +            case STRING -> new StringDataEntry(proto.getKey(), proto.getStringV());
 +            case JSON -> new JsonDataEntry(proto.getKey(), proto.getJsonV());
 +        };
      }
  
-     public static TransportProtos.KeyValueType toProto(DataType dataType) {
 -    public static List<TsKvEntry> toTsKvEntityList(List<TransportProtos.TsKvProto> dataList) {
 -        List<TsKvEntry> result = new ArrayList<>(dataList.size());
 -        dataList.forEach(proto -> result.add(new BasicTsKvEntry(proto.getTs(), getKvEntry(proto.getKv()))));
 -        return result;
++    public static TransportProtos.KeyValueType toKeyValueTypeProto(DataType dataType) {
 +        return TransportProtos.KeyValueType.forNumber(dataType.getProtoNumber());
      }
  
-     public static DataType fromProto(TransportProtos.KeyValueType keyValueType) {
 -    public static List<AttributeKvEntry> toAttributeKvList(List<TransportProtos.TsKvProto> dataList) {
 -        List<AttributeKvEntry> result = new ArrayList<>(dataList.size());
 -        dataList.forEach(proto -> result.add(new BaseAttributeKvEntry(getKvEntry(proto.getKv()), proto.getTs())));
 -        return result;
++    public static DataType fromKeyValueTypeProto(TransportProtos.KeyValueType keyValueType) {
 +        return dataTypeByProtoNumber[keyValueType.getNumber()];
      }
  
 -    private static KvEntry getKvEntry(TransportProtos.KeyValueProto proto) {
 -        KvEntry entry = null;
 -        DataType type = DataType.values()[proto.getType().getNumber()];
 -        switch (type) {
 -            case BOOLEAN:
 -                entry = new BooleanDataEntry(proto.getKey(), proto.getBoolV());
 -                break;
 -            case LONG:
 -                entry = new LongDataEntry(proto.getKey(), proto.getLongV());
 -                break;
 -            case DOUBLE:
 -                entry = new DoubleDataEntry(proto.getKey(), proto.getDoubleV());
 -                break;
 -            case STRING:
 -                entry = new StringDataEntry(proto.getKey(), proto.getStringV());
 -                break;
 -            case JSON:
 -                entry = new JsonDataEntry(proto.getKey(), proto.getJsonV());
 -                break;
 -        }
 -        return entry;
 -    }
  }
diff --cc common/proto/src/test/java/org/thingsboard/server/common/util/KvProtoUtilTest.java
index 0fad4e48a2,0000000000..1fbfaf52d9
mode 100644,000000..100644
--- a/common/proto/src/test/java/org/thingsboard/server/common/util/KvProtoUtilTest.java
+++ b/common/proto/src/test/java/org/thingsboard/server/common/util/KvProtoUtilTest.java
@@@ -1,114 -1,0 +1,114 @@@
 +/**
 + * Copyright © 2016-2024 The Thingsboard Authors
 + *
 + * Licensed under the Apache License, Version 2.0 (the "License");
 + * you may not use this file except in compliance with the License.
 + * You may obtain a copy of the License at
 + *
 + *     http://www.apache.org/licenses/LICENSE-2.0
 + *
 + * Unless required by applicable law or agreed to in writing, software
 + * distributed under the License is distributed on an "AS IS" BASIS,
 + * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 + * See the License for the specific language governing permissions and
 + * limitations under the License.
 + */
 +package org.thingsboard.server.common.util;
 +
 +import org.junit.jupiter.api.Test;
 +import org.junit.jupiter.params.ParameterizedTest;
 +import org.junit.jupiter.params.provider.EnumSource;
 +import org.junit.jupiter.params.provider.MethodSource;
 +import org.junit.jupiter.params.provider.ValueSource;
 +import org.thingsboard.server.common.data.kv.AggTsKvEntry;
 +import org.thingsboard.server.common.data.kv.AttributeKvEntry;
 +import org.thingsboard.server.common.data.kv.BaseAttributeKvEntry;
 +import org.thingsboard.server.common.data.kv.BasicTsKvEntry;
 +import org.thingsboard.server.common.data.kv.BooleanDataEntry;
 +import org.thingsboard.server.common.data.kv.DataType;
 +import org.thingsboard.server.common.data.kv.DoubleDataEntry;
 +import org.thingsboard.server.common.data.kv.JsonDataEntry;
 +import org.thingsboard.server.common.data.kv.KvEntry;
 +import org.thingsboard.server.common.data.kv.LongDataEntry;
 +import org.thingsboard.server.common.data.kv.StringDataEntry;
 +import org.thingsboard.server.common.data.kv.TsKvEntry;
 +
 +import java.util.List;
 +import java.util.stream.Collectors;
 +import java.util.stream.Stream;
 +
 +import static org.assertj.core.api.Assertions.assertThat;
 +
 +class KvProtoUtilTest {
 +
 +    private static final long TS = System.currentTimeMillis();
 +
 +    private static Stream<KvEntry> kvEntryData() {
 +        String key = "key";
 +        return Stream.of(
 +                new BooleanDataEntry(key, true),
 +                new LongDataEntry(key, 23L),
 +                new DoubleDataEntry(key, 23.0),
 +                new StringDataEntry(key, "stringValue"),
 +                new JsonDataEntry(key, "jsonValue")
 +        );
 +    }
 +
 +    private static Stream<KvEntry> basicTsKvEntryData() {
 +        return kvEntryData().map(kvEntry -> new BasicTsKvEntry(TS, kvEntry));
 +    }
 +
 +    private static Stream<AttributeKvEntry> attributeKvEntryData() {
 +        return kvEntryData().map(kvEntry -> new BaseAttributeKvEntry(TS, kvEntry));
 +    }
 +
 +    private static List<TsKvEntry> createTsKvEntryList(boolean withAggregation) {
 +        return kvEntryData().map(kvEntry -> {
 +                    if (withAggregation) {
 +                        return new AggTsKvEntry(TS, kvEntry, 0);
 +                    } else {
 +                        return new BasicTsKvEntry(TS, kvEntry);
 +                    }
 +                }).collect(Collectors.toList());
 +    }
 +
 +    @ParameterizedTest
 +    @EnumSource(DataType.class)
 +    void protoDataTypeSerialization(DataType dataType) {
-         assertThat(KvProtoUtil.fromProto(KvProtoUtil.toProto(dataType))).as(dataType.name()).isEqualTo(dataType);
++        assertThat(KvProtoUtil.fromKeyValueTypeProto(KvProtoUtil.toKeyValueTypeProto(dataType))).as(dataType.name()).isEqualTo(dataType);
 +    }
 +
 +    @ParameterizedTest
 +    @MethodSource("kvEntryData")
 +    void protoKeyValueProtoSerialization(KvEntry kvEntry) {
-         assertThat(KvProtoUtil.fromProto(KvProtoUtil.toProto(kvEntry)))
++        assertThat(KvProtoUtil.fromTsKvProto(KvProtoUtil.toKeyValueTypeProto(kvEntry)))
 +                .as("deserialized")
 +                .isEqualTo(kvEntry);
 +    }
 +
 +    @ParameterizedTest
 +    @MethodSource("basicTsKvEntryData")
 +    void protoTsKvEntrySerialization(KvEntry kvEntry) {
-         assertThat(KvProtoUtil.fromProto(KvProtoUtil.toProto(TS, kvEntry)))
++        assertThat(KvProtoUtil.fromTsKvProto(KvProtoUtil.toTsKvProto(TS, kvEntry)))
 +                .as("deserialized")
 +                .isEqualTo(kvEntry);
 +    }
 +
 +    @ParameterizedTest
 +    @ValueSource(booleans = {true, false})
 +    void protoListTsKvEntrySerialization(boolean withAggregation) {
 +        List<TsKvEntry> tsKvEntries = createTsKvEntryList(withAggregation);
-         assertThat(KvProtoUtil.fromProtoList(KvProtoUtil.toProtoList(tsKvEntries)))
++        assertThat(KvProtoUtil.fromTsKvProtoList(KvProtoUtil.toTsKvProtoList(tsKvEntries)))
 +                .as("deserialized")
 +                .isEqualTo(tsKvEntries);
 +    }
 +
 +    @Test
 +    void protoListAttributeKvSerialization() {
 +        List<AttributeKvEntry> protoList = attributeKvEntryData().toList();
 +        assertThat(KvProtoUtil.toAttributeKvList(KvProtoUtil.attrToTsKvProtos(protoList)))
 +                .as("deserialized")
 +                .isEqualTo(protoList);
 +    }
 +
 +}
```
