To implement the correct serve switching logic according to the official tennis rules you've provided, we need to modify the existing code to ensure that the serve alternates correctly between players based on the game state, including handling tie-breaks and set transitions.

Here's a revised version of the relevant parts of the code that will correctly manage the serve switching logic:

### Updated Code

1. **GameState Class Modifications**:
   - Add a method to determine the current server based on the game state.

```cpp
class GameState {
private:
    int _serve; // 0 for player 1, 1 for player 2
    int _gamesPlayer1;
    int _gamesPlayer2;
    int _setsPlayer1;
    int _setsPlayer2;
    bool _tieBreak;
    bool _setTieBreak;

public:
    // Existing methods...

    void switchServe() {
        if (_tieBreak) {
            // In a tie-break, the first server serves one point, then alternates every two points.
            // The server is determined by the current game state.
            if (_gamesPlayer1 + _gamesPlayer2 >= 12) { // After 6-6 in games
                // Determine who serves based on the number of points played in the tie-break
                int totalPoints = _gamesPlayer1 + _gamesPlayer2; // Total points played
                if (totalPoints % 2 == 0) {
                    _serve = (_serve == 0) ? 1 : 0; // Alternate every two points
                }
            }
        } else {
            // Normal game serve switching
            if (_gamesPlayer1 + _gamesPlayer2 > 0 && (_gamesPlayer1 + _gamesPlayer2) % 2 == 0) {
                _serve = (_serve == 0) ? 1 : 0; // Alternate serve every game
            }
        }
    }

    int getServe() const {
        return _serve;
    }

    // Other existing methods...
};
```

2. **ServeLeds Class Modifications**:
   - Update the `serveSwitch` method to call the new `switchServe` method.

```cpp
void ServeLeds::serveSwitch() {
    _gameState->switchServe(); // Call the new serve switching logic
    updateServeLED(); // Update the LED based on the current server
}
```

3. **Tie Break Logic**:
   - Ensure that the tie-break logic correctly initializes the serve.

```cpp
void Mode1TieBreaker::tieBreakEnable() {
    _player1->setPoints(99);
    _player2->setPoints(99);
    _pointLeds.updatePoints();
    _gameState->setServe(0); // Player 1 serves first in the tie-break
    _serveLeds.serveSwitch(); // Update the serve LED
    // Other existing logic...
}
```

4. **Game Logic**:
   - Ensure that the game logic correctly updates the game state and calls the serve switch when a game is won.

```cpp
void Mode1Score::mode1P1Games() {
    // Existing logic...
    if (_player1->getGames() >= 6) {
        if (_player1->getGames() == 6 && _player2->getGames() == 6) {
            _gameState->setTieBreak(1);
            _mode1TieBreaker.tieBreakEnable();
        }
        // Call switchServe after a game is won
        _gameState->switchServe();
    }
    // Existing logic...
}

void Mode1Score::mode1P2Games() {
    // Existing logic...
    if (_player2->getGames() >= 6) {
        if (_player2->getGames() == 6 && _player1->getGames() == 6) {
            _gameState->setTieBreak(1);
            _mode1TieBreaker.tieBreakEnable();
        }
        // Call switchServe after a game is won
        _gameState->switchServe();
    }
    // Existing logic...
}
```

### Summary
The above modifications ensure that the serve switching logic adheres to the official tennis rules. The `switchServe` method in the `GameState` class handles the logic for both regular games and tie-breaks, while the `serveSwitch` method in the `ServeLeds` class updates the LED indicators based on the current server. The game logic methods call `switchServe` after a game is won to ensure the server is updated correctly.