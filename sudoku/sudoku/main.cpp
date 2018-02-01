#include <stdio.h>
#include <cstdlib>
#include <string.h>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include <map>

class Sudoku;

class Sudoku
{
public:
    int choice;
    int difficulty;
    int sudokuArray[9][9];
    int probArray[9][9];
    
    Sudoku(int choice): choice(choice){};
    Sudoku(){};
    
    void create();
    void createProb();
    void insert(int xMax, int yMax, int check);
    void diagonals();
    void answer();
    friend std::ostream &operator<<(std::ostream &os, const Sudoku &sa);
    friend std::istream &operator<<(std::istream &is, Sudoku &sa);
};

std::ostream &operator<<(std::ostream &os, const Sudoku &sa){
    for (int y = 0; y!= 9; y++) {
        for(int x = 0; x!= 9; x ++){
            int num = sa.probArray[y][x];
            if(num != 0){
                os << sa.sudokuArray[y][x] << " ";
            }
            else{
                os << "_ ";
            }
            if ((x+1)%3 == 0 && x!=8) {
                os << "| ";
            }
        }
        os << "\n";
        if ((y+1)%3 == 0 && y!=8) {
            os << "---------------------\n";
        }
    }
    return os;
}

std::istream &operator>>(std::istream &is, Sudoku &sa){
    int check;
    is >> check;
    is >> sa.difficulty;
    if (check < 1 || check >3){
        sa.choice = 1;
    }
    else{
        sa.choice = check;
    }
    return is;
}

void Sudoku::create(){
    diagonals();
    insert(9,3,2);
    insert(3,9,2);
    insert(6,3,1);
    insert(3,6,1);
    insert(9,6,0);
    insert(6,9,0);
    createProb();
}
void Sudoku::createProb(){
    int mod = 11 - difficulty;
    for (int y = 0; y!= 9; y++) {
        for(int x = 0; x!= 9; x ++){
            int random = rand()%mod;
            if(random != 0){
                probArray[y][x] = sudokuArray[y][x];
            }
            else{
                probArray[y][x] = 0;
            }
        }
    }
}

void Sudoku::answer(){
    for (int y = 0; y!=9; y++) {
        printf(" %i %i %i | %i %i %i | %i %i %i\n", sudokuArray[y][0],sudokuArray[y][1],sudokuArray[y][2],sudokuArray[y][3],sudokuArray[y][4],sudokuArray[y][5],sudokuArray[y][6],sudokuArray[y][7],sudokuArray[y][8]);
        if ((y+1)%3 == 0 && y!=8) {
            std::cout << "-----------------------\n";
        }
    }
}

void Sudoku::insert(int xMax, int yMax, int check){
    std::map<int, std::vector<int>> box;
    int index = 1;
    for(int a = yMax-3; a < yMax; a++){
        for(int b = xMax-3; b < xMax; b++){
            int numbers[2][9] = {{0,0,0,0,0,0,0,0,0}, {0,0,0,0,0,0,0,0,0}};
            std::vector<int> empty;
            
            for (int i = 0; i<9; i++) {
                if (sudokuArray[a][i] != 0) {
                    numbers[0][sudokuArray[a][i]-1] += 1;
                }
            }
            
            for(int i = 0; i<9; i++){
                if (sudokuArray[i][b] != 0) {
                    numbers[1][sudokuArray[i][b]-1] += 1;
                }
            }
            
            for (int i = 0; i < 9; i++) {
                if(numbers[0][i] == 0 && numbers[1][i] == 0){
                    empty.push_back(i);
                }
            }
            box[index] = empty;
            index++;
        }
    }
    
    int numbers[2][9] = {{0,0,0,0,0,0,0,0,0}, {0,0,0,0,0,0,0,0,0}};
    index = 1;
    
    for(int a = yMax-3; a < yMax; a++){
        for(int b = xMax-3; b < xMax; b++){
            if (box[index].size() == 0) {
                sudokuArray[a][b] = 0;
                index++;
            }
            else{
                int counter = 0;
                int current = box[index][counter];
                int times = 0;
                for (int i = 0; i < box[index].size(); i++) {
                    numbers[0][box[index][i]]+=1;
                    if(times == 0 && numbers[0][box[index][i]]>check && numbers[1][box[index][i]] == 0){
                        current = box[index][i];
                        times++;
                    }
                    if(times == 1 && numbers[0][box[index][i]]>check+1 && numbers[1][box[index][i]] == 0){
                        current = box[index][i];
                        times++;
                    }
                }
                times = 0;
            restart:
                if(numbers[1][current]==0){
                    sudokuArray[a][b] = current+1;
                    numbers[1][current]+=1;
                    index++;
                }
                else{
                    counter++;
                    current = box[index][counter];
                    goto restart;
                }
            }
        }
    }
    std::vector<int> empty;
    for(int i = 0; i<9; i++){
        if (numbers[1][i]==0){
            empty.push_back(i);
        }
    }
    for(int a = yMax-3; a < yMax; a++){
        for(int b = xMax-3; b < xMax; b++){
            if(sudokuArray[a][b]==0){
                int numbers[9] = {0,0,0,0,0,0,0,0,0};
                int num;
                for (int i = 0; i<9; i++) {
                    if (sudokuArray[a][i] != 0) {
                        numbers[sudokuArray[a][i]-1] += 1;
                    }
                }
                for (int i = 0; i<9; i++) {
                    if (numbers[i] == 0) {
                        num = i;
                    }
                }
                for (const auto &number : empty) {
                    if(number == num){
                        sudokuArray[a][b] = num+1;
                        break;
                    }
                }
            }
        }
    }
}

void Sudoku::diagonals(){
    int mod = 7+choice*2;
    for(int y = 0; y < 9; y++){
        for(int x = 0; x < 9; x++){
            sudokuArray[y][x] = 0;
        }
    }
    
    for(int i = 3; i < 10; i+=3){
        int unique[9] = {0,0,0,0,0,0,0,0,0};
        for(int y = i-3; y<i; y++){
            for(int x = i-3; x<i; x++){
            here:
                int random = (rand()%mod)%9+1;
                if (unique[random-1]==0) {
                    sudokuArray[y][x] = random;
                    unique[random-1] += 1;
                    mod = 9;
                }
                else{
                    mod++;
                    goto here;
                }
            }
        }
    }
}

void enterAns(Sudoku sudoku){
    int errors = 0;
    for (int a = 0; a < 9; a++) {
        for (int b = 0; b <9; b++) {
            int num;
            if (sudoku.probArray[a][b] == 0) {
                printf("Row %i, Column %i: ",a+1,b+1);
                std::cin >> num;
                if (num == sudoku.sudokuArray[a][b]) {
                    sudoku.probArray[a][b] = num;
                }
            }
        }
    }
    for (int a = 0; a < 9; a++) {
        for (int b = 0; b <9; b++) {
            if (sudoku.probArray[a][b] == 0) {
                printf("Error at row %i, column %i.\n",a+1,b+1);
                errors++;
            }
        }
    }
    if (errors==0) {
        std::cout << "Good job! You got everything right.\nThanks for playing!\n";
    }
    else{
        std::cout << "Do you want to try again? 1 for yes or 2 for no: ";
        int retry;
        std::cin >> retry;
        
        if (retry == 1) {
            std::cout << sudoku;
            enterAns(sudoku);
        }
        else{
            std::cout << "Do you want the solutions? 1 for yes or 2 for no: ";
            int solu;
            std::cin >> solu;
            if (solu == 1) {
                sudoku.answer();
            }
            else{
                std::cout << "Thanks for playing!\n";
            }
        }
    }
}

int main(){
    Sudoku mySudoku;
    std::cout << "Please enter 1, 2, or 3 in order to choose from 3 sudoku pieces and 7, 8, or 9 for easy, medium, or hard: ";
    std::cin >> mySudoku;
    
    mySudoku.create();
    std::cout << mySudoku;
    std::cout << "Once you have finished, enter the numbers accordingly and afterwards, see where you made an error.\n";
    enterAns(mySudoku);
    
    return 0;
}



