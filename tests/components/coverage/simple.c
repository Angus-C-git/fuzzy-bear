#include <stdio.h>

void
function1()
{
    char buf[10];
    gets(&buf);

    // printf("%s\n", buf);

    int hex_cmp;

    if (0x9 == 9)
        hex_cmp = 1;
    else
        hex_cmp = 0;
}


int 
main(int argc, char const *argv[])
{
    /* code */
    int answer;
    printf("grabage data");
    
    // just call another function
    function1();

    // cmp 1, 1
    if (1 == 1)
        answer = 1;

    return 0;
}
