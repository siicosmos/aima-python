/*
Cmpt 310 assignment 5
Created by Liam Ling
Date: Mon July 29 2019
Decription: inplementation of monte carlo tree search algorithm
Note: this tree search algorithm is modified from previous python version of assignment 4
*/

#include <chrono> // for calculating elapsing time
#include <random> // for generating random number in unifor distribution
#include <cmath> // for calculating squre root
#include <algorithm> // for find element in vector
#include <vector> // for constructing vector
#include <tuple> // return multiple values
#include <iostream>

using namespace std;

template<class Node, class State>
tuple<Node*, int, chrono::duration<double>> MonteCarloTreeSearch(State* current_state, int iteration_max, Node* current_node, chrono::duration<double> timeout, int player, int move) {
    Node* root;
    int iteration;
    chrono::duration<double> elapsed_time = chrono::duration<double>(0.0);
    if(current_node != nullptr) {
        root = current_node;
    } else {
        root = new Node(current_state);
    }
    root -> set_move(move);
    root -> set_player(player);

    auto start = chrono::system_clock::now();
    for(iteration = 0; iteration < iteration_max; iteration ++) {
        Node* node = root;
        
        // selection
        while(node -> fully_expaned() && node -> children_exist()) {
            node = node -> select();
        }
        
        // expantion
        if(!node -> fully_expaned()) {   
            node = node -> expand();
        }

        // rollout
        int switch_player = node -> get_player();
        State* rollout_state = new State(*(current_state));
        while(!rollout_state -> game_over()) {
            vector<int> possible_moves = rollout_state -> legal_moves();
            random_shuffle(possible_moves.begin(), possible_moves.end());
            rollout_state -> move(possible_moves[0], -switch_player);
            switch_player = -switch_player;
        }

        // backpropagate
        while(node != nullptr) {
            node -> update(rollout_state -> get_result());
            node = node -> get_parent();
        }

        auto end = chrono::system_clock::now();
        elapsed_time = end - start;
        if(elapsed_time > timeout) {
            break;
        }
    }

    Node* ptr = nullptr;
    auto best = [](Node* node) {
		return double(node -> get_number_wins()) / double(node -> get_number_visits());
	};
	vector<double> result;
	for(int i = 0; i < root -> get_children().size(); i ++) {
		result.push_back(best(root -> get_children()[i]));
	}

    cout << "After " << iteration << " iterations, AI thinks the ";
    cout << "Win Rates: " << endl;
    for(int index = 0; index < result.size(); index++) {
        cout << "Move: " <<  root -> get_children()[index] -> get_move()+1 << "  Rate: " << result[index]*100.0 << "%" << endl;
    }

	double largest = result[0];
	int largest_index = 0;
	for(int index = 1; index < result.size(); index++) {
		if(result[index] > largest) {
       		largest = result[index];
			largest_index = index;
    	}
	}

	ptr = root -> get_children()[largest_index]; // return child as a pointer

    return make_tuple(ptr, ptr -> get_move(), elapsed_time);
}