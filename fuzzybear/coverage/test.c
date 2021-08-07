#include <stdio.h>
#include <stdlib.h>

int fun1(void){
	int a = 1;
	int b = 2;
	int c = 3;
	return 0;
}

int fun2(void){
	int a = 1;
	int b = 2;
	int c = 3;
	fun1();
	return 0;
}

int fun3(void){
	int a = 1;
	int b = 2;
	int c = 3;
	fun2();
	return 0;
}

int main(void) {
	fun3();	
	return 0;
}
