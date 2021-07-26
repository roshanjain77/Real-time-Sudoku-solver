#include <bits/stdc++.h>
using namespace std;


class Solution {
public:
    
    bool box(vector<vector<int>> & board,int i,int j,int n){
        i=i/3,j=j/3;
        i=i*3,j=j*3;
            
        for(int x=i;x<i+3;x++)for(int y=j;y<j+3;y++)if(board[x][y]==n)return false; 
            
        return true;
    }    
        
    bool check(vector<vector<int>> & board,int i,int j,int n){
            
        int size=board.size();
        for(int row=0;row<size;row++) if(board[row][j]==n) return false;
        for(int col=0;col<size;col++) if(board[i][col]==n) return false; 
        return true;        
            
    }     
        
    bool solver(vector<vector<int>> &board,int i,int j){
            
        if(i>=board.size()-1 && j>=board.size()) return true;
            
        if(j == board.size()){
           if(solver(board,i+1,0)) return true;
           return false;
        }
            
        if(board[i][j]==0){
                
            for(int n=1;n<10;n++){    
                if(check(board,i,j,n) && box(board,i,j,n)){
                      board[i][j] = n;  
                      if(solver(board,i,j+1))return true;
                      board[i][j]=0;
                }    
            }    
             return false;
        }    
       if(solver(board,i,j+1))return true;
            
     return false;       
    }    
        
    void solveSudoku(vector<vector<int>>& board) {
        
        solver(board,0,0);    
            
    }
};


int main() {

    vector<vector<int>> board(9, vector<int> (9));

    for(int i=0;i<9;i++) {
        for(int j=0;j<9;j++) {
            cin >> board[i][j];
        }
    }

    Solution a;
    a.solveSudoku(board);

    for(int i=0;i<9;i++) {
        for(int j=0;j<9;j++) {
            cout << board[i][j] << " ";
        }
        cout << endl;
    }

}