# Project Plan: Enhancing the Log Viewer System

<style>
table {
    width: 100%;
    border-collapse: collapse;
}

th {
    background-color: #444; 
    color: white;
    padding: 10px;
    text-align: left;
}

td {
    background-color: white;
    color: black;
    padding: 8px;
    border: 1px solid #ddd;
}
</style>

## Overview
This document describes the new features and required components for enhancing the existing log viewer system.

## New Features to Implement

### **Startup Behavior**
| Action | Description |
|--------|-------------|
| Read `monitored_objects` table | Retrieve relevant objects to be displayed |
| Create web components | Instantiate components for each monitored object |
| Insert components | Arrange components in execution order |

### **Web Component Behavior**
| Condition | Action |
|------------|----------|
| Initial state | Set all components to **white** |
| When running | Change components to **yellow** |
| On failure | Turn the component **red** and halt all tests |

### **Test Completion**
| Button | Function |
|--------|----------|
| **Run Next Test** | Runs the next test in sequence |
| **Run This Test Again** | Repeats the current test |
| **Run Previous Test** | Runs the previous test |
| **Run The 1st Test** | Runs the first test |
| **Run All Tests** | Runs all tests sequentially |

### **Before Running the Next Test**
| Action | Description |
|--------|-------------|
| Clear previous web components | Remove test results from the display |

### **Additional Feature**
| Feature | Description |
|---------|-------------|
| **Python Output Box** | Displays the output of the Python script orchestrating the tests |

---

## Objects Required for Implementation

### **1. Existing Objects to Reuse**
The following objects are already part of the system and will be reused or extended:

| Object | Description |
|--------|-------------|
| **LogViewer** | Displays logs in real-time |
| **LogObject** | Represents an individual log entry |
| **LogObjectContainer & LogObjectProcessor** | Handle log collection and processing |
| **LogObjectContainerSource** | Retrieves logs from the database or a file |
| **MonitoredObject** | Represents an object under test and tracks logs and status |
| **MonitorLed** | Controls pass/fail/running colors |
| **MonitoredObjectsTableSelector** | Queries the monitored objects table |
| **MonitoredObjectsTableInserter** | Inserts monitored objects into the table |
| **MonitoredObjectsTableUpdater** | Updates monitored object data |
| **TableManager** | Manages the monitored objects table |
| **Accordion Component** | Used to display monitored objects in an expandable format |

---

### **2. New Objects Required**
New objects or major extensions needed:

| Object | Description |
|--------|-------------|
| **TestOrchestrator** | Controls test execution, UI updates, and failure handling |
| **TestControlButtons** | Provides the five test control buttons |
| **PythonScriptOutput** | Displays real-time Python script output |

---

## **Implementation Steps**

| Step | Description |
|------|-------------|
| 1 | Implement `TestOrchestrator` to handle test orchestration logic |
| 2 | Modify `MonitorLed` to support white/yellow/red status changes |
| 3 | Create `TestControlButtons` and link button clicks to `TestOrchestrator` |
| 4 | Implement `PythonScriptOutput` to capture script output |
| 5 | Ensure `LogViewer` and `MonitoredObject` integrate seamlessly |
| 6 | Test the entire workflow from monitored object retrieval to UI updates |

---

## **Final Object List**

### **Reused Objects (with minor modifications)**
| Object |
|--------|
| LogViewer |
| LogObject |
| LogObjectContainer |
| LogObjectProcessor |
| LogObjectContainerSource |
| MonitoredObject |
| MonitorLed |
| MonitoredObjectsTableSelector |
| MonitoredObjectsTableInserter |
| MonitoredObjectsTableUpdater |
| TableManager |
| **Accordion Component** |

### **New or Extended Objects**
| Object |
|--------|
| **TestOrchestrator** (or `TestFlowController`) |
| **TestControlButtons** |
| **PythonScriptOutput** |

---

This document should be used to guide the AI orchestration of the new log viewer system.
