// #include <ctime>
#include <unistd.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

struct GameBoard {

        int board[7][7];
        int AI[7];
        bool over;
        bool isX;
        bool aiOn;
        int max;
        bool testing;

};

bool action(struct GameBoard board, int columnNum, bool isItX);
void printBoard(struct GameBoard board, bool changed);
bool aiTurn(struct GameBoard board);
int maxLine(struct GameBoard board, int row, int col, bool isX);
bool checkOver(struct GameBoard board, int row, int column, int player);



struct GameBoard new_GameBoard() {

        struct GameBoard board;
	board.over = false;
	board.isX = false;
        board.aiOn = false;

        return board;

}

bool getOver(struct GameBoard board) {

	return board.over;
}

bool getIsX(struct GameBoard board) {

	return board.isX;
}

void switchIsX(struct GameBoard board) {

	if (board.isX) board.isX = false;
	else board.isX = true;

}

void setAI(struct GameBoard board) {
    
    board.aiOn = true;
}

int getMax(struct GameBoard board){
    
    return board.max;
    
}

void initialize(struct GameBoard board) {

	for (int i = 0; i < 7; i++) {

		for (int j = 0; j < 7; j++) {

			board.board[i][j] = 0; // Sets entire 7x7 to be 0

		}

	}

}

void initAI(struct GameBoard board) {
    
    for (int i = 0; i < 7; i++) {
        
        board.AI[i] = 0;
        
    }
}

void printBoard(struct GameBoard board, bool changed) {

	if (board.over) return;

	if (!changed) printf("(Nothing changed!)\n");

	printf("+---------------+\n");
	//cout << "|               |" << endl;

	for (int i = 1; i < 7; i++) {

		printf("| ");

		for (int j = 0; j < 7; j++) {

			if (board.board[i][j] == 0) printf(" ");
			else if (board.board[i][j] == 1) printf("X");
			else printf("0");
			printf(" ");

		}

		printf("|\n");

	}

	printf("+-1-2-3-4-5-6-7-+\n\n");

	if (!board.over) {
		if (board.isX) printf("X's turn!\n");
		else printf("0's turn!\n");
	}
}


bool aiTurn(struct GameBoard board) {
    
    board.testing = true;
    
    usleep(1000000);
	// this_thread::sleep_for(std::chrono::seconds(1));

    bool changed;
    
    int score;
    int row;
    int max;
    
    // simulate offense and score
    for (int col = 0; col < 7; col++) {
        
        row = 6 - board.board[0][col];
        if (row == 0) {
            
            board.AI[col] = 10;
            continue;
        }
        // if the entire column is filled, tell AI that it can't go there and keep going
        
        // for all seven rows we now have the row,col location of the drop.
        
        board.max = maxLine(board,row,col,true);
        
        //cout << "Max is " << max << endl;
        
        if (board.max == 4) score = 1;
        else if (board.max == 3) score = 3;
        else if (board.max == 2) score = 5;
        else score = 7;
        
        //cout << "score for " << col << " is set to " << score << endl;
        
        board.AI[col] = score;
        
        
    }
    // simulate defense and score
    for (int col = 0; col < 7; col++) {
        
        row = 6 - board.board[0][col];
        
        // for all seven rows we now have the row,col location of the drop.
        
        board.max = maxLine(board,row,col,false); // checking defense
        
        if (board.max == 4) score = 2;
        else if (board.max == 3) score = 4;
        else if (board.max == 2) score = 6;
        else score = 7;
        
        if (score < board.AI[col]) board.AI[col] = score; // if the score is lower, it is overridden
        
    }
    
    // Now we have an array of seven choices.
    int bestCol = 0;
    int bestScore = 10;
    
    for (int kol = 0; kol < 7; kol++) {
        
        //cout << AI[kol] << endl;

        if (board.AI[kol] < bestScore) {
            
            bestScore = board.AI[kol];
            bestCol = kol;
            
        } // if the score is good, this number becomes the best column
        
    }
    srand(time(NULL));
    if (bestScore >= 7) bestCol = rand() % 6; // == 7 IS HARD MODE. 3 IS EASY MODE.
    //cout << "The best column for me to choose is " << bestCol+1 << endl;
    
    // now, finally, we can place the piece.
    int bestRow = 6 - board.board[0][bestCol];
    
    
    board.board[bestRow][bestCol] = 1; // adding in
    
	board.board[0][bestCol]++; // incrementing the count
    
	switchIsX(board);
    
	changed = true;
        board.testing = false;
    
	board.over = checkOver(board, bestRow, bestCol, board.board[bestRow][bestCol]);
	printBoard(board, changed);

    
    if (board.over) printf("The computer has won! ");
    
    board.testing = false;
    
    return changed;
    
}

int maxLine(struct GameBoard board, int row, int col, bool isX) { // moves, calculates, undoes
    
    int player; // X or 0
    
    if (isX) player = 1; else player = 2;
    
    if (board.board[0][col] == 6) return 0;
    
    board.board[row][col] = player;
    
    checkOver(board, row, col, player); // now this will store, temporarily, the max line available
    
    board.board[row][col] = 0; // undo
    
    //cout << "The max for " << row << "," << col << " is " << getMax() << endl;
    
    return getMax(board);
    
}

bool checkOver(struct GameBoard board, int row, int column, int player) {
    
    board.max = 0;

	int topCheck = 0;

	while (board.board[0][topCheck] == 6) { // check to see if all columns are full

		if (topCheck == 6) return true;
		topCheck++;

	}

	int checkNum = player; // set check to be whatever the player's move was, X or 0, equaling 1 or 2 in the data structure.

	int consecCount = 0; // a counter for consecutive tiles in a line

	//search horizontal row in question
	for (int i = 0; i < 7; i++) {

		if (board.board[row][i] != checkNum) consecCount = 0;
		else {
            
            consecCount++;
            if (consecCount > board.max) board.max = consecCount;
        
        }
		if (consecCount == 4) {

			if (!board.testing) printf("Horizontal line! ");

			return true;
		}


	}

	consecCount = 0;

	//search vertical column in question
	for (int i = 1; i < 7; i++) {

		if (board.board[i][column] != checkNum) consecCount = 0;
		else {
            
            consecCount++;
            if (consecCount > board.max) board.max = consecCount;
            
        }
		if (consecCount == 4) {

			if (!board.testing) printf("Vertical line! ");

			return true;
		}

	}

	consecCount = 0;

	// search forward slash bottom left to upper right
	int lowerRow; int upperRow;
	int lowerCol; int upperCol;

	// WHILE LOOP FOR FINDING BOUNDS OF / DIAGONAL

	// LOWER BOUND
	//cout << row << "," << column << endl;
	lowerRow = row; lowerCol = column; // setting the starting point to be the position
	while ((lowerRow < 6) && (lowerCol > 0)) {

		lowerCol--; lowerRow++; // move down and left, down and left.

	}

	upperRow = row; upperCol = column; // setting the starting point to be the position
	while ((upperRow > 1) && (upperCol < 6)) {

		upperCol++; upperRow--; // move up and right, up and right.

	}


	// ITERATE THROUGH THE / DIAGONAL
	int iterRow = lowerRow; int iterCol = lowerCol; // we have the bounds, so start at the lower left

	//cout << "Starting at " << lowerRow << "," << lowerCol << " and ending at " << upperRow << "," << upperCol << endl;

	while ((iterRow >= upperRow) && (iterCol <= upperCol)) {

		//cout << "Checking for " << checkNum << endl;

		if (board.board[iterRow][iterCol] != checkNum) consecCount = 0;
		else {

			consecCount++;
            if (consecCount > board.max) board.max = consecCount;
            //cout << "Found " << consecCount << endl;

		}
		if (consecCount == 4) {

			if (!board.testing) printf("Forward diagonal line! "); // something in here is causing bugs. Forward slash diag.

			return true;
		}

		iterRow--; iterCol++;
	}

	// Finally, find bounds of the \ diagonal

	lowerRow = row; lowerCol = column; // setting the starting point to be the position
	while ((lowerRow < 6) && (lowerCol < 6)) {

		lowerCol++; lowerRow++; // move down and right, down and right.

	}

	upperRow = row; upperCol = column; // setting the starting point to be the position
	while ((upperRow > 1) && (upperCol > 0)) {

		upperCol--; upperRow--; // move up and right, up and right.

	}


	// ITERATE THROUGH THE / DIAGONAL
	iterRow = upperRow; iterCol = upperCol; // we have the bounds, so start at the lower left

	//cout << "Starting at " << upperRow << "," << upperCol << " and ending at " << lowerRow << "," << lowerCol << endl;

	while ((iterRow <= lowerRow) && (iterCol <= lowerCol)) {

		//cout << "Checking for " << checkNum << endl;

		if (board.board[iterRow][iterCol] != checkNum) consecCount = 0;
		else {

			consecCount++; //cout << "Found " << consecCount << endl;
            if (consecCount > board.max) board.max = consecCount;

		}
		if (consecCount == 4) {

			if (!board.testing) printf("Backward diagonal line! ");

			return true;
		}

		iterRow++; iterCol++;

	}
	return false;
}


bool action(struct GameBoard board, int columnNum, bool isItX) {
  
        if (columnNum != 1 && columnNum != 2 &&
                columnNum != 3 && columnNum != 4 &&
                columnNum != 5 && columnNum != 6 && columnNum != 7) {

                printf("That's not a valid move. Please enter a column 1-7, or q to quit.\n");
                return false;
        }

        bool changed = false;

        int column = columnNum-1;

        if (board.board[0][column] == 6) {

                printf("That column is full! Try again.\n");

                return changed;

        } // if the invisible top layer says it's full

        int row = 6 - board.board[0][column];

        if (board.isX) {

                board.board[row][column] = 1;
        } // placing the piece!
        else board.board[row][column] = 2;

        board.board[0][column]++;

        switchIsX(board); // DO WE CALL IT ON BOARD?

        changed = true;

        board.over = checkOver(board, row, column, board.board[row][column]); // REMOVE FINAL ARGUMENT PROBABLY
        printBoard(board, changed);

    if (board.over) return changed;
    
    if ((board.aiOn == true) && (changed)) aiTurn(board);
    
        return changed;

}

int main()
{

        struct GameBoard theBoard;
        initialize(theBoard);
        printf("Hello, player!\nWould you like to play against the AI? (y/n)\n");
        char * ans;
        fgets (ans, 100, stdin);
    
    while ((strcmp(ans, "y") && (strcmp(ans, "n")))) {
        
        printf("Try again, that's not a valid option.\n");
        fgets(ans, 100, stdin);
    }
    
    if ((!strcmp(ans,"y"))) {
        
        printf("Okay, you'll be going first! Enter your desired column number, 1-7.\n");
        
        setAI(theBoard);
    
    }
    
    else {
    
        printf("Okay, two players it is! 0 goes first! Enter your desired column number, 1-7.\n");
        
    }

        printBoard(theBoard, true);

        // theBoard.printBoard(true);

        // string move;

        // cin >> move;

        char * move;
        fgets (move, 100, stdin);

        while (strcmp(move, "q")) {
        
        int column = atoi(move); // making it one smaller LOL THIS?

                action(theBoard, column, getIsX(theBoard));
                if (getOver(theBoard)) {

                        printf("Game over! Play again? (y/n)\n");
                        char answer[100];
                        fgets (answer, 100, stdin);

                        while ((strcmp(answer, "y") && (strcmp(answer, "n")))) { 
                                
                                printf("Try again, that's not a valid option.\n"); 
                                fgets(answer, 100, stdin);
                        }

                        if (!strcmp(answer, "n")) { return 0; }
                        if (!strcmp(answer, "y")) { main(); }

                        return 0;

                }

                fgets(move, 100, stdin);
        }

        return 0;
}