#include <stdio.h>

int main(int argc, char *argv[]) {
    char buffer[10];
    if (argc < 2) {
        printf("Usage: %s <input string>\n", argv[0]);
        return 1;
    }
    sprintf(buffer, "Input: %s", argv[1]);
    printf("%s\n", buffer);
    return 0;
}
