#include <stdio.h>

void
dummy_function(void)
{
    printf("Entered dummy\n");
}


int main(int argc, char const *argv[])
{
    /* code */
    printf("Entered main\n");
    dummy_function();

    char dummy_buf[10];
    gets(&dummy_buf);

    return 0;
}
