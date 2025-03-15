# User Request:
The code base that you have access to is a Tennis scoreboard controller.  The scoreboard controller is not determining the next server properly.
Here are the official rules for switching serves:
```markdown
# Tennis Serve Switching Rules

## 1. At the Start of the Match:
- One player serves the entire game.
- The opponent serves the next game.
- Players alternate serving each game.

## 2. During a Set:
- The serve alternates between players every game.
- If the set reaches a **tiebreak (6-6 in games):**
  - The player who was supposed to serve in the next game serves the first point of the tiebreak.
  - After the first point, the opponent serves the next two points.
  - From then on, players serve two points in a row, alternating every two points.

## 3. Between Sets:
- If a set ends, the player who served first in the previous set will receive in the first game of the next set.
```

Could you help me put the serve logic in a more central place?  We can just ignore the serveSwitch.  I'll delete it when we get something else working.
# Relevant Code:
```cpp
int GameState::getServeSwitch() {
    return _serveSwitch;
}
```
```cpp
void ServeLeds::serveSwitch() {
  if ( _gameState->getServeSwitch() /* serveSwitch */ >= 1 ) {
    if (_gameState->getServe() /* serve */ == 0) {
      _gameState->setServe(1);  // serve = 1;
    } else {
      _gameState->setServe(0);  // serve = 0;
    }
    _gameState->setServeSwitch(0);  // serveSwitch = 0;
  }
  updateServeLED();
}
```
```cpp
int GameState::getServe() {
    return _serve;
}
```
```cpp
void Mode1TieBreaker::tieBreakEnable() {
    _player1->setPoints( 99 );        
    _player2->setPoints( 99 );   
    _pointLeds.updatePoints();      
    _gameState->setServeSwitch( 1 );  
    _gameState->setServe( 0 );        
    _serveLeds.serveSwitch();     
    if ( _gameState->getTieLEDsOn() == 0 ) { tieLEDsOn(); }
    _player1->setGames( 6 );
    _player2->setGames( 6 ); 
    _gameLeds.updateGames();
    Inputs _inputs( _player1, _player2, _pinInterface, _gameState );
    WatchTimer _watchTimer;
    // took out below loop on nov 3, 2022, back in on March 16, 2023
    for ( int currentPulseCount = 0; currentPulseCount < TIE_PULSE_COUNT; currentPulseCount++ ) {
        tieLEDsOff();
        if ( _watchTimer.watchInputDelay( TIE_BREAK_BLINK_DELAY, &_inputs, TIE_BREAK_WATCH_INTERVAL ) > 0 ) { return; }
        tieLEDsOn();
        if ( _watchTimer.watchInputDelay( TIE_BREAK_BLINK_DELAY, &_inputs, TIE_BREAK_WATCH_INTERVAL ) > 0 ) { return; } 
    }
    _player1->setGames( 0 );
    _player2->setGames( 0 );
    _gameLeds.updateGames();
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY ); 
    tieLEDsOn(); }
```
```cpp
void GameState::setServeSwitch( int serveSwitch ) {
    _serveSwitch = serveSwitch;
}
```
```cpp
void Mode1TieBreaker::mode1SetTBP1Games() {
    _gameLeds.updateGames();
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );
    if ( _player1->getGames() == 7 ) {
        _player1->setSets( _player1->getSets() + 1 );
        // _setLeds.updateSets();                // blinking one to many
        // GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );
        _mode1WinSequences.p1SetTBWinSequence();
        tieLEDsOff();                          
        _mode1WinSequences.p1MatchWinSequence(); }
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 ); }
```
```cpp
void Mode1Score::mode1SetTBP2Games() {
    _gameLeds.updateGames();
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );
    if ( _player2->getGames() == 7 ) {
        _player2->setSets( _player2->getSets() + 1 );  
        _setLeds.updateSets();                      
        GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );
        _mode1WinSequences.p2SetTBWinSequence();  
        _mode1TieBreaker.tieLEDsOff();           
        _mode1WinSequences.p2MatchWinSequence();  
    }
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 );  
}
```
```cpp
void Mode1Score::mode1SetTBP1Games() {
    _gameLeds.updateGames();
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );

    if ( _player1->getGames() == 7 ) {
        _player1->setSets( _player1->getSets() + 1 );
        _setLeds.updateSets();                       
        GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );
        _mode1WinSequences.p1SetTBWinSequence();  
        _mode1TieBreaker.tieLEDsOff();            
        _mode1WinSequences.p1MatchWinSequence();  
    }
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 );
}
```
```cpp
void Mode1TieBreaker::mode1SetTBP2Games() {
    _gameLeds.updateGames();
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );
    if ( _player2->getGames() == 7 ) {
        _player2->setSets( _player2->getSets() + 1 );
        // _setLeds.updateSets();
        // GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );
        _mode1WinSequences.p2SetTBWinSequence();
        tieLEDsOff();
        _mode1WinSequences.p2MatchWinSequence(); }
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 ); }
```
```cpp
void Mode1TieBreaker::mode1TBP2Games() {
    _gameLeds.updateGames();  // UpdateGames();
    _gameState->setServeSwitch( _gameState->getServeSwitch() +
        1 );  // serveSwitch++;
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );

    if ( _player2->getGames() == 15 ) {
        _player2->setSets( _player2->getSets() + 1 );  // p2Sets++;

        if ( _player2->getSets() == _player1->getSets() ) {
            endTieBreak();                            // EndTieBreak();
            _mode1WinSequences.p2TBSetWinSequence();  // P2TBSetWinSequence();
            _gameState->setSetTieBreak( 1 );          // setTieBreak = true;
            setTieBreakEnable( /*blink */ false );    // SetTieBreakEnable();
        }
        else {
            _mode1WinSequences.p2SetWinSequence();  // P2SetWinSequence();
            endTieBreak();                          // EndTieBreak();
        }
    }

    if ( _player2->getGames() >= 10 && ( _player2->getGames() - _player1->getGames() ) > 1 ) {
        _player2->setSets( _player2->getSets() + 1 );
        if ( _player2->getSets() == _player1->getSets() ) {
            endTieBreak();                            // EndTieBreak();
            _mode1WinSequences.p2TBSetWinSequence();  // P2TBSetWinSequence();
            _gameState->setSetTieBreak( 1 );          // setTieBreak = true;
            setTieBreakEnable( /*blink */ false );    // SetTieBreakEnable();
        }
        else {
            _mode1WinSequences.p2SetWinSequence();  // P2SetWinSequence();
            endTieBreak();                          // EndTieBreak();
        }
    }
}
```
```cpp
void Mode1Score::mode1P1Games() { 
    _gameLeds.updateGames();
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 );
    if ( _player1->getGames() >= 6 ) {
        if ( _player1->getGames() == 6 && _player2->getGames() == 6 ) {
            _gameState->setTieBreak( 1 );
            _mode1TieBreaker.tieBreakEnable();
        }
        if ( _gameState->getTieBreak() == 0 ) {
            if (( _player1->getGames() - _player2->getGames() ) > 1 ) { 
                _player1->setSets( _player1->getSets() + 1 );
                _setLeds.updateSets();
                if ( _player1->getSets() == _player2->getSets() ) {
                    _mode1WinSequences.p1TBSetWinSequence();
                    _gameState->setSetTieBreak( 1 );
                    _mode1TieBreaker.setTieBreakEnable( /* blink */ false );
                } else if ( _player1->getSets() == 2 ) {
                    _mode1WinSequences.p1MatchWinSequence();
                } else {
                    _mode1WinSequences.p1SetWinSequence();  
                    _setLeds.updateSets();                  
                    GameTimer::gameDelay( _gameState->getWinDelay());
                    _player1->setPoints( 0 );
                    _player2->setPoints( 0 );
                }
                _player1->setGames( 0 );
                _player2->setGames( 0 );
            } else {
                _mode1WinSequences.p1GameWinSequence(); 
                _gameLeds.updateGames();                 
                GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );  
                _player1->setPoints( 0 );
                _player2->setPoints( 0 );
            }
        }
    } else {
        _mode1WinSequences.p1GameWinSequence(); 
        _gameLeds.updateGames();                 
        GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );  
        _player1->setPoints( 0 );             
        _player2->setPoints( 0 );             
    }
}
```
```cpp
void Mode1Score::mode1P2Games() {
    _gameLeds.updateGames();
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 );
    if ( _player2->getGames()  >= 6 ) {
        if ( _player2->getGames()  == 6 && _player1->getGames() == 6 ) {
            _gameState->setTieBreak( 1 );        
            _mode1TieBreaker.tieBreakEnable(); 
        }
        if ( _gameState->getTieBreak() == 0 ) {
            if (( _player2->getGames() - _player1->getGames() ) > 1 ) {
                _player2->setSets( _player2->getSets() + 1 );  
                _setLeds.updateSets();
                if ( _player2->getSets() == _player1->getSets() ) {
                    _mode1WinSequences.p2TBSetWinSequence(); 
                    _gameState->setSetTieBreak( 1 );         
                    _mode1TieBreaker.setTieBreakEnable( /* blink */ false );     
                }
                else if ( _player2->getSets() == 2 ) {
                    _mode1WinSequences.p2MatchWinSequence();  
                }  else {
                    _mode1WinSequences.p2SetWinSequence();  
                    _setLeds.updateSets();                  
                    GameTimer::gameDelay( _gameState->getWinDelay());
                    _player1->setPoints( 0 ); 
                    _player2->setPoints( 0 ); 
                }
                _player1->setGames( 0 );  
                _player2->setGames( 0 );  
            }
            else {
                _mode1WinSequences.p2GameWinSequence();  
                _gameLeds.updateGames();                
                GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );
                _player1->setPoints( 0 ); 
                _player2->setPoints( 0 ); 
            }
        }
    }
    else {
        _mode1WinSequences.p2GameWinSequence();  
        _gameLeds.updateGames();                 
        GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );
        _player1->setPoints( 0 );
        _player2->setPoints( 0 );
    }
}
```
```cpp
void Mode1Score::mode1TBP1Games() {
    _gameLeds.updateGames();
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 );
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );

    if ( _player1->getGames() == 15 ) {
        _player1->setSets( _player1->getSets() + 1 );

        if ( _player2->getSets() == _player1->getSets() ) {
            _mode1TieBreaker.endTieBreak();           
            _mode1WinSequences.p1TBSetWinSequence(); 
            _gameState->setSetTieBreak( 1 );          
            _mode1TieBreaker.setTieBreakEnable( /* blink */ false );     
        }
        else {
            _mode1WinSequences.p1SetWinSequence();  
            _mode1TieBreaker.endTieBreak();         
        }
    }

    if ( _player1->getGames() >= 10 &&
        ( _player1->getGames() - _player2->getGames() ) > 1 ) {
        _player1->setSets( _player1->getSets() + 1 );
        if ( _player2->getSets() == _player1->getSets() ) {
            _mode1TieBreaker.endTieBreak();          
            _mode1WinSequences.p1TBSetWinSequence();  
            _gameState->setSetTieBreak( 1 );           
            _mode1TieBreaker.setTieBreakEnable( /*blink */ false );     
        }
        else {
            _mode1WinSequences.p1SetWinSequence();  
            _mode1TieBreaker.endTieBreak();         
        }
    }
}
```
```cpp
void Mode1Score::mode1TBP2Games() {
    _gameLeds.updateGames();  
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 ); 
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );

    if ( _player2->getGames() == 15 ) {
        _player2->setSets( _player2->getSets() + 1 );

        if ( _player2->getSets() == _player1->getSets() ) {
            _mode1TieBreaker.endTieBreak();           
            _mode1WinSequences.p2TBSetWinSequence();  
            _gameState->setSetTieBreak( 1 );           
            _mode1TieBreaker.setTieBreakEnable( /*blink */ false );    
        }
        else {
            _mode1WinSequences.p2SetWinSequence(); 
            _mode1TieBreaker.endTieBreak();         
        }
    }

    if ( _player2->getGames() >= 10 &&
        ( _player2->getGames() - _player1->getGames() ) > 1 ) {
        _player2->setSets( _player2->getSets() + 1 );
        if ( _player2->getSets() == _player1->getSets() ) {
            _mode1TieBreaker.endTieBreak();           
            _mode1WinSequences.p2TBSetWinSequence();
            _gameState->setSetTieBreak( 1 );         
            _mode1TieBreaker.setTieBreakEnable( /*blink */ false ); 
        }
        else {
            _mode1WinSequences.p2SetWinSequence();
            _mode1TieBreaker.endTieBreak();         
        }
    }
}
```
```cpp
void Mode1TieBreaker::mode1TBP1Games() {
    _gameLeds.updateGames();  // UpdateGames();
    _gameState->setServeSwitch( _gameState->getServeSwitch() + 1 );
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY );

    if ( _player1->getGames() == 15 ) {
        _player1->setSets( _player1->getSets() + 1 );;

        if ( _player2->getSets() == _player1->getSets()) {
            endTieBreak();                            // EndTieBreak();
            _mode1WinSequences.p1TBSetWinSequence();  // P1TBSetWinSequence();
            _gameState->setSetTieBreak( 1 );          // setTieBreak = true;
            setTieBreakEnable( /*blink */ false );    // SetTieBreakEnable();
        }
        else {
            _mode1WinSequences.p1SetWinSequence();  // P1SetWinSequence();
            endTieBreak();                          // EndTieBreak();
        }
    }

    if ( _player1->getGames() >= 10 && ( _player1->getGames() - _player2->getGames() ) > 1 ) {
        _player1->setSets( _player1->getSets() + 1 );  // p1Sets++;
        if ( _player2->getSets() == _player1->getSets() /* p1Sets */ ) {
            endTieBreak();                             // EndTieBreak();
            _mode1WinSequences.p1TBSetWinSequence();   // P1TBSetWinSequence();
            _gameState->setSetTieBreak( 1 );           // setTieBreak = true;
            setTieBreakEnable( /*blink */ false );     // SetTieBreakEnable();
        }
        else {
            _mode1WinSequences.p1SetWinSequence();  // P1SetWinSequence();
            endTieBreak();                          // EndTieBreak();
        }
    }
}
```
```cpp
void Mode1TieBreaker::setTieBreakEnable( bool blink ) {
    _player1->setPoints( 99 );
    _player2->setPoints( 99 );
    _pointLeds.updatePoints();     
    _gameState->setServeSwitch( 1 );
    _gameState->setServe( 0 );        
    _serveLeds.serveSwitch();

    // add on March 20, 2023  copied from tieBreakEnable()
    if ( blink ) {
        Inputs _inputs( _player1, _player2, _pinInterface, _gameState );
        WatchTimer _watchTimer;
        for ( int currentPulseCount = 0; currentPulseCount < TIE_PULSE_COUNT; currentPulseCount++ ) {
            tieLEDsOff();
            if ( _watchTimer.watchInputDelay( TIE_BREAK_BLINK_DELAY, &_inputs, TIE_BREAK_WATCH_INTERVAL ) > 0 ) { return; }
            tieLEDsOn();
            if ( _watchTimer.watchInputDelay( TIE_BREAK_BLINK_DELAY, &_inputs, TIE_BREAK_WATCH_INTERVAL ) > 0 ) { return; } 
        }
    }
    
    if ( _gameState->getTieLEDsOn() == 0 ) { tieLEDsOn(); }
    _player1->setGames( 0 );
    _player2->setGames( 0 );
    _gameLeds.updateGames();
    GameTimer::gameDelay( UPDATE_DISPLAY_DELAY  ); }
```
```cpp
void ServeLeds::updateServeLED() {
  if (_gameState->getServe() /* serve */ == 0) {
    _pinInterface->pinDigitalWrite(P1_SERVE, HIGH);
    _pinInterface->pinDigitalWrite(P2_SERVE, LOW);
  } else {
    _pinInterface->pinDigitalWrite(P1_SERVE, LOW);
    _pinInterface->pinDigitalWrite(P2_SERVE, HIGH);
  }
}
```
```cpp
void GameState::setServe( int serve ) {
    _serve = serve;
}
```
```cpp
void GameModes::gameStart() {
    if ( _gameState->getStarted() == 0 ) {  // if not started...
        _player1->setPoints( 0 );             // p1Points = 0;
        _player2->setPoints( 0 );             // p2Points = 0;
        _player1->setGames( 0 );              // p1Games = 0;
        _player2->setGames( 0 );              // p2Games = 0;
        _player1->setSets( 0 );               // p1Sets = 0;
        _player2->setSets( 0 );               // p2Sets = 0;
        _pointLeds.updatePoints();          // UpdatePoints();
        _gameLeds.updateGames();            // UpdateGames();
        _setLeds.updateSets();              // UpdateSets();
        _gameState->setTieBreakOnly( 0 );     // tieBreakOnly = false;
        _gameState->setStarted( 1 ); }}
```
```cpp
void Mode1Functions::mode1ServeFunction() {
    _undo.setMode1Undo( _history );
    _serveLeds.serveSwitch();
}
```
```cpp
void GameModes::mode1() {
    #if defined _WIN32 || defined _WIN64
    // std::cout << "inside game mode 1." << std::endl;
    #endif
    _gameState->setNow( GameTimer::gameMillis() );          // now =
    _inputs.readUndoButton();                             // ReadUndoButton();
    if ( _gameState->getUndo() == 1 ) {  // undo button pressed
        #if defined _WIN32 || defined _WIN64
        std::cout << "undo button pressed!" << std::endl;
        #endif
        _gameState->setUndo( 0 );
        #if defined _WIN32 || defined _WIN64
        std::cout << "calling mode1Undo( _history )... " << std::endl;
        #endif                         // set undo = false;
        _undo.mode1Undo( _history );
    }  // Mode1Undo();

    _inputs.readPlayerButtons();  // digital read on player buttons.  sets playerButton if tripped.
    _serveLeds.serveSwitch();     // ServeSwitch(); // if serveSwitch >= 2,
    // serveSwitch = 0; and toggle serve variable

    if ( _gameState->getTieBreak() == 1 ) {
        _mode1TieBreaker.tieBreaker();
    }  // TieBreaker();

    if ( _gameState->getSetTieBreak() == 1 ) {
        _mode1TieBreaker.setTieBreaker();  // SetTieBreaker();
    } else {
        _mode1Functions.mode1ButtonFunction();  // Mode1ButtonFunction();
        _mode1Functions.pointFlash();           // PointFlash(); 
        // nothing happens if point flash is not 1
    }}
```
```cpp
void Reset::resetScoreboard() {
    _logger->logUpdate( "resetting scoreboard...", __FUNCTION__ );
    _pinInterface->pinDigitalWrite( P1_POINTS_LED1, LOW );
    _pinInterface->pinDigitalWrite( P1_POINTS_LED2, LOW );
    _pinInterface->pinDigitalWrite( P1_POINTS_LED3, LOW );
    _pinInterface->pinDigitalWrite(
        P1_POINTS_LED4,
        LOW );  //<------- add a mapped for loop to flash Player 1 LED's ---<<

    _pinInterface->pinDigitalWrite( P2_POINTS_LED1, LOW );
    _pinInterface->pinDigitalWrite( P2_POINTS_LED2, LOW );
    _pinInterface->pinDigitalWrite( P2_POINTS_LED3, LOW );
    _pinInterface->pinDigitalWrite( P2_POINTS_LED4, LOW );

    _pinInterface->pinDigitalWrite( P1_GAMES_LED0, LOW );
    _pinInterface->pinDigitalWrite( P1_GAMES_LED1, LOW );
    _pinInterface->pinDigitalWrite( P1_GAMES_LED2, LOW );
    _pinInterface->pinDigitalWrite( P1_GAMES_LED3, LOW );
    _pinInterface->pinDigitalWrite( P1_GAMES_LED4, LOW );
    _pinInterface->pinDigitalWrite( P1_GAMES_LED5, LOW );
    _pinInterface->pinDigitalWrite( P1_GAMES_LED6, LOW );
    _pinInterface->pinDigitalWrite( P1_TIEBREAKER, LOW );

    _pinInterface->pinDigitalWrite( P2_GAMES_LED0, LOW );
    _pinInterface->pinDigitalWrite( P2_GAMES_LED1, LOW );
    _pinInterface->pinDigitalWrite( P2_GAMES_LED2, LOW );
    _pinInterface->pinDigitalWrite( P2_GAMES_LED3, LOW );
    _pinInterface->pinDigitalWrite( P2_GAMES_LED4, LOW );
    _pinInterface->pinDigitalWrite( P2_GAMES_LED5, LOW );
    _pinInterface->pinDigitalWrite( P2_GAMES_LED6, LOW );
    _pinInterface->pinDigitalWrite( P2_TIEBREAKER, LOW );

    _pinInterface->pinDigitalWrite( P1_SETS_LED1, LOW );
    _pinInterface->pinDigitalWrite( P1_SETS_LED2, LOW );

    _pinInterface->pinDigitalWrite( P2_SETS_LED1, LOW );
    _pinInterface->pinDigitalWrite( P2_SETS_LED2, LOW );

    _pinInterface->pinDigitalWrite( P1_SERVE, LOW );
    _pinInterface->pinDigitalWrite( P2_SERVE, LOW );

    _logger->logUpdate( "turning tie leds off... ", __FUNCTION__ );
    tieLEDsOff();

    _gameState->setTieBreak( 0 );      
    _gameState->setSetTieBreak( 0 );   
    _gameState->setServeSwitch( 1 );   
    _gameState->setServe( 0 );        
    _gameState->setPlayerButton( 0 );  
    _gameState->setStarted(
        /*1*/ 0 );  // gameStart = true; TODO: the placing of this is questionable
    GameTimer::gameDelay( 200 );  // delay( 200 );
    _logger->logUpdate( "done resetting game.", __FUNCTION__ );
}
```
```cpp
void Mode1Score::mode1P2Score() {
    if ( _player2->getPoints() >= 3 ) {
        if ( _player2->getPoints() == _player1->getPoints() ) {  // Tie, Back to Deuce
            _player1->setPoints( 3 );                              
            _player2->setPoints( 3 );                              
        }

        // Game win Scenario
        else if ( _player2->getPoints() > 3 && ( _player2->getPoints() - _player1->getPoints()) > 1 ) {                                // Game win Scenario
            _player2->setGames( _player2->getGames() + 1 );  
            _undo.memory();                                
            _pointLeds.updatePoints();                    
            mode1P2Games();
        }

        if ( _player2->getPoints() == 4 ) {
            _gameState->setPointFlash( 1 );
            _gameState->setPreviousTime( GameTimer::gameMillis());
            _gameState->setToggle( 0 );                              
        }
    }
    _pointLeds.updatePoints(); 
}
```
```cpp
void Mode1Score::mode1P1Score() {
    if ( _player1->getPoints() >= 3 ) {
        if ( _player1->getPoints() == _player2->getPoints() ) {
            // Tie, Back to Deuce
            _player1->setPoints( 3 );  
            _player2->setPoints( 3 );  
        } else if ( _player1->getPoints() > 3 && ( _player1->getPoints() - _player2->getPoints() ) > 1 ) {
            // Game win Scenario
            _player1->setGames( _player1->getGames() + 1 );
            _undo.memory();
            _pointLeds.updatePoints();
            mode1P1Games();
        }

        if ( _player1->getPoints() == 4 ) {
            _gameState->setPointFlash( 1 );  
            _gameState->setPreviousTime( GameTimer::gameMillis()); 
            _gameState->setToggle( 0 );                          
        }
    }
    _pointLeds.updatePoints();
}
```
```cpp
void GameModes::mode2() {
    _gameState->setNow( GameTimer::gameMillis() );  // now =
    if ( _gameState->getTieBreakOnly() == 0 ) {
        _gameState->setTieBreak( 1 );  // tieBreak = true;
        _mode1TieBreaker.tieBreakEnable();
        _gameState->setTieBreakOnly( 1 );  // tieBreakOnly = true;
    }
    mode1(); }
```
```cpp
GameState gameState;
```
```cpp
void Mode1TieBreaker::endTieBreak() {
    tieLEDsOff();
    _player1->setPoints( 0 );       
    _player2->setPoints( 0 );         
    _player1->setGames( 0 );         
    _player2->setGames( 0 );         
    _pointLeds.updatePoints();      
    _gameLeds.updateGames();       
    _gameState->setTieBreak( 0 );     
    _gameState->setSetTieBreak( 0 ); }
```
```cpp
void GameModes::mode4() {
    _gameState->setNow( GameTimer::gameMillis() );  // now =
    if ( _gameState->getTieBreakOnly() == 0 ) {
        _gameState->setTieBreak( 1 );  // tieBreak = true;
        _mode1TieBreaker.tieBreakEnable();
        _gameState->setTieBreakOnly( 1 );  // tieBreakOnly = true;
    }
    mode1(); }
```
```cpp
void Mode1WinSequences::p1MatchWinSequence() {
    _undo.memory();              
    _pointLeds.updateTBPoints();  
    _player2->setGames( 99 ); 
    _gameLeds.updateGames();   

    MatchWinSequence matchWinSequence; matchWinSequence.run( _player1, _gameState, &_gameLeds, &_setLeds );    

    // for ( int currentPulseCount = 0; currentPulseCount < _gameState->getMatchWinPulseCount(); currentPulseCount++ ) {
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED0, HIGH );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED1, HIGH );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED2, HIGH );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED3, HIGH );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED4, HIGH );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED5, HIGH );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED6, HIGH );
    //     // _pinInterface->pinDigitalWrite( P1_TIEBREAKER, HIGH );

    //     _pinInterface->pinDigitalWrite( P1_SETS_LED1, HIGH );
    //     _pinInterface->pinDigitalWrite( P1_SETS_LED2, HIGH );
    //     GameTimer::gameDelay( _gameState->getFlashDelay());

    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED0, LOW );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED1, LOW );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED2, LOW );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED3, LOW );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED4, LOW );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED5, LOW );
    //     _pinInterface->pinDigitalWrite( P1_GAMES_LED6, LOW );
    //     // _pinInterface->pinDigitalWrite( P1_TIEBREAKER, LOW );

    //     _pinInterface->pinDigitalWrite( P1_SETS_LED1, LOW );
    //     _pinInterface->pinDigitalWrite( P1_SETS_LED2, LOW );
    //     GameTimer::gameDelay( _gameState->getFlashDelay());
    // }
    _reset.resetScoreboard();
}
```
```cpp
int GameState::getSetTieBreak() {
    return _setTieBreak;
}
```
```cpp
void GameModes::noCode() {
    _player1->setPoints( _player1->getPoints() + 1 );  // p1Points++;
    _pointLeds.updatePoints();                       // UpdatePoints();
    GameTimer::gameDelay( 1000 );
    _player1->setPoints( _player1->getPoints() - 1 );  // p1Points--;
    _pointLeds.updatePoints();                       // UpdatePoints();
    GameTimer::gameDelay( 1000 ); }
```
```cpp
int GameState::getTieBreak() {
    return _tieBreak;
}
```
```cpp
Inputs _inputs( _player1, _player2, _pinInterface, _gameState );
```
```cpp
Inputs _inputs( _player1, _player2, _pinInterface, _gameState );
```
```cpp
void Mode1WinSequences::p2TBMatchWinSequence() {
    _player1->setGames( 99 );
    _gameLeds.updateGames();  // UpdateGames();
    _undo.memory();           // Memory();
    tieLEDsOff();

    MatchWinSequence matchWinSequence; matchWinSequence.run( _player2, _gameState, &_gameLeds, &_setLeds );

    // for ( int currentPulseCount = 0; currentPulseCount < _gameState->getMatchWinPulseCount(); currentPulseCount++ ) {
    //     _player2->setSets( 0 );
    //     _setLeds.updateSets(); 
    //     GameTimer::gameDelay( _gameState->getFlashDelay());
    //     _player2->setSets( _gameState->getP2SetsMem() );
    //     _setLeds.updateSets();                         
    //     GameTimer::gameDelay( _gameState->getFlashDelay());
    // }
    _reset.resetScoreboard();
}
```
```cpp
void ScoreBoard::update() {
  // _lcd->setCursor(1, 0);
  // _lcd->print("PLayer1   Player2");
  // _lcd->setCursor(1, 1);
  // _lcd->print("Points:" + std::to_string(_player1->getPoints()) +
  //             "  Points:" + std::to_string(_player2->getPoints()));
  // _lcd->setCursor(1, 2);
  // _lcd->print("Games :" + std::to_string(_player1->getGames()) +
  //             "  Games :" + std::to_string(_player2->getGames()));
  // _lcd->setCursor(1, 3);
  // _lcd->print("Sets  :" + std::to_string(_player1->getSets()) +
  //             "  Sets  :" + std::to_string(_player2->getSets()));
}
```
```cpp
void Mode1WinSequences::p1TBMatchWinSequence() {
    _player2->setGames( 99 );   // p2Games = 99;
    _gameLeds.updateGames();  // UpdateGames();
    _undo.memory();           // Memory();
    tieLEDsOff();

    MatchWinSequence matchWinSequence; matchWinSequence.run( _player1, _gameState, &_gameLeds, &_setLeds );

    // for ( int currentPulseCount = 0; currentPulseCount < _gameState->getMatchWinPulseCount(); currentPulseCount++ ) {
    //     _player1->setSets( 0 );
    //     _setLeds.updateSets(); 
    //     GameTimer::gameDelay( _gameState->getFlashDelay());
    //     _player1->setSets( _gameState->getP1SetsMem() );
    //     _setLeds.updateSets();                         
    //     GameTimer::gameDelay( _gameState->getFlashDelay()); }
    _reset.resetScoreboard();
}
```
```cpp
GameState::GameState() {
    _pointFlash = 0;
    _serve = 0;
    _tieBreak = 0;
    _setTieBreak = 0;
    _tieLEDsOn = 0;
    _started = 0;
    _serveSwitch = 1;
    _playerButton = 0;
    _undo = 0;
    _freezePlayerButton = 0;
    
    _winDelay           = WIN_DELAY;
    _buttonDelay        = BUTTON_DELAY;
    #if defined _WIN32 || defined _WIN64
    _flashDelay         = 250;
    _gameFlashDelay     = 250;
    #else
    _flashDelay         = FLASH_DELAY;
    _gameFlashDelay     = GAME_FLASH_DELAY;
    #endif
    _gameWinPulseCount = 4;
    _tieBreakMem = 0;
    _setTieBreakMem = 0;
    _p1PointsMem = 0;
    _p2PointsMem = 0;
    _p1GamesMem = 0;
    _p2GamesMem = 0;
    _p1SetsMem = 0;
    _p2SetsMem = 0;
    _player1_points  = 0;
    _player2_points  = 0;
    _player1_games   = 0;
    _player2_games   = 0;
    _player1_sets    = 0;
    _player2_sets    = 0;
    _player1_matches = 0;
    _player2_matches = 0;
}
```
```cpp
void Mode1WinSequences::p2MatchWinSequence() {
    _undo.memory();               // Memory();
    _pointLeds.updateTBPoints();  // UpdateTBPoints();
    _player1->setGames( 99 );
    _gameLeds.updateGames();      // UpdateGames();

    MatchWinSequence matchWinSequence; matchWinSequence.run( _player2, _gameState, &_gameLeds, &_setLeds );

    // for ( int currentPulseCount = 0;
    //     currentPulseCount < _gameState->getMatchWinPulseCount();
    //     currentPulseCount++ ) {
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED0, HIGH );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED1, HIGH );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED2, HIGH );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED3, HIGH );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED4, HIGH );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED5, HIGH );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED6, HIGH );
    //     // _pinInterface->pinDigitalWrite( P2_TIEBREAKER, HIGH );

    //     _pinInterface->pinDigitalWrite( P2_SETS_LED1, HIGH );
    //     _pinInterface->pinDigitalWrite( P2_SETS_LED2, HIGH );
    //     GameTimer::gameDelay( _gameState->getFlashDelay() );

    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED0, LOW );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED1, LOW );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED2, LOW );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED3, LOW );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED4, LOW );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED5, LOW );
    //     _pinInterface->pinDigitalWrite( P2_GAMES_LED6, LOW );
    //     // _pinInterface->pinDigitalWrite( P2_TIEBREAKER, LOW );

    //     _pinInterface->pinDigitalWrite( P2_SETS_LED1, LOW );
    //     _pinInterface->pinDigitalWrite( P2_SETS_LED2, LOW );
    //     GameTimer::gameDelay( _gameState->getFlashDelay());
    // }
    _reset.resetScoreboard();
    // Serial.println("End P2 Match Win Sequence");
}
```
```cpp
void Mode2Functions::m2Loop() {
  _gameState->setNow(/* now = */ GameTimer::gameMillis());
  // unsigned long elapsed_time = now -  previous_time;
  // Serial.println( "elapsed_time: " + to_string( elapsed_time ));
  if (_gameState->getNow() /* now */ -
          _gameState->getPreviousTime() /* previous_time */
      >= 1000 /*10000*/) {
    // if ( true ) {
    switch (_player1->getMode()) { /* modeP1 */

      // _player1 Points
      case 0:
        _player1->incrementSetting();                 // p1Setting++;
        _player1->setPoints(_player1->getSetting());  //  p1Points = p1Setting;
        _pointLeds.updatePoints();                    // UpdatePoints();
        if (_player1->getSetting() > 3) /* p1Setting > 3 */ {
          _player1->setSetting(0);  // p1Setting = 0;
          _player1->setPoints(0);   // p1Points = 0;
          _player1->setMode(1);     // modeP1 = 1;
          // Serial.println( "_player1 set to mode 1" );
        }
        break;

      // _player1 Games
      case 1:
        _player1->incrementSetting();                // p1Setting++;
        _player1->setGames(_player1->getSetting());  // p1Games = p1Setting;
        _gameLeds.updateGames();                     // UpdateGames();
        if (_player1->getSetting() > 6 /* p1Setting > 6 */) {
          _player1->setSetting(0);  // p1Setting = 0;
          _player1->setGames(0);    // p1Games = 0;
          _player1->setMode(2);     //   modeP1 = 2;
          // Serial.println( "_player1 set to mode 2" );
        }
        break;

      // _player1 Sets
      case 2:
        _player1->incrementSetting();
        _player1->setSets(_player1->getSetting());
        _setLeds.updateSets();                      // UpdateSets();
        if (_player1->getSetting() > 1 /* p1Setting > 1 */) {
          _player1->setSetting(0);  // p1Setting = 0;
          _player1->setSets(0);     
          _player1->setMode(0);     // modeP1 = 0;
        }
        break;
    }

    // _player2 Points
    switch (_player2->getMode() ) {
      case 0:
        // _player2->incrementSetting();
        _player2->setPoints(
            _player2->incrementSetting());
        _pointLeds.updatePoints();          // UpdatePoints();
        if (_player2->getSetting() > 4 ) {
          _player2->setSetting(0); 
          _player2->setPoints(0);  
          _player2->setMode(1);   
        }
        break;

      // _player2 Games
      case 1:
        // p2Setting++;
        // p2Games = p2Setting;
        _player2->setGames(
            _player2->incrementSetting());  // p2Games = p2Setting;
        _gameLeds.updateGames();            // UpdateGames();
        if (_player2->getSetting() > 7) /* p2Setting > 7 */ {
          _player2->setSetting(0);  // p2Setting = 0;
          _player2->setGames(0);    // p2Games = 0;
          _player2->setMode(2);     // modeP2 = 2;
        }
        break;

      // _player2 Sets
      case 2:
        // p2Setting++;
        _player2->setSets(_player2->incrementSetting());  // p2Sets = p2Setting;
        _setLeds.updateSets();
        if (_player2->getSetting() > 1 /* p2Setting > 1 */) {
          _player2->setSetting(0);  // p2Setting = 0;
          _player2->setSets(0);     
          _player2->setMode(0);     /* modeP2 = 0; */
        }
    }
    _gameState->setPreviousTime(_gameState->getNow());  //  previous_time = now;
  } else {
    // Serial.println( "elapsed_time: " + to_string( elapsed_time ));
    // Serial.println("*** DID NOT ENTER BECAUSE NOT ENOUGH TIME HAS PASSED
    // ***");
  }
}
```