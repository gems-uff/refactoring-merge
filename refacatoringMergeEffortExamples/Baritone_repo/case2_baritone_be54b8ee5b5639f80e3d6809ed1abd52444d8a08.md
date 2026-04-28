# Case 2 — Project: baritone — Merge commit SHA1: be54b8ee5b5639f80e3d6809ed1abd52444d8a08

---

## Modified file(s):
`src/launch/java/baritone/launch/mixins/MixinBlockStateContainer.java`

---

## Class(es) modified in the merge:
`MixinBlockStateContainer` → `MixinBlockStateContainer<T>`

---

## Merge effort lines in the combined diff

```diff
-- public abstract class MixinBlockStateContainer implements IBlockStateContainer {
++ public abstract class MixinBlockStateContainer<T> implements IBlockStateContainer<T> {

-  protected IBlockStatePalette<IBlockState> palette;
-- protected IBlockStatePalette palette;
++ protected IBlockStatePalette<T> palette;

-- public IBlockStatePalette getPalette() {
++ public IBlockStatePalette<T> getPalette() {

-- public IBlockState getAtPalette(int index) {
++ public T getAtPalette(int index) {
```

---

## Relevant final code in the merge

```java
@Mixin(BlockStateContainer.class)
public abstract class MixinBlockStateContainer<T> implements IBlockStateContainer<T> {

    @Shadow
    protected BitArray storage;

    @Shadow
    protected IBlockStatePalette<T> palette;

    @Override
    public IBlockStatePalette<T> getPalette() {
        return palette;
    }

    @Override
    public BitArray getStorage() {
        return storage;
    }

    @Override
    public T getAtPalette(int index) {
        return palette.get(index);
    }
}
```

---

## Number of merge-effort lines (`++` and `--`) associated with the refactoring types under analysis:
**8 lines**

---

## What each side had

**Parent 1** had `MixinBlockStateContainer` as a non-generic class implementing the raw `IBlockStateContainer` interface. The `palette` field was typed as `IBlockStatePalette<IBlockState>` (concrete type parameter), and `getAtPalette` returned `IBlockState`.

**Parent 2** had introduced generics: the class became `MixinBlockStateContainer<T>` implementing `IBlockStateContainer<T>`. The `palette` field changed to `IBlockStatePalette<T>` (raw type in P2's version, but intended to be generic), and `getAtPalette` was updated to return `T`. Additionally, `getPalette()` return type changed to `IBlockStatePalette<T>`.

---

## Interpretation

P2 performed a **Change_Return_Type** and **Change_Parameter_Type** refactoring on `MixinBlockStateContainer` by introducing a type parameter `<T>` that propagates through:

1. **Class declaration**: raw `implements IBlockStateContainer` → generic `implements IBlockStateContainer<T>` (lines `--`/`++`)
2. **Field type**: `IBlockStatePalette` (raw) → `IBlockStatePalette<T>` (lines `--`/`++`) — **Replace_Attribute** / **Change_Parameter_Type** on the field
3. **`getPalette()` return type**: raw `IBlockStatePalette` → `IBlockStatePalette<T>` (lines `--`/`++`) — **Change_Return_Type**
4. **`getAtPalette()` return type**: `IBlockState` → `T` (lines `--`/`++`) — **Change_Return_Type**

The merge had to reconcile P1's concrete `IBlockState`-typed version with P2's generic `<T>`-parameterized version, producing `++`/`--` lines at all four declaration sites. This is a clear, defensible example of **Change_Return_Type** applied to two methods simultaneously, driven by the introduction of a type parameter in the class declaration.

## Complete diff

```diff
diff --cc src/api/java/baritone/api/Settings.java
index 8155bb3b0,da241d6ba..f85a2dc78
--- a/src/api/java/baritone/api/Settings.java
+++ b/src/api/java/baritone/api/Settings.java
@@@ -1143,7 -1176,8 +1180,8 @@@ public final class Settings 
       * via {@link Consumer#andThen(Consumer)} or it can completely be overriden via setting
       * {@link Setting#value};
       */
+     @JavaOnly
 -    public final Setting<Consumer<ITextComponent>> logger = new Setting<>(msg -> Minecraft.getMinecraft().ingameGUI.getChatGUI().printChatMessage(msg));
 +    public final Setting<Consumer<ITextComponent>> logger = new Setting<>(msg -> Minecraft.getInstance().ingameGUI.getChatGUI().printChatMessage(msg));
  
      /**
       * The function that is called when Baritone will send a desktop notification. This function can be added to
diff --cc src/api/java/baritone/api/command/datatypes/BlockById.java
index bb288c12e,0efb738ca..4e2f3dbf6
--- a/src/api/java/baritone/api/command/datatypes/BlockById.java
+++ b/src/api/java/baritone/api/command/datatypes/BlockById.java
@@@ -22,8 -22,8 +22,9 @@@ import baritone.api.command.helpers.Tab
  import net.minecraft.block.Block;
  import net.minecraft.init.Blocks;
  import net.minecraft.util.ResourceLocation;
 +import net.minecraft.util.registry.IRegistry;
  
+ import java.util.regex.Pattern;
  import java.util.stream.Stream;
  
  public enum BlockById implements IDatatypeFor<Block> {
@@@ -33,7 -38,7 +39,7 @@@
      public Block get(IDatatypeContext ctx) throws CommandException {
          ResourceLocation id = new ResourceLocation(ctx.getConsumer().getString());
          Block block;
-         if ((block = IRegistry.BLOCK.get(id)) == Blocks.AIR) {
 -        if ((block = Block.REGISTRY.getObject(id)) == Blocks.AIR) {
++        if ((block = IRegistry.BLOCK.get(id)) == null) {
              throw new IllegalArgumentException("no block found by that id");
          }
          return block;
@@@ -41,9 -46,15 +47,15 @@@
  
      @Override
      public Stream<String> tabComplete(IDatatypeContext ctx) throws CommandException {
+         String arg = ctx.getConsumer().getString();
+ 
+         if (!PATTERN.matcher(arg).matches()) {
+             return Stream.empty();
+         }
+ 
          return new TabCompleteHelper()
                  .append(
 -                        Block.REGISTRY.getKeys()
 +                        IRegistry.BLOCK.keySet()
                                  .stream()
                                  .map(Object::toString)
                  )
diff --cc src/api/java/baritone/api/command/datatypes/ForBlockOptionalMeta.java
index 978450a23,079ec03fd..3528d59c1
--- a/src/api/java/baritone/api/command/datatypes/ForBlockOptionalMeta.java
+++ b/src/api/java/baritone/api/command/datatypes/ForBlockOptionalMeta.java
@@@ -18,8 -18,15 +18,16 @@@
  package baritone.api.command.datatypes;
  
  import baritone.api.command.exception.CommandException;
+ import baritone.api.command.helpers.TabCompleteHelper;
  import baritone.api.utils.BlockOptionalMeta;
+ import net.minecraft.block.Block;
 -import net.minecraft.block.properties.IProperty;
++import net.minecraft.state.IProperty;
+ import net.minecraft.util.ResourceLocation;
++import net.minecraft.util.registry.IRegistry;
  
+ import java.util.Set;
+ import java.util.regex.Pattern;
+ import java.util.stream.Collectors;
  import java.util.stream.Stream;
  
  public enum ForBlockOptionalMeta implements IDatatypeFor<BlockOptionalMeta> {
@@@ -31,7 -46,108 +47,108 @@@
      }
  
      @Override
-     public Stream<String> tabComplete(IDatatypeContext ctx) {
-         return ctx.getConsumer().tabCompleteDatatype(BlockById.INSTANCE);
+     public Stream<String> tabComplete(IDatatypeContext ctx) throws CommandException {
+         String arg = ctx.getConsumer().peekString();
+ 
+         if (!PATTERN.matcher(arg).matches()) {
+             // Invalid format; we can't complete this.
+             ctx.getConsumer().getString();
+             return Stream.empty();
+         }
+ 
+         if (arg.endsWith("]")) {
+             // We are already done.
+             ctx.getConsumer().getString();
+             return Stream.empty();
+         }
+ 
+         if (!arg.contains("[")) {
+             // no properties so we are completing the block id
+             return ctx.getConsumer().tabCompleteDatatype(BlockById.INSTANCE);
+         }
+ 
+         ctx.getConsumer().getString();
+ 
+         // destructuring assignment? Please?
+         String blockId, properties;
+         {
+             String[] parts = splitLast(arg, '[');
+             blockId = parts[0];
+             properties = parts[1];
+         }
+ 
 -        Block block = Block.REGISTRY.getObject(new ResourceLocation(blockId));
++        Block block = IRegistry.BLOCK.get(new ResourceLocation(blockId));
+         if (block == null) {
+             // This block doesn't exist so there's no properties to complete.
+             return Stream.empty();
+         }
+ 
+         String leadingProperties, lastProperty;
+         {
+             String[] parts = splitLast(properties, ',');
+             leadingProperties = parts[0];
+             lastProperty = parts[1];
+         }
+ 
+         if (!lastProperty.contains("=")) {
+             // The last property-value pair doesn't have a value yet so we are completing its name
+             Set<String> usedProps = Stream.of(leadingProperties.split(","))
+                     .map(pair -> pair.split("=")[0])
+                     .collect(Collectors.toSet());
+ 
+             String prefix = arg.substring(0, arg.length() - lastProperty.length());
+             return new TabCompleteHelper()
+                     .append(
 -                            block.getBlockState()
++                            block.getStateContainer()
+                                     .getProperties()
+                                     .stream()
+                                     .map(IProperty::getName)
+                     )
+                     .filter(prop -> !usedProps.contains(prop))
+                     .filterPrefix(lastProperty)
+                     .sortAlphabetically()
+                     .map(prop -> prefix + prop)
+                     .stream();
+         }
+ 
+         String lastName, lastValue;
+         {
+             String[] parts = splitLast(lastProperty, '=');
+             lastName = parts[0];
+             lastValue = parts[1];
+         }
+ 
+         // We are completing the value of a property
+         String prefix = arg.substring(0, arg.length() - lastValue.length());
+ 
 -        IProperty<?> property = block.getBlockState().getProperty(lastName);
++        IProperty<?> property = block.getStateContainer().getProperty(lastName);
+         if (property == null) {
+             // The property does not exist so there's no values to complete
+             return Stream.empty();
+         }
+ 
+         return new TabCompleteHelper()
+                 .append(getValues(property))
+                 .filterPrefix(lastValue)
+                 .sortAlphabetically()
+                 .map(val -> prefix + val)
+                 .stream();
+     }
+ 
+     /**
+      * Always returns exactly two strings.
+      * If the separator is not found the FIRST returned string is empty.
+      */
+     private static String[] splitLast(String string, char chr) {
+         int idx = string.lastIndexOf(chr);
+         if (idx == -1) {
+             return new String[]{"", string};
+         }
+         return new String[]{string.substring(0, idx), string.substring(idx + 1)};
+     }
+ 
+     // this shouldn't need to be a separate method?
+     private static <T extends Comparable<T>> Stream<String> getValues(IProperty<T> property) {
+         return property.getAllowedValues().stream().map(property::getName);
      }
  }
diff --cc src/api/java/baritone/api/command/datatypes/RelativeFile.java
index 0bc3604ab,ec605c048..6eccbb302
--- a/src/api/java/baritone/api/command/datatypes/RelativeFile.java
+++ b/src/api/java/baritone/api/command/datatypes/RelativeFile.java
@@@ -30,8 -32,8 +32,6 @@@ import java.util.Locale
  import java.util.Objects;
  import java.util.stream.Stream;
  
--import static baritone.api.utils.Helper.HELPER;
--
  public enum RelativeFile implements IDatatypePost<File, File> {
      INSTANCE;
  
diff --cc src/api/java/baritone/api/process/IBuilderProcess.java
index 664055234,29d8968a7..58d257c28
--- a/src/api/java/baritone/api/process/IBuilderProcess.java
+++ b/src/api/java/baritone/api/process/IBuilderProcess.java
@@@ -51,8 -51,9 +51,9 @@@ public interface IBuilderProcess extend
       */
      boolean build(String name, File schematic, Vec3i origin);
  
+     @Deprecated
      default boolean build(String schematicFile, BlockPos origin) {
 -        File file = new File(new File(Minecraft.getMinecraft().gameDir, "schematics"), schematicFile);
 +        File file = new File(new File(Minecraft.getInstance().gameDir, "schematics"), schematicFile);
          return build(schematicFile, file, origin);
      }
  
diff --cc src/api/java/baritone/api/utils/BlockOptionalMeta.java
index 708f14872,9864d5144..621fca596
--- a/src/api/java/baritone/api/utils/BlockOptionalMeta.java
+++ b/src/api/java/baritone/api/utils/BlockOptionalMeta.java
@@@ -18,57 -18,265 +18,96 @@@
  package baritone.api.utils;
  
  import baritone.api.utils.accessor.IItemStack;
 -import com.google.common.collect.ImmutableSet;
+ import com.google.common.collect.ImmutableMap;
 -import net.minecraft.block.*;
 -import net.minecraft.block.properties.IProperty;
 +import com.google.common.collect.ImmutableSet;
 +import net.minecraft.block.Block;
  import net.minecraft.block.state.IBlockState;
  import net.minecraft.item.ItemStack;
 -import net.minecraft.util.EnumFacing;
++import net.minecraft.state.IProperty;
  import net.minecraft.util.ResourceLocation;
 +import net.minecraft.util.registry.IRegistry;
  
  import javax.annotation.Nonnull;
 -import javax.annotation.Nullable;
 -import java.util.*;
 -import java.util.function.Consumer;
 -import java.util.regex.MatchResult;
++import java.util.Collections;
 +import java.util.HashSet;
++import java.util.Map;
 +import java.util.Set;
- import java.util.regex.MatchResult;
  import java.util.regex.Matcher;
  import java.util.regex.Pattern;
+ import java.util.stream.Collectors;
  
  public final class BlockOptionalMeta {
 -    // id:meta or id[] or id[properties] where id and properties are any text with at least one character and meta is a one or two digit number
 -    private static final Pattern PATTERN = Pattern.compile("^(?<id>.+?)(?::(?<meta>\\d\\d?)|\\[(?<properties>.+?)?\\])?$");
++    // id or id[] or id[properties] where id and properties are any text with at least one character
++    private static final Pattern PATTERN = Pattern.compile("^(?<id>.+?)(?:\\[(?<properties>.+?)?\\])?$");
  
      private final Block block;
 -    private final int meta;
 -    private final boolean noMeta;
+     private final String propertiesDescription; // exists so toString() can return something more useful than a list of all blockstates
      private final Set<IBlockState> blockstates;
-     private final ImmutableSet<Integer> stateHashes;
-     private final ImmutableSet<Integer> stackHashes;
-     private static final Pattern pattern = Pattern.compile("^(.+?)(?::(\\d+))?$");
+     private final Set<Integer> stateHashes;
+     private final Set<Integer> stackHashes;
 -    private static final Map<Object, Object> normalizations;
  
 -    public BlockOptionalMeta(@Nonnull Block block, @Nullable Integer meta) {
 +    public BlockOptionalMeta(@Nonnull Block block) {
          this.block = block;
-         this.blockstates = getStates(block);
 -        this.noMeta = meta == null;
 -        this.meta = noMeta ? 0 : meta;
+         this.propertiesDescription = "{}";
 -        this.blockstates = getStates(block, meta, Collections.emptyMap());
++        this.blockstates = getStates(block, Collections.emptyMap());
          this.stateHashes = getStateHashes(blockstates);
          this.stackHashes = getStackHashes(blockstates);
      }
  
 -    public BlockOptionalMeta(@Nonnull Block block) {
 -        this(block, null);
 -    }
 -
      public BlockOptionalMeta(@Nonnull String selector) {
-         Matcher matcher = pattern.matcher(selector);
+         Matcher matcher = PATTERN.matcher(selector);
  
          if (!matcher.find()) {
              throw new IllegalArgumentException("invalid block selector");
          }
  
-         MatchResult matchResult = matcher.toMatchResult();
 -        noMeta = matcher.group("meta") == null;
--
-         ResourceLocation id = new ResourceLocation(matchResult.group(1));
+         ResourceLocation id = new ResourceLocation(matcher.group("id"));
  
 -        if (!Block.REGISTRY.containsKey(id)) {
 +        if (!IRegistry.BLOCK.containsKey(id)) {
              throw new IllegalArgumentException("Invalid block ID");
          }
 -        block = Block.REGISTRY.getObject(id);
 +        block = IRegistry.BLOCK.get(id);
-         blockstates = getStates(block);
+ 
+         String props = matcher.group("properties");
+         Map<IProperty<?>, ?> properties = props == null || props.equals("") ? Collections.emptyMap() : parseProperties(block, props);
+ 
+         propertiesDescription = props == null ? "{}" : "{" + props.replace("=", ":") + "}";
 -        meta = noMeta ? 0 : Integer.parseInt(matcher.group("meta"));
 -        blockstates = getStates(block, getMeta(), properties);
++        blockstates = getStates(block, properties);
          stateHashes = getStateHashes(blockstates);
          stackHashes = getStackHashes(blockstates);
      }
  
-     private static Set<IBlockState> getStates(@Nonnull Block block) {
-         return new HashSet<>(block.getStateContainer().getValidStates());
 -    static {
 -        Map<Object, Object> _normalizations = new HashMap<>();
 -        Consumer<Enum> put = instance -> _normalizations.put(instance.getClass(), instance);
 -        put.accept(EnumFacing.NORTH);
 -        put.accept(EnumFacing.Axis.Y);
 -        put.accept(BlockLog.EnumAxis.Y);
 -        put.accept(BlockStairs.EnumHalf.BOTTOM);
 -        put.accept(BlockStairs.EnumShape.STRAIGHT);
 -        put.accept(BlockLever.EnumOrientation.DOWN_X);
 -        put.accept(BlockDoublePlant.EnumBlockHalf.LOWER);
 -        put.accept(BlockSlab.EnumBlockHalf.BOTTOM);
 -        put.accept(BlockDoor.EnumDoorHalf.LOWER);
 -        put.accept(BlockDoor.EnumHingePosition.LEFT);
 -        put.accept(BlockBed.EnumPartType.HEAD);
 -        put.accept(BlockRailBase.EnumRailDirection.NORTH_SOUTH);
 -        put.accept(BlockTrapDoor.DoorHalf.BOTTOM);
 -        _normalizations.put(BlockBanner.ROTATION, 0);
 -        _normalizations.put(BlockBed.OCCUPIED, false);
 -        _normalizations.put(BlockBrewingStand.HAS_BOTTLE[0], false);
 -        _normalizations.put(BlockBrewingStand.HAS_BOTTLE[1], false);
 -        _normalizations.put(BlockBrewingStand.HAS_BOTTLE[2], false);
 -        _normalizations.put(BlockButton.POWERED, false);
 -        // _normalizations.put(BlockCactus.AGE, 0);
 -        // _normalizations.put(BlockCauldron.LEVEL, 0);
 -        // _normalizations.put(BlockChorusFlower.AGE, 0);
 -        _normalizations.put(BlockChorusPlant.NORTH, false);
 -        _normalizations.put(BlockChorusPlant.EAST, false);
 -        _normalizations.put(BlockChorusPlant.SOUTH, false);
 -        _normalizations.put(BlockChorusPlant.WEST, false);
 -        _normalizations.put(BlockChorusPlant.UP, false);
 -        _normalizations.put(BlockChorusPlant.DOWN, false);
 -        // _normalizations.put(BlockCocoa.AGE, 0);
 -        // _normalizations.put(BlockCrops.AGE, 0);
 -        _normalizations.put(BlockDirt.SNOWY, false);
 -        _normalizations.put(BlockDoor.OPEN, false);
 -        _normalizations.put(BlockDoor.POWERED, false);
 -        // _normalizations.put(BlockFarmland.MOISTURE, 0);
 -        _normalizations.put(BlockFence.NORTH, false);
 -        _normalizations.put(BlockFence.EAST, false);
 -        _normalizations.put(BlockFence.WEST, false);
 -        _normalizations.put(BlockFence.SOUTH, false);
 -        // _normalizations.put(BlockFenceGate.POWERED, false);
 -        // _normalizations.put(BlockFenceGate.IN_WALL, false);
 -        _normalizations.put(BlockFire.AGE, 0);
 -        _normalizations.put(BlockFire.NORTH, false);
 -        _normalizations.put(BlockFire.EAST, false);
 -        _normalizations.put(BlockFire.SOUTH, false);
 -        _normalizations.put(BlockFire.WEST, false);
 -        _normalizations.put(BlockFire.UPPER, false);
 -        // _normalizations.put(BlockFrostedIce.AGE, 0);
 -        _normalizations.put(BlockGrass.SNOWY, false);
 -        // _normalizations.put(BlockHopper.ENABLED, true);
 -        // _normalizations.put(BlockLever.POWERED, false);
 -        // _normalizations.put(BlockLiquid.LEVEL, 0);
 -        // _normalizations.put(BlockMycelium.SNOWY, false);
 -        // _normalizations.put(BlockNetherWart.AGE, false);
 -        _normalizations.put(BlockLeaves.CHECK_DECAY, false);
 -        // _normalizations.put(BlockLeaves.DECAYABLE, false);
 -        // _normalizations.put(BlockObserver.POWERED, false);
 -        _normalizations.put(BlockPane.NORTH, false);
 -        _normalizations.put(BlockPane.EAST, false);
 -        _normalizations.put(BlockPane.WEST, false);
 -        _normalizations.put(BlockPane.SOUTH, false);
 -        // _normalizations.put(BlockPistonBase.EXTENDED, false);
 -        // _normalizations.put(BlockPressurePlate.POWERED, false);
 -        // _normalizations.put(BlockPressurePlateWeighted.POWER, false);
 -        _normalizations.put(BlockQuartz.EnumType.LINES_X, BlockQuartz.EnumType.LINES_Y);
 -        _normalizations.put(BlockQuartz.EnumType.LINES_Z, BlockQuartz.EnumType.LINES_Y);
 -        // _normalizations.put(BlockRailDetector.POWERED, false);
 -        // _normalizations.put(BlockRailPowered.POWERED, false);
 -        _normalizations.put(BlockRedstoneWire.NORTH, false);
 -        _normalizations.put(BlockRedstoneWire.EAST, false);
 -        _normalizations.put(BlockRedstoneWire.SOUTH, false);
 -        _normalizations.put(BlockRedstoneWire.WEST, false);
 -        // _normalizations.put(BlockReed.AGE, false);
 -        _normalizations.put(BlockSapling.STAGE, 0);
 -        _normalizations.put(BlockSkull.NODROP, false);
 -        _normalizations.put(BlockStandingSign.ROTATION, 0);
 -        _normalizations.put(BlockStem.AGE, 0);
 -        _normalizations.put(BlockTripWire.NORTH, false);
 -        _normalizations.put(BlockTripWire.EAST, false);
 -        _normalizations.put(BlockTripWire.WEST, false);
 -        _normalizations.put(BlockTripWire.SOUTH, false);
 -        _normalizations.put(BlockVine.NORTH, false);
 -        _normalizations.put(BlockVine.EAST, false);
 -        _normalizations.put(BlockVine.SOUTH, false);
 -        _normalizations.put(BlockVine.WEST, false);
 -        _normalizations.put(BlockVine.UP, false);
 -        _normalizations.put(BlockWall.UP, false);
 -        _normalizations.put(BlockWall.NORTH, false);
 -        _normalizations.put(BlockWall.EAST, false);
 -        _normalizations.put(BlockWall.WEST, false);
 -        _normalizations.put(BlockWall.SOUTH, false);
 -        normalizations = Collections.unmodifiableMap(_normalizations);
 -    }
 -
 -    public static <C extends Comparable<C>, P extends IProperty<C>> P castToIProperty(Object value) {
++    private static <C extends Comparable<C>, P extends IProperty<C>> P castToIProperty(Object value) {
+         //noinspection unchecked
+         return (P) value;
+     }
+ 
 -    public static <C extends Comparable<C>, P extends IProperty<C>> C castToIPropertyValue(P iproperty, Object value) {
 -        //noinspection unchecked
 -        return (C) value;
 -    }
 -
 -    /**
 -     * Normalizes the specified blockstate by setting meta-affecting properties which
 -     * are not being targeted by the meta parameter to their default values.
 -     * <p>
 -     * For example, block variant/color is the primary target for the meta value, so properties
 -     * such as rotation/facing direction will be set to default values in order to nullify
 -     * the effect that they have on the state's meta value.
 -     *
 -     * @param state The state to normalize
 -     * @return The normalized block state
 -     */
 -    public static IBlockState normalize(IBlockState state) {
 -        IBlockState newState = state;
 -
 -        for (IProperty<?> property : state.getProperties().keySet()) {
 -            Class<?> valueClass = property.getValueClass();
 -            if (normalizations.containsKey(property)) {
 -                try {
 -                    newState = newState.withProperty(
 -                            castToIProperty(property),
 -                            castToIPropertyValue(property, normalizations.get(property))
 -                    );
 -                } catch (IllegalArgumentException ignored) {}
 -            } else if (normalizations.containsKey(state.getValue(property))) {
 -                try {
 -                    newState = newState.withProperty(
 -                            castToIProperty(property),
 -                            castToIPropertyValue(property, normalizations.get(state.getValue(property)))
 -                    );
 -                } catch (IllegalArgumentException ignored) {}
 -            } else if (normalizations.containsKey(valueClass)) {
 -                try {
 -                    newState = newState.withProperty(
 -                            castToIProperty(property),
 -                            castToIPropertyValue(property, normalizations.get(valueClass))
 -                    );
 -                } catch (IllegalArgumentException ignored) {}
 -            }
 -        }
 -
 -        return newState;
 -    }
 -
 -    /**
 -     * Evaluate the target meta value for the specified state. The target meta value is
 -     * most often that which is influenced by the variant/color property of the block state.
 -     *
 -     * @param state The state to check
 -     * @return The target meta of the state
 -     * @see #normalize(IBlockState)
 -     */
 -    public static int stateMeta(IBlockState state) {
 -        return state.getBlock().getMetaFromState(normalize(state));
 -    }
 -
+     private static Map<IProperty<?>, ?> parseProperties(Block block, String raw) {
+         ImmutableMap.Builder<IProperty<?>, Object> builder = ImmutableMap.builder();
+         for (String pair : raw.split(",")) {
+             String[] parts = pair.split("=");
+             if (parts.length != 2) {
+                 throw new IllegalArgumentException(String.format("\"%s\" is not a valid property-value pair", pair));
+             }
+             String rawKey = parts[0];
+             String rawValue = parts[1];
 -            IProperty<?> key = block.getBlockState().getProperty(rawKey);
++            IProperty<?> key = block.getStateContainer().getProperty(rawKey);
+             Comparable<?> value = castToIProperty(key).parseValue(rawValue)
 -                    .toJavaUtil().orElseThrow(() -> new IllegalArgumentException(String.format(
++                    .orElseThrow(() -> new IllegalArgumentException(String.format(
+                             "\"%s\" is not a valid value for %s on %s",
+                             rawValue, key, block
+                     )));
+             builder.put(key, value);
+         }
+         return builder.build();
+     }
+ 
 -    private static Set<IBlockState> getStates(@Nonnull Block block, @Nullable Integer meta, @Nonnull Map<IProperty<?>, ?> properties) {
 -        return block.getBlockState().getValidStates().stream()
 -                .filter(blockstate -> meta == null || stateMeta(blockstate) == meta)
++    private static Set<IBlockState> getStates(@Nonnull Block block, @Nonnull Map<IProperty<?>, ?> properties) {
++        return block.getStateContainer().getValidStates().stream()
+                 .filter(blockstate -> properties.entrySet().stream().allMatch(entry ->
 -                        blockstate.getValue(entry.getKey()) == entry.getValue()
++                        blockstate.get(entry.getKey()) == entry.getValue()
+                 ))
+                 .collect(Collectors.toSet());
      }
  
      private static ImmutableSet<Integer> getStateHashes(Set<IBlockState> blockstates) {
@@@ -116,7 -331,16 +155,7 @@@
  
      @Override
      public String toString() {
-         return String.format("BlockOptionalMeta{block=%s}", block);
 -        if (noMeta) {
 -            return String.format("BlockOptionalMeta{block=%s,properties=%s}", block, propertiesDescription);
 -        } else {
 -            return String.format("BlockOptionalMeta{block=%s,meta=%s}", block, getMeta());
 -        }
 -    }
 -
 -    public static IBlockState blockStateFromStack(ItemStack stack) {
 -        //noinspection deprecation
 -        return Block.getBlockFromItem(stack.getItem()).getStateFromMeta(stack.getMetadata());
++        return String.format("BlockOptionalMeta{block=%s,properties=%s}", block, propertiesDescription);
      }
  
      public IBlockState getAnyBlockState() {
diff --cc src/api/java/baritone/api/utils/BlockOptionalMetaLookup.java
index 041c6162c,6479854bc..de39b91cf
--- a/src/api/java/baritone/api/utils/BlockOptionalMetaLookup.java
+++ b/src/api/java/baritone/api/utils/BlockOptionalMetaLookup.java
@@@ -72,13 -78,9 +78,9 @@@ public class BlockOptionalMetaLookup 
      }
  
      public boolean has(ItemStack stack) {
-         for (BlockOptionalMeta bom : boms) {
-             if (bom.matches(stack)) {
-                 return true;
-             }
-         }
- 
-         return false;
+         int hash = ((IItemStack) (Object) stack).getBaritoneHash();
 -        return stackHashes.contains(hash)
 -                || stackHashes.contains(hash - stack.getItemDamage());
++        hash -= stack.getDamage();
++        return stackHashes.contains(hash);
      }
  
      public List<BlockOptionalMeta> blocks() {
diff --cc src/api/java/baritone/api/utils/Helper.java
index c975d6f28,b99074ae0..f39abd641
--- a/src/api/java/baritone/api/utils/Helper.java
+++ b/src/api/java/baritone/api/utils/Helper.java
@@@ -42,9 -42,11 +42,11 @@@ public interface Helper 
      Helper HELPER = new Helper() {};
  
      /**
-      * Instance of the game
 -     * The main game instance returned by {@link Minecraft#getMinecraft()}.
++     * The main game instance returned by {@link Minecraft#getInstance()}.
+      * Deprecated since {@link IPlayerContext#minecraft()} should be used instead (In the majority of cases).
       */
+     @Deprecated
 -    Minecraft mc = Minecraft.getMinecraft();
 +    Minecraft mc = Minecraft.getInstance();
  
      static ITextComponent getPrefix() {
          // Inner text component
@@@ -70,7 -72,7 +72,7 @@@
       * @param message The message to display in the popup
       */
      default void logToast(ITextComponent title, ITextComponent message) {
-         mc.addScheduledTask(() -> BaritoneAPI.getSettings().toaster.value.accept(title, message));
 -        Minecraft.getMinecraft().addScheduledTask(() -> BaritoneAPI.getSettings().toaster.value.accept(title, message));
++        Minecraft.getInstance().addScheduledTask(() -> BaritoneAPI.getSettings().toaster.value.accept(title, message));
      }
  
      /**
@@@ -131,7 -133,7 +133,7 @@@
       * @param error   Whether to log as an error
       */
      default void logNotificationDirect(String message, boolean error) {
-         mc.addScheduledTask(() -> BaritoneAPI.getSettings().notifier.value.accept(message, error));
 -        Minecraft.getMinecraft().addScheduledTask(() -> BaritoneAPI.getSettings().notifier.value.accept(message, error));
++        Minecraft.getInstance().addScheduledTask(() -> BaritoneAPI.getSettings().notifier.value.accept(message, error));
      }
  
      /**
@@@ -168,7 -170,7 +170,7 @@@
          if (logAsToast) {
              logToast(getPrefix(), component);
          } else {
-             mc.addScheduledTask(() -> BaritoneAPI.getSettings().logger.value.accept(component));
 -            Minecraft.getMinecraft().addScheduledTask(() -> BaritoneAPI.getSettings().logger.value.accept(component));
++            Minecraft.getInstance().addScheduledTask(() -> BaritoneAPI.getSettings().logger.value.accept(component));
          }
      }
  
diff --cc src/api/java/baritone/api/utils/RotationUtils.java
index b0c12ec19,9fc65df9f..c9b6bf295
--- a/src/api/java/baritone/api/utils/RotationUtils.java
+++ b/src/api/java/baritone/api/utils/RotationUtils.java
@@@ -179,11 -172,11 +178,11 @@@ public final class RotationUtils 
               *
               * or if you're a normal person literally all this does it ensure that we don't nudge the pitch to a normal level
               */
-             Rotation hypothetical = new Rotation(entity.rotationYaw, entity.rotationPitch + 0.0001F);
+             Rotation hypothetical = ctx.playerRotations().add(new Rotation(0, 0.0001F));
              if (wouldSneak) {
                  // the concern here is: what if we're looking at it now, but as soon as we start sneaking we no longer are
-                 RayTraceResult result = RayTraceUtils.rayTraceTowards(entity, hypothetical, blockReachDistance, true);
+                 RayTraceResult result = RayTraceUtils.rayTraceTowards(ctx.player(), hypothetical, blockReachDistance, true);
 -                if (result != null && result.typeOfHit == RayTraceResult.Type.BLOCK && result.getBlockPos().equals(pos)) {
 +                if (result != null && result.type == RayTraceResult.Type.BLOCK && result.getBlockPos().equals(pos)) {
                      return Optional.of(hypothetical); // yes, if we sneaked we would still be looking at the block
                  }
              } else {
@@@ -196,16 -189,13 +195,16 @@@
              return possibleRotation;
          }
  
-         IBlockState state = entity.world.getBlockState(pos);
-         VoxelShape shape = state.getShape(entity.world, pos);
+         IBlockState state = ctx.world().getBlockState(pos);
 -        AxisAlignedBB aabb = state.getBoundingBox(ctx.world(), pos);
++        VoxelShape shape = state.getShape(ctx.world(), pos);
 +        if (shape.isEmpty()) {
 +            shape = VoxelShapes.fullCube();
 +        }
          for (Vec3d sideOffset : BLOCK_SIDE_MULTIPLIERS) {
 -            double xDiff = aabb.minX * sideOffset.x + aabb.maxX * (1 - sideOffset.x);
 -            double yDiff = aabb.minY * sideOffset.y + aabb.maxY * (1 - sideOffset.y);
 -            double zDiff = aabb.minZ * sideOffset.z + aabb.maxZ * (1 - sideOffset.z);
 +            double xDiff = shape.getStart(EnumFacing.Axis.X) * sideOffset.x + shape.getEnd(EnumFacing.Axis.X) * (1 - sideOffset.x);
 +            double yDiff = shape.getStart(EnumFacing.Axis.Y) * sideOffset.y + shape.getEnd(EnumFacing.Axis.Y) * (1 - sideOffset.y);
 +            double zDiff = shape.getStart(EnumFacing.Axis.Z) * sideOffset.z + shape.getEnd(EnumFacing.Axis.Z) * (1 - sideOffset.z);
-             possibleRotation = reachableOffset(entity, pos, new Vec3d(pos).add(xDiff, yDiff, zDiff), blockReachDistance, wouldSneak);
+             possibleRotation = reachableOffset(ctx, pos, new Vec3d(pos).add(xDiff, yDiff, zDiff), blockReachDistance, wouldSneak);
              if (possibleRotation.isPresent()) {
                  return possibleRotation;
              }
@@@ -224,12 -214,13 +223,13 @@@
       * @param blockReachDistance The block reach distance of the entity
       * @return The optional rotation
       */
-     public static Optional<Rotation> reachableOffset(Entity entity, BlockPos pos, Vec3d offsetPos, double blockReachDistance, boolean wouldSneak) {
-         Vec3d eyes = wouldSneak ? RayTraceUtils.inferSneakingEyePosition(entity) : entity.getEyePosition(1.0F);
-         Rotation rotation = calcRotationFromVec3d(eyes, offsetPos, new Rotation(entity.rotationYaw, entity.rotationPitch));
-         RayTraceResult result = RayTraceUtils.rayTraceTowards(entity, rotation, blockReachDistance, wouldSneak);
+     public static Optional<Rotation> reachableOffset(IPlayerContext ctx, BlockPos pos, Vec3d offsetPos, double blockReachDistance, boolean wouldSneak) {
 -        Vec3d eyes = wouldSneak ? RayTraceUtils.inferSneakingEyePosition(ctx.player()) : ctx.player().getPositionEyes(1.0F);
++        Vec3d eyes = wouldSneak ? RayTraceUtils.inferSneakingEyePosition(ctx.player()) : ctx.player().getEyePosition(1.0F);
+         Rotation rotation = calcRotationFromVec3d(eyes, offsetPos, ctx.playerRotations());
+         Rotation actualRotation = BaritoneAPI.getProvider().getBaritoneForPlayer(ctx.player()).getLookBehavior().getAimProcessor().peekRotation(rotation);
+         RayTraceResult result = RayTraceUtils.rayTraceTowards(ctx.player(), actualRotation, blockReachDistance, wouldSneak);
          //System.out.println(result);
 -        if (result != null && result.typeOfHit == RayTraceResult.Type.BLOCK) {
 +        if (result != null && result.type == RayTraceResult.Type.BLOCK) {
              if (result.getBlockPos().equals(pos)) {
                  return Optional.of(rotation);
              }
@@@ -249,6 -240,40 +249,40 @@@
       * @param blockReachDistance The block reach distance of the entity
       * @return The optional rotation
       */
+     public static Optional<Rotation> reachableCenter(IPlayerContext ctx, BlockPos pos, double blockReachDistance, boolean wouldSneak) {
+         return reachableOffset(ctx, pos, VecUtils.calculateBlockCenter(ctx.world(), pos), blockReachDistance, wouldSneak);
+     }
+ 
+     @Deprecated
+     public static Optional<Rotation> reachable(EntityPlayerSP entity, BlockPos pos, double blockReachDistance) {
+         return reachable(entity, pos, blockReachDistance, false);
+     }
+ 
+     @Deprecated
+     public static Optional<Rotation> reachable(EntityPlayerSP entity, BlockPos pos, double blockReachDistance, boolean wouldSneak) {
+         IBaritone baritone = BaritoneAPI.getProvider().getBaritoneForPlayer(entity);
+         IPlayerContext ctx = baritone.getPlayerContext();
+         return reachable(ctx, pos, blockReachDistance, wouldSneak);
+     }
+ 
+     @Deprecated
+     public static Optional<Rotation> reachableOffset(Entity entity, BlockPos pos, Vec3d offsetPos, double blockReachDistance, boolean wouldSneak) {
 -        Vec3d eyes = wouldSneak ? RayTraceUtils.inferSneakingEyePosition(entity) : entity.getPositionEyes(1.0F);
++        Vec3d eyes = wouldSneak ? RayTraceUtils.inferSneakingEyePosition(entity) : entity.getEyePosition(1.0F);
+         Rotation rotation = calcRotationFromVec3d(eyes, offsetPos, new Rotation(entity.rotationYaw, entity.rotationPitch));
+         RayTraceResult result = RayTraceUtils.rayTraceTowards(entity, rotation, blockReachDistance, wouldSneak);
+         //System.out.println(result);
 -        if (result != null && result.typeOfHit == RayTraceResult.Type.BLOCK) {
++        if (result != null && result.type == RayTraceResult.Type.BLOCK) {
+             if (result.getBlockPos().equals(pos)) {
+                 return Optional.of(rotation);
+             }
+             if (entity.world.getBlockState(pos).getBlock() instanceof BlockFire && result.getBlockPos().equals(pos.down())) {
+                 return Optional.of(rotation);
+             }
+         }
+         return Optional.empty();
+     }
+ 
+     @Deprecated
      public static Optional<Rotation> reachableCenter(Entity entity, BlockPos pos, double blockReachDistance, boolean wouldSneak) {
          return reachableOffset(entity, pos, VecUtils.calculateBlockCenter(entity.world, pos), blockReachDistance, wouldSneak);
      }
diff --cc src/api/java/baritone/api/utils/SettingsUtil.java
index e72fb465b,efc080cf5..811a6e21c
--- a/src/api/java/baritone/api/utils/SettingsUtil.java
+++ b/src/api/java/baritone/api/utils/SettingsUtil.java
@@@ -107,6 -104,10 +106,10 @@@ public class SettingsUtil 
          }
      }
  
+     private static Path settingsByName(String name) {
 -        return Minecraft.getMinecraft().gameDir.toPath().resolve("baritone").resolve(name);
++        return Minecraft.getInstance().gameDir.toPath().resolve("baritone").resolve(name);
+     }
+ 
      public static List<Settings.Setting> modifiedSettings(Settings settings) {
          List<Settings.Setting> modified = new ArrayList<>();
          for (Settings.Setting setting : settings.allSettings) {
diff --cc src/api/java/baritone/api/utils/gui/BaritoneToast.java
index 3c68ee5a9,9e9a6403c..69d806214
--- a/src/api/java/baritone/api/utils/gui/BaritoneToast.java
+++ b/src/api/java/baritone/api/utils/gui/BaritoneToast.java
@@@ -73,6 -74,6 +74,6 @@@ public class BaritoneToast implements I
      }
  
      public static void addOrUpdate(ITextComponent title, ITextComponent subtitle) {
-         addOrUpdate(net.minecraft.client.Minecraft.getInstance().getToastGui(), title, subtitle, baritone.api.BaritoneAPI.getSettings().toastTimer.value);
 -        addOrUpdate(Minecraft.getMinecraft().getToastGui(), title, subtitle, baritone.api.BaritoneAPI.getSettings().toastTimer.value);
++        addOrUpdate(Minecraft.getInstance().getToastGui(), title, subtitle, baritone.api.BaritoneAPI.getSettings().toastTimer.value);
      }
  }
diff --cc src/launch/java/baritone/launch/mixins/MixinBitArray.java
index bece3e3bf,bf7d9e535..166dc51c9
--- a/src/launch/java/baritone/launch/mixins/MixinBitArray.java
+++ b/src/launch/java/baritone/launch/mixins/MixinBitArray.java
@@@ -64,4 -64,14 +64,9 @@@ public abstract class MixinBitArray imp
  
          return out;
      }
+ 
+     @Override
+     public long getMaxEntryValue() {
+         return maxEntryValue;
+     }
 -
 -    @Override
 -    public int getBitsPerEntry() {
 -        return bitsPerEntry;
 -    }
  }
diff --cc src/launch/java/baritone/launch/mixins/MixinBlockStateContainer.java
index fdaf3ea87,566c3cf8b..8f96e3ad4
--- a/src/launch/java/baritone/launch/mixins/MixinBlockStateContainer.java
+++ b/src/launch/java/baritone/launch/mixins/MixinBlockStateContainer.java
@@@ -19,7 -19,7 +19,6 @@@ package baritone.launch.mixins
  
  import baritone.utils.accessor.IBitArray;
  import baritone.utils.accessor.IBlockStateContainer;
--import net.minecraft.block.state.IBlockState;
  import net.minecraft.util.BitArray;
  import net.minecraft.world.chunk.BlockStateContainer;
  import net.minecraft.world.chunk.IBlockStatePalette;
@@@ -27,17 -27,27 +26,27 @@@ import org.spongepowered.asm.mixin.Mixi
  import org.spongepowered.asm.mixin.Shadow;
  
  @Mixin(BlockStateContainer.class)
--public abstract class MixinBlockStateContainer implements IBlockStateContainer {
++public abstract class MixinBlockStateContainer<T> implements IBlockStateContainer<T> {
  
      @Shadow
      protected BitArray storage;
  
      @Shadow
-     protected IBlockStatePalette<IBlockState> palette;
 -    protected IBlockStatePalette palette;
++    protected IBlockStatePalette<T> palette;
  
      @Override
-     public IBlockState getAtPalette(int index) {
 -    public IBlockStatePalette getPalette() {
++    public IBlockStatePalette<T> getPalette() {
+         return palette;
+     }
+ 
+     @Override
+     public BitArray getStorage() {
+         return storage;
+     }
+ 
+     @Override
 -    public IBlockState getAtPalette(int index) {
 -        return palette.getBlockState(index);
++    public T getAtPalette(int index) {
 +        return palette.get(index);
      }
  
      @Override
diff --cc src/launch/java/baritone/launch/mixins/MixinEntityLivingBase.java
index c3d3cb1fb,f8544dd2f..10ba31c83
--- a/src/launch/java/baritone/launch/mixins/MixinEntityLivingBase.java
+++ b/src/launch/java/baritone/launch/mixins/MixinEntityLivingBase.java
@@@ -23,9 -23,9 +23,10 @@@ import baritone.api.event.events.Rotati
  import net.minecraft.client.entity.EntityPlayerSP;
  import net.minecraft.entity.Entity;
  import net.minecraft.entity.EntityLivingBase;
 +import net.minecraft.entity.EntityType;
  import net.minecraft.world.World;
  import org.spongepowered.asm.mixin.Mixin;
+ import org.spongepowered.asm.mixin.Unique;
  import org.spongepowered.asm.mixin.injection.At;
  import org.spongepowered.asm.mixin.injection.Inject;
  import org.spongepowered.asm.mixin.injection.Redirect;
@@@ -43,10 -45,14 +46,14 @@@ public abstract class MixinEntityLiving
      /**
       * Event called to override the movement direction when jumping
       */
+     @Unique
      private RotationMoveEvent jumpRotationEvent;
  
+     @Unique
+     private RotationMoveEvent elytraRotationEvent;
+ 
 -    public MixinEntityLivingBase(World worldIn) {
 -        super(worldIn);
 +    public MixinEntityLivingBase(EntityType<?> entityTypeIn, World worldIn) {
 +        super(entityTypeIn, worldIn);
      }
  
      @Inject(
diff --cc src/launch/java/baritone/launch/mixins/MixinEntityPlayerSP.java
index 16ca15b07,281ff96f5..041fdb688
--- a/src/launch/java/baritone/launch/mixins/MixinEntityPlayerSP.java
+++ b/src/launch/java/baritone/launch/mixins/MixinEntityPlayerSP.java
@@@ -58,12 -58,11 +58,11 @@@ public class MixinEntityPlayerSP 
      }
  
      @Inject(
 -            method = "onUpdate",
 +            method = "tick",
              at = @At(
                      value = "INVOKE",
-                     target = "net/minecraft/client/entity/EntityPlayerSP.isPassenger()Z",
-                     shift = At.Shift.BY,
-                     by = -3
 -                    target = "net/minecraft/client/entity/AbstractClientPlayer.onUpdate()V",
++                    target = "net/minecraft/client/entity/AbstractClientPlayer.tick()V",
+                     shift = At.Shift.AFTER
              )
      )
      private void onPreUpdate(CallbackInfo ci) {
@@@ -73,24 -72,8 +72,8 @@@
          }
      }
  
-     @Inject(
-             method = "tick",
-             at = @At(
-                     value = "INVOKE",
-                     target = "net/minecraft/client/entity/EntityPlayerSP.onUpdateWalkingPlayer()V",
-                     shift = At.Shift.BY,
-                     by = 2
-             )
-     )
-     private void onPostUpdate(CallbackInfo ci) {
-         IBaritone baritone = BaritoneAPI.getProvider().getBaritoneForPlayer((EntityPlayerSP) (Object) this);
-         if (baritone != null) {
-             baritone.getGameEventHandler().onPlayerUpdate(new PlayerUpdateEvent(EventState.POST));
-         }
-     }
- 
      @Redirect(
 -            method = "onLivingUpdate",
 +            method = "livingTick",
              at = @At(
                      value = "FIELD",
                      target = "net/minecraft/entity/player/PlayerCapabilities.allowFlying:Z"
diff --cc src/launch/java/baritone/launch/mixins/MixinMinecraft.java
index 8b2ab7e3f,edc1e3fcc..a3bc75bb1
--- a/src/launch/java/baritone/launch/mixins/MixinMinecraft.java
+++ b/src/launch/java/baritone/launch/mixins/MixinMinecraft.java
@@@ -84,7 -85,21 +85,21 @@@ public class MixinMinecraft 
  
              baritone.getGameEventHandler().onTick(tickProvider.apply(EventState.PRE, type));
          }
+     }
  
+     @Inject(
+             method = "runTick",
+             at = @At(
+                     value = "INVOKE",
 -                    target = "net/minecraft/client/multiplayer/WorldClient.updateEntities()V",
++                    target = "net/minecraft/client/multiplayer/WorldClient.tickEntities()V",
+                     shift = At.Shift.AFTER
+             )
+     )
+     private void postUpdateEntities(CallbackInfo ci) {
+         IBaritone baritone = BaritoneAPI.getProvider().getBaritoneForPlayer(this.player);
+         if (baritone != null) {
+             baritone.getGameEventHandler().onPlayerUpdate(new PlayerUpdateEvent(EventState.POST));
+         }
      }
  
      @Inject(
diff --cc src/main/java/baritone/BaritoneProvider.java
index d5457cf85,b96cf03f7..f34d9bcb9
--- a/src/main/java/baritone/BaritoneProvider.java
+++ b/src/main/java/baritone/BaritoneProvider.java
@@@ -36,15 -38,16 +38,16 @@@ import java.util.concurrent.CopyOnWrite
   */
  public final class BaritoneProvider implements IBaritoneProvider {
  
-     private final Baritone primary;
      private final List<IBaritone> all;
+     private final List<IBaritone> allView;
  
-     {
-         this.primary = new Baritone();
-         this.all = Collections.singletonList(this.primary);
+     public BaritoneProvider() {
+         this.all = new CopyOnWriteArrayList<>();
+         this.allView = Collections.unmodifiableList(this.all);
  
          // Setup chat control, just for the primary instance
-         new ExampleBaritoneControl(this.primary);
 -        final Baritone primary = (Baritone) this.createBaritone(Minecraft.getMinecraft());
++        final Baritone primary = (Baritone) this.createBaritone(Minecraft.getInstance());
+         primary.registerBehavior(ExampleBaritoneControl::new);
      }
  
      @Override
diff --cc src/main/java/baritone/behavior/LookBehavior.java
index 801a5e43e,372cf1aae..7a669fa3f
--- a/src/main/java/baritone/behavior/LookBehavior.java
+++ b/src/main/java/baritone/behavior/LookBehavior.java
@@@ -110,14 -145,132 +145,142 @@@ public final class LookBehavior extend
      @Override
      public void onPlayerRotationMove(RotationMoveEvent event) {
          if (this.target != null) {
+             final Rotation actual = this.processor.peekRotation(this.target.rotation);
+             event.setYaw(actual.getYaw());
+             event.setPitch(actual.getPitch());
+         }
+     }
  
-             event.setYaw(this.target.getYaw());
+     private static final class AimProcessor extends AbstractAimProcessor {
  
-             // If we have antiCheatCompatibility on, we're going to use the target value later in onPlayerUpdate()
-             // Also the type has to be MOTION_UPDATE because that is called after JUMP
-             if (!Baritone.settings().antiCheatCompatibility.value && event.getType() == RotationMoveEvent.Type.MOTION_UPDATE && !this.force) {
-                 this.target = null;
+         public AimProcessor(final IPlayerContext ctx) {
+             super(ctx);
+         }
+ 
+         @Override
+         protected Rotation getPrevRotation() {
+             // Implementation will use LookBehavior.serverRotation
+             return ctx.playerRotations();
+         }
+     }
+ 
+     private static abstract class AbstractAimProcessor implements ITickableAimProcessor {
+ 
+         protected final IPlayerContext ctx;
+         private final ForkableRandom rand;
+         private double randomYawOffset;
+         private double randomPitchOffset;
+ 
+         public AbstractAimProcessor(IPlayerContext ctx) {
+             this.ctx = ctx;
+             this.rand = new ForkableRandom();
+         }
+ 
+         private AbstractAimProcessor(final AbstractAimProcessor source) {
+             this.ctx = source.ctx;
+             this.rand = source.rand.fork();
+             this.randomYawOffset = source.randomYawOffset;
+             this.randomPitchOffset = source.randomPitchOffset;
+         }
+ 
+         @Override
+         public final Rotation peekRotation(final Rotation rotation) {
+             final Rotation prev = this.getPrevRotation();
+ 
+             float desiredYaw = rotation.getYaw();
+             float desiredPitch = rotation.getPitch();
+ 
+             // In other words, the target doesn't care about the pitch, so it used playerRotations().getPitch()
+             // and it's safe to adjust it to a normal level
+             if (desiredPitch == prev.getPitch()) {
+                 desiredPitch = nudgeToLevel(desiredPitch);
              }
+ 
+             desiredYaw += this.randomYawOffset;
+             desiredPitch += this.randomPitchOffset;
+ 
+             return new Rotation(
+                     this.calculateMouseMove(prev.getYaw(), desiredYaw),
+                     this.calculateMouseMove(prev.getPitch(), desiredPitch)
+             ).clamp();
+         }
+ 
+         @Override
+         public final void tick() {
++            // randomLooking
+             this.randomYawOffset = (this.rand.nextDouble() - 0.5) * Baritone.settings().randomLooking.value;
+             this.randomPitchOffset = (this.rand.nextDouble() - 0.5) * Baritone.settings().randomLooking.value;
++
++            // randomLooking113
++            double random = this.rand.nextDouble() - 0.5;
++            if (Math.abs(random) < 0.1) {
++                random *= 4;
++            }
++            this.randomYawOffset += random * Baritone.settings().randomLooking113.value;
+         }
+ 
+         @Override
+         public final void advance(int ticks) {
+             for (int i = 0; i < ticks; i++) {
+                 this.tick();
+             }
+         }
+ 
+         @Override
+         public Rotation nextRotation(final Rotation rotation) {
+             final Rotation actual = this.peekRotation(rotation);
+             this.tick();
+             return actual;
+         }
+ 
+         @Override
+         public final ITickableAimProcessor fork() {
+             return new AbstractAimProcessor(this) {
+ 
+                 private Rotation prev = AbstractAimProcessor.this.getPrevRotation();
+ 
+                 @Override
+                 public Rotation nextRotation(final Rotation rotation) {
+                     return (this.prev = super.nextRotation(rotation));
+                 }
+ 
+                 @Override
+                 protected Rotation getPrevRotation() {
+                     return this.prev;
+                 }
+             };
+         }
+ 
+         protected abstract Rotation getPrevRotation();
+ 
+         /**
+          * Nudges the player's pitch to a regular level. (Between {@code -20} and {@code 10}, increments are by {@code 1})
+          */
+         private float nudgeToLevel(float pitch) {
+             if (pitch < -20) {
+                 return pitch + 1;
+             } else if (pitch > 10) {
+                 return pitch - 1;
+             }
+             return pitch;
+         }
+ 
++        // The game uses rotation = (float) ((double) rotation + delta) so we'll do that as well
+         private float calculateMouseMove(float current, float target) {
 -            final float delta = target - current;
 -            final int deltaPx = angleToMouse(delta);
 -            return current + mouseToAngle(deltaPx);
++            final double delta = target - current;
++            final double deltaPx = angleToMouse(delta); // yes, even the mouse movements use double
++            return (float) ((double) current + mouseToAngle(deltaPx));
+         }
+ 
 -        private int angleToMouse(float angleDelta) {
 -            final float minAngleChange = mouseToAngle(1);
++        private double angleToMouse(double angleDelta) {
++            final double minAngleChange = mouseToAngle(1);
+             return Math.round(angleDelta / minAngleChange);
+         }
+ 
 -        private float mouseToAngle(int mouseDelta) {
 -            final float f = ctx.minecraft().gameSettings.mouseSensitivity * 0.6f + 0.2f;
 -            return mouseDelta * f * f * f * 8.0f * 0.15f;
++        private double mouseToAngle(double mouseDelta) {
++            // casting float literals to double gets us the precise values used by mc
++            final double f = ctx.minecraft().gameSettings.mouseSensitivity * (double) 0.6f + (double) 0.2f;
++            return mouseDelta * f * f * f * 8.0d * 0.15d;
          }
      }
  
diff --cc src/main/java/baritone/cache/FasterWorldScanner.java
index 000000000,fbdc238ce..ea0698360
mode 000000,100644..100644
--- a/src/main/java/baritone/cache/FasterWorldScanner.java
+++ b/src/main/java/baritone/cache/FasterWorldScanner.java
@@@ -1,0 -1,276 +1,271 @@@
+ /*
+  * This file is part of Baritone.
+  *
+  * Baritone is free software: you can redistribute it and/or modify
+  * it under the terms of the GNU Lesser General Public License as published by
+  * the Free Software Foundation, either version 3 of the License, or
+  * (at your option) any later version.
+  *
+  * Baritone is distributed in the hope that it will be useful,
+  * but WITHOUT ANY WARRANTY; without even the implied warranty of
+  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
+  * GNU Lesser General Public License for more details.
+  *
+  * You should have received a copy of the GNU Lesser General Public License
+  * along with Baritone.  If not, see <https://www.gnu.org/licenses/>.
+  */
+ 
+ package baritone.cache;
+ 
+ import baritone.api.cache.ICachedWorld;
+ import baritone.api.cache.IWorldScanner;
+ import baritone.api.utils.BetterBlockPos;
+ import baritone.api.utils.BlockOptionalMetaLookup;
+ import baritone.api.utils.IPlayerContext;
+ import baritone.utils.accessor.IBitArray;
+ import baritone.utils.accessor.IBlockStateContainer;
+ import io.netty.buffer.Unpooled;
 -import it.unimi.dsi.fastutil.ints.IntArrayList;
 -import it.unimi.dsi.fastutil.ints.IntList;
+ import net.minecraft.block.Block;
+ import net.minecraft.block.state.IBlockState;
+ import net.minecraft.network.PacketBuffer;
+ import net.minecraft.util.BitArray;
+ import net.minecraft.util.ObjectIntIdentityMap;
+ import net.minecraft.util.math.BlockPos;
+ import net.minecraft.util.math.ChunkPos;
+ import net.minecraft.world.chunk.*;
 -import net.minecraft.world.chunk.storage.ExtendedBlockStorage;
+ 
+ import java.util.ArrayList;
+ import java.util.List;
 -import java.util.function.BiConsumer;
 -import java.util.function.IntConsumer;
+ import java.util.stream.Collectors;
+ import java.util.stream.Stream;
+ 
+ public enum FasterWorldScanner implements IWorldScanner {
+     INSTANCE;
+     @Override
+     public List<BlockPos> scanChunkRadius(IPlayerContext ctx, BlockOptionalMetaLookup filter, int max, int yLevelThreshold, int maxSearchRadius) {
+         assert ctx.world() != null;
+         if (maxSearchRadius < 0) {
+             throw new IllegalArgumentException("chunkRange must be >= 0");
+         }
+         return scanChunksInternal(ctx, filter, getChunkRange(ctx.playerFeet().x >> 4, ctx.playerFeet().z >> 4, maxSearchRadius), max);
+     }
+ 
+     @Override
+     public List<BlockPos> scanChunk(IPlayerContext ctx, BlockOptionalMetaLookup filter, ChunkPos pos, int max, int yLevelThreshold) {
+         Stream<BlockPos> stream = scanChunkInternal(ctx, filter, pos);
+         if (max >= 0) {
+             stream = stream.limit(max);
+         }
+         return stream.collect(Collectors.toList());
+     }
+ 
+     @Override
+     public int repack(IPlayerContext ctx) {
+         return this.repack(ctx, 40);
+     }
+ 
+     @Override
+     public int repack(IPlayerContext ctx, int range) {
+         IChunkProvider chunkProvider = ctx.world().getChunkProvider();
+         ICachedWorld cachedWorld = ctx.worldData().getCachedWorld();
+ 
+         BetterBlockPos playerPos = ctx.playerFeet();
+ 
+         int playerChunkX = playerPos.getX() >> 4;
+         int playerChunkZ = playerPos.getZ() >> 4;
+ 
+         int minX = playerChunkX - range;
+         int minZ = playerChunkZ - range;
+         int maxX = playerChunkX + range;
+         int maxZ = playerChunkZ + range;
+ 
+         int queued = 0;
+         for (int x = minX; x <= maxX; x++) {
+             for (int z = minZ; z <= maxZ; z++) {
 -                Chunk chunk = chunkProvider.getLoadedChunk(x, z);
++                Chunk chunk = chunkProvider.getChunk(x, z, false, false);
+ 
+                 if (chunk != null && !chunk.isEmpty()) {
+                     queued++;
+                     cachedWorld.queueForPacking(chunk);
+                 }
+             }
+         }
+ 
+         return queued;
+     }
+ 
+     // ordered in a way that the closest blocks are generally first
+     public static List<ChunkPos> getChunkRange(int centerX, int centerZ, int chunkRadius) {
+         List<ChunkPos> chunks = new ArrayList<>();
+         // spiral out
+         chunks.add(new ChunkPos(centerX, centerZ));
+         for (int i = 1; i < chunkRadius; i++) {
+             for (int j = 0; j <= i; j++) {
+                 chunks.add(new ChunkPos(centerX - j, centerZ - i));
+                 if (j != 0) {
+                     chunks.add(new ChunkPos(centerX + j, centerZ - i));
+                     chunks.add(new ChunkPos(centerX - j, centerZ + i));
+                 }
+                 chunks.add(new ChunkPos(centerX + j, centerZ + i));
+                 if (j != i) {
+                     chunks.add(new ChunkPos(centerX - i, centerZ - j));
+                     chunks.add(new ChunkPos(centerX + i, centerZ - j));
+                     if (j != 0) {
+                         chunks.add(new ChunkPos(centerX - i, centerZ + j));
+                         chunks.add(new ChunkPos(centerX + i, centerZ + j));
+                     }
+                 }
+             }
+         }
+         return chunks;
+     }
+ 
+     private List<BlockPos> scanChunksInternal(IPlayerContext ctx, BlockOptionalMetaLookup lookup, List<ChunkPos> chunkPositions, int maxBlocks) {
+         assert ctx.world() != null;
+         try {
+             // p -> scanChunkInternal(ctx, lookup, p)
+             Stream<BlockPos> posStream = chunkPositions.parallelStream().flatMap(p -> scanChunkInternal(ctx, lookup, p));
+             if (maxBlocks >= 0) {
+                 // WARNING: this can be expensive if maxBlocks is large...
+                 // see limit's javadoc
+                 posStream = posStream.limit(maxBlocks);
+             }
+             return posStream.collect(Collectors.toList());
+         } catch (Exception e) {
+             e.printStackTrace();
+             throw e;
+         }
+     }
+ 
+     private Stream<BlockPos> scanChunkInternal(IPlayerContext ctx, BlockOptionalMetaLookup lookup, ChunkPos pos) {
+         IChunkProvider chunkProvider = ctx.world().getChunkProvider();
+         // if chunk is not loaded, return empty stream
 -        if (!chunkProvider.isChunkGeneratedAt(pos.x, pos.z)) {
++        if (chunkProvider.getChunk(pos.x, pos.z, false, false) == null) {
+             return Stream.empty();
+         }
+ 
+         long chunkX = (long) pos.x << 4;
+         long chunkZ = (long) pos.z << 4;
+ 
+         int playerSectionY = ctx.playerFeet().y >> 4;
+ 
 -        return collectChunkSections(lookup, chunkProvider.getLoadedChunk(pos.x, pos.z), chunkX, chunkZ, playerSectionY).stream();
++        return collectChunkSections(lookup, chunkProvider.getChunk(pos.x, pos.z, false, false), chunkX, chunkZ, playerSectionY).stream();
+     }
+ 
+ 
+ 
+     private List<BlockPos> collectChunkSections(BlockOptionalMetaLookup lookup, Chunk chunk, long chunkX, long chunkZ, int playerSection) {
+         // iterate over sections relative to player
+         List<BlockPos> blocks = new ArrayList<>();
 -        ExtendedBlockStorage[] sections = chunk.getBlockStorageArray();
++        ChunkSection[] sections = chunk.getSections();
+         int l = sections.length;
+         int i = playerSection - 1;
+         int j = playerSection;
+         for (; i >= 0 || j < l; ++j, --i) {
+             if (j < l) {
+                 visitSection(lookup, sections[j], blocks, chunkX, chunkZ);
+             }
+             if (i >= 0) {
+                 visitSection(lookup, sections[i], blocks, chunkX, chunkZ);
+             }
+         }
+         return blocks;
+     }
+ 
 -    private void visitSection(BlockOptionalMetaLookup lookup, ExtendedBlockStorage section, List<BlockPos> blocks, long chunkX, long chunkZ) {
++    private void visitSection(BlockOptionalMetaLookup lookup, ChunkSection section, List<BlockPos> blocks, long chunkX, long chunkZ) {
+         if (section == null || section.isEmpty()) {
+             return;
+         }
+ 
 -        BlockStateContainer sectionContainer = section.getData();
++        BlockStateContainer<IBlockState> sectionContainer = section.getData();
+         //this won't work if the PaletteStorage is of the type EmptyPaletteStorage
 -        if (((IBlockStateContainer) sectionContainer).getStorage() == null) {
++        if (((IBlockStateContainer<IBlockState>) sectionContainer).getStorage() == null) {
+             return;
+         }
+ 
 -        boolean[] isInFilter = getIncludedFilterIndices(lookup, ((IBlockStateContainer) sectionContainer).getPalette());
++        boolean[] isInFilter = getIncludedFilterIndices(lookup, ((IBlockStateContainer<IBlockState>) sectionContainer).getPalette());
+         if (isInFilter.length == 0) {
+             return;
+         }
+ 
 -        BitArray array = ((IBlockStateContainer) section.getData()).getStorage();
++        BitArray array = ((IBlockStateContainer<IBlockState>) section.getData()).getStorage();
+         long[] longArray = array.getBackingLongArray();
+         int arraySize = array.size();
 -        int bitsPerEntry = ((IBitArray) array).getBitsPerEntry();
++        int bitsPerEntry = array.bitsPerEntry();
+         long maxEntryValue = ((IBitArray) array).getMaxEntryValue();
+ 
+ 
+         int yOffset = section.getYLocation();
+ 
+         for (int idx = 0, kl = bitsPerEntry - 1; idx < arraySize; idx++, kl += bitsPerEntry) {
+             final int i = idx * bitsPerEntry;
+             final int j = i >> 6;
+             final int l = i & 63;
+             final int k = kl >> 6;
+             final long jl = longArray[j] >>> l;
+ 
+             if (j == k) {
+                 if (isInFilter[(int) (jl & maxEntryValue)]) {
+                     //noinspection DuplicateExpressions
+                     blocks.add(new BlockPos(
+                         chunkX + ((idx & 255) & 15),
+                         yOffset + (idx >> 8),
+                         chunkZ + ((idx & 255) >> 4)
+                     ));
+                 }
+             } else {
+                 if (isInFilter[(int) ((jl | longArray[k] << (64 - l)) & maxEntryValue)]) {
+                     //noinspection DuplicateExpressions
+                     blocks.add(new BlockPos(
+                         chunkX + ((idx & 255) & 15),
+                         yOffset + (idx >> 8),
+                         chunkZ + ((idx & 255) >> 4)
+                     ));
+                 }
+             }
+         }
+     }
+ 
 -    private boolean[] getIncludedFilterIndices(BlockOptionalMetaLookup lookup, IBlockStatePalette palette) {
++    private boolean[] getIncludedFilterIndices(BlockOptionalMetaLookup lookup, IBlockStatePalette<IBlockState> palette) {
+         boolean commonBlockFound = false;
+         ObjectIntIdentityMap<IBlockState> paletteMap = getPalette(palette);
+         int size = paletteMap.size();
+ 
+         boolean[] isInFilter = new boolean[size];
+ 
+         for (int i = 0; i < size; i++) {
+             IBlockState state = paletteMap.getByValue(i);
+             if (lookup.has(state)) {
+                 isInFilter[i] = true;
+                 commonBlockFound = true;
+             } else {
+                 isInFilter[i] = false;
+             }
+         }
+ 
+         if (!commonBlockFound) {
+             return new boolean[0];
+         }
+         return isInFilter;
+     }
+ 
+     /**
+      * cheats to get the actual map of id -> blockstate from the various palette implementations
+      */
 -    private static ObjectIntIdentityMap<IBlockState> getPalette(IBlockStatePalette palette) {
++    private static ObjectIntIdentityMap<IBlockState> getPalette(IBlockStatePalette<IBlockState> palette) {
+         if (palette instanceof BlockStatePaletteRegistry) {
+             return Block.BLOCK_STATE_IDS;
+         } else {
+             PacketBuffer buf = new PacketBuffer(Unpooled.buffer());
+             palette.write(buf);
+             int size = buf.readVarInt();
+             ObjectIntIdentityMap<IBlockState> states = new ObjectIntIdentityMap<>();
+             for (int i = 0; i < size; i++) {
+                 IBlockState state = Block.BLOCK_STATE_IDS.getByValue(buf.readVarInt());
+                 assert state != null;
+                 states.put(state, i);
+             }
+             return states;
+         }
+     }
+ }
diff --cc src/main/java/baritone/cache/WorldProvider.java
index 2d287eaee,59f671c99..350091585
--- a/src/main/java/baritone/cache/WorldProvider.java
+++ b/src/main/java/baritone/cache/WorldProvider.java
@@@ -19,18 -19,17 +19,18 @@@ package baritone.cache
  
  import baritone.Baritone;
  import baritone.api.cache.IWorldProvider;
- import baritone.api.utils.Helper;
+ import baritone.api.utils.IPlayerContext;
  import baritone.utils.accessor.IAnvilChunkLoader;
  import baritone.utils.accessor.IChunkProviderServer;
- import net.minecraft.server.integrated.IntegratedServer;
+ import net.minecraft.client.multiplayer.ServerData;
+ import net.minecraft.util.Tuple;
  import net.minecraft.world.World;
  import net.minecraft.world.WorldServer;
 +import net.minecraft.world.dimension.DimensionType;
  import org.apache.commons.lang3.SystemUtils;
  
- import java.io.File;
- import java.io.FileOutputStream;
  import java.io.IOException;
+ import java.nio.charset.StandardCharsets;
  import java.nio.file.Files;
  import java.nio.file.Path;
  import java.util.HashMap;
@@@ -57,66 -68,36 +69,36 @@@ public class WorldProvider implements I
      /**
       * Called when a new world is initialized to discover the
       *
-      * @param dimension The ID of the world's dimension
+      * @param world The new world
       */
-     public final void initWorld(DimensionType dimension) {
-         File directory;
-         File readme;
- 
-         IntegratedServer integratedServer = mc.getIntegratedServer();
+     public final void initWorld(World world) {
+         this.getSaveDirectories(world).ifPresent(dirs -> {
 -            final Path worldDir = dirs.getFirst();
 -            final Path readmeDir = dirs.getSecond();
++            final Path worldDir = dirs.getA();
++            final Path readmeDir = dirs.getB();
  
-         // If there is an integrated server running (Aka Singleplayer) then do magic to find the world save file
-         if (mc.isSingleplayer()) {
-             WorldServer localServerWorld = integratedServer.getWorld(dimension);
-             IChunkProviderServer provider = (IChunkProviderServer) localServerWorld.getChunkProvider();
-             IAnvilChunkLoader loader = (IAnvilChunkLoader) provider.getChunkLoader();
-             directory = loader.getChunkSaveLocation();
- 
-             // Gets the "depth" of this directory relative the the game's run directory, 2 is the location of the world
-             if (directory.toPath().relativize(mc.gameDir.toPath()).getNameCount() != 2) {
-                 // subdirectory of the main save directory for this world
-                 directory = directory.getParentFile();
-             }
- 
-             directory = new File(directory, "baritone");
-             readme = directory;
-         } else { // Otherwise, the server must be remote...
-             String folderName;
-             if (mc.getCurrentServerData() != null) {
-                 folderName = mc.getCurrentServerData().serverIP;
-             } else {
-                 //replaymod causes null currentServerData and false singleplayer.
-                 System.out.println("World seems to be a replay. Not loading Baritone cache.");
-                 currentWorld = null;
-                 mcWorld = mc.world;
-                 return;
-             }
-             if (SystemUtils.IS_OS_WINDOWS) {
-                 folderName = folderName.replace(":", "_");
-             }
-             directory = new File(Baritone.getDir(), folderName);
-             readme = Baritone.getDir();
-         }
- 
-         // lol wtf is this baritone folder in my minecraft save?
-         try (FileOutputStream out = new FileOutputStream(new File(readme, "readme.txt"))) {
-             // good thing we have a readme
-             out.write("https://github.com/cabaletta/baritone\n".getBytes());
-         } catch (IOException ignored) {}
+             try {
+                 // lol wtf is this baritone folder in my minecraft save?
+                 // good thing we have a readme
+                 Files.createDirectories(readmeDir);
+                 Files.write(
+                         readmeDir.resolve("readme.txt"),
+                         "https://github.com/cabaletta/baritone\n".getBytes(StandardCharsets.US_ASCII)
+                 );
+             } catch (IOException ignored) {}
  
-         // We will actually store the world data in a subfolder: "DIM<id>"
-         Path dir = new File(directory, "DIM" + dimension.getId()).toPath();
-         if (!Files.exists(dir)) {
+             // We will actually store the world data in a subfolder: "DIM<id>"
+             final Path worldDataDir = this.getWorldDataDirectory(worldDir, world);
              try {
-                 Files.createDirectories(dir);
+                 Files.createDirectories(worldDataDir);
              } catch (IOException ignored) {}
-         }
  
-         System.out.println("Baritone world data dir: " + dir);
-         synchronized (worldCache) {
-             this.currentWorld = worldCache.computeIfAbsent(dir, d -> new WorldData(d, dimension.getId()));
-         }
-         this.mcWorld = mc.world;
+             System.out.println("Baritone world data dir: " + worldDataDir);
+             synchronized (worldCache) {
 -                final int dimension = world.provider.getDimensionType().getId();
++                final int dimension = world.getDimension().getType().getId();
+                 this.currentWorld = worldCache.computeIfAbsent(worldDataDir, d -> new WorldData(d, dimension));
+             }
+             this.mcWorld = ctx.world();
+         });
      }
  
      public final void closeWorld() {
@@@ -129,15 -110,64 +111,64 @@@
          world.onClose();
      }
  
-     public final void ifWorldLoaded(Consumer<WorldData> currentWorldConsumer) {
-         detectAndHandleBrokenLoading();
-         if (this.currentWorld != null) {
-             currentWorldConsumer.accept(this.currentWorld);
+     private Path getWorldDataDirectory(Path parent, World world) {
 -        return parent.resolve("DIM" + world.provider.getDimensionType().getId());
++        return parent.resolve("DIM" + world.getDimension().getType().getId());
+     }
+ 
+     /**
+      * @param world The world
+      * @return An {@link Optional} containing the world's baritone dir and readme dir, or {@link Optional#empty()} if
+      *         the world isn't valid for caching.
+      */
+     private Optional<Tuple<Path, Path>> getSaveDirectories(World world) {
+         Path worldDir;
+         Path readmeDir;
+ 
+         // If there is an integrated server running (Aka Singleplayer) then do magic to find the world save file
+         if (ctx.minecraft().isSingleplayer()) {
 -            final int dimension = world.provider.getDimensionType().getId();
++            final DimensionType dimension = world.getDimension().getType();
+             final WorldServer localServerWorld = ctx.minecraft().getIntegratedServer().getWorld(dimension);
+             final IChunkProviderServer provider = (IChunkProviderServer) localServerWorld.getChunkProvider();
+             final IAnvilChunkLoader loader = (IAnvilChunkLoader) provider.getChunkLoader();
+             worldDir = loader.getChunkSaveLocation().toPath();
+ 
+             // Gets the "depth" of this directory relative to the game's run directory, 2 is the location of the world
+             if (worldDir.relativize(ctx.minecraft().gameDir.toPath()).getNameCount() != 2) {
+                 // subdirectory of the main save directory for this world
+                 worldDir = worldDir.getParent();
+             }
+ 
+             worldDir = worldDir.resolve("baritone");
+             readmeDir = worldDir;
+         } else { // Otherwise, the server must be remote...
+             String folderName;
+             final ServerData serverData = ctx.minecraft().getCurrentServerData();
+             if (serverData != null) {
+                 folderName = serverData.serverIP;
+             } else {
+                 //replaymod causes null currentServerData and false singleplayer.
+                 System.out.println("World seems to be a replay. Not loading Baritone cache.");
+                 currentWorld = null;
+                 mcWorld = ctx.world();
+                 return Optional.empty();
+             }
+             if (SystemUtils.IS_OS_WINDOWS) {
+                 folderName = folderName.replace(":", "_");
+             }
+             // TODO: This should probably be in "baritone/servers"
+             worldDir = baritone.getDirectory().resolve(folderName);
+             // Just write the readme to the baritone directory instead of each server save in it
+             readmeDir = baritone.getDirectory();
          }
+ 
+         return Optional.of(new Tuple<>(worldDir, readmeDir));
      }
  
-     private final void detectAndHandleBrokenLoading() {
-         if (this.mcWorld != mc.world) {
+     /**
+      * Why does this exist instead of fixing the event? Some mods break the event. Lol.
+      */
+     private void detectAndHandleBrokenLoading() {
+         if (this.mcWorld != ctx.world()) {
              if (this.currentWorld != null) {
                  System.out.println("mc.world unloaded unnoticed! Unloading Baritone cache now.");
                  closeWorld();
diff --cc src/main/java/baritone/cache/WorldScanner.java
index 4255326a9,362506298..fb27d891f
--- a/src/main/java/baritone/cache/WorldScanner.java
+++ b/src/main/java/baritone/cache/WorldScanner.java
@@@ -156,7 -156,7 +156,7 @@@ public enum WorldScanner implements IWo
                  continue;
              }
              int yReal = y0 << 4;
--            IBlockStateContainer bsc = (IBlockStateContainer) extendedblockstorage.getData();
++            IBlockStateContainer<IBlockState> bsc = (IBlockStateContainer<IBlockState>) extendedblockstorage.getData();
              // storageArray uses an optimized algorithm that's faster than getAt
              // creating this array and then using getAtPalette is faster than even getFast(int index)
              int[] storage = bsc.storageArray();
diff --cc src/main/java/baritone/command/ExampleBaritoneControl.java
index a4722a2ff,1a7b69644..e7ccf8426
--- a/src/main/java/baritone/command/ExampleBaritoneControl.java
+++ b/src/main/java/baritone/command/ExampleBaritoneControl.java
@@@ -27,9 -27,10 +27,9 @@@ import baritone.api.command.helpers.Tab
  import baritone.api.command.manager.ICommandManager;
  import baritone.api.event.events.ChatEvent;
  import baritone.api.event.events.TabCompleteEvent;
--import baritone.api.event.listener.AbstractGameEventListener;
  import baritone.api.utils.Helper;
  import baritone.api.utils.SettingsUtil;
+ import baritone.behavior.Behavior;
  import baritone.command.argument.ArgConsumer;
  import baritone.command.argument.CommandArguments;
  import baritone.command.manager.CommandManager;
@@@ -124,10 -125,10 +124,10 @@@ public class ExampleBaritoneControl ext
              }
          } else if (argc.hasExactlyOne()) {
              for (Settings.Setting setting : settings.allSettings) {
-                 if (SettingsUtil.javaOnlySetting(setting)) {
+                 if (setting.isJavaOnly()) {
                      continue;
                  }
 -                if (setting.getName().equalsIgnoreCase(pair.getFirst())) {
 +                if (setting.getName().equalsIgnoreCase(pair.getA())) {
                      logRanCommand(command, rest);
                      try {
                          this.manager.execute(String.format("set %s %s", setting.getName(), argc.getString()));
diff --cc src/main/java/baritone/command/defaults/MineCommand.java
index 63712fe3e,0f0f9bcb1..597d105ca
--- a/src/main/java/baritone/command/defaults/MineCommand.java
+++ b/src/main/java/baritone/command/defaults/MineCommand.java
@@@ -23,8 -24,7 +24,6 @@@ import baritone.api.command.argument.IA
  import baritone.api.command.datatypes.ForBlockOptionalMeta;
  import baritone.api.command.exception.CommandException;
  import baritone.api.utils.BlockOptionalMeta;
--import baritone.cache.WorldScanner;
  
  import java.util.ArrayList;
  import java.util.Arrays;
diff --cc src/main/java/baritone/command/defaults/PathCommand.java
index 182a1e5bc,24f47d625..b2021adf6
--- a/src/main/java/baritone/command/defaults/PathCommand.java
+++ b/src/main/java/baritone/command/defaults/PathCommand.java
@@@ -22,7 -23,7 +23,6 @@@ import baritone.api.command.Command
  import baritone.api.command.argument.IArgConsumer;
  import baritone.api.command.exception.CommandException;
  import baritone.api.process.ICustomGoalProcess;
--import baritone.cache.WorldScanner;
  
  import java.util.Arrays;
  import java.util.List;
diff --cc src/main/java/baritone/command/defaults/RenderCommand.java
index a77add6e6,ab4a9dbcd..4dd99a462
--- a/src/main/java/baritone/command/defaults/RenderCommand.java
+++ b/src/main/java/baritone/command/defaults/RenderCommand.java
@@@ -37,8 -37,8 +37,8 @@@ public class RenderCommand extends Comm
      public void execute(String label, IArgConsumer args) throws CommandException {
          args.requireMax(0);
          BetterBlockPos origin = ctx.playerFeet();
-         int renderDistance = (mc.gameSettings.renderDistanceChunks + 1) * 16;
-         mc.worldRenderer.markBlockRangeForRenderUpdate(
+         int renderDistance = (ctx.minecraft().gameSettings.renderDistanceChunks + 1) * 16;
 -        ctx.minecraft().renderGlobal.markBlockRangeForRenderUpdate(
++        ctx.minecraft().worldRenderer.markBlockRangeForRenderUpdate(
                  origin.x - renderDistance,
                  0,
                  origin.z - renderDistance,
diff --cc src/main/java/baritone/command/defaults/RepackCommand.java
index cafbea524,cd054b10b..9f972561d
--- a/src/main/java/baritone/command/defaults/RepackCommand.java
+++ b/src/main/java/baritone/command/defaults/RepackCommand.java
@@@ -21,7 -22,7 +22,6 @@@ import baritone.api.IBaritone
  import baritone.api.command.Command;
  import baritone.api.command.argument.IArgConsumer;
  import baritone.api.command.exception.CommandException;
--import baritone.cache.WorldScanner;
  
  import java.util.Arrays;
  import java.util.List;
diff --cc src/main/java/baritone/command/defaults/SetCommand.java
index fd9bb0457,4325cd625..87c4a4c8a
--- a/src/main/java/baritone/command/defaults/SetCommand.java
+++ b/src/main/java/baritone/command/defaults/SetCommand.java
@@@ -209,6 -223,9 +223,9 @@@ public class SetCommand extends Comman
                              .addToggleableSettings()
                              .filterPrefix(args.getString())
                              .stream();
+                 } else if (Arrays.asList("ld", "load").contains(arg.toLowerCase(Locale.US))) {
+                     // settings always use the directory of the main Minecraft instance
 -                    return RelativeFile.tabComplete(args, Minecraft.getMinecraft().gameDir.toPath().resolve("baritone").toFile());
++                    return RelativeFile.tabComplete(args, Minecraft.getInstance().gameDir.toPath().resolve("baritone").toFile());
                  }
                  Settings.Setting setting = Baritone.settings().byLowerName.get(arg.toLowerCase(Locale.US));
                  if (setting != null) {
diff --cc src/main/java/baritone/pathing/movement/CalculationContext.java
index 433101c1e,129f00e20..f47fd7f20
--- a/src/main/java/baritone/pathing/movement/CalculationContext.java
+++ b/src/main/java/baritone/pathing/movement/CalculationContext.java
@@@ -91,11 -91,11 +91,11 @@@ public class CalculationContext 
          this.baritone = baritone;
          EntityPlayerSP player = baritone.getPlayerContext().player();
          this.world = baritone.getPlayerContext().world();
-         this.worldData = (WorldData) baritone.getWorldProvider().getCurrentWorld();
-         this.bsi = new BlockStateInterface(world, worldData, forUseOnAnotherThread);
+         this.worldData = (WorldData) baritone.getPlayerContext().worldData();
+         this.bsi = new BlockStateInterface(baritone.getPlayerContext(), forUseOnAnotherThread);
          this.toolSet = new ToolSet(player);
          this.hasThrowaway = Baritone.settings().allowPlace.value && ((Baritone) baritone).getInventoryBehavior().hasGenericThrowaway();
 -        this.hasWaterBucket = Baritone.settings().allowWaterBucketFall.value && InventoryPlayer.isHotbar(player.inventory.getSlotFor(STACK_BUCKET_WATER)) && !world.provider.isNether();
 +        this.hasWaterBucket = Baritone.settings().allowWaterBucketFall.value && InventoryPlayer.isHotbar(player.inventory.getSlotFor(STACK_BUCKET_WATER)) && !world.getDimension().isNether();
          this.canSprint = Baritone.settings().allowSprint.value && player.getFoodStats().getFoodLevel() > 6;
          this.placeBlockCost = Baritone.settings().blockPlacementPenalty.value;
          this.allowBreak = Baritone.settings().allowBreak.value;
diff --cc src/main/java/baritone/pathing/movement/Movement.java
index d61713952,5a17d26c5..068eed0c0
--- a/src/main/java/baritone/pathing/movement/Movement.java
+++ b/src/main/java/baritone/pathing/movement/Movement.java
@@@ -160,10 -161,10 +160,10 @@@ public abstract class Movement implemen
              if (!ctx.world().getEntitiesWithinAABB(EntityFallingBlock.class, new AxisAlignedBB(0, 0, 0, 1, 1.1, 1).offset(blockPos)).isEmpty() && Baritone.settings().pauseMiningForFallingBlocks.value) {
                  return false;
              }
 -            if (!MovementHelper.canWalkThrough(ctx, blockPos) && !(BlockStateInterface.getBlock(ctx, blockPos) instanceof BlockLiquid)) { // can't break liquid, so don't try
 +            if (!MovementHelper.canWalkThrough(ctx, blockPos)) { // can't break air, so don't try
                  somethingInTheWay = true;
                  MovementHelper.switchToBestToolFor(ctx, BlockStateInterface.get(ctx, blockPos));
-                 Optional<Rotation> reachable = RotationUtils.reachable(ctx.player(), blockPos, ctx.playerController().getBlockReachDistance());
+                 Optional<Rotation> reachable = RotationUtils.reachable(ctx, blockPos, ctx.playerController().getBlockReachDistance());
                  if (reachable.isPresent()) {
                      Rotation rotTowardsBlock = reachable.get();
                      state.setTarget(new MovementState.MovementTarget(rotTowardsBlock, true));
diff --cc src/main/java/baritone/pathing/movement/MovementHelper.java
index e8180c0b0,881bb6f15..2af341035
--- a/src/main/java/baritone/pathing/movement/MovementHelper.java
+++ b/src/main/java/baritone/pathing/movement/MovementHelper.java
@@@ -726,8 -684,9 +726,9 @@@ public interface MovementHelper extend
                  double faceY = (placeAt.getY() + against1.getY() + 0.5D) * 0.5D;
                  double faceZ = (placeAt.getZ() + against1.getZ() + 1.0D) * 0.5D;
                  Rotation place = RotationUtils.calcRotationFromVec3d(wouldSneak ? RayTraceUtils.inferSneakingEyePosition(ctx.player()) : ctx.playerHead(), new Vec3d(faceX, faceY, faceZ), ctx.playerRotations());
-                 RayTraceResult res = RayTraceUtils.rayTraceTowards(ctx.player(), place, ctx.playerController().getBlockReachDistance(), wouldSneak);
+                 Rotation actual = baritone.getLookBehavior().getAimProcessor().peekRotation(place);
+                 RayTraceResult res = RayTraceUtils.rayTraceTowards(ctx.player(), actual, ctx.playerController().getBlockReachDistance(), wouldSneak);
 -                if (res != null && res.typeOfHit == RayTraceResult.Type.BLOCK && res.getBlockPos().equals(against1) && res.getBlockPos().offset(res.sideHit).equals(placeAt)) {
 +                if (res != null && res.type == RayTraceResult.Type.BLOCK && res.getBlockPos().equals(against1) && res.getBlockPos().offset(res.sideHit).equals(placeAt)) {
                      state.setTarget(new MovementState.MovementTarget(place, true));
                      found = true;
  
diff --cc src/main/java/baritone/pathing/movement/movements/MovementDescend.java
index 4a43df52d,2d8180356..c8261f21e
--- a/src/main/java/baritone/pathing/movement/movements/MovementDescend.java
+++ b/src/main/java/baritone/pathing/movement/movements/MovementDescend.java
@@@ -20,7 -20,7 +20,6 @@@ package baritone.pathing.movement.movem
  import baritone.api.IBaritone;
  import baritone.api.pathing.movement.MovementStatus;
  import baritone.api.utils.BetterBlockPos;
--import baritone.api.utils.Rotation;
  import baritone.api.utils.RotationUtils;
  import baritone.api.utils.input.Input;
  import baritone.pathing.movement.CalculationContext;
@@@ -33,7 -33,7 +32,6 @@@ import com.google.common.collect.Immuta
  import net.minecraft.block.Block;
  import net.minecraft.block.BlockFalling;
  import net.minecraft.block.state.IBlockState;
--import net.minecraft.client.entity.EntityPlayerSP;
  import net.minecraft.init.Blocks;
  import net.minecraft.util.math.BlockPos;
  import net.minecraft.util.math.Vec3d;
diff --cc src/main/java/baritone/process/BuilderProcess.java
index a0682b1ca,60066971e..b0b9ea416
--- a/src/main/java/baritone/process/BuilderProcess.java
+++ b/src/main/java/baritone/process/BuilderProcess.java
@@@ -281,9 -278,9 +282,9 @@@ public final class BuilderProcess exten
                          continue; // irrelevant
                      }
                      IBlockState curr = bcc.bsi.get0(x, y, z);
 -                    if (curr.getBlock() != Blocks.AIR && !(curr.getBlock() instanceof BlockLiquid) && !valid(curr, desired, false)) {
 +                    if (!(curr.getBlock() instanceof BlockAir) && !(curr.getBlock() == Blocks.WATER || curr.getBlock() == Blocks.LAVA) && !valid(curr, desired, false)) {
                          BetterBlockPos pos = new BetterBlockPos(x, y, z);
-                         Optional<Rotation> rot = RotationUtils.reachable(ctx.player(), pos, ctx.playerController().getBlockReachDistance());
+                         Optional<Rotation> rot = RotationUtils.reachable(ctx, pos, ctx.playerController().getBlockReachDistance());
                          if (rot.isPresent()) {
                              return Optional.of(new Tuple<>(pos, rot.get()));
                          }
@@@ -362,9 -351,10 +363,10 @@@
                  double placeY = placeAgainstPos.y + aabb.minY * placementMultiplier.y + aabb.maxY * (1 - placementMultiplier.y);
                  double placeZ = placeAgainstPos.z + aabb.minZ * placementMultiplier.z + aabb.maxZ * (1 - placementMultiplier.z);
                  Rotation rot = RotationUtils.calcRotationFromVec3d(RayTraceUtils.inferSneakingEyePosition(ctx.player()), new Vec3d(placeX, placeY, placeZ), ctx.playerRotations());
-                 RayTraceResult result = RayTraceUtils.rayTraceTowards(ctx.player(), rot, ctx.playerController().getBlockReachDistance(), true);
+                 Rotation actualRot = baritone.getLookBehavior().getAimProcessor().peekRotation(rot);
+                 RayTraceResult result = RayTraceUtils.rayTraceTowards(ctx.player(), actualRot, ctx.playerController().getBlockReachDistance(), true);
 -                if (result != null && result.typeOfHit == RayTraceResult.Type.BLOCK && result.getBlockPos().equals(placeAgainstPos) && result.sideHit == against.getOpposite()) {
 +                if (result != null && result.type == RayTraceResult.Type.BLOCK && result.getBlockPos().equals(placeAgainstPos) && result.sideHit == against.getOpposite()) {
-                     OptionalInt hotbar = hasAnyItemThatWouldPlace(toPlace, result, rot);
+                     OptionalInt hotbar = hasAnyItemThatWouldPlace(toPlace, result, actualRot);
                      if (hotbar.isPresent()) {
                          return Optional.of(new Placement(hotbar.getAsInt(), placeAgainstPos, against.getOpposite(), rot));
                      }
diff --cc src/main/java/baritone/process/FarmProcess.java
index 12a21531f,1536bdb61..081041a04
--- a/src/main/java/baritone/process/FarmProcess.java
+++ b/src/main/java/baritone/process/FarmProcess.java
@@@ -28,7 -30,7 +30,6 @@@ import baritone.api.utils.RayTraceUtils
  import baritone.api.utils.Rotation;
  import baritone.api.utils.RotationUtils;
  import baritone.api.utils.input.Input;
--import baritone.cache.WorldScanner;
  import baritone.pathing.movement.MovementHelper;
  import baritone.utils.BaritoneProcessHelper;
  import net.minecraft.block.*;
@@@ -83,8 -87,8 +84,9 @@@ public final class FarmProcess extends 
              Items.POTATO,
              Items.CARROT,
              Items.NETHER_WART,
 -            Items.REEDS,
 -            Item.getItemFromBlock(Blocks.CACTUS)
++            Items.COCOA_BEANS,
 +            Blocks.SUGAR_CANE.asItem(),
 +            Blocks.CACTUS.asItem()
      );
  
      public FarmProcess(Baritone baritone) {
@@@ -114,9 -118,10 +116,10 @@@
          POTATOES((BlockCrops) Blocks.POTATOES),
          BEETROOT((BlockCrops) Blocks.BEETROOTS),
          PUMPKIN(Blocks.PUMPKIN, state -> true),
 -        MELON(Blocks.MELON_BLOCK, state -> true),
 -        NETHERWART(Blocks.NETHER_WART, state -> state.getValue(BlockNetherWart.AGE) >= 3),
 -        COCOA(Blocks.COCOA, state -> state.getValue(BlockCocoa.AGE) >= 2),
 -        SUGARCANE(Blocks.REEDS, null) {
 +        MELON(Blocks.MELON, state -> true),
 +        NETHERWART(Blocks.NETHER_WART, state -> state.get(BlockNetherWart.AGE) >= 3),
++        COCOA(Blocks.COCOA, state -> state.get(BlockCocoa.AGE) >= 2),
 +        SUGARCANE(Blocks.SUGAR_CANE, null) {
              @Override
              public boolean readyToHarvest(World world, BlockPos pos, IBlockState state) {
                  if (Baritone.settings().replantCrops.value) {
@@@ -173,6 -178,10 +176,10 @@@
          return !stack.isEmpty() && stack.getItem().equals(Items.NETHER_WART);
      }
  
+     private boolean isCocoa(ItemStack stack) {
 -        return !stack.isEmpty() && stack.getItem() instanceof ItemDye && EnumDyeColor.byDyeDamage(stack.getMetadata()) == EnumDyeColor.BROWN;
++        return !stack.isEmpty() && stack.getItem().equals(Items.COCOA_BEANS);
+     }
+ 
      @Override
      public PathingCommand onTick(boolean calcFailed, boolean isSafeToCancel) {
          ArrayList<Block> scan = new ArrayList<>();
@@@ -181,6 -190,7 +188,7 @@@
          }
          if (Baritone.settings().replantCrops.value) {
              scan.add(Blocks.FARMLAND);
 -            scan.add(Blocks.LOG);
++            scan.add(Blocks.JUNGLE_LOG);
              if (Baritone.settings().replantNetherWart.value) {
                  scan.add(Blocks.SOUL_SAND);
              }
@@@ -216,6 -227,19 +225,15 @@@
                  }
                  continue;
              }
 -            if (state.getBlock() == Blocks.LOG) {
 -                // yes, both log blocks and the planks block define separate properties but share the enum
 -                if (state.getValue(BlockOldLog.VARIANT) != BlockPlanks.EnumType.JUNGLE) {
 -                    continue;
 -                }
++            if (state.getBlock() == Blocks.JUNGLE_LOG) {
+                 for (EnumFacing direction : EnumFacing.Plane.HORIZONTAL) {
+                     if (ctx.world().getBlockState(pos.offset(direction)).getBlock() instanceof BlockAir) {
+                         openLog.add(pos);
+                         break;
+                     }
+                 }
+                 continue;
+             }
              if (readyForHarvest(ctx.world(), pos, state)) {
                  toBreak.add(pos);
                  continue;
@@@ -244,10 -268,10 +262,10 @@@
          both.addAll(openSoulsand);
          for (BlockPos pos : both) {
              boolean soulsand = openSoulsand.contains(pos);
-             Optional<Rotation> rot = RotationUtils.reachableOffset(ctx.player(), pos, new Vec3d(pos.getX() + 0.5, pos.getY() + 1, pos.getZ() + 0.5), ctx.playerController().getBlockReachDistance(), false);
+             Optional<Rotation> rot = RotationUtils.reachableOffset(ctx, pos, new Vec3d(pos.getX() + 0.5, pos.getY() + 1, pos.getZ() + 0.5), ctx.playerController().getBlockReachDistance(), false);
              if (rot.isPresent() && isSafeToCancel && baritone.getInventoryBehavior().throwaway(true, soulsand ? this::isNetherWart : this::isPlantable)) {
                  RayTraceResult result = RayTraceUtils.rayTraceTowards(ctx.player(), rot.get(), ctx.playerController().getBlockReachDistance());
 -                if (result.typeOfHit == RayTraceResult.Type.BLOCK && result.sideHit == EnumFacing.UP) {
 +                if (result.type == RayTraceResult.Type.BLOCK && result.sideHit == EnumFacing.UP) {
                      baritone.getLookBehavior().updateTarget(rot.get(), true);
                      if (ctx.isLookingAt(pos)) {
                          baritone.getInputOverrideHandler().setInputForceState(Input.CLICK_RIGHT, true);
@@@ -256,6 -280,25 +274,25 @@@
                  }
              }
          }
+         for (BlockPos pos : openLog) {
+             for (EnumFacing dir : EnumFacing.Plane.HORIZONTAL) {
+                 if (!(ctx.world().getBlockState(pos.offset(dir)).getBlock() instanceof BlockAir)) {
+                     continue;
+                 }
+                 Vec3d faceCenter = new Vec3d(pos).add(0.5, 0.5, 0.5).add(new Vec3d(dir.getDirectionVec()).scale(0.5));
+                 Optional<Rotation> rot = RotationUtils.reachableOffset(ctx, pos, faceCenter, ctx.playerController().getBlockReachDistance(), false);
+                 if (rot.isPresent() && isSafeToCancel && baritone.getInventoryBehavior().throwaway(true, this::isCocoa)) {
+                     RayTraceResult result = RayTraceUtils.rayTraceTowards(ctx.player(), rot.get(), ctx.playerController().getBlockReachDistance());
 -                    if (result.typeOfHit == RayTraceResult.Type.BLOCK && result.sideHit == dir) {
++                    if (result.type == RayTraceResult.Type.BLOCK && result.sideHit == dir) {
+                         baritone.getLookBehavior().updateTarget(rot.get(), true);
+                         if (ctx.isLookingAt(pos)) {
+                             baritone.getInputOverrideHandler().setInputForceState(Input.CLICK_RIGHT, true);
+                         }
+                         return new PathingCommand(null, PathingCommandType.REQUEST_PAUSE);
+                     }
+                 }
+             }
+         }
          for (BlockPos pos : bonemealable) {
              Optional<Rotation> rot = RotationUtils.reachable(ctx, pos);
              if (rot.isPresent() && isSafeToCancel && baritone.getInventoryBehavior().throwaway(true, this::isBoneMeal)) {
diff --cc src/main/java/baritone/process/MineProcess.java
index 34f5c4c35,8cd1a6cae..b890e96f3
--- a/src/main/java/baritone/process/MineProcess.java
+++ b/src/main/java/baritone/process/MineProcess.java
@@@ -25,7 -26,7 +26,6 @@@ import baritone.api.process.PathingComm
  import baritone.api.utils.*;
  import baritone.api.utils.input.Input;
  import baritone.cache.CachedChunk;
--import baritone.cache.WorldScanner;
  import baritone.pathing.movement.CalculationContext;
  import baritone.pathing.movement.MovementHelper;
  import baritone.utils.BaritoneProcessHelper;
diff --cc src/main/java/baritone/utils/BlockStateInterface.java
index 51927d263,1d6dcaf79..35168c74c
--- a/src/main/java/baritone/utils/BlockStateInterface.java
+++ b/src/main/java/baritone/utils/BlockStateInterface.java
@@@ -44,9 -43,8 +43,8 @@@ public class BlockStateInterface 
  
      private final Long2ObjectMap<Chunk> loadedChunks;
      private final WorldData worldData;
-     protected final IBlockReader world;
      public final BlockPos.MutableBlockPos isPassableBlockPos;
 -    public final IBlockAccess access;
 +    public final IBlockReader access;
      public final BetterWorldBorder worldBorder;
  
      private Chunk prev = null;
diff --cc src/main/java/baritone/utils/IRenderer.java
index e6a7d0f1c,680d7e380..ab9f4c5a5
--- a/src/main/java/baritone/utils/IRenderer.java
+++ b/src/main/java/baritone/utils/IRenderer.java
@@@ -35,12 -36,18 +36,18 @@@ public interface IRenderer 
  
      Tessellator tessellator = Tessellator.getInstance();
      BufferBuilder buffer = tessellator.getBuffer();
-     RenderManager renderManager = Helper.mc.getRenderManager();
 -    RenderManager renderManager = Minecraft.getMinecraft().getRenderManager();
 -    TextureManager textureManager = Minecraft.getMinecraft().getTextureManager();
++    RenderManager renderManager = Minecraft.getInstance().getRenderManager();
++    TextureManager textureManager = Minecraft.getInstance().getTextureManager();
      Settings settings = BaritoneAPI.getSettings();
  
+     float[] color = new float[] {1.0F, 1.0F, 1.0F, 255.0F};
+ 
      static void glColor(Color color, float alpha) {
          float[] colorComponents = color.getColorComponents(null);
-         GlStateManager.color4f(colorComponents[0], colorComponents[1], colorComponents[2], alpha);
+         IRenderer.color[0] = colorComponents[0];
+         IRenderer.color[1] = colorComponents[1];
+         IRenderer.color[2] = colorComponents[2];
+         IRenderer.color[3] = alpha;
      }
  
      static void startLines(Color color, float alpha, float lineWidth, boolean ignoreDepth) {
@@@ -52,8 -59,9 +59,9 @@@
          GlStateManager.depthMask(false);
  
          if (ignoreDepth) {
 -            GlStateManager.disableDepth();
 +            GlStateManager.disableDepthTest();
          }
+         buffer.begin(GL_LINES, DefaultVertexFormats.POSITION_COLOR);
      }
  
      static void startLines(Color color, float lineWidth, boolean ignoreDepth) {
@@@ -61,8 -69,9 +69,9 @@@
      }
  
      static void endLines(boolean ignoredDepth) {
+         tessellator.draw();
          if (ignoredDepth) {
 -            GlStateManager.enableDepth();
 +            GlStateManager.enableDepthTest();
          }
  
          GlStateManager.depthMask(true);
diff --cc src/main/java/baritone/utils/PathRenderer.java
index 691c66502,b3abc8cd2..d53476f67
--- a/src/main/java/baritone/utils/PathRenderer.java
+++ b/src/main/java/baritone/utils/PathRenderer.java
@@@ -29,16 -29,14 +29,16 @@@ import baritone.pathing.path.PathExecut
  import net.minecraft.block.state.IBlockState;
  import net.minecraft.client.renderer.GlStateManager;
  import net.minecraft.client.renderer.tileentity.TileEntityBeaconRenderer;
- import net.minecraft.client.renderer.vertex.DefaultVertexFormats;
  import net.minecraft.entity.Entity;
 -import net.minecraft.init.Blocks;
 +import net.minecraft.util.ResourceLocation;
  import net.minecraft.util.math.AxisAlignedBB;
  import net.minecraft.util.math.BlockPos;
  import net.minecraft.util.math.MathHelper;
 +import net.minecraft.util.math.shapes.VoxelShape;
 +import net.minecraft.util.math.shapes.VoxelShapes;
  
  import java.awt.*;
+ import java.util.Arrays;
  import java.util.Collection;
  import java.util.Collections;
  import java.util.List;
@@@ -57,14 -52,19 +57,19 @@@ public final class PathRenderer impleme
      private PathRenderer() {}
  
      public static void render(RenderEvent event, PathingBehavior behavior) {
-         float partialTicks = event.getPartialTicks();
-         Goal goal = behavior.getGoal();
-         if (Helper.mc.currentScreen instanceof GuiClick) {
-             ((GuiClick) Helper.mc.currentScreen).onRender();
+         final IPlayerContext ctx = behavior.ctx;
+         if (ctx.world() == null) {
+             return;
+         }
+         if (ctx.minecraft().currentScreen instanceof GuiClick) {
+             ((GuiClick) ctx.minecraft().currentScreen).onRender();
          }
  
-         int thisPlayerDimension = behavior.baritone.getPlayerContext().world().getDimension().getType().getId();
-         int currentRenderViewDimension = BaritoneAPI.getProvider().getPrimaryBaritone().getPlayerContext().world().getDimension().getType().getId();
+         final float partialTicks = event.getPartialTicks();
+         final Goal goal = behavior.getGoal();
+ 
 -        final int thisPlayerDimension = ctx.world().provider.getDimensionType().getId();
 -        final int currentRenderViewDimension = BaritoneAPI.getProvider().getPrimaryBaritone().getPlayerContext().world().provider.getDimensionType().getId();
++        final int thisPlayerDimension = ctx.world().getDimension().getType().getId();
++        final int currentRenderViewDimension = BaritoneAPI.getProvider().getPrimaryBaritone().getPlayerContext().world().getDimension().getType().getId();
  
          if (thisPlayerDimension != currentRenderViewDimension) {
              // this is a path for a bot in a different dimension, don't render it
@@@ -191,10 -183,15 +188,10 @@@
  
          positions.forEach(pos -> {
              IBlockState state = bsi.get0(pos);
 -            AxisAlignedBB toDraw;
 -
 -            if (state.getBlock().equals(Blocks.AIR)) {
 -                toDraw = Blocks.DIRT.getDefaultState().getSelectedBoundingBox(player.world, pos);
 -            } else {
 -                toDraw = state.getSelectedBoundingBox(player.world, pos);
 -            }
 -
 +            VoxelShape shape = state.getShape(player.world, pos);
 +            AxisAlignedBB toDraw = shape.isEmpty() ? VoxelShapes.fullCube().getBoundingBox() : shape.getBoundingBox();
 +            toDraw = toDraw.offset(pos);
-             IRenderer.drawAABB(toDraw, .002D);
+             IRenderer.emitAABB(toDraw, .002D);
          });
  
          IRenderer.endLines(settings.renderSelectionBoxesIgnoreDepth.value);
@@@ -238,11 -240,10 +240,9 @@@
              if (settings.renderGoalXZBeacon.value) {
                  glPushAttrib(GL_LIGHTING_BIT);
  
-                 TileEntityBeaconRenderer a;
 -                textureManager.bindTexture(TileEntityBeaconRenderer.TEXTURE_BEACON_BEAM);
--
-                 Helper.mc.getTextureManager().bindTexture(TEXTURE_BEACON_BEAM);
++                textureManager.bindTexture(TEXTURE_BEACON_BEAM);
                  if (settings.renderGoalIgnoreDepth.value) {
 -                    GlStateManager.disableDepth();
 +                    GlStateManager.disableDepthTest();
                  }
  
                  TileEntityBeaconRenderer.renderBeamSegment(
diff --cc src/main/java/baritone/utils/accessor/IBitArray.java
index baea5c1da,08f54584c..15f5f7c36
--- a/src/main/java/baritone/utils/accessor/IBitArray.java
+++ b/src/main/java/baritone/utils/accessor/IBitArray.java
@@@ -3,4 -3,8 +3,6 @@@ package baritone.utils.accessor
  public interface IBitArray {
  
      int[] toArray();
+ 
+     long getMaxEntryValue();
 -
 -    int getBitsPerEntry();
  }
diff --cc src/main/java/baritone/utils/accessor/IBlockStateContainer.java
index 39572fc5d,bd280aeb1..3b83cf277
--- a/src/main/java/baritone/utils/accessor/IBlockStateContainer.java
+++ b/src/main/java/baritone/utils/accessor/IBlockStateContainer.java
@@@ -1,10 -1,16 +1,15 @@@
  package baritone.utils.accessor;
  
--import net.minecraft.block.state.IBlockState;
+ import net.minecraft.util.BitArray;
+ import net.minecraft.world.chunk.IBlockStatePalette;
  
--public interface IBlockStateContainer {
++public interface IBlockStateContainer<T> {
  
-     IBlockState getAtPalette(int index);
 -    IBlockStatePalette getPalette();
++    IBlockStatePalette<T> getPalette();
+ 
+     BitArray getStorage();
+ 
 -    IBlockState getAtPalette(int index);
++    T getAtPalette(int index);
  
      int[] storageArray();
  }
```
