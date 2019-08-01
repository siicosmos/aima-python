/*
Cmpt 310 assignment 5
Created by Liam Ling
Date: Mon July 29 2019
Decription: interface of connect 4 game class
*/

#ifndef CONNECT4_H
#define CONNECT4_H
#endif

#include <vector>

using namespace std;

class Connect4
{
private:
	vector<vector<int>> board;
	int width;
	int height;
	int player; 
	/*
	player == 1 human
	player == -1 AI
	Player == 0 unspecified */
public:
	// constructor
	Connect4();
	Connect4(int width, int height);
	// copy constructor
	Connect4(const Connect4 &copy);
	// destructor
	~Connect4();
	// operator
	Connect4& operator = (Connect4 rhs);
	// setters
	void set_board(vector<vector<int>> board);
	void set_width(int width);
	void set_height(int height);
	void set_player(int player);
	// getters
	vector<vector<int>> get_board() const;
	int get_width() const;
	int get_height() const;
	int get_player() const;
	// methods
	void move(int move, int player);
	bool has_move();
	bool is_legal_move(int move);
	vector<int> legal_moves();
	int get_result();
	int get_winner();
	int contains_win_set(string copy);
	vector<vector<int>> transpose();
	bool game_over();
	void print_game_board();
};