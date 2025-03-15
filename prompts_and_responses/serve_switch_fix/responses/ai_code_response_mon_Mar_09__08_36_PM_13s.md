To address the issue with the server switching logic in your Tennis scoreboard controller, we need to focus on the parts of the code that handle the serve switching based on the rules you've provided. Here are the key areas to investigate:

1. **Serve Switch Logic**:
   - The `ServeLeds::serveSwitch()` function is responsible for toggling the server based on the `_serveSwitch` value. It checks if `_serveSwitch` is greater than or equal to 1, and if so, it toggles the server between player 0 and player 1.
   - The `_serveSwitch` is reset to 0 after toggling the server.

   ```cpp
   void ServeLeds::serveSwitch() {
       if (_gameState->getServeSwitch() >= 1) {
           if (_gameState->getServe() == 0) {
               _gameState->setServe(1);  // serve = 1;
           } else {
               _gameState->setServe(0);  // serve = 0;
           }
           _gameState->setServeSwitch(0);  // serveSwitch = 0;
       }
       updateServeLED();
   }
   ```

2. **Serve Switch Increment**:
   - The `_serveSwitch` is incremented in several places, particularly in the `mode1SetTBP1Games()`, `mode1SetTBP2Games()`, and other game-related functions. Each time a game is won, `_serveSwitch` is incremented, which should lead to a server switch.

   ```cpp
   _gameState->setServeSwitch(_gameState->getServeSwitch() + 1);
   ```

3. **Tie Break Logic**:
   - The `tieBreakEnable()` function sets the initial server for the tiebreak and also sets `_serveSwitch` to 1, indicating that the server should switch for the first point of the tiebreak.

   ```cpp
   void Mode1TieBreaker::tieBreakEnable() {
       _gameState->setServeSwitch(1);
       _gameState->setServe(0);        
       _serveLeds.serveSwitch();     
   }
   ```

4. **Game Start Logic**:
   - The `gameStart()` function initializes the game state, including setting the initial server. Ensure that the initial server is set correctly based on the rules.

   ```cpp
   void GameModes::gameStart() {
       if (_gameState->getStarted() == 0) {
           _gameState->setServe(0); // Initial server
           _gameState->setServeSwitch(1); // Set serve switch to 1
           // Other initializations...
       }
   }
   ```

### Recommendations for Debugging:
- **Check Initial Server Assignment**: Ensure that the initial server is set correctly when the game starts. The first server should be player 0 or player 1 based on your game rules.
- **Verify Serve Switch Logic**: Ensure that `_serveSwitch` is being incremented correctly after each game and that the `serveSwitch()` function is being called appropriately.
- **Tiebreak Logic**: Ensure that the tiebreak logic correctly sets the server and that the serve switching rules are followed during the tiebreak.
- **Logging**: Add logging statements to track the values of `_serve`, `_serveSwitch`, and the current game state to help identify where the logic may be failing.

By focusing on these areas, you should be able to identify and correct the issue with the server switching logic in your Tennis scoreboard controller. If you need further assistance with specific modifications or debugging, feel free to ask!