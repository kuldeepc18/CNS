#include <bits/stdc++.h>
#include <iostream>
using namespace std;

int main()
{
    int key;
    cout << "Enter key: ";
    cin >> key;
    char arr[] = "kuldeepchoudhary294";
    cout << "Original: " << arr << endl;
    for (int i = 0; i < strlen(arr); i++)
    {
        if (isalpha(arr[i]))
        {
            char base = 'a';
            arr[i] = (arr[i] - base + key) % 26 + base;
        }
        else
        {
            char base = '0';
            arr[i] = (arr[i] - base + key) % 10 + base;
        }
    }
    cout << "Encrypted: " << arr << endl;
    for (int i = 0; i < strlen(arr); i++)
    {
        if (isalpha(arr[i]))
        {
            char base = 'a';
            arr[i] = (arr[i] - base - key + 26) % 26 + base;
        }
        else
        {
            char base = '0';
            arr[i] = (arr[i] - base - key + 10) % 10 + base;
        }
    }
    cout << "Decrypted: " << arr << endl;
    return 0;
}