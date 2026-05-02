# Case 3 — Project: baritone — Merge commit SHA1: 2b3a302a5fdae4d150c381d48436c4d674c275b2

## Modified file(s):
- `src/launch/java/baritone/launch/mixins/MixinChatScreen.java`
- `src/launch/resources/mixins.baritone.json`

## Class(es) modified in the merge:
`MixinGuiChat` (renamed to `MixinChatScreen`)

## Merge effort lines in the combined diff

```diff
 -import net.minecraft.client.gui.GuiChat;
 -import net.minecraft.client.gui.GuiTextField;
++import net.minecraft.client.gui.screen.ChatScreen;
++import net.minecraft.client.gui.widget.TextFieldWidget;

 -@Mixin(GuiChat.class)
 -public class MixinGuiChat {
++@Mixin(ChatScreen.class)
++public class MixinChatScreen {

     @Shadow
 -    protected GuiTextField inputField;
++    protected TextFieldWidget inputField;
```

```diff
 -    \"MixinGuiChat\",
++    \"MixinChatScreen\",
```

## Relevant final code in the merge

```java
import net.minecraft.client.gui.screen.ChatScreen;
import net.minecraft.client.gui.widget.TextFieldWidget;
// ...

@Mixin(ChatScreen.class)
public class MixinChatScreen {

    @Shadow
    protected TextFieldWidget inputField;
    // ...
}
```

```json
"client": [
    "MixinChatScreen",
    ...
]
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
7 lines (7 `++`, 0 `--`)

## What each side had

**Parent 1 (1.12/old MC branch):**
The mixin class was named `MixinGuiChat`, targeting the old Minecraft class `GuiChat` with a field `GuiTextField inputField`, and registered in `mixins.baritone.json` as `"MixinGuiChat"`. P1 had:
```
- import net.minecraft.client.gui.GuiChat;
- import net.minecraft.client.gui.GuiTextField;
- @Mixin(GuiChat.class)
- public class MixinGuiChat {
-     protected GuiTextField inputField;
```

**Parent 2 (1.14+ Forge/MC update branch):**
Renamed `GuiChat` to `ChatScreen` and `GuiTextField` to `TextFieldWidget` in the Minecraft API. P2 adapted the mixin but did not yet add `MixinChatScreen` to the mixin registry. P2 had:
```
+ @Mixin(ChatScreen.class)
+ public class MixinChatScreen {
+     protected TextFieldWidget inputField;
```

## Interpretation

This case evidences a **Rename_Class** refactoring: `MixinGuiChat` was renamed to `MixinChatScreen` in P2 as a consequence of the Minecraft API migration from `GuiChat` to `ChatScreen`. The merge had to reconcile P1's reference to `"MixinGuiChat"` in `mixins.baritone.json` with P2's new class name, producing `++` on the new class declaration (`@Mixin(ChatScreen.class)`, `public class MixinChatScreen`), the renamed field type (`TextFieldWidget`), and the updated entry in the JSON registry. The `++` lines directly confirm the rename: the class annotation, class name, and field type all change together as a unit, which is the hallmark of a Rename_Class refactoring. The conflict is surgical and specific to this mixin class.

## Complete diff

```diff
diff --cc src/launch/java/baritone/launch/mixins/MixinChatScreen.java
index 000000000,8d4c867e5..fe52723df
mode 000000,100644..100644
--- a/src/launch/java/baritone/launch/mixins/MixinChatScreen.java
+++ b/src/launch/java/baritone/launch/mixins/MixinChatScreen.java
@@@ -1,0 -1,99 +1,99 @@@
+ package baritone.launch.mixins;
 -import net.minecraft.client.gui.GuiChat;
 -import net.minecraft.client.gui.GuiTextField;
++import net.minecraft.client.gui.screen.ChatScreen;
++import net.minecraft.client.gui.widget.TextFieldWidget;
 -@Mixin(GuiChat.class)
 -public class MixinGuiChat {
++@Mixin(ChatScreen.class)
++public class MixinChatScreen {
     @Shadow
 -    protected GuiTextField inputField;
++    protected TextFieldWidget inputField;

diff --cc src/launch/resources/mixins.baritone.json
@@@ -8,21 -8,26 +8,22 @@@
 -    \"MixinGuiChat\",
++    \"MixinChatScreen\",
```
