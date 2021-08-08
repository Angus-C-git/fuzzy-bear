#include <stdio.h>

int
absolutely_meaningless()
{
    char keypress[10];

    printf("Congratulations welcome to the meaningless function\n");
    printf("You will find no meaning here ...\n\n");

    printf("Press a key to continue\n");
    gets(&keypress);

    return 42;
}


int 
main(int argc, char const *argv[])
{
    char response[5];

    /* code */
    printf(":::::::: Welcome to the coverage simulator ::::::::\n\n");

    printf("Press x to doubt and continue\n");
    fgets(response, 5, stdin);

    printf("We will now jump to a pointless function\n");
    absolutely_meaningless();
    return 0;
}
