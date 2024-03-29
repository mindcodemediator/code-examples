

#include "pch.h"
#include <iostream>
#include <map>
#include <utility>
#include <string>
#include <iterator>
#include <cstring>
#include <vector>
#include <stack>
#include <cmath>
#include <iomanip>



class AJNode{
	//AJNode both indicates one node on the vertical axis of a matrix but also contains an array of edges to this node
private:
	//member vars
	int size = 0;
	int my_outdegree = 0;
	std::vector<int> connections; //tracks indices of nodes that link to the index of AJNode
	std::vector<double> ratio; //will eventually store what is actually the matrix being multiplied

public:
	//functions
	void addConnection(int add);
	void incrementMyOutDegree();
	int myOutDegree();
	void changeValue(int index, int value);
	int getValue(int index);
	int nodeSize();
	void setRatio(int index, double ratio);
	double getRatio(int index);
};


class AdjacencyList{
	//contains a collection of AJNodes and contains functions for page rank and print
	private:
		//member vars
		std::vector<AJNode> connectionList;
		double roundResult(double num);

	public:
		std::vector<double> PageRank(int powerIterations);
		void PrintRank(std::vector<double> rank, std::map<std::string, int> names);
		void Add(int from, int to);
};

void AJNode::incrementMyOutDegree() {
	//tracks out degree of links from node at this index.
	this->my_outdegree++;
}

int AJNode::myOutDegree() {
	//access private variable
	return this->my_outdegree;
}

void AJNode::changeValue(int index, int value) {
	//access private variable
	this->connections[index] = value;
}

int AJNode::getValue(int index) {
	//access private variable
	return this->connections[index];
}

void AJNode::addConnection(int add) {
	//add if edge doesn't exist yet. temporarily adds connections as index names until out degrees calculated

	std::vector<int>::iterator it;

	for (it = this->connections.begin(); it < this->connections.end(); it++) {
		//iterates through current list and inserts in numerical order	
		if (*it == add) {  //already exists, return
			return;
		}
		else if (*it > add) {  //found a bigger number, add before continuing
			this->connections.insert(it, add);
			return;
		}
	}
	//doesn't need to be inserted, add to the back
	this->connections.push_back(add);
	return;
}

int AJNode::nodeSize() {
	//access private variable
	return this->connections.size();
}

void AJNode::setRatio(int index, double ratio) {
	//access private variable
	if (this->ratio.size() == 0) {
		this->ratio.resize(this->connections.size());
	}
	
	this->ratio[index] = ratio;
}
double AJNode::getRatio(int index) {
	//access private variable
	return this->ratio[index];
}

std::vector<double> AdjacencyList::PageRank(int powerIterations) {
	//finds the connections of pages to each other based on how many pages they link to

	int in_connection, out_degree;
	int size = this->connectionList.size();
	std::vector<double> rank(size);
	std::vector<double> temp(size); //create rank array storing power iterations solutions, will be overwritten with each pass since answer is cumulative

	
	//initialize matrices, since this will iterate over powerIterations, this is essentially powerIterations = 1 pass
	for (int i = 0; i < size; i++) {
		rank[i] = 1 / static_cast<double>(size); //set 2nd matrix
		for (int j = 0; j < this->connectionList[i].nodeSize(); j++) { //set first matrix
			in_connection = this->connectionList[i].getValue(j);
			this->connectionList[i].setRatio(j, 1 / static_cast<double>(this->connectionList[in_connection - 1].myOutDegree())); //track ratio
		}
	}
	
	for (int i = powerIterations; i > 1; i--) {
		for (int j = 0; j < size; j++) {
			temp[j] = 0; //reset for new line
			for (int k = 0; k < this->connectionList[j].nodeSize(); k++) {
				/*because we have stored keys that are like indices, we can solve to know index of second matrix by subtracting 1 (since keys started at 1)
				this way,  we can ignore 0's in imaginary matrix*/
				temp[j] += this->connectionList[j].getRatio(k) * rank[this->connectionList[j].getValue(k) - 1];
			}
			if (temp[j] * 100 < 0){
				temp[j] = 0;//since we only want two decimal places, set to 0 for anything less than hundreths place
			}
		}
		rank = temp;
	}

	return rank;

} //prints the PageRank of all pages

void AdjacencyList::PrintRank(std::vector<double> rank, std::map<std::string, int> names) {
//print, using the string as the key and a map assures alphabetical order
	for (std::pair<std::string, int> page : names)
	{
		std::cout << page.first << " " << std::fixed << std::showpoint << std::setprecision(2) << this->roundResult(rank[page.second - 1]) << "\n";
	}

	return;
}

void AdjacencyList::Add(int from, int to) {
/* checks to see if from and to are already in the node array and resizes
the array if necessary and notes new edge connection
note: this function depends on index "from" being greater that "to"*/

	AJNode from_node, to_node;
	int size = this->connectionList.size();

	if (size < to || size == 0){// this node doesnt exist yet in the connectionList
		to_node.addConnection(from);
		this->connectionList.push_back(to_node);
	}
	else {    //from already exists, add to connection
		this->connectionList[to - 1].addConnection(from);
	}
	if (this->connectionList.size() < from) //from hasn't been created yet, make it as a place holder
		this->connectionList.push_back(from_node);

	//increment outdegree of "to"
	this->connectionList[from - 1].incrementMyOutDegree();
}


double AdjacencyList::roundResult(double num) {
	//function rounds to two decimal places 
	//this does not add the filler zero on the end

	int intValue;

	num *= 100;
	intValue = static_cast<int>(std::round(num));

	return static_cast<double> (intValue) / 100;
}





int main()
{
	int no_of_lines, power_iterations;
	AdjacencyList Created_Graph;
	std::map<std::string, int> pageNames;
	std::vector<double> rank;
	std::string from, to;
	int pageCount = 1;

	typedef std::map<std::string, int>::iterator MapIterator;
	std::pair <MapIterator, bool> from_pair, to_pair;


	std::cin >> no_of_lines;
	std::cin >> power_iterations;


	for (int i = 0; i < no_of_lines; i++)
		//input page connections and store in adjacency list to track edges
	{
		std::cin >> from;
		std::cin >> to;

		//add from and to if unique to  map to make list of site & created key
		
		to_pair = pageNames.insert(std::make_pair(to, pageCount));

		if (to_pair.second == true) {//was unique and successfully inserted into map
			pageCount++;
		}

		if (from != to) {
			from_pair = pageNames.insert(std::make_pair(from, pageCount));

			if (from_pair.second == true) {// value was unique and successfully inserted as new element
				pageCount++;
			}

			Created_Graph.Add(from_pair.first->second, to_pair.first->second);
		}
	}
	//create a matrix
	rank = Created_Graph.PageRank(power_iterations);
	Created_Graph.PrintRank(rank, pageNames);
}



