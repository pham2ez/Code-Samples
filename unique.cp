#include <iostream>
#include <vector>
#include <string>
#include <math.h>

using namespace std;
bool UniqueNumbers(unsigned int num)
{
    
    string number = to_string(num);
    unsigned int use = num;
    unsigned int length = number.length();
    vector<int> digits(length);
    //creates a vector with all of the digits of the number in it and also checks to see if there are any repeats in the vector(repeating numbers)
    for(int numPos=0; numPos<length; numPos++){
        digits[use%10] += 1;
        int use = floor(use/10);
        if (digits[numPos] > 1){
            return false;
        }
    }
    return true;
}

//test runs
int main()
{
    cout<<12345<<endl;
    cout<<AllDigitsUnique(12345)<<endl;
    cout<<11111<<endl;
    cout<<AllDigitsUnique(11111)<<endl;
    cout<<112233<<endl;
    cout<<AllDigitsUnique(112233)<<endl;
    cout<<142908<<endl;
    cout<<AllDigitsUnique(142908)<<endl;
    return 0;
}



