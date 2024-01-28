#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    char buffer[10];
    if (argc < 2) {
        printf("Usage: %s <input string>\n", argv[0]);
        return 1;
    }
    strncpy(buffer, argv[1], sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0'; // Ensure null termination
    printf("You entered: %s\n", buffer);
    return 0;
}
