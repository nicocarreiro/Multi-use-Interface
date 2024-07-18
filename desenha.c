#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <stdbool.h>
#include <SDL2/SDL.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>


//defines tornados em variáveis globais para possibilitar leitura a partir de arquivos futuramente
//gcc desenha.c -o desenha $(sdl2-config --cflags --libs) -lSDL2 -lm -lrt
int SCREEN_LENGTH;
int NUM_SQUARES;
int SQUARE_SIZE;

typedef struct {
	SDL_Renderer *renderer;
	SDL_Window *window;
} Tela; //struct relacionada ao sdl.

void inicializaSDL(Tela* tela); //inicializa o renderizador e a janela
void mostraTela(Tela* tela);
void arrumaTela(Tela* tela);
int XYparaIJ(int x);
int IJparaXY(int i);
void arrumaGrid(int grid[NUM_SQUARES][NUM_SQUARES], Tela* tela);
void lerOrigemDestino(int grid[NUM_SQUARES][NUM_SQUARES], Tela* tela);

void arrumaTela(Tela* tela) {
    SDL_SetRenderDrawColor(tela->renderer, 255, 255, 255, 255);
    SDL_RenderClear(tela->renderer);
}

void mostraTela(Tela* tela) {
    SDL_RenderPresent(tela->renderer);
}

int XYparaIJ(int x) {
    return x/SQUARE_SIZE;
}

int IJparaXY(int i) {
    return i * SQUARE_SIZE + SQUARE_SIZE / 2;
}

void inicializaSDL(Tela* tela)
{
	if (SDL_Init(SDL_INIT_VIDEO) < 0)
	{
		exit(1);
	}

	tela->window = SDL_CreateWindow("Desenhe o cenário. D marca o destino e O a origem", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_LENGTH, SCREEN_LENGTH, 0);

	if (!tela->window)
	{
		exit(1);
	}

	SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "linear");

	tela->renderer = SDL_CreateRenderer(tela->window, -1, SDL_RENDERER_ACCELERATED);

	if (!tela->renderer)
	{
		exit(1);
	}
}

void arrumaGrid(int grid[NUM_SQUARES][NUM_SQUARES], Tela* tela) {
    for(int i = 0; i < NUM_SQUARES; i++) {
        for(int j = 0; j < NUM_SQUARES; j++) {
            SDL_Rect rect_aux = {j*(SQUARE_SIZE), i*(SQUARE_SIZE), SQUARE_SIZE, SQUARE_SIZE};
            if(grid[i][j] == 3) {
                SDL_SetRenderDrawColor(tela->renderer, 0, 0, 255, 255);
                SDL_RenderFillRect(tela->renderer, &rect_aux);
            } else if (grid[i][j] == 2) {
                SDL_SetRenderDrawColor(tela->renderer, 255, 255, 0, 255);
                SDL_RenderFillRect(tela->renderer, &rect_aux);
            } else if(grid[i][j] == 1) {
                SDL_SetRenderDrawColor(tela->renderer, 0, 0, 0, 255);
                SDL_RenderFillRect(tela->renderer, &rect_aux);
            }
        }
    }
}

void lerOrigemDestino(int grid[NUM_SQUARES][NUM_SQUARES], Tela* tela) {
    arrumaTela(tela);
    arrumaGrid(grid, tela);
    mostraTela(tela);
    int mouseClicado = 0;
    SDL_Event event;
    int destino_escolhido = 0, origem_escolhida = 0;
    int mouse_x, mouse_y;
    SDL_Keycode keyPressed;

    int shm_fd;
    long *shm;
    const char *name = "/posix_shm";

    // Open the shared memory object
    shm_fd = shm_open(name, O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        exit(1);
    }

    // Map the shared memory object into the process's address space
    shm = (long *)mmap(NULL, 8, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shm == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    while(!destino_escolhido || !origem_escolhida)
    while (SDL_PollEvent(&event))
	{
		switch (event.type)
		{
			case SDL_QUIT:
				exit(0);
				break;
            
            case SDL_KEYDOWN:
                keyPressed = event.key.keysym.sym;
                if(keyPressed == SDLK_d && !destino_escolhido) {//define o destino na grid e na variavel destino
                    SDL_GetMouseState(&mouse_x, &mouse_y);
                    destino_escolhido = 1;
                    //bom lembrar que a cordenada y diz respeito à linha, isso me gerou confusão, por isso o mouse_y vem antes do mouse_x
                    grid[XYparaIJ(mouse_y)][XYparaIJ(mouse_x)] = 3;
                    arrumaTela(tela);
                    arrumaGrid(grid, tela);
                    mostraTela(tela);
                }
                else if(keyPressed == SDLK_o && !origem_escolhida) {//define o destino na grid e na variavel destino
                    SDL_GetMouseState(&mouse_x, &mouse_y);
                    origem_escolhida = 1;
                    grid[XYparaIJ(mouse_y)][XYparaIJ(mouse_x)] = 2;
                    arrumaTela(tela);
                    arrumaGrid(grid, tela);
                    mostraTela(tela);
                }
                break;
            case SDL_MOUSEBUTTONDOWN:
                mouseClicado = 1;
                break;
            case SDL_MOUSEBUTTONUP:
                mouseClicado = 0;
                break;
            case SDL_MOUSEMOTION:
                if(!mouseClicado) break;
                SDL_GetMouseState(&mouse_x, &mouse_y);
                for (int i = (-1 * (*shm)) + 1; abs(i) < *shm; i++){
                    for (int j = (-1 * (*shm)) + 1; abs(j) < *shm; j++){
                        if ((XYparaIJ(mouse_y)+i) >= 0 && (XYparaIJ(mouse_y)+i) < NUM_SQUARES && (XYparaIJ(mouse_x)+j) >= 0 && (XYparaIJ(mouse_x)+j) < NUM_SQUARES)                        
                            grid[XYparaIJ(mouse_y)+i][XYparaIJ(mouse_x)+j] = 1;
                    }
                }
                arrumaTela(tela);
                arrumaGrid(grid, tela);
                mostraTela(tela);
                break;
            default:
				break;
		}
	}
}

int main(int argc, char* argv[]) {
    if(argc != 2) {
        printf("Erro na abertura arquivo.\n");
        return 1;
    }
    Tela tela;
    SDL_Event event;
    SCREEN_LENGTH = 640;
    NUM_SQUARES = 80;
    SQUARE_SIZE = SCREEN_LENGTH / NUM_SQUARES;
    inicializaSDL(&tela);
    int grid[NUM_SQUARES][NUM_SQUARES];//inicializa toda a matriz com 0
    //1 significa obstaculo, 2 inicio e 3 destino e 0 é apenas caminho navegável
    for(int i = 0; i < NUM_SQUARES; i++) {
        for(int j = 0; j < NUM_SQUARES; j++) {
            grid[i][j] = 0;
        }
    }
    lerOrigemDestino(grid, &tela);
    FILE* cenario;
    while(1) {
        while (SDL_PollEvent(&event))
        {
            switch (event.type)
                {
                    case SDL_QUIT:
                    
                    cenario = fopen(argv[1], "wb");
                    if(cenario == NULL) {
                        printf("Erro no salvamento de arquivo.\n");
                        exit(1);
                    }
                    for(int i = 0; i < NUM_SQUARES; i++) {
                        for(int j = 0; j < NUM_SQUARES; j++) {
                            fwrite(&(grid[i][j]), sizeof(int), 1, cenario);
                        }
                    }
                    fclose(cenario);
                    exit(0);
                }
        }
        arrumaTela(&tela);
        arrumaGrid(grid, &tela);
        mostraTela(&tela);
    }
}