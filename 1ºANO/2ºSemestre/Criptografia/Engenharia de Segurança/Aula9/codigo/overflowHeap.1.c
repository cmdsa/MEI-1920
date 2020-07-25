#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    char *dummy = (char *) malloc (sizeof(char) * 10);
    char *readonly = (char *) malloc (sizeof(char) * 10);
    
    printf("Endereço de dummy %p\n",dummy);
    printf("Endereço de readonly %p\n",readonly);

    /*
    strcpy(readonly, "laranjas");
    strcpy(dummy, argv[1]);
    printf("%s\n", readonly);
    */
   
    //Podemos simplesmente usar uma opção mais segura do strcpy
    //o snprintf faz o mesmo, isto é, copia a string,
    //mas quando a string é copiada e chega ao fim
    //é truncada colocando o character null '\0' no fim
    snprintf(readonly,sizeof(char) * 10,"%s", "laranjas");
    snprintf(dummy, sizeof(char) * 10,"%s", argv[1]);
    printf("%s\n", readonly);


}
