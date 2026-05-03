# Case 2 — Project: druid — Merge commit SHA1: 8bc56cefcc17b94e3ccde4dab9b288f7b7af1f73

## Modified file(s):
- `src/main/java/com/alibaba/druid/sql/ast/statement/SQLAlterTableStatement.java`
- `src/main/java/com/alibaba/druid/sql/dialect/mysql/ast/statement/MySqlAlterTableStatement.java`
- `src/main/java/com/alibaba/druid/sql/dialect/oracle/ast/stmt/OracleAlterTableAddColumn.java`
- `src/main/java/com/alibaba/druid/sql/dialect/oracle/ast/stmt/OracleAlterTableStatement.java`
- `src/main/java/com/alibaba/druid/sql/dialect/oracle/visitor/OracleASTVisitor.java`
- `src/main/java/com/alibaba/druid/sql/dialect/oracle/visitor/OracleASTVisitorAdapter.java`
- `src/main/java/com/alibaba/druid/sql/dialect/oracle/visitor/OracleOutputVisitor.java`
- `src/main/java/com/alibaba/druid/sql/dialect/oracle/visitor/OracleSchemaStatVisitor.java`
- `src/main/java/com/alibaba/druid/sql/visitor/SQLASTOutputVisitor.java`
- `src/main/java/com/alibaba/druid/sql/visitor/SQLASTVisitor.java`
- `src/main/java/com/alibaba/druid/sql/visitor/SQLASTVisitorAdapter.java`
- `src/main/java/com/alibaba/druid/sql/visitor/SchemaStatVisitor.java`

## Class(es) modified in the merge:
- `SQLAlterTableStatement`
- `MySqlAlterTableStatement`
- `OracleAlterTableAddColumn`
- `OracleAlterTableStatement`

## Merge effort lines in the combined diff

```diff
diff --cc src/main/java/com/alibaba/druid/sql/ast/statement/SQLAlterTableStatement.java
@@@ -28,4 -28,4 +29,14 @@@
++    public SQLName getName() {
++        if (getTableSource() == null) {
++            return null;
++        }
++        return (SQLName) getTableSource().getExpr();
++    }
++
++    public void setName(SQLName name) {
++        this.setTableSource(new SQLExprTableSource(name));
++    }

diff --cc src/main/java/com/alibaba/druid/sql/dialect/mysql/ast/statement/MySqlAlterTableStatement.java
@@@ -1,8 -1,8 +1,24 @@@
--public class MySqlAlterTableStatement extends MySqlStatementImpl {
++public class MySqlAlterTableStatement extends SQLAlterTableStatement {

++    @Override
++    protected void accept0(SQLASTVisitor visitor) {
++        if (visitor instanceof MySqlASTVisitor) {
++            accept0((MySqlASTVisitor) visitor);
++        } else {
++            throw new IllegalArgumentException("not support visitor type : " + visitor.getClass().getName());
++        }
++    }
++    
++    public void accept0(MySqlASTVisitor visitor) {
++        throw new UnsupportedOperationException(this.getClass().getName());
++    }

diff --cc src/main/java/com/alibaba/druid/sql/dialect/oracle/ast/stmt/OracleAlterTableAddColumn.java
@@@ -3,17 -3,17 +3,19 @@@
++import com.alibaba.druid.sql.ast.SQLObjectImpl;
++import com.alibaba.druid.sql.ast.statement.SQLAlterTableItem;
  import com.alibaba.druid.sql.ast.statement.SQLColumnDefinition;
--import com.alibaba.druid.sql.dialect.oracle.visitor.OracleASTVisitor;
++import com.alibaba.druid.sql.visitor.SQLASTVisitor;

--public class OracleAlterTableAddColumn extends OracleAlterTableItem {
++public class OracleAlterTableAddColumn extends SQLObjectImpl implements SQLAlterTableItem {

++    @Override
--    public void accept0(OracleASTVisitor visitor) {
++    protected void accept0(SQLASTVisitor visitor) {
          if (visitor.visit(this)) {
              acceptChild(visitor, columns);
          }

diff --cc src/main/java/com/alibaba/druid/sql/dialect/oracle/ast/stmt/OracleAlterTableStatement.java
@@@ -1,8 -1,8 +1,6 @@@
--import com.alibaba.druid.sql.ast.SQLName;
  import com.alibaba.druid.sql.ast.statement.SQLAlterTableStatement;
--import com.alibaba.druid.sql.ast.statement.SQLExprTableSource;
  ...
@@@ -41,15 -41,15 +39,4 @@@
--    public SQLName getName() {
--        if (getTableSource() == null) {
--            return null;
--        }
--        return (SQLName) getTableSource().getExpr();
--    }
--
--    public void setName(SQLName name) {
--        this.setTableSource(new SQLExprTableSource(name));
--    }

diff --cc src/main/java/com/alibaba/druid/sql/dialect/oracle/visitor/OracleASTVisitor.java
@@@ -473,10 -473,10 +473,6 @@@
--    boolean visit(OracleAlterTableAddColumn x);
--    void endVisit(OracleAlterTableAddColumn x);

diff --cc src/main/java/com/alibaba/druid/sql/visitor/SQLASTOutputVisitor.java
++import com.alibaba.druid.sql.dialect.oracle.ast.stmt.OracleAlterTableAddColumn;
++    public boolean visit(OracleAlterTableAddColumn x) { ... }
++    public void endVisit(OracleAlterTableAddColumn x) { ... }

diff --cc src/main/java/com/alibaba/druid/sql/visitor/SQLASTVisitor.java
++    boolean visit(OracleAlterTableAddColumn x);
++    void endVisit(OracleAlterTableAddColumn x);
```

## Relevant final code in the merge

```java
// SQLAlterTableStatement.java – getName()/setName() pulled up from OracleAlterTableStatement
public class SQLAlterTableStatement extends SQLStatementImpl implements SQLDDLStatement {
    public SQLName getName() {
        if (getTableSource() == null) return null;
        return (SQLName) getTableSource().getExpr();
    }
    public void setName(SQLName name) {
        this.setTableSource(new SQLExprTableSource(name));
    }
}

// MySqlAlterTableStatement.java – parent class changed from MySqlStatementImpl to SQLAlterTableStatement
public class MySqlAlterTableStatement extends SQLAlterTableStatement {
    @Override
    protected void accept0(SQLASTVisitor visitor) {
        if (visitor instanceof MySqlASTVisitor) {
            accept0((MySqlASTVisitor) visitor);
        } else {
            throw new IllegalArgumentException(...);
        }
    }
}

// OracleAlterTableAddColumn.java – parent class changed from OracleAlterTableItem to SQLObjectImpl+SQLAlterTableItem
public class OracleAlterTableAddColumn extends SQLObjectImpl implements SQLAlterTableItem {
    @Override
    protected void accept0(SQLASTVisitor visitor) { ... }
}
```

## Number of merge-effort lines (++ and --) associated with the refactoring types under analysis:
32 lines

## What each side had

**Parent 1 (P1)** had:
- `getName()`/`setName()` methods only in `OracleAlterTableStatement` (not in the common base `SQLAlterTableStatement`)
- `MySqlAlterTableStatement extends MySqlStatementImpl` (no common `SQLAlterTableStatement` parent)
- `OracleAlterTableAddColumn extends OracleAlterTableItem` with an `OracleASTVisitor`-typed `accept0`
- `OracleASTVisitor` interface declared `visit(OracleAlterTableAddColumn)` and `endVisit(OracleAlterTableAddColumn)`

**Parent 2 (P2)** performed several refactorings before the merge:
- **Pull_Up_Attribute / Pull_Up_Method:** Moved `getName()`/`setName()` from `OracleAlterTableStatement` up to `SQLAlterTableStatement` (the common base)
- **Pull_Up_Attribute:** Changed `MySqlAlterTableStatement` to extend `SQLAlterTableStatement` instead of `MySqlStatementImpl`
- **Change_Parameter_Type:** Changed `OracleAlterTableAddColumn.accept0()` parameter from `OracleASTVisitor` to the common `SQLASTVisitor`, and removed its Oracle-specific visitor methods from `OracleASTVisitor`

These three changes all took place in P2 before the merge. The merge had to reconcile which visitor interface (`OracleASTVisitor` vs `SQLASTVisitor`) and which parent class (`MySqlStatementImpl` vs `SQLAlterTableStatement`, and `OracleAlterTableItem` vs `SQLObjectImpl+SQLAlterTableItem`) to adopt. The `++` and `--` lines across the visitor adapters, visitor interfaces, and class declarations confirm the merge effort.

## Interpretation

**Refactoring types evidenced:** `Pull_Up_Attribute` (for `getName`/`setName`), `Pull_Up_Attribute` (for `MySqlAlterTableStatement` parent class change), `Change_Parameter_Type` (for `accept0` in `OracleAlterTableAddColumn`)

The three changes are structurally related and all reflect an inheritance-restructuring refactoring introduced in P2. The merge effort is confirmed by the `--` lines removing the old declarations (duplicate `getName`/`setName` in `OracleAlterTableStatement`, `MySqlStatementImpl` as parent, `OracleASTVisitor` as `accept0` parameter type) and the `++` lines introducing the merged resolution adopting P2's generalized version. The case is well-supported across multiple files with clear parent-context lines establishing which side introduced each change.

## Complete diff

```diff
diff --cc src/main/java/com/alibaba/druid/sql/ast/statement/SQLAlterTableStatement.java
index e9ac4bc66,e9ac4bc66..777649f2f
--- a/src/main/java/com/alibaba/druid/sql/ast/statement/SQLAlterTableStatement.java
+++ b/src/main/java/com/alibaba/druid/sql/ast/statement/SQLAlterTableStatement.java
@@@ -3,6 -3,6 +3,7 @@@
  import java.util.ArrayList;
  import java.util.List;
  
++import com.alibaba.druid.sql.ast.SQLName;
  import com.alibaba.druid.sql.ast.SQLStatementImpl;
  
  public class SQLAlterTableStatement extends SQLStatementImpl implements SQLDDLStatement {
@@@ -28,4 -28,4 +29,14 @@@
      public void setTableSource(SQLExprTableSource tableSource) {
          this.tableSource = tableSource;
      }
  
++    public SQLName getName() {
++        if (getTableSource() == null) {
++            return null;
++        }
++        return (SQLName) getTableSource().getExpr();
++    }
++
++    public void setName(SQLName name) {
++        this.setTableSource(new SQLExprTableSource(name));
++    }
  }

diff --cc src/main/java/com/alibaba/druid/sql/dialect/mysql/ast/statement/MySqlAlterTableStatement.java
index 243056905,243056905..865d0b347
--- a/src/main/java/com/alibaba/druid/sql/dialect/mysql/ast/statement/MySqlAlterTableStatement.java
+++ b/src/main/java/com/alibaba/druid/sql/dialect/mysql/ast/statement/MySqlAlterTableStatement.java
@@@ -1,8 -1,8 +1,24 @@@
  package com.alibaba.druid.sql.dialect.mysql.ast.statement;
  
++import com.alibaba.druid.sql.ast.statement.SQLAlterTableStatement;
++import com.alibaba.druid.sql.dialect.mysql.visitor.MySqlASTVisitor;
++import com.alibaba.druid.sql.visitor.SQLASTVisitor;
  
--public class MySqlAlterTableStatement extends MySqlStatementImpl {
++public class MySqlAlterTableStatement extends SQLAlterTableStatement {
  
      private static final long serialVersionUID = 1L;
  
++    @Override
++    protected void accept0(SQLASTVisitor visitor) {
++        if (visitor instanceof MySqlASTVisitor) {
++            accept0((MySqlASTVisitor) visitor);
++        } else {
++            throw new IllegalArgumentException("not support visitor type : " + visitor.getClass().getName());
++        }
++    }
++    
++    public void accept0(MySqlASTVisitor visitor) {
++        throw new UnsupportedOperationException(this.getClass().getName());
++    }
  }

diff --cc src/main/java/com/alibaba/druid/sql/dialect/oracle/ast/stmt/OracleAlterTableAddColumn.java
index 32c659dd2,32c659dd2..6fb45a6ff
--- a/src/main/java/com/alibaba/druid/sql/dialect/oracle/ast/stmt/OracleAlterTableAddColumn.java
+++ b/src/main/java/com/alibaba/druid/sql/dialect/oracle/ast/stmt/OracleAlterTableAddColumn.java
@@@ -3,17 -3,17 +3,19 @@@
  import java.util.ArrayList;
  import java.util.List;
  
++import com.alibaba.druid.sql.ast.SQLObjectImpl;
++import com.alibaba.druid.sql.ast.statement.SQLAlterTableItem;
  import com.alibaba.druid.sql.ast.statement.SQLColumnDefinition;
--import com.alibaba.druid.sql.dialect.oracle.visitor.OracleASTVisitor;
++import com.alibaba.druid.sql.visitor.SQLASTVisitor;
  
--public class OracleAlterTableAddColumn extends OracleAlterTableItem {
++public class OracleAlterTableAddColumn extends SQLObjectImpl implements SQLAlterTableItem {
  
      private static final long         serialVersionUID = 1L;
      private List<SQLColumnDefinition> columns          = new ArrayList<SQLColumnDefinition>();
  
      @Override
--    public void accept0(OracleASTVisitor visitor) {
++    protected void accept0(SQLASTVisitor visitor) {
          if (visitor.visit(this)) {
              acceptChild(visitor, columns);
          }

diff --cc src/main/java/com/alibaba/druid/sql/dialect/oracle/ast/stmt/OracleAlterTableStatement.java
index 012d903bf,9a357bcb4..0c83ded0f
@@@ -1,8 -1,8 +1,6 @@@
  package com.alibaba.druid.sql.dialect.oracle.ast.stmt;
  
--import com.alibaba.druid.sql.ast.SQLName;
  import com.alibaba.druid.sql.ast.statement.SQLAlterTableStatement;
--import com.alibaba.druid.sql.ast.statement.SQLExprTableSource;
  import com.alibaba.druid.sql.dialect.oracle.visitor.OracleASTVisitor;
  ...
@@@ -41,15 -41,15 +39,4 @@@
--    public SQLName getName() {
--        if (getTableSource() == null) {
--            return null;
--        }
--        return (SQLName) getTableSource().getExpr();
--    }
--
--    public void setName(SQLName name) {
--        this.setTableSource(new SQLExprTableSource(name));
--    }
  }

diff --cc src/main/java/com/alibaba/druid/sql/dialect/oracle/visitor/OracleASTVisitor.java
@@@ -473,10 -473,10 +473,6 @@@
--    boolean visit(OracleAlterTableAddColumn x);
--    void endVisit(OracleAlterTableAddColumn x);

diff --cc src/main/java/com/alibaba/druid/sql/visitor/SQLASTOutputVisitor.java
++import com.alibaba.druid.sql.dialect.oracle.ast.stmt.OracleAlterTableAddColumn;
  ...
++    @Override
++    public boolean visit(OracleAlterTableAddColumn x) {
++        print("ADD (");
++        printAndAccept(x.getColumns(), ", ");
++        print(")");
++        return false;
++    }
++    @Override
++    public void endVisit(OracleAlterTableAddColumn x) { }

diff --cc src/main/java/com/alibaba/druid/sql/visitor/SQLASTVisitor.java
++    boolean visit(OracleAlterTableAddColumn x);
++    void endVisit(OracleAlterTableAddColumn x);

diff --cc src/main/java/com/alibaba/druid/sql/visitor/SQLASTVisitorAdapter.java
++    @Override
++    public boolean visit(OracleAlterTableAddColumn x) { return true; }
++    @Override
++    public void endVisit(OracleAlterTableAddColumn x) { }

diff --cc src/main/java/com/alibaba/druid/sql/visitor/SchemaStatVisitor.java
++    @Override
++    public boolean visit(OracleAlterTableAddColumn x) {
++        SQLAlterTableStatement stmt = (SQLAlterTableStatement) x.getParent();
++        String table = stmt.getName().toString();
++        for (SQLColumnDefinition column : x.getColumns()) {
++            String columnName = column.getName().toString();
++            addColumn(table, columnName);
++        }
++        return false;
++    }
++    @Override
++    public void endVisit(OracleAlterTableAddColumn x) { }
```
