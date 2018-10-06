#include <iostream>

using namespace std;

char* SortingLetters(char* string, char* sortOrder){
    int stringLen = strlen(string);
    int sortLen = strlen(sortOrder);
    int currentPos = 0;
    char answer[stringLen];
    //uses the sortOrder to easily assemble the sorted char*
    for(int i=0;i<sortLen;i++){
        char currentLetter = sortOrder[i];
        for(int j=0; j<stringLen; j++){
            if(currentLetter==string[j]){
                answer[currentPos] = currentLetter;
                currentPos++;
            }
        }
    }
    //copies array over to pointer
    char* original = string;
    for(int i=0;i<stringLen;i++){original[i] = answer[i];}
    return original;
}

//test runs with alphabet+keyboard sliding
int main()
{
    char* amazing = strdup("qwertyuiopasdfghjklzxcvbnmabbcccddddeeeee");
    char* wonderful = strdup("abcdefghijklmnopqrstuvwxyz");
    cout<<SortLetters(amazing, wonderful)<<endl;
    return 0;
}
