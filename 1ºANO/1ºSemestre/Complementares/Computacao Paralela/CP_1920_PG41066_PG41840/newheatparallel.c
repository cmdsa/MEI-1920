#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

void iteration(int size, float **new_M, float **old_M,  int maxIt, int threads) 
{
	 
    //Itera ate maxIt iteracoes

    for(int i = 0; i < maxIt; i++) 
    #pragma omp parallel num_threads(threads)
    {
		    //Calcula os novos valores dos pontos interiores para new_M.
            #pragma omp for
		    for(int i = 1; i < size-1; i++) 
        {
			      for(int j = 1; j < size-1; j++) 
            {
			        	new_M[i][j] =(old_M[i-1][j] 
                            + old_M[i+1][j] 
                            + old_M[i][j-1] 
                            + old_M[i][j+1] 
                            + old_M[i][j])/5;
			      }
		    }

		//Guarda a ultima solucao em old_M
        #pragma omp for
		for(int i = 0; i < size; i++) 
        {
			    for(int j = 0; j < size; j++) 
            {
				        old_M[i][j] = new_M[i][j];
			      }
	    	}
		
	  }
}

void printMatrix(int size,float (*M_New)[size], FILE *file) 
{
	for(int i = 0; i < size; i++) 
  {
	    	for(int j = 0; j < size; j++) 
        {
		    	fprintf(file, "%.7f ", M_New[i][j]);
		    }

		fprintf(file, "\n");
	}

}

int main(int argc, char * argv[])
{
   
    int matrix_size;
    int n_max_it;
    int num_threads;
    double start, final;
    FILE *file = NULL;

     //arg1 - tamanho matrix, 
    matrix_size = atoi(argv[1]);
    //arg2 - numero maximo de iteraçeos
    n_max_it = atoi(argv[2]);

    num_threads = atoi(argv[3]);
    //alocação das matrizes
    float **heat_new = malloc(matrix_size * sizeof(float *));
    float **heat_old = malloc(matrix_size * sizeof(float *));
     
    for(int i = 0; i < matrix_size; i++)
    {
        heat_new[i] = malloc(matrix_size * sizeof(float));
        heat_old[i] = malloc(matrix_size * sizeof(float));
    }
     
     //Preenche a primeira linha com 100
	for(int i = 0; i < matrix_size; i++) 
    {
        heat_new[0][i] = (float)100;
    }
	//Preenche o resto com 0
	for(int i = 1; i < matrix_size; i++) 
    {
		  for(int j = 0; j < matrix_size; j++) 
        {
			    heat_new[i][j] = (float)0;
		    }
  	}

    /*file = fopen("matrizInicial", "ab+");
    printMatrix(matrix_size,heat_new, file);
    fclose(file);*/

    //Executa n_max_it iteraçoes, indicando o tempo de execução
    start = omp_get_wtime();
    iteration(matrix_size,heat_new,heat_old,n_max_it, num_threads);
    final = omp_get_wtime();
    //Imprimir em milsegundos o tempo de execuçao
    printf("Time seq: %.5f ms \n", (final -start)*1000);

    /**file = fopen("matrizFinal", "ab+");
    printMatrix(matrix_size,heat_new, file);
    fclose(file);*/
    for(int i = 0; i < matrix_size; i++)
    {
        free(heat_new[i]);
         free(heat_old[i]);
    }
    //Libertar memoria utilizada
    free(heat_new);
    //Libertar memoria utilizada
    free(heat_old);

    return 1;

}



