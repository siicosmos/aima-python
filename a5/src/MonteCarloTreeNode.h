/*
Cmpt 310 assignment 5
Created by Liam Ling
Date: Mon July 29 2019
Decription: interface of monte carlo tree node class
Note: this tree node is modified from previous python version of assignment 4
*/

#ifndef MONTECARLOTREENODE_H
#define MONTECARLOTREENODE_H
#endif

#include <random> // for generating random number in unifor distribution
#include <vector> // for constructing vector
#include <cmath> // for calculating squre root
#include <algorithm> // for find element in vector
#include <limits>

using namespace std;

template <class State>
class MonteCarloTreeNode
{
private:
	State* state;
	int move;
	int player;
	MonteCarloTreeNode<State>* parent;
	vector<MonteCarloTreeNode<State>*> children;
	double number_wins;
	unsigned number_visits;
	vector<int> unexplored_children;
	double uct_constant = sqrt(2.0);
public:
	// constructors
	MonteCarloTreeNode();
	MonteCarloTreeNode(State* state);
	MonteCarloTreeNode(State* state, MonteCarloTreeNode<State>* parent, int move);
	// destructor
	~MonteCarloTreeNode();
	// setter
	void set_state(State* state);
	void set_move(int move);
	void set_player(int player);
	void set_parent(MonteCarloTreeNode<State>* parent);
	void set_children(vector<MonteCarloTreeNode<State>*> children);
	void set_number_wins(double number_wins);
	void set_number_visits(unsigned number_visits);
	void set_unexplored_children(vector<int> unexplored_children);
	// getter
	State* get_state() const;
	int get_move() const;
	int get_player() const;
	MonteCarloTreeNode<State>* get_parent() const;
	vector<MonteCarloTreeNode<State>*> get_children() const;
	double get_number_wins() const;
	unsigned get_number_visits() const;
	vector<int> get_unexplored_children() const;
	// methods
	bool fully_expaned();
	bool children_exist();
	bool terminal_node();
	int expansion_policy();
	MonteCarloTreeNode<State>* select();
	MonteCarloTreeNode<State>* expand();
	void update(double game_result);
	// operators
	template <typename T> 
	friend ostream& operator << (ostream& os, const vector<T>& vec);
};

// constructors
template <class State>
MonteCarloTreeNode<State>::MonteCarloTreeNode() {
	set_player(-1);
	set_parent(nullptr);
	vector<MonteCarloTreeNode<State>*> temp_children;
	set_children(temp_children);
	set_number_wins(0);
	set_number_visits(0);
	vector<int> temp_unexplored_children;
	set_unexplored_children(temp_unexplored_children);
}

template <class State>
MonteCarloTreeNode<State>::MonteCarloTreeNode(State* state) {
	set_player(state -> get_player());
	set_state(state);
	set_parent(nullptr);
	vector<MonteCarloTreeNode<State>*> temp_children;
	set_children(temp_children);
	set_number_wins(0);
	set_number_visits(0);
	vector<int> temp_unexplored_children = get_state() -> legal_moves();
	set_unexplored_children(temp_unexplored_children);;
}

template <class State>
MonteCarloTreeNode<State>::MonteCarloTreeNode(State* state, MonteCarloTreeNode<State>* parent, int move) {
	set_player(state -> get_player());
	set_state(state);
	set_move(move);
	set_parent(parent);
	vector<MonteCarloTreeNode<State>*> temp_children;
	set_children(temp_children);
	set_number_wins(0);
	set_number_visits(0);
	vector<int> temp_unexplored_children = get_state() -> legal_moves();
	set_unexplored_children(temp_unexplored_children);
}

// destructor
template <class State>
MonteCarloTreeNode<State>::~MonteCarloTreeNode() {
}

// setter
template <class State>
void MonteCarloTreeNode<State>::set_state(State* state) {
	this -> state = state;
}

template <class State>
void MonteCarloTreeNode<State>::set_move(int move) {
	this -> move = move;
}

template <class State>
void MonteCarloTreeNode<State>::set_player(int player) {
	this -> player = player;
}

template <class State>
void MonteCarloTreeNode<State>::set_parent(MonteCarloTreeNode<State>* parent) {
	this -> parent = parent;
}

template <class State>
void MonteCarloTreeNode<State>::set_children(vector<MonteCarloTreeNode<State>*> children) {
	this -> children = children;
}

template <class State>
void MonteCarloTreeNode<State>::set_number_wins(double number_wins) {
	this -> number_wins = number_wins;
}

template <class State>
void MonteCarloTreeNode<State>::set_number_visits(unsigned number_visits) {
	this -> number_visits = number_visits;
}

template <class State>
void MonteCarloTreeNode<State>::set_unexplored_children(vector<int> unexplored_children) {
	this -> unexplored_children = unexplored_children;
}

// getter
template <class State>
State* MonteCarloTreeNode<State>::get_state() const {
	return state;
}

template <class State>
int MonteCarloTreeNode<State>::get_move() const {
	return move;
}

template <class State>
int MonteCarloTreeNode<State>::get_player() const {
	return player;
}

template <class State>
MonteCarloTreeNode<State>* MonteCarloTreeNode<State>::get_parent() const {
	return parent;
}

template <class State>
vector<MonteCarloTreeNode<State>*> MonteCarloTreeNode<State>::get_children() const {
	return children;
}

template <class State>
double MonteCarloTreeNode<State>::get_number_wins() const {
	return number_wins;
}

template <class State>
unsigned MonteCarloTreeNode<State>::get_number_visits() const {
	return number_visits;
}

template <class State>
vector<int> MonteCarloTreeNode<State>::get_unexplored_children() const {
	return unexplored_children;
}

// methods
template <class State>
bool MonteCarloTreeNode<State>::fully_expaned() {
	return unexplored_children.empty();
}

template <class State>
bool MonteCarloTreeNode<State>::children_exist() {
	return !children.empty();
}

template <class State>
bool MonteCarloTreeNode<State>::terminal_node() {
	return state.game_over();
}

template <class State>
int MonteCarloTreeNode<State>::expansion_policy() {
	random_shuffle(unexplored_children.begin(), unexplored_children.end());
	return 0;
}

template <class State>
MonteCarloTreeNode<State>* MonteCarloTreeNode<State>::select() {

	vector<double> result;
	for(int i = 0; i < children.size(); i ++) {

        double uct_exploitation = children[i]->get_number_wins() / (double)(children[i]->get_number_visits());
        double uct_exploration = sqrt( log((double)get_number_visits()) / (double)(children[i]->get_number_visits()) );
        double uct_score = uct_exploitation + uct_constant * uct_exploration;

		result.push_back(uct_score);
			
	}

	double largest = result[0];
	int largest_index = 0;
	for(int index = 1; index < result.size(); index++) {
		if(result[index] > largest) {
       		largest = result[index];
			largest_index = index;
    	}
	}
	return children[largest_index];
}

template <class State>
MonteCarloTreeNode<State>* MonteCarloTreeNode<State>::expand() {
	int random = expansion_policy();
	int next_move = unexplored_children[random];
	State* next_state = new State(*get_state());
	next_state -> move(next_move, -get_player());
	MonteCarloTreeNode<State>* child = new MonteCarloTreeNode<State>(next_state, this, next_move);
	children.push_back(child);
	unexplored_children.erase(unexplored_children.begin()+random);
	return child;
}

template <class State>
void MonteCarloTreeNode<State>::update(double result) {
	set_number_visits(get_number_visits() + 1.0);
	set_number_wins(get_number_wins() + result);
}

// operators
template <typename T> 
ostream& operator << (ostream& os, const vector<T>& vec) {
    os << "[";
    for(auto i = vec.begin(); i != vec.end(); ++i) {
        os << " " << *i;
    }
    os << " ]";
    return os;
}
//