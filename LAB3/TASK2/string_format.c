#include <stdio.h>

int main() {
    char inputString[100];

    printf("Enter a string: ");
    fgets(inputString, sizeof(inputString), stdin); // Reads a line of text, including spaces

    // Directly pass the user's input to printf
    printf(inputString);

    return 0;
}
