#include <stdio.h>
#include <stdlib.h>

int main() {
    unsigned int balance;
    unsigned int transaction;
    char operation;
    int numTransactions, i;

    // Ask user for the initial balance
    printf("Enter the initial balance: ");
    scanf("%u", &balance);

    // Ask user for the number of transactions
    printf("Enter the number of transactions: ");
    scanf("%d", &numTransactions);

    for (i = 0; i < numTransactions; i++) {
        printf("Enter transaction %d (D for deposit, W for withdrawal followed by amount): ", i + 1);
        scanf(" %c%u", &operation, &transaction);

        if (operation == 'D' || operation == 'd') {
            balance += transaction;
        } else if (operation == 'W' || operation == 'w') {
            if (transaction > balance) {
                printf("Insufficient balance for withdrawal. Transaction skipped.\n");
            } else {
                balance -= transaction;
            }
        } else {
            printf("Invalid operation. Please enter D for deposit or W for withdrawal.\n");
        }
    }

    printf("Final balance: %u\n", balance);

    return 0;
}
