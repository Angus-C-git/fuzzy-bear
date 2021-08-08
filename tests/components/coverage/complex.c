#include <stdio.h>

void
untouchable_code_path(void)
{
    printf("untouchable_code_path\n");
}

void
vulnerable(){
    char hack[10];
    printf("hack me\n");
    gets(&hack);
    
    printf("The password is: but what is coverage?\n");
}


int
function2(int a)
{
    char dummy_buf[100];

    printf("function2\n");

    if (a > 0) {
        vulnerable();
    }

    fgets(dummy_buf, 100, stdin);
    return 0;
}



void
function1()
{

    char safe_buffer[200];
    int sth_foolish;

    printf("function1\n");
    fgets(safe_buffer, 200, stdin);
    printf("enter a number\n");
    scanf("%d", &sth_foolish);

    function2(sth_foolish);
}

int 
main(int argc, char const *argv[])
{
    /* code */
    for (int i = 0; i < 4000; i++) {
        //printf("Wasting time * %d", i);
    }

    function1();
    return 0;
}
