/*
Cmpt 310 assignment 5
Created by Liam Ling
Date: Mon July 29 2019
Decription: main game lopp of connect 4 game class
*/

#include <iostream>
#include <string>
#include <tuple>
#include "MonteCarloTreeNode.h"
#include "MonteCarloTreeSearch.cpp"
#include "Connect4.h"

using namespace std;

template<class Game>
int get_keyboard_input(int width, Game* game) {
    int col = 0;
    bool entered = true;
    while(col < 1 || col > width && !game -> is_legal_move(col-1)) {
        cout << "Please chose a move(1-" << width << "): ";
        entered = false;
        while(!(cin >> col)) {
            entered = true;
            cout << "Please enter a integer" << endl;
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            break;
        }
        if(!entered && !game -> is_legal_move(col-1))
            cout << "The move is illegal" << endl;
    }
    return col;
}

template<class Node, class Game>
void play_a_new_game(Node* node, Game* dummy) {
    int col = 0;
    int move = 0;
    int next_move = 0;
    int current_player = 1;
    int player = 0;
    Node* best_child = nullptr;
    Game* board = node -> get_state();
    int width = board -> get_width();
    int height = board -> get_height();
    
    int iteration_max = 60000;
    chrono::duration<double> elapsed_time = chrono::duration<double>(0.0);
    chrono::duration<double> timeout = chrono::duration<double>(15.0);

    cout << "Connect 4 Game (Width: " << width << " Height: " << height << ")" << endl;
    board -> print_game_board();

    while(true){
        if(current_player == 1) {
            col = get_keyboard_input(width, board);
            move = col-1;
            board -> move(move, current_player);
        } else {
            player = -current_player;
            cout << "AI is thinking..." << endl;
            tie(best_child, next_move, elapsed_time) = MonteCarloTreeSearch(board, iteration_max, node, timeout, player, move);
            cout << "AI placed at column " << next_move+1 << endl;
            node = best_child;
            board -> move(next_move, current_player);
        }
        board -> print_game_board();

        // cout << "player:" << board->get_player() << endl;
        // (node -> get_state()) -> print_game_board();

        if(board -> game_over()) {
            int game_result = board -> get_winner();
            if(game_result == 1) {
                cout << "Human win" << endl;
            } else if(game_result == -1) {
                cout << "AI win" << endl;
            } else if(game_result == 2) {
                cout << "Draw" << endl;
            }
            break;
        } else {
            current_player = -current_player;
        }
    }
}

int main(int argc, char** argv) {
    // initializing
    typedef MonteCarloTreeNode<Connect4> Node;
    typedef Connect4 Game;
    int board_width = 6;
    int board_height = 7;
    int player = 1;

    Game* new_game = new Game(board_width, board_height); 
    Node* root = new Node(new_game);
    
    // enter the game
    play_a_new_game(root, new_game);

    delete root;
    delete new_game;
    return 0;
}