# Case 1 — Project: dbeaver — Merge commit SHA1: 86d2d189a1d5fdf1f08e83b3843e068e9aa50bb5

## Modified file(s):

`plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/controls/resultset/ResultSetViewer.java`

## Class(es) modified in the merge:

`ResultSetViewer`

## Merge effort lines in the combined diff

```diff
  import org.jkiss.dbeaver.ui.data.IValueController;
  import org.jkiss.dbeaver.ui.dialogs.ConfirmationDialog;
- import org.jkiss.dbeaver.ui.editors.EditorUtils;
+ import org.jkiss.dbeaver.ui.editors.TextEditorUtils;
  import org.jkiss.dbeaver.ui.editors.object.struct.EditConstraintPage;
  import org.jkiss.dbeaver.ui.editors.object.struct.EditDictionaryPage;
```

The merge-effort line is the import replacement resolving the naming conflict:

```diff
- import org.jkiss.dbeaver.ui.editors.EditorUtils;
+ import org.jkiss.dbeaver.ui.editors.TextEditorUtils;
```

Note: In the combined diff notation, the final merged result contains neither a pure `" +"` nor `"+ "` line for this import — the line `+ import org.jkiss.dbeaver.ui.editors.TextEditorUtils;` appears as a P2-contributed line, indicating that P2 performed the rename and the merge adopted P2's version, discarding P1's `EditorUtils` import. The `- import org.jkiss.dbeaver.ui.editors.EditorUtils;` is the line discarded from P1.

Full context from the combined diff:

```diff
@@@ -85,11 -86,9 +86,11 @@@ import org.jkiss.dbeaver.ui.controls.re
  import org.jkiss.dbeaver.ui.controls.resultset.valuefilter.FilterValueEditPopup;
  import org.jkiss.dbeaver.ui.controls.resultset.view.EmptyPresentation;
  import org.jkiss.dbeaver.ui.controls.resultset.view.StatisticsPresentation;
 +import org.jkiss.dbeaver.ui.css.CSSUtils;
 +import org.jkiss.dbeaver.ui.css.DBStyles;
  import org.jkiss.dbeaver.ui.data.IValueController;
  import org.jkiss.dbeaver.ui.dialogs.ConfirmationDialog;
- import org.jkiss.dbeaver.ui.editors.EditorUtils;
+ import org.jkiss.dbeaver.ui.editors.TextEditorUtils;
  import org.jkiss.dbeaver.ui.editors.object.struct.EditConstraintPage;
  import org.jkiss.dbeaver.ui.editors.object.struct.EditDictionaryPage;
  import org.jkiss.dbeaver.ui.preferences.PrefPageDataFormat;
```

## Relevant final code in the merge

```java
import org.jkiss.dbeaver.ui.editors.TextEditorUtils;
```

The merged file uses `TextEditorUtils` instead of `EditorUtils` wherever `EditorUtils` was previously referenced in `ResultSetViewer`.

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:

**1 line** (the import substitution resolving the Rename_Class conflict; this is a surgical, file-specific replacement, not a large-scale namespace migration)

## What each side had

**Parent 1** imported `org.jkiss.dbeaver.ui.editors.EditorUtils` and used it in `ResultSetViewer`.

**Parent 2** renamed `EditorUtils` to `TextEditorUtils` (a Rename_Class refactoring), updating the import in `ResultSetViewer` to `org.jkiss.dbeaver.ui.editors.TextEditorUtils`.

## Interpretation

This is a **Rename_Class** refactoring case. Parent 2 renamed `EditorUtils` to `TextEditorUtils`, a targeted, surgical rename: only this specific import in `ResultSetViewer` is affected in this file's diff, distinguishing it from a broad namespace migration. The conflict arises because P1 still references the old name. The merge resolves it by adopting P2's renamed import. This is a well-supported, defensible case: the rename is specific to a single class (`EditorUtils` → `TextEditorUtils`), it is an import-level signal confirmed by structural context (the import is replacing the old class name with a new one in the same package), and it is isolated — not part of dozens of files uniformly shifting packages.

## Complete diff

```diff
diff --cc plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/controls/resultset/ResultSetFilterPanel.java
index 0d6421f2c8,1057275b9f..712756f9dd
--- a/plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/controls/resultset/ResultSetFilterPanel.java
+++ b/plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/controls/resultset/ResultSetFilterPanel.java
@@@ -59,16 -62,7 +62,9 @@@ import org.jkiss.dbeaver.runtime.ui.UIS
  import org.jkiss.dbeaver.ui.*;
  import org.jkiss.dbeaver.ui.controls.StyledTextContentAdapter;
  import org.jkiss.dbeaver.ui.controls.StyledTextUtils;
+ import org.jkiss.utils.CommonUtils;
 +import org.jkiss.dbeaver.ui.css.CSSUtils;
 +import org.jkiss.dbeaver.ui.css.DBStyles;
- import org.jkiss.dbeaver.ui.editors.StringEditorInput;
- import org.jkiss.dbeaver.ui.editors.SubEditorSite;
- import org.jkiss.dbeaver.ui.editors.sql.SQLEditorBase;
- import org.jkiss.dbeaver.ui.editors.sql.handlers.OpenHandler;
- import org.jkiss.dbeaver.ui.editors.sql.syntax.SQLContextInformer;
- import org.jkiss.dbeaver.ui.editors.sql.syntax.SQLWordPartDetector;
- import org.jkiss.dbeaver.utils.GeneralUtils;
- import org.jkiss.utils.CommonUtils;
 
  import java.util.ArrayList;
  import java.util.Collection;
diff --cc plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/controls/resultset/ResultSetViewer.java
index 88d3ce9b45,8d79e406d0..7d65259dc7
--- a/plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/controls/resultset/ResultSetViewer.java
+++ b/plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/controls/resultset/ResultSetViewer.java
@@@ -85,11 -86,9 +86,11 @@@ import org.jkiss.dbeaver.ui.controls.re
  import org.jkiss.dbeaver.ui.controls.resultset.valuefilter.FilterValueEditPopup;
  import org.jkiss.dbeaver.ui.controls.resultset.view.EmptyPresentation;
  import org.jkiss.dbeaver.ui.controls.resultset.view.StatisticsPresentation;
 +import org.jkiss.dbeaver.ui.css.CSSUtils;
 +import org.jkiss.dbeaver.ui.css.DBStyles;
  import org.jkiss.dbeaver.ui.data.IValueController;
  import org.jkiss.dbeaver.ui.dialogs.ConfirmationDialog;
- import org.jkiss.dbeaver.ui.editors.EditorUtils;
+ import org.jkiss.dbeaver.ui.editors.TextEditorUtils;
  import org.jkiss.dbeaver.ui.editors.object.struct.EditConstraintPage;
  import org.jkiss.dbeaver.ui.editors.object.struct.EditDictionaryPage;
  import org.jkiss.dbeaver.ui.preferences.PrefPageDataFormat;
diff --cc plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/editors/entity/properties/TabbedFolderPageForm.java
index 48396dbdd7,5e04f193db..d42d6f05c0
--- a/plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/editors/entity/properties/TabbedFolderPageForm.java
+++ b/plugins/org.jkiss.dbeaver.core/src/org/jkiss/dbeaver/ui/editors/entity/properties/TabbedFolderPageForm.java
@@@ -58,20 -46,12 +58,14 @@@ import org.jkiss.dbeaver.model.preferen
  import org.jkiss.dbeaver.model.runtime.DBRProgressMonitor;
  import org.jkiss.dbeaver.model.runtime.load.DatabaseLoadService;
  import org.jkiss.dbeaver.model.struct.DBSObject;
- import org.jkiss.dbeaver.registry.editor.EntityEditorsRegistry;
+ import org.jkiss.dbeaver.registry.ObjectManagerRegistry;
  import org.jkiss.dbeaver.runtime.properties.ObjectPropertyDescriptor;
- import org.jkiss.dbeaver.ui.ActionUtils;
- import org.jkiss.dbeaver.ui.DBeaverIcons;
- import org.jkiss.dbeaver.ui.ICustomActionsProvider;
- import org.jkiss.dbeaver.ui.IRefreshablePart;
- import org.jkiss.dbeaver.ui.LoadingJob;
- import org.jkiss.dbeaver.ui.UIIcon;
- import org.jkiss.dbeaver.ui.UIUtils;
- import org.jkiss.dbeaver.ui.actions.navigator.NavigatorHandlerObjectOpen;
+ import org.jkiss.dbeaver.ui.*;
+ import org.jkiss.dbeaver.ui.navigator.actions.NavigatorHandlerObjectOpen;
  import org.jkiss.dbeaver.ui.controls.ObjectEditorPageControl;
  import org.jkiss.dbeaver.ui.controls.folders.TabbedFolderPage;
 +import org.jkiss.dbeaver.ui.css.CSSUtils;
 +import org.jkiss.dbeaver.ui.css.DBStyles;
  import org.jkiss.dbeaver.ui.editors.IDatabaseEditorInput;
  import org.jkiss.dbeaver.ui.editors.entity.EntityEditor;
  import org.jkiss.dbeaver.utils.GeneralUtils;
```
