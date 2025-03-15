# Log Viewer System Enhancement - Project Plan

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
We are enhancing the log viewer system by adding new features. This document outlines the required objects, behaviors, and workflow for the enhancement.

## Features to Add

### **Web Page Startup Behavior**
| Action | Description |
|--------|-------------|
| Read `monitored_objects` table | Retrieve relevant objects that need to be viewed |
| Create web components | Instantiate components for each monitored object |
| Insert components | Arrange components in execution order |

### **Web Component Behavior**
| Condition | Action |
|------------|----------|
| Initial state | Set all components to **white** |
| When running | Change components to **yellow** |
| On failure | Turn the component **red** and halt all testing |

### **Post-Test Actions**
| Button | Function |
|--------|----------|
| **Run Next Test** | Runs the next test in sequence |
| **Run This Test Again** | Repeats the current test |
| **Run Previous Test** | Runs the previous test |
| **Run The 1st Test** | Runs the first test |
| **Run All Tests** | Runs all tests sequentially |

### **Additional Features**
| Feature | Description |
|---------|-------------|
| **Clear previous test data** | Ensure that previous web components are removed before running a new test |
| **Python Output Box** | Displays the output of the Python script orchestrating the tests |

---

## Objects Required

### **1. Existing Objects (Reused)**
| Object | Description |
|--------|-------------|
| `LogViewer` | Displays logs and monitored object data |
| `ILogObject` | Interface for log objects |
| `LogObject` | Web component for individual logs |
| `MonitoredObject` | Manages monitored objects |
| `MonitoredObjectsTableSelector` | Selects objects from the database |
| `MonitoredObjectsTableUpdater` | Updates table after tests |
| `MonitorLed` | Shows test status (white/yellow/red) |
| `LogObjectContainer` | Stores log objects |
| `LogObjectProcessor` | Handles queued log objects |
| `MonitoredObjectsTableInserter` | Inserts new objects |
| `Model` | Manages data access |
| `AccordionComponent` | Displays monitored object details |

### **2. New Objects to Create**
| Object | Description |
|--------|-------------|
| `TestController` | Orchestrates test runs and reads monitored objects table |
| `TestRunner` | Executes tests, updates component colors, and handles errors |
| `TestNavigator` | Provides test control buttons (Run Next, Previous, All, etc.) |
| `PythonScriptOutputViewer` | Displays real-time Python script outputs |
| `TestStateController` | Manages test states (Idle, Running, Halted, Passed) |

---

## System Initialization Flow

| Step | Description |
|------|-------------|
| 1 | `TestStateController` initializes |
| 2 | `TestRunner` reads monitored objects via `MonitoredObjectsTableSelector` |
| 3 | Each monitored object instantiates: a `LogViewer` component and a `MonitorLed` object (initially white) |
| 4 | Components are inserted using existing accordion UI components |

## Runtime Logic

| Condition | Action |
|------------|----------|
| Test starts | Change web components to **yellow** |
| Test fails | Change color to **red** and halt tests |
| Test completes | Enable button actions via `TestNavigator` and display logs in `PythonScriptOutputViewer` |

---

## Object Responsibilities Summary

| Object Name                     | Responsibility                                      | Status  |
|----------------------------------|-----------------------------------------------------|---------|
| `LogViewer`                     | Displays logs and monitored object data.           | ✅ Existing |
| `MonitorLed`                     | Shows component test status colors.                | ✅ Existing |
| `TestStateController`            | Manages test states (Idle, Running, Halted, Passed).| 🟢 New |
| `TestRunner`                     | Runs tests, updates status, and triggers events.   | 🟢 New |
| `TestNavigator`                  | UI buttons to control test flow.                   | 🟢 New |
| `PythonScriptOutputViewer`        | Displays Python logs from test execution.          | 🟢 New |
| `AccordionComponent`              | Displays monitored object logs/details.            | ✅ Existing |
| `MonitoredObjectsTableSelector`   | Selects objects from the database.                 | ✅ Existing |
| `LogObjectProcessor`              | Processes and manages log objects.                 | ✅ Existing |
| `LogObjectContainer`              | Stores and manages log objects.                    | ✅ Existing |

---

## Recommended Patterns

| Pattern | Purpose |
|---------|---------|
| **State Pattern** | Handles transitions between test states |
| **Command Pattern** | Implements test-run button behavior |
| **Observer Pattern** | Ensures real-time log updates |

---

This document provides a structured plan to build the enhanced Log Viewer system using existing and new objects.
