#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIZE 30

void toLowerCase(char plain[], int ps)
{
    int i;
    for (i = 0; i < ps; i++)
    {
        if (plain[i] >= 'A' && plain[i] <= 'Z')
        {
            plain[i] += 32;
        }
    }
}

int removeSpaces(char *plain, int ps)
{
    int i, count = 0;
    for (i = 0; i < ps; i++)
    {
        if (plain[i] != ' ')
        {
            plain[count++] = plain[i];
        }
    }
    plain[count] = '\0';
    return count;
}

void generateKeyTable(char key[], int ks, char keyT[5][5])
{
    int dicty[26] = {0}; // Dictionary to keep track of letters already in the key
    int i, j, k;

    // Initialize key table positions
    for (i = 0; i < 5; i++)
    {
        for (j = 0; j < 5; j++)
        {
            keyT[i][j] = '\0';
        }
    }

    // Add the keyword to the key table
    i = 0;
    j = 0;
    for (k = 0; k < ks; k++)
    {
        if (key[k] == 'j')
            key[k] = 'i'; // Treat 'J' as 'I'
        if (!dicty[key[k] - 'a'])
        {
            dicty[key[k] - 'a'] = 1;
            keyT[i][j++] = key[k];
            if (j == 5)
            {
                i++;
                j = 0;
            }
        }
    }

    // Fill the rest of the key table with the remaining letters
    for (k = 0; k < 26; k++)
    {
        if (k + 'a' == 'j')
            continue; // Skip 'J', as it's represented by 'I'
        if (!dicty[k])
        {
            keyT[i][j++] = k + 'a';
            if (j == 5)
            {
                i++;
                j = 0;
            }
        }
    }
}

void search(char keyT[5][5], char a, char b, int arr[])
{
    int i, j;

    if (a == 'j')
        a = 'i';
    if (b == 'j')
        b = 'i';

    for (i = 0; i < 5; i++)
    {
        for (j = 0; j < 5; j++)
        {
            if (keyT[i][j] == a)
            {
                arr[0] = i;
                arr[1] = j;
            }
            else if (keyT[i][j] == b)
            {
                arr[2] = i;
                arr[3] = j;
            }
        }
    }
}

int mod5(int a)
{
    return (a % 5);
}

int prepare(char str[], int ptrs)
{
    if (ptrs % 2 != 0)
    {
        str[ptrs++] = 'z';
        str[ptrs] = '\0';
    }
    return ptrs;
}

void encrypt(char str[], char keyT[5][5], int ps)
{
    int i, a[4];

    for (i = 0; i < ps; i += 2)
    {
        search(keyT, str[i], str[i + 1], a);

        if (a[0] == a[2])
        {
            // Same row
            str[i] = keyT[a[0]][mod5(a[1] + 1)];
            str[i + 1] = keyT[a[0]][mod5(a[3] + 1)];
        }
        else if (a[1] == a[3])
        {
            // Same column
            str[i] = keyT[mod5(a[0] + 1)][a[1]];
            str[i + 1] = keyT[mod5(a[2] + 1)][a[1]];
        }
        else
        {
            // Rectangle swap
            str[i] = keyT[a[0]][a[3]];
            str[i + 1] = keyT[a[2]][a[1]];
        }
    }
}

void decrypt(char str[], char keyT[5][5], int ps)
{
    int i, a[4];

    for (i = 0; i < ps; i += 2)
    {
        search(keyT, str[i], str[i + 1], a);

        if (a[0] == a[2])
        {
            // Same row
            str[i] = keyT[a[0]][mod5(a[1] - 1 + 5)];
            str[i + 1] = keyT[a[0]][mod5(a[3] - 1 + 5)];
        }
        else if (a[1] == a[3])
        {
            // Same column
            str[i] = keyT[mod5(a[0] - 1 + 5)][a[1]];
            str[i + 1] = keyT[mod5(a[2] - 1 + 5)][a[1]];
        }
        else
        {
            // Rectangle swap
            str[i] = keyT[a[0]][a[3]];
            str[i + 1] = keyT[a[2]][a[1]];
        }
    }
}

void encryptByPlayfairCipher(char str[], char key[])
{
    int ps, ks;
    char keyT[5][5];

    ks = strlen(key);
    ks = removeSpaces(key, ks);
    toLowerCase(key, ks);

    ps = strlen(str);
    toLowerCase(str, ps);
    ps = removeSpaces(str, ps);

    ps = prepare(str, ps);

    generateKeyTable(key, ks, keyT);

    encrypt(str, keyT, ps);
}

void decryptByPlayfairCipher(char str[], char key[])
{
    int ps, ks;
    char keyT[5][5];

    ks = strlen(key);
    ks = removeSpaces(key, ks);
    toLowerCase(key, ks);

    ps = strlen(str);
    toLowerCase(str, ps);
    ps = removeSpaces(str, ps);

    ps = prepare(str, ps);

    generateKeyTable(key, ks, keyT);

    decrypt(str, keyT, ps);
}

void printKeyTable(char keyT[5][5])
{
    int i, j;
    printf("\nPlayfair Key Table:\n");
    for (i = 0; i < 5; i++)
    {
        for (j = 0; j < 5; j++)
        {
            printf("%c ", keyT[i][j]);
        }
        printf("\n");
    }
}

int main()
{
    char str[SIZE], key[SIZE], cipher[SIZE];

    printf("Enter the key text: ");
    fgets(key, SIZE, stdin);
    key[strcspn(key, "\n")] = 0; // Remove the trailing newline

    printf("\nEnter the plain text: ");
    fgets(str, SIZE, stdin);
    str[strcspn(str, "\n")] = 0; // Remove the trailing newline

    // Make a copy of the plaintext for encryption
    strcpy(cipher, str);

    // Generate the key table and print it
    char keyT[5][5];
    generateKeyTable(key, strlen(key), keyT);
    printKeyTable(keyT);

    // Encrypt the plaintext
    encryptByPlayfairCipher(cipher, key);
    printf("\nCipher text: %s\n", cipher);

    // Decrypt the ciphertext
    decryptByPlayfairCipher(cipher, key);
    printf("\nDecrypted text: %s\n", cipher);

    return 0;
}