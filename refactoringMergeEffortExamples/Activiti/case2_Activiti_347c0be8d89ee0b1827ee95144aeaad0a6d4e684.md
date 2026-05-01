# Case 2 — Project: Activiti — Merge commit SHA1: 347c0be8d89ee0b1827ee95144aeaad0a6d4e684

---

## Modified file(s):
- `modules/activiti-cxf/src/main/java/org/activiti/engine/impl/webservice/CxfWebServiceClient.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/bpmn/behavior/WebServiceActivityBehavior.java`
- `modules/activiti-engine/src/main/java/org/activiti/engine/impl/cfg/ProcessEngineConfigurationImpl.java` (via `ProcessEngineConfiguration`)

---

## Class(es) modified in the merge:
`CxfWebServiceClient`, `WebServiceActivityBehavior`, `ProcessEngineConfigurationImpl`

---

## Merge effort lines in the combined diff

In `CxfWebServiceClient.java` — method signature change:
```diff
++ public Object[] send(String methodName, Object[] arguments, java.util.concurrent.ConcurrentMap<QName,URL> overridenEndpointAddresses) throws Exception {
++     URL newEndpointAddress = null;
++     if (overridenEndpointAddresses != null) {
++         newEndpointAddress = overridenEndpointAddresses
++                    .get(this.client.getEndpoint().getEndpointInfo().getName());
++     }
++     if (newEndpointAddress != null) {
++         this.client.getRequestContext().put(Message.ENDPOINT_ADDRESS, newEndpointAddress.toExternalForm());
++     }
++     return client.invoke(methodName, arguments);
```

In `WebServiceActivityBehavior.java` — call site reconciliation:
```diff
++     ProcessEngineConfigurationImpl processEngineConfig = Context.getProcessEngineConfiguration();
++     MessageInstance receivedMessage = this.operation.sendMessage(message,
++         processEngineConfig.getWsOverridenEndpointAddresses());
++     String firstDataOutputName = this.ioSpecification.getFirstDataOutputName();
++     this.returnMessage(receivedMessage, execution);
```

In `ProcessEngineConfigurationImpl.java` — new field:
```diff
++ protected ConcurrentMap<QName, URL> wsOverridenEndpointAddresses = new ConcurrentHashMap<QName, URL>();
```

In test — call site:
```diff
++ processEngineConfiguration.addWsEndpointAddress(
```

---

## Relevant final code in the merge

```java
// CxfWebServiceClient.java
public Object[] send(String methodName, Object[] arguments,
    java.util.concurrent.ConcurrentMap<QName,URL> overridenEndpointAddresses) throws Exception {
    URL newEndpointAddress = null;
    if (overridenEndpointAddresses != null) {
        newEndpointAddress = overridenEndpointAddresses
            .get(this.client.getEndpoint().getEndpointInfo().getName());
    }
    if (newEndpointAddress != null) {
        this.client.getRequestContext().put(Message.ENDPOINT_ADDRESS, newEndpointAddress.toExternalForm());
    }
    return client.invoke(methodName, arguments);
}

// ProcessEngineConfigurationImpl.java
protected ConcurrentMap<QName, URL> wsOverridenEndpointAddresses = new ConcurrentHashMap<QName, URL>();

public ProcessEngineConfiguration addWsEndpointAddress(QName endpointName, URL address) {
    this.wsOverridenEndpointAddresses.put(endpointName, address);
    return this;
}
```

---

## Number of merge-effort lines (`++` and `--`) associated with the refactoring types under analysis:
**18 lines**

---

## What each side had

**Parent 1** had `CxfWebServiceClient.send(String methodName, Object[] arguments)` with only 2 parameters — no endpoint address override support. `WebServiceActivityBehavior` called `this.operation.sendMessage(message)` without any configuration context. No `wsOverridenEndpointAddresses` field existed anywhere.

**Parent 2** had introduced the 3-parameter version `send(String, Object[], ConcurrentMap<QName,URL>)` and the corresponding `wsOverridenEndpointAddresses` field in `ProcessEngineConfigurationImpl`, plus the `addWsEndpointAddress` API. However P2's implementation had a slightly different null-check logic and error handling structure for the endpoint address.

The merge had to reconcile P1's 2-parameter `send` with P2's 3-parameter version, synthesizing the final null-safe implementation.

---

## Interpretation

P2 performed a **Change_Parameter_Type** / parameter addition refactoring on `CxfWebServiceClient.send()` — adding `ConcurrentMap<QName,URL> overridenEndpointAddresses` as a new parameter. This caused a direct conflict with P1's 2-parameter signature, requiring the merge to produce `++` lines for the complete new signature and implementation.

The key refactoring types:

1. **Change_Parameter_Type** on `send()`: from `(String, Object[])` in P1 to `(String, Object[], ConcurrentMap<QName,URL>)` in P2. The `++` lines on the full new method signature and body are the merge effort to apply this change.

2. **Extract_Variable**: within the reconciled `send()` body, `URL newEndpointAddress = null` followed by a null-conditional assignment (lines `++`) represents the merge synthesizing a null-safe version that neither parent had in exactly this form — P1 had no such variable, P2 had it without the null guard on `overridenEndpointAddresses`.

3. **Extract_Attribute** on `ProcessEngineConfigurationImpl`: the `++` line `protected ConcurrentMap<QName, URL> wsOverridenEndpointAddresses` introduces a new field that P1 lacked, enabling the endpoint address override capability across the engine configuration.

4. Call site reconciliation in `WebServiceActivityBehavior` (lines `++`): `Context.getProcessEngineConfiguration()` replaces the P1 call `execution.getEngineServices().getProcessEngineConfiguration()`, threading the new `wsOverridenEndpointAddresses` parameter to `sendMessage`.


## Complete diff

```diff
diff --cc modules/activiti-cxf/src/main/java/org/activiti/engine/impl/webservice/CxfWebServiceClient.java
index e25c6e50a6,5fa7b7b6c9..1226dee866
--- a/modules/activiti-cxf/src/main/java/org/activiti/engine/impl/webservice/CxfWebServiceClient.java
+++ b/modules/activiti-cxf/src/main/java/org/activiti/engine/impl/webservice/CxfWebServiceClient.java
@@@ -16,12 -16,14 +16,15 @@@ import java.io.IOException
  import java.net.URL;
  import java.util.Arrays;
  import java.util.Enumeration;
 -import java.util.concurrent.ConcurrentMap;
  
+ import javax.xml.namespace.QName;
+ 
  import org.activiti.engine.ActivitiException;
 +import org.activiti.engine.delegate.BpmnError;
  import org.apache.cxf.endpoint.Client;
 +import org.apache.cxf.interceptor.Fault;
  import org.apache.cxf.jaxws.endpoint.dynamic.JaxWsDynamicClientFactory;
+ import org.apache.cxf.message.Message;
  import org.slf4j.Logger;
  import org.slf4j.LoggerFactory;
  
@@@ -63,16 -63,13 +66,25 @@@ public class CxfWebServiceClient implem
    /**
     * {@inheritDoc}}
     */
-   public Object[] send(String methodName, Object[] arguments) throws Exception {
 -  public Object[] send(String methodName, Object[] arguments, final ConcurrentMap<QName, URL> overridenEndpointAddresses) throws Exception {
 -    // If needed, we override the endpoint address
 -    final URL newEndpointAddress = overridenEndpointAddresses
 -             .get(this.client.getEndpoint().getEndpointInfo().getName());
 -    if (newEndpointAddress != null) {
 -       this.client.getRequestContext().put(Message.ENDPOINT_ADDRESS, newEndpointAddress.toExternalForm());
++  public Object[] send(String methodName, Object[] arguments, java.util.concurrent.ConcurrentMap<QName,URL> overridenEndpointAddresses) throws Exception {
 +    try {
-        return client.invoke(methodName, arguments);
++	    URL newEndpointAddress = null;
++	    if (overridenEndpointAddresses != null) {
++  	    newEndpointAddress = overridenEndpointAddresses
++               .get(this.client.getEndpoint().getEndpointInfo().getName());
++	    }
++	    
++    	if (newEndpointAddress != null) {
++       		this.client.getRequestContext().put(Message.ENDPOINT_ADDRESS, newEndpointAddress.toExternalForm());
++    	}
++    	return client.invoke(methodName, arguments);
 +    } catch (Fault e) {
 +       LOGGER.debug("Technical error calling WS", e);
 +       throw new ActivitiException(e.getMessage(), e);
 +    } catch (Exception e) {
 +       // Other exceptions should be associated to business fault defined in the service WSDL
 +       LOGGER.debug("Business error calling WS", e);
 +       throw new BpmnError(e.getClass().getName(), e.getMessage());
      }
 -    return client.invoke(methodName, arguments);
    }
  }
diff --cc modules/activiti-cxf/src/test/java/org/activiti/engine/impl/webservice/WebServiceTaskTest.java
index eec87e0153,d59766f093..a1301d1a75
--- a/modules/activiti-cxf/src/test/java/org/activiti/engine/impl/webservice/WebServiceTaskTest.java
+++ b/modules/activiti-cxf/src/test/java/org/activiti/engine/impl/webservice/WebServiceTaskTest.java
@@@ -15,15 -16,17 +16,17 @@@ import java.net.URL
  import java.util.Calendar;
  import java.util.Date;
  import java.util.HashMap;
 +import java.util.List;
  import java.util.Map;
  
+ import javax.xml.namespace.QName;
+ 
 -import org.activiti.engine.impl.test.PluggableActivitiTestCase;
 +import org.activiti.engine.ActivitiException;
 +import org.activiti.engine.history.HistoricProcessInstance;
  import org.activiti.engine.runtime.ProcessInstance;
  import org.activiti.engine.test.Deployment;
 -import org.apache.cxf.endpoint.Server;
 -import org.apache.cxf.interceptor.LoggingInInterceptor;
 -import org.apache.cxf.interceptor.LoggingOutInterceptor;
 -import org.apache.cxf.jaxws.JaxWsServerFactoryBean;
 +import org.apache.cxf.binding.soap.SoapFault;
 +import org.apache.cxf.interceptor.Fault;
  
  /**
   * An integration test for CXF based web services
@@@ -44,6 -71,22 +47,22 @@@ public class WebServiceTaskTest extend
          assertTrue(processInstance.isEnded());
      }
  
+     @Deployment
+     public void testWebServiceInvocationWithEndpointAddressConfigured() throws Exception {
+ 
+         assertEquals(-1, webServiceMock.getCount());
+ 
 -        processEngine.getProcessEngineConfiguration().addWsEndpointAddress(
++        processEngineConfiguration.addWsEndpointAddress(
+                 new QName("http://webservice.impl.engine.activiti.org/", "CounterImplPort"),
+                 new URL("http://localhost:63081/webservicemock"));
+ 
+         ProcessInstance processInstance = runtimeService.startProcessInstanceByKey("webServiceInvocation");
+         waitForJobExecutorToProcessAllJobs(10000L, 250L);
+ 
+         assertEquals(0, webServiceMock.getCount());
+         assertTrue(processInstance.isEnded());
+     }
+ 
      @Deployment
      public void testWebServiceInvocationDataStructure() throws Exception {
  
diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/bpmn/behavior/WebServiceActivityBehavior.java
index b0c7d8b299,21d2eed303..6da0d6b7b1
--- a/modules/activiti-engine/src/main/java/org/activiti/engine/impl/bpmn/behavior/WebServiceActivityBehavior.java
+++ b/modules/activiti-engine/src/main/java/org/activiti/engine/impl/bpmn/behavior/WebServiceActivityBehavior.java
@@@ -15,13 -15,12 +15,16 @@@ package org.activiti.engine.impl.bpmn.b
  import java.util.ArrayList;
  import java.util.List;
  
+ import org.activiti.engine.ProcessEngineConfiguration;
 +import org.activiti.engine.delegate.BpmnError;
  import org.activiti.engine.impl.bpmn.data.AbstractDataAssociation;
  import org.activiti.engine.impl.bpmn.data.IOSpecification;
  import org.activiti.engine.impl.bpmn.data.ItemInstance;
 +import org.activiti.engine.impl.bpmn.helper.ErrorPropagation;
  import org.activiti.engine.impl.bpmn.webservice.MessageInstance;
  import org.activiti.engine.impl.bpmn.webservice.Operation;
++import org.activiti.engine.impl.cfg.ProcessEngineConfigurationImpl;
++import org.activiti.engine.impl.context.Context;
  import org.activiti.engine.impl.pvm.delegate.ActivityExecution;
  
  /**
@@@ -61,54 -60,36 +64,60 @@@ public class WebServiceActivityBehavio
     */
    public void execute(ActivityExecution execution) throws Exception {
      MessageInstance message;
 -    
 -    if (ioSpecification != null) {
 -      this.ioSpecification.initialize(execution);
 -      ItemInstance inputItem = (ItemInstance) execution.getVariable(this.ioSpecification.getFirstDataInputName());
 -      message = new MessageInstance(this.operation.getInMessage(), inputItem);
 -    } else {
 -      message = this.operation.getInMessage().createInstance();
 -    }
 -    
 -    execution.setVariable(CURRENT_MESSAGE, message);
 -    
 -    this.fillMessage(message, execution);
--    
 -    ProcessEngineConfiguration processEngineConfig = execution.getEngineServices().getProcessEngineConfiguration();
 -    MessageInstance receivedMessage = this.operation.sendMessage(message, processEngineConfig.getWsOverridenEndpointAddresses());
 -
 -    execution.setVariable(CURRENT_MESSAGE, receivedMessage);
 -
 -    if (ioSpecification != null) {
 -      String firstDataOutputName = this.ioSpecification.getFirstDataOutputName();
 -      if (firstDataOutputName != null) {
 -        ItemInstance outputItem = (ItemInstance) execution.getVariable(firstDataOutputName);
 -        outputItem.getStructureInstance().loadFrom(receivedMessage.getStructureInstance().toArray());
++
 +    try {
-        if (ioSpecification != null) {
-          this.ioSpecification.initialize(execution);
-          ItemInstance inputItem = (ItemInstance) execution.getVariable(this.ioSpecification.getFirstDataInputName());
-          message = new MessageInstance(this.operation.getInMessage(), inputItem);
-        } else {
-          message = this.operation.getInMessage().createInstance();
-        }
-     
-        execution.setVariable(CURRENT_MESSAGE, message);
-     
-        this.fillMessage(message, execution);
-     
-        MessageInstance receivedMessage = this.operation.sendMessage(message);
- 
-        execution.setVariable(CURRENT_MESSAGE, receivedMessage);
- 
-        if (ioSpecification != null) {
-          String firstDataOutputName = this.ioSpecification.getFirstDataOutputName();
-          if (firstDataOutputName != null) {
-            ItemInstance outputItem = (ItemInstance) execution.getVariable(firstDataOutputName);
-            outputItem.getStructureInstance().loadFrom(receivedMessage.getStructureInstance().toArray());
-          }
-        }
-     
-        this.returnMessage(receivedMessage, execution);
-     
-        execution.setVariable(CURRENT_MESSAGE, null);
-        leave(execution);
++      if (ioSpecification != null) {
++        this.ioSpecification.initialize(execution);
++        ItemInstance inputItem = (ItemInstance) execution
++            .getVariable(this.ioSpecification.getFirstDataInputName());
++        message = new MessageInstance(this.operation.getInMessage(), inputItem);
++      } else {
++        message = this.operation.getInMessage().createInstance();
++      }
++
++      execution.setVariable(CURRENT_MESSAGE, message);
++
++      this.fillMessage(message, execution);
++
++      ProcessEngineConfigurationImpl processEngineConfig = Context.getProcessEngineConfiguration();
++      MessageInstance receivedMessage = this.operation.sendMessage(message,
++          processEngineConfig.getWsOverridenEndpointAddresses());
++
++      execution.setVariable(CURRENT_MESSAGE, receivedMessage);
++
++      if (ioSpecification != null) {
++        String firstDataOutputName = this.ioSpecification
++            .getFirstDataOutputName();
++        if (firstDataOutputName != null) {
++          ItemInstance outputItem = (ItemInstance) execution
++              .getVariable(firstDataOutputName);
++          outputItem.getStructureInstance().loadFrom(
++              receivedMessage.getStructureInstance().toArray());
++        }
++      }
++
++      this.returnMessage(receivedMessage, execution);
++
++      execution.setVariable(CURRENT_MESSAGE, null);
++      leave(execution);
 +    } catch (Exception exc) {
 +
-        Throwable cause = exc;
-        BpmnError error = null;
-        while (cause != null) {
-           if (cause instanceof BpmnError) {
-              error = (BpmnError) cause;
-              break;
-           }
-           cause = cause.getCause();
-        }
- 
-        if (error != null) {
-           ErrorPropagation.propagateError(error, execution);
-        } else {
-           throw exc;
-        }
++      Throwable cause = exc;
++      BpmnError error = null;
++      while (cause != null) {
++        if (cause instanceof BpmnError) {
++          error = (BpmnError) cause;
++          break;
++        }
++        cause = cause.getCause();
++      }
++
++      if (error != null) {
++        ErrorPropagation.propagateError(error, execution);
++      } else {
++        throw exc;
+       }
      }
 -    
 -    this.returnMessage(receivedMessage, execution);
 -    
 -    execution.setVariable(CURRENT_MESSAGE, null);
 -    leave(execution);
    }
    
    private void returnMessage(MessageInstance message, ActivityExecution execution) {
diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/cfg/ProcessEngineConfigurationImpl.java
index c59feab829,c59feab829..429f721b85
--- a/modules/activiti-engine/src/main/java/org/activiti/engine/impl/cfg/ProcessEngineConfigurationImpl.java
+++ b/modules/activiti-engine/src/main/java/org/activiti/engine/impl/cfg/ProcessEngineConfigurationImpl.java
@@@ -16,6 -16,6 +16,7 @@@ package org.activiti.engine.impl.cfg
  import java.io.InputStream;
  import java.io.InputStreamReader;
  import java.io.Reader;
++import java.net.URL;
  import java.sql.Connection;
  import java.sql.DatabaseMetaData;
  import java.sql.SQLException;
@@@ -32,9 -32,9 +33,12 @@@ import java.util.ServiceLoader
  import java.util.Set;
  import java.util.concurrent.ArrayBlockingQueue;
  import java.util.concurrent.BlockingQueue;
++import java.util.concurrent.ConcurrentHashMap;
++import java.util.concurrent.ConcurrentMap;
  
  import javax.naming.InitialContext;
  import javax.sql.DataSource;
++import javax.xml.namespace.QName;
  
  import org.activiti.bpmn.model.BpmnModel;
  import org.activiti.engine.ActivitiException;
@@@ -523,6 -523,6 +527,7 @@@ public abstract class ProcessEngineConf
    protected int historicProcessInstancesQueryLimit = 20000;
  
    protected String wsSyncFactoryClassName = DEFAULT_WS_SYNC_FACTORY;
++  protected ConcurrentMap<QName, URL> wsOverridenEndpointAddresses = new ConcurrentHashMap<QName, URL>();
  
    protected CommandContextFactory commandContextFactory;
    protected TransactionContextFactory transactionContextFactory;
@@@ -1904,6 -1904,6 +1909,34 @@@
      return this;
    }
    
++  /**
++   * Add or replace the address of the given web-service endpoint with the given value
++   * @param endpointName The endpoint name for which a new address must be set
++   * @param address The new address of the endpoint
++   */
++  public ProcessEngineConfiguration addWsEndpointAddress(QName endpointName, URL address) {
++      this.wsOverridenEndpointAddresses.put(endpointName, address);
++      return this;
++  }
++  
++  /**
++   * Remove the address definition of the given web-service endpoint
++   * @param endpointName The endpoint name for which the address definition must be removed
++   */
++  public ProcessEngineConfiguration removeWsEndpointAddress(QName endpointName) {
++      this.wsOverridenEndpointAddresses.remove(endpointName);
++      return this;
++  }
++  
++  public ConcurrentMap<QName, URL> getWsOverridenEndpointAddresses() {
++      return this.wsOverridenEndpointAddresses;
++  }
++  
++  public ProcessEngineConfiguration setWsOverridenEndpointAddresses(final ConcurrentMap<QName, URL> wsOverridenEndpointAdress) {
++    this.wsOverridenEndpointAddresses.putAll(wsOverridenEndpointAdress);
++    return this;
++  }
++  
    public Map<String, FormEngine> getFormEngines() {
      return formEngines;
    }
diff --cc modules/activiti-engine/src/main/java/org/activiti/engine/impl/webservice/WSOperation.java
index 80725e0eaa,93eba66ad3..22fe34accb
--- a/modules/activiti-engine/src/main/java/org/activiti/engine/impl/webservice/WSOperation.java
+++ b/modules/activiti-engine/src/main/java/org/activiti/engine/impl/webservice/WSOperation.java
@@@ -67,11 -72,15 +72,8 @@@ public class WSOperation implements Ope
      return message.getStructureInstance().toArray();
    }
    
-   private Object[] safeSend(Object[] arguments) throws Exception {
-     Object[] results = null;
- 
-     results = this.service.getClient().send(this.name, arguments);
- 
+   private Object[] safeSend(Object[] arguments, final ConcurrentMap<QName, URL> overridenEndpointAddresses) throws Exception {
 -    Object[] results = null;
 -    
 -    try {
 -      results = this.service.getClient().send(this.name, arguments, overridenEndpointAddresses);
 -    } catch (Exception e) {
 -      LOGGER.warn("Error calling WS {}", this.service.getName(), e);
 -    }
 -    
++    Object[] results = this.service.getClient().send(this.name, arguments, overridenEndpointAddresses);
      if (results == null) {
        results = new Object[] {};
      }
```