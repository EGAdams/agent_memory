To address the issue with the scoreboard controller not determining the next server properly, we need to analyze how the serve switching logic is implemented in the provided code. 

### Key Observations:

1. **Serve Switching Logic**:
   - The `serveSwitch()` method in the `ServeLeds` class is responsible for toggling the server based on the `_serveSwitch` value.
   - The `_serveSwitch` is set to `1` when a new game starts or when a tiebreak is initiated, as seen in the `tieBreakEnable()` method and other game state updates.

2. **Game State Management**:
   - The `_serveSwitch` is incremented in various methods like `mode1SetTBP1Games()`, `mode1SetTBP2Games()`, `mode1P1Games()`, and `mode1P2Games()`. This incrementing logic seems to be consistent with the rules of switching serves every game.

3. **Tiebreak Logic**:
   - The tiebreak logic in `Mode1TieBreaker` appears to set the serve correctly for the first point of the tiebreak, but the subsequent serves (after the first point) are handled by alternating every two points.

4. **Initial Serve**:
   - The initial serve is set to player 1 (`_gameState->setServe(0);`) in the `tieBreakEnable()` method, which is correct according to the rules.

### Potential Issues:

1. **Serve Switching Not Triggering**:
   - The `serveSwitch()` method only toggles the server when `_serveSwitch` is `>= 1`. If `_serveSwitch` is not being set correctly at the start of each game or after a tiebreak, the server may not switch as expected.

2. **Inconsistent State Management**:
   - The `_serveSwitch` is incremented in multiple places, but it is not clear if it is being reset or managed correctly after each game or set. This could lead to incorrect toggling of the server.

### Recommendations for Fixes:

1. **Ensure Proper Initialization**:
   - Make sure that `_serveSwitch` is initialized correctly at the start of each game and set. For example, in the `gameStart()` method, you might want to set `_gameState->setServeSwitch(1);` to ensure the serve toggles correctly.

2. **Review Serve Switching Logic**:
   - In the `serveSwitch()` method, ensure that the logic for toggling the server is only executed when it is appropriate. You might want to add debug statements to track the value of `_serveSwitch` and `_serve` to see if they are being set as expected.

3. **Check Tiebreak Logic**:
   - Ensure that the tiebreak logic correctly handles the serve switching after the first point. You may need to implement additional logic to manage the serve switching after the first point in the tiebreak.

### Example Code Adjustment:

Here’s a potential adjustment to ensure the serve switching works correctly:

```cpp
void GameModes::gameStart() {
    if (_gameState->getStarted() == 0) {
        // Initialize game state
        _player1->setPoints(0);
        _player2->setPoints(0);
        _player1->setGames(0);
        _player2->setGames(0);
        _player1->setSets(0);
        _player2->setSets(0);
        _pointLeds.updatePoints();
        _gameLeds.updateGames();
        _setLeds.updateSets();
        _gameState->setTieBreakOnly(0);
        _gameState->setStarted(1);
        
        // Set initial serve state
        _gameState->setServeSwitch(1); // Ensure serve switch is set to start toggling
        _gameState->setServe(0); // Player 1 serves first
    }
}
```

### Conclusion:

By ensuring that the `_serveSwitch` is managed correctly and that the serve switching logic is executed at the right times, you should be able to resolve the issue with the next server not being determined properly. Debugging the values of `_serveSwitch` and `_serve` during the game flow will also help identify any inconsistencies.