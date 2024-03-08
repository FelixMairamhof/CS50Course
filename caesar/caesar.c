#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string s);
string get_plaintext(void);
void create_ciphertext(string s, int k);
char rotate(char ch, int key);

int main(int argc, string argv[])
{
    if (argc == 2 && only_digits(argv[1]))
    {
        // Get Key from CommandLine
        int k = atoi(argv[1]);
        string plaintext = get_plaintext();
        create_ciphertext(plaintext, k);

        return 0;
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}
bool only_digits(string s)
{
    int count = 0;
    for (int i = 0; i < strlen(s); i++)
    {
        // if true
        if (isdigit(s[i]))
        {
            count++;
        }
    }
    if (count == strlen(s))
    {
        return true;
    }
    else
    {
        return false;
    }
}
string get_plaintext(void)
{
    return get_string("Plaintext: ");
}
void create_ciphertext(string s, int k)
{
    printf("Ciphertext: ");
    for (int i = 0; i < strlen(s); i++)
    {

        char c = rotate(s[i], k);
        printf("%c", c);
    }
    printf("\n");
}
char rotate(char ch, int key)
{

    if (isalpha(ch))
    {
        char base = isupper(ch) ? 'A' : 'a';
        return ((ch - base + key) % 26) + base;
    }
    return ch; // If not an alphabet, return the character as it is
}
