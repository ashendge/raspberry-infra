#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    printf("Parent PID: %d\n", getpid());
    pid_t pid = fork();
    if (pid == 0) {
        execlp("./cputest", "cputest", NULL);
    } else {
        wait(NULL);
        printf("Child finished\n");
    }
    return 0;
}

