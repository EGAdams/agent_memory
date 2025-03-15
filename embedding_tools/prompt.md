# Project Plan
We are enhancing the log viewer system that we already have.  We already have many of the web components and code working but we want to start to add new features.
## What we want to add:
- When the web page starts up:
  - Read the monitored objects table to get the relevant objects that need to be viewed.
  - Create a web component for each object.
  - Insert the web components in the order they should be run.

- Web component behavior:
  - Initially, set all components to white.
  - Change them to yellow when they are running.
  - If a component fails:
    - Turn it red.
    - Halt all testing.

- After the test is finished, provide five buttons:
  - **Run Next Test**
  - **Run This Test Again**
  - **Run Previous Test**
  - **Run The 1st Test**
  - **Run All Tests**

- Before running the next test:
  - Ensure that the web components from the last test are cleared from the display.

- Additional feature:
  - A text box below should display the output of the Python script orchestrating all of the tests.

# Your Task
List all of the objects needed to create this new system.  Use the existing objects and Interfaces where ever possible.  For example, we have an accordion component that should be used for each row that is pulled from the table and has log information in it.
