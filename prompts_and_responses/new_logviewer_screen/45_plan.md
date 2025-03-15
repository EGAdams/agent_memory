# Log Viewer System Enhancement - Project Plan

## Overview
We are enhancing the log viewer system by adding new features. This document outlines the required objects, behaviors, and workflow for the enhancement.

## Features to Add

### Web Page Startup Behavior:
- Read the monitored objects table to get the relevant objects that need to be viewed.
- Create a web component for each object.
- Insert the web components in the order they should be run.

### Web Component Behavior:
- Initially, set all components to **white**.
- Change them to **yellow** when they are running.
- If a component fails:
  - Turn it **red**.
  - Halt all testing.

### Post-Test Actions:
- Provide five buttons:
  - **Run Next Test**
  - **Run This Test Again**
  - **Run Previous Test**
  - **Run The 1st Test**
  - **Run All Tests**
- Before running the next test, ensure that the web components from the last test are cleared from the display.
- A text box below should display the output of the Python script orchestrating all of the tests.

## Objects Required

### **Existing Objects (Reused)**
- `LogViewer` - Displays logs and monitored object data.
- `ILogObject` - Interface for log objects.
- `LogObject` - Web component for individual logs.
- `MonitoredObject` - Manages monitored objects.
- `MonitoredObjectsTableSelector` - Selects objects from the database.
- `MonitoredObjectsTableUpdater` - Updates table after tests.
- `MonitorLed` - Shows test status (white/yellow/red).
- `LogObjectContainer` - Stores log objects.
- `LogObjectProcessor` - Handles queued log objects.
- `MonitoredObjectsTableInserter` - Inserts new objects.
- `Model` - Manages data access.
- `AccordionComponent` - Displays monitored object details.

### **New Objects to Create**
1. `TestController`
   - Orchestrates test runs.
   - Reads monitored objects table.
   - Instantiates `TestRunner`.

2. `TestRunner`
   - Executes tests.
   - Changes component colors (white → yellow → red on failure).
   - Notifies `TestStateController` of test completion/errors.

3. `TestNavigator`
   - Provides user controls for:
     - **Run Next Test**
     - **Run This Test Again**
     - **Run Previous Test**
     - **Run The 1st Test**
     - **Run All Tests**
   - Invokes methods on `TestRunner`.

4. `PythonScriptOutputViewer`
   - Displays Python script outputs in real-time.

5. `TestStateController`
   - Manages test lifecycle states (Idle, Running, Failed, Passed).
   - Handles stopping of tests on failure.

## System Initialization Flow:
1. `TestStateController` initializes.
2. `TestRunner` reads monitored objects via `MonitoredObjectsTableSelector`.
3. Each monitored object instantiates:
   - A `LogViewer` component.
   - A `MonitorLed` object (initially white).
4. Components are inserted using existing accordion UI components.

## Runtime Logic:
- Tests begin, changing web components to **yellow**.
- On failure:
  - Change color to **red**.
  - Notify `TestStateController` to halt all tests.
- On test completion:
  - Provide button actions via `TestNavigator`.
  - Display Python script outputs in `PythonScriptOutputViewer`.

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
| `TestStateController`             | Handles test lifecycle and component transitions.  | 🟢 New |
| `LogObjectContainer`              | Stores and manages log objects.                    | ✅ Existing |

## Recommended Patterns:
- **State Pattern** → Handles transitions between test states.
- **Command Pattern** → Implements test-run button behavior.
- **Observer Pattern** → Ensures real-time log updates.

---

This document provides a structured plan to build the enhanced Log Viewer system using existing and new objects.
