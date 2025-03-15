# Project Plan: Enhancing the Log Viewer System

## Overview
This document describes the new features and required components for enhancing the existing log viewer system.

## New Features to Implement

1. **Startup Behavior:**
   - Read the `monitored_objects` table to retrieve relevant objects.
   - Create a web component for each monitored object.
   - Insert web components in the correct execution order.

2. **Web Component Behavior:**
   - Initially, set all components to **white**.
   - Change components to **yellow** when they start running.
   - If a component fails:
     - Turn it **red**.
     - Halt all testing.

3. **Test Completion:**
   - Provide five test control buttons:
     - **Run Next Test**
     - **Run This Test Again**
     - **Run Previous Test**
     - **Run The 1st Test**
     - **Run All Tests**

4. **Before Running the Next Test:**
   - Clear the previous web components from the display.

5. **Additional Feature:**
   - A text box below should display the output of the Python script orchestrating the tests.

---

## Objects Required for Implementation

### **1. Existing Objects to Reuse**
The following objects are already part of the system and will be reused or extended:

- **LogViewer**  
  - Displays logs in real-time.

- **LogObject**  
  - Represents an individual log entry.

- **LogObjectContainer** & **LogObjectProcessor**  
  - Handle log collection and processing.

- **LogObjectContainerSource**  
  - Retrieves logs from the database or a file.

- **MonitoredObject**  
  - Represents an object under test and tracks logs and status.

- **MonitorLed**  
  - Controls pass/fail/running colors.

- **MonitoredObjectsTableSelector**, **MonitoredObjectsTableInserter**, **MonitoredObjectsTableUpdater**  
  - Query, insert, and update monitored objects in the database.

- **TableManager**  
  - Manages the monitored objects table.

- **Accordion Component**  
  - Used to display monitored objects in an expandable format.

---

### **2. New Objects Required**
New objects or major extensions needed:

#### **TestOrchestrator**  
- Responsible for:
  - Querying `monitored_objects` on startup.
  - Creating and ordering UI components.
  - Managing test flow and color changes (white → yellow → red/green).
  - Halting tests on failure.
  - Clearing old test components before running a new test.
  - Hooking up test control buttons.

#### **TestControlButtons**  
- Provides five control buttons:
  - **Run Next Test**
  - **Run This Test Again**
  - **Run Previous Test**
  - **Run The 1st Test**
  - **Run All Tests**
- Calls back into `TestOrchestrator` to execute tests.

#### **PythonScriptOutput**  
- Displays real-time Python script output in a text box or console area.

---

## **Implementation Steps**
1. Implement `TestOrchestrator` to handle test orchestration logic.
2. Modify `MonitorLed` to support white/yellow/red status changes.
3. Create `TestControlButtons` and link button clicks to `TestOrchestrator`.
4. Implement `PythonScriptOutput` to capture script output.
5. Ensure `LogViewer` and `MonitoredObject` integrate seamlessly.
6. Test the entire workflow from monitored object retrieval to UI updates.

---

## **Final Object List**
1. **Reused Objects (with minor modifications)**
   - `LogViewer`
   - `LogObject`
   - `LogObjectContainer`, `LogObjectProcessor`, `LogObjectContainerSource`
   - `MonitoredObject`
   - `MonitorLed`
   - `MonitoredObjectsTableSelector`, `MonitoredObjectsTableInserter`, `MonitoredObjectsTableUpdater`
   - `TableManager`
   - **Accordion Component**

2. **New or Extended Objects**
   - **TestOrchestrator** (or `TestFlowController`)
   - **TestControlButtons**
   - **PythonScriptOutput`

---

This document should be used to guide the AI orchestration of the new log viewer system.
