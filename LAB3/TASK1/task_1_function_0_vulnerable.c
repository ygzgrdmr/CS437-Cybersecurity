#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    char buffer[10];
    if (argc < 2) {
        printf("Usage: %s <input string>\n", argv[0]);
        return 1;
    }
    strcpy(buffer, argv[1]);
    printf("You entered: %s\n", buffer);
    return 0;
}
