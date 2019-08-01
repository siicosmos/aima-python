/*
Cmpt 310 assignment 5
Created by Liam Ling
Date: Mon July 29 2019
Decription: implementation of connect 4 game class
*/

#include <iostream>
#include <string> // for test winning
#include <iterator> // for ostream_iterator
#include <sstream> // for str()
#include <algorithm> // for find element in vector
#include "Connect4.h"

using namespace std;

// constructor
Connect4::Connect4() {
    width = 0;
    height = 0;
    board = {{}};
    player = 0;
    /*
	player == 1 player
	player == -1 opponent
	Player == 0 unspecified */
}

Connect4::Connect4(int width, int height){
    this -> width = width;
    this -> height = height;
    board.resize(height);
    for(int i = 0; i < height; i ++) {
        board[i].resize(width);
    }
    player = 1;
}

// copy constructor
Connect4::Connect4(const Connect4 &copy) {
    width = copy.width;
    height = copy.height;
    board = copy.board;
    player = copy.player;
}

// destructor
Connect4::~Connect4() {
}

// operator
Connect4& Connect4::operator = (Connect4 rhs) {
    swap(width, rhs.width);
    swap(height, rhs.height);
    swap(board, rhs.board);
    swap(player, rhs.player);
    return *this;
}

// setters
void Connect4::set_board(vector<vector<int>> board){
    this -> board = board;
}

void Connect4::set_width(int width)  {
    this -> width = width;
}

void Connect4::set_height(int height) {
    this -> height = height;
}

void Connect4::set_player(int player) {
    this -> player = player;
}

// getters
vector<vector<int>> Connect4::get_board() const {
    return board;
}

int Connect4::get_width() const {
    return width;
}

int Connect4::get_height() const {
    return height;
}

int Connect4::get_player() const {
    return player;
}

// methods
void Connect4::move(int move, int player) {
    this -> player = player;
    if(!is_legal_move(move)) {
        cout << "Error: the move is not a legal move" << endl;
    } else {
        for(int row = height-1; row >= 0; row --) {
            if(board[row][move] == 0) {
                board[row][move] = player;
                break;
            }
        }
    }
}

bool Connect4::has_move() {
    return !(this -> legal_moves().empty());
}

bool Connect4::is_legal_move(int move) {
    // if(player == this -> player) {
    //     if(player == 1) {
    //         cout << "Error: the AI played last move, the current move should be played by human" << endl;
    //     } else if(player == -1) {
    //         cout << "Error: the human played last move, the current move should be played by AI" << endl;
    //     } else if(player == 0) {
    //         cout << "Error: please specify the player" << endl;
    //     }
    //     return false;
    // }
    // cout << "is legal move" << endl;
    vector<int> legal_moves = this -> legal_moves();
    auto itr = find(legal_moves.begin(), legal_moves.end(), move);
    if(itr == legal_moves.end()) {
        return false;
    }
    return true;
}

vector<int> Connect4::legal_moves() {
    vector<int> legal_moves;
    for(int col = 0; col < width; col ++) {
        if(board[0][col] == 0) {
            legal_moves.push_back(col);
        }
    }
    return legal_moves;
}

int Connect4::get_result() {
    if(get_winner() == -1) { // 1 is player wins
        return 1.0;
    } else if(get_winner() == 1) { // -1 is opponent wins
        return 0.0;
    } else if(get_winner() == 2) { // 2 is draw
        return 0.5;
    }
}

int Connect4::get_winner() {
    int result = 0;
    if(has_move()) {
        for(auto itr = board.begin(); itr != board.end(); itr ++) {
            string temp;
            for(int i = 0; i < (*itr).size(); i++) {
                if((*itr)[i] == 1) {
                    temp += "o";
                } else if((*itr)[i] == -1) {
                    temp += "x";
                } else if((*itr)[i] == 0) {
                    temp += "*";
                }
            }
            result = contains_win_set(temp);
            if(result != 0) {
                return result;
            }
        }

        vector<vector<int>> trans = transpose();
        for(auto itr = trans.begin(); itr != trans.end(); itr ++) {
            string temp;
            for(int i = 0; i < (*itr).size(); i++) {
                if((*itr)[i] == 1) {
                    temp += "o";
                } else if((*itr)[i] == -1) {
                    temp += "x";
                } else if((*itr)[i] == 0) {
                    temp += "*";
                }
            }
            result = contains_win_set(temp);
            if(result != 0) {
                return result;
            }
        }

        vector<int> temp_left;
        vector<int> temp_right;
        for(int row = 0; row < height-row; row ++) {
            for(int col = 0; col < ((height-row) < width ? (height-row):width); col ++) {
                // cout << "(" << row+col << ", " << col << ") " << board[row+col][col] << endl;
                // cout << "(" << width-2-col << ", " << col << ") " << board[width-2-col][col] << endl;
                temp_left.push_back(board[row+col][col]);
                temp_right.push_back(board[row+col][width-1-col]);
            }
            if(temp_left.size() >= 4) {
                string temp;
                for(int i = 0; i < temp_left.size(); i++) {
                    if(temp_left[i] == 1) {
                    temp += "o";
                    } else if(temp_left[i] == -1) {
                        temp += "x";
                    } else if(temp_left[i] == 0) {
                        temp += "*";
                    }
                }
                result = contains_win_set(temp);
                if(result != 0) {
                    return result;
                }
            }
            if(temp_right.size() >= 4) {
                string temp;
                for(int i = 0; i < temp_right.size(); i++) {
                    if(temp_right[i] == 1) {
                    temp += "o";
                    } else if(temp_right[i] == -1) {
                        temp += "x";
                    } else if(temp_right[i] == 0) {
                        temp += "*";
                    }
                }
                result = contains_win_set(temp);
                if(result != 0) {
                    return result;
                }
            }
            temp_left.clear();
            temp_right.clear();
        }

        for(int col = 1; col < width-col; col ++) {
            for(int row = 0; row < ((width-col) < height ? (width-col):height); row ++) {
                temp_left.push_back(board[row][col+row]);
                temp_right.push_back(board[row][width-1-col-row]);
            }
            if(temp_left.size() >= 4) {
                string temp;
                for(int i = 0; i < temp_left.size(); i++) {
                    if(temp_left[i] == 1) {
                    temp += "o";
                    } else if(temp_left[i] == -1) {
                        temp += "x";
                    } else if(temp_left[i] == 0) {
                        temp += "*";
                    }
                }
                result = contains_win_set(temp);
                if(result != 0) {
                    return result;
                }
            }
            if(temp_right.size() >= 4) {
                string temp;
                for(int i = 0; i < temp_right.size(); i++) {
                    if(temp_right[i] == 1) {
                    temp += "o";
                    } else if(temp_right[i] == -1) {
                        temp += "x";
                    } else if(temp_right[i] == 0) {
                        temp += "*";
                    }
                }
                result = contains_win_set(temp);
                if(result != 0) {
                    return result;
                }
            }
            temp_left.clear();
            temp_right.clear();
        }
        return 0;
    } else if(!has_move()) {
        return 2;
    }
}

int Connect4::contains_win_set(string str) {
    string human = "oooo";
    string ai = "xxxx";

    if(str.find(human) != string::npos) {
        return 1;
    } else if(str.find(ai) != string::npos) {
        return -1;
    }
    return 0;
}

vector<vector<int>> Connect4::transpose() {
    vector<vector<int>> trans(board[0].size(), vector<int>());
    if (board.size() == 0)
        return trans;
    for(int i = 0; i < board.size(); i++) {
        for(int j = 0; j < board[i].size(); j++) {
            trans[j].push_back(board[i][j]);
        }
    }
    return trans;
}

bool Connect4::game_over() {
    if(get_winner() != 0) {
        return true;
    } else {
        return false;
    }
}

void Connect4::print_game_board() {
    for(auto itr = board.begin(); itr != board.end(); itr ++) {
        for(auto itr_inner = (*itr).begin(); itr_inner != (*itr).end(); itr_inner ++) {
            if(*itr_inner == 0) {
                cout << "*";
            } else if(*itr_inner == -1) {
                cout << "X";
            } else if(*itr_inner == 1) {
                cout << "O";
            }
            if(itr_inner != (*itr).end()) {
                cout << " ";
            } 
        }
        cout << endl;
    }
    for(int i = 1; i <= width; i ++) {
        cout << i << " ";
        if(i == width) {
            cout << endl;
        }
    }
}
