When using PyCharm to run this python project, make sure to install the pygame package in the Interpreter Settings.
Go to the bottom right of the screen in PyCharm and click Python 3.8 > Interpreter Settings > + button at bottom > search for pygame > Install Package.
If there is an error with installing pygame, a common fix is to install an updated version of pip. 
To do this, repeat the same process, but make sure to specify the newest verision in the "Specify version" checkbox and this should allow you
to install pygame successfully.

This repository contains two python files that make up a fully functioning and proper chess game.
This project was created in a group of three students in a Software Engineering course using the AGILE process.
Each contributor was of no greater authority than any other. A Jira baord was used to manage weekly sprints and assign stories to the contributors.
The ChessEngine file is responsible for storing all information regarding the current game state and for determining valid chess moves at the current game state.
A log of all moves is also kept within the ChessEngine file.
The ChessMain is the main driver class and will handle user input and display of the current game state. 
The two python files work in tandem to run and display a chess board with all pieces.
Some other available user features include the ability to undo moves and see each pieces available moves at each user's turn.

This chess game includes all of the necessary functionality for a chess game. 
Each piece moves the correct way. pieces can be properly cpatured, and end-game scenarios such as checkmate and stalemate.
Special moves are also implemented like castling to either the king or queen side, en passant captures, and pawn promotion.
However, the game does not include some high level rules and game-specific functionalities such as not being able to select any piece when a pawn is promoted.
A Queen piece is automatically selected in this scenario.
Another functionality that is missing from this project is the 50 move rule which states that a player can claim a draw if no capture has been made
and no pawn has been moved in the last fifty moves.
