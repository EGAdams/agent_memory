To centralize the serve logic in your Tennis scoreboard controller, we can create a dedicated method in the `GameState` class that handles the serve switching based on the current game state, including whether it's a tiebreak or a regular game. This will allow us to eliminate the `serveSwitch` method and ensure that the serve logic is consistently applied throughout the codebase.

Here's how you can implement this:

1. **Create a method in `GameState` to handle serve switching.**
2. **Update the relevant parts of the code to call this new method instead of using `serveSwitch`.**

### Step 1: Create a Method in `GameState`

Add the following method to the `GameState` class:

```cpp
void GameState::updateServe() {
    if (getTieBreak() == 1) {
        // Handle tiebreak serve logic
        if (getServe() == 0) {
            setServe(1); // Player 2 serves first in tiebreak
        } else {
            // Alternate serves every two points
            // Logic to determine who serves next can be added here
            // For simplicity, we can just toggle for now
            setServe(0);
        }
    } else {
        // Regular game serve logic
        if (getServeSwitch() >= 1) {
            setServe(getServe() == 0 ? 1 : 0); // Toggle serve
            setServeSwitch(0); // Reset serve switch
        }
    }
    // Update the serve LED
    _serveLeds.updateServeLED();
}
```

### Step 2: Update the Code to Use the New Method

Now, replace the calls to `serveSwitch` in your code with calls to `updateServe`. Here are the relevant changes:

1. **In `ServeLeds::serveSwitch`**, remove the entire method since we will handle it in `GameState`.

2. **In `Mode1TieBreaker::tieBreakEnable`**, replace the call to `serveSwitch` with `updateServe`:

```cpp
_gameState->updateServe(); // Instead of _serveLeds.serveSwitch();
```

3. **In `Mode1Score::mode1P1Games`, `Mode1Score::mode1P2Games`, and other relevant methods**, replace the calls to `serveSwitch` with `updateServe`:

```cpp
_gameState->updateServe(); // Instead of _serveLeds.serveSwitch();
```

4. **In `GameModes::mode1`**, replace the call to `serveSwitch`:

```cpp
_gameState->updateServe(); // Instead of _serveLeds.serveSwitch();
```

### Final Code Snippet

Here’s how the updated `GameState` class might look with the new method:

```cpp
class GameState {
    // Existing members...

public:
    void updateServe() {
        if (getTieBreak() == 1) {
            // Handle tiebreak serve logic
            if (getServe() == 0) {
                setServe(1); // Player 2 serves first in tiebreak
            } else {
                // Alternate serves every two points
                // Logic to determine who serves next can be added here
                // For simplicity, we can just toggle for now
                setServe(0);
            }
        } else {
            // Regular game serve logic
            if (getServeSwitch() >= 1) {
                setServe(getServe() == 0 ? 1 : 0); // Toggle serve
                setServeSwitch(0); // Reset serve switch
            }
        }
        // Update the serve LED
        _serveLeds.updateServeLED();
    }
};
```

### Conclusion

By centralizing the serve logic in the `GameState` class, you ensure that all parts of your codebase refer to a single source of truth for serve management. This makes it easier to maintain and modify the serve logic in the future.