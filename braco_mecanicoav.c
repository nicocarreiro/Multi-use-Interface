#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <SDL2/SDL.h>

//para compilar use gcc braco_mecanicoav.c -o braco $(sdl2-config --cflags --libs) -lSDL2 -lm
//Para a parte gráfica, utilizei a biblioteca sdl2
//Como utilizar o programa:
//Ao iniciar, o programa espera que o usuário desenhe os obstáculos, a cada dois cliques um obstaculo retangular é gerado.
//Quando terminar de desenhar os obstaculos, aperte enter para definir o ponto inicial dos braços.
//Após esse clique, o programa começa.
//Agora, basta definir seu objetivo durante a execução do programa, esse objetivo pode ser modificado com um clique.
//A tecla Q causa um genocídio, inclusive do melhor histórico.
//A tecla Z aumenta a mutação, enquanto a X diminui. O valor mínimo da mutação é 1.
//A tecla P alterna entre mostrar ou não a população.

int SQUARE_SIZE;
int SCREEN_LENGTH;
int NUM_SQUARES;
int NUM_INDIVIDUOS = 100;
int COMPRIMENTO_TOTAL = 700;
int NUM_JUNTAS = 30;


#define PESO_PERTO 1
#define PESO_LONGE_OBS 1
#define DELAY 1 //quantos milissegundos de delay entre uma iteração e outra.
#define GERACOES_REPETIDAS 200 //Quantas gerações com o melhor repetido para que a mutação varie 
#define TAXA_MUTACAO 1  //Taxa de mutação inicial, durante a execução será na prática alterada pelo usuário
#define DISTANCIA_MIN 5
#define GERACOES_POR_OBJETIVO 500

typedef struct {
	SDL_Renderer *renderer;
	SDL_Window *window;
} Tela; //struct relacionada ao sdl.

typedef struct {
    float* angulos; //vetor de angulos de cada uma das juntas
    SDL_Point inicio; //ponto inicial do individuo, é definido pelo usuário e igual para todos
    float distanciaDestino;//distancia da ponta final do braço até o destino
    float menorDistancia; //a distancia da junta mais próxima a algum obstaculo(!= pontuação)
} Individuo; //o individuo a ser analisado

void arrumaTela(Tela* tela); //limpa a tela
void inicializaSDL(Tela* tela); //inicializa o renderizador e a janela
Individuo* individuoAleatorio(SDL_Point inicio, int num_juntas); //gera um individuo aleatorio
void copiaIndividuo(Individuo* destino, Individuo* origem); //copia todos os atributos de um individuo
int lerInput(int* mutacao, SDL_Point* objetivo, int* mostra_pop); //le possiveis inputs relacionados a fechar o progama, alterar a mutacao ou alterar o destino
void desenhaCirculo(Tela* tela, SDL_Point ponto, int raio);
void mostraIndividuo(Tela* tela, Individuo* individuo, int r, int g, int b); //desenha um braço na tela
void mutaIndividuo(Individuo* individuo, int mutacao);//muta um numero definido na chamada da função de angulos do individuo
void avaliaIndividuo(Individuo* individuo, int** obstaculos, SDL_Point objetivo);//funcao explicada mais detalhadamente na sua definição
float distancia(SDL_Point a, SDL_Point b);//calcula a distancia entre dois pontos
void mostraTela(Tela* tela); //simplesmente apresenta o que foi desenhado até agora para o usuário
int temVazio(int** obstaculos);
void printaMatriz(int** obstaculos);
int min(int a, int b);
int max(int a, int b);
int XYparaIJ(int x);
int IJparaXY(int i);

int min(int a, int b) {return (a < b) ? a : b;}
int max(int a, int b) {return (a > b) ? a : b;}

int XYparaIJ(int x) {
    return x/SQUARE_SIZE;
}

int IJparaXY(int i) {
    return i * SQUARE_SIZE + SQUARE_SIZE / 2;
}

void mostraTela(Tela* tela) {
    SDL_RenderPresent(tela->renderer);
}

void arrumaTela(Tela* tela) {
    SDL_SetRenderDrawColor(tela->renderer, 255, 255, 255, 255);
    SDL_RenderClear(tela->renderer);
}

void printaMatriz(int** obstaculos) {
    for(int i = 0; i < NUM_SQUARES; i++) {
        for(int j = 0; j < NUM_SQUARES; j++) {
            printf("%d ", obstaculos[i][j]);
        }
        printf("\n");
    }
}

float distancia(SDL_Point a, SDL_Point b) {
    //para evitar divisões por 0, a função retorna 1 se a distancia for menor que isso;
    return max(sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2)), 1);
}

void avaliaIndividuo(Individuo* individuo, int** obstaculos, SDL_Point objetivo) {
    //A pontuação do individuo leva primeiro em conta a distancia do seu ponto final ao objetivo.
    //Se essa distancia for menor do que um valor predeterminado, passa a analisar também sua distancia aos obstaculos.
    float menor_distancia = 0;
    int x_atual = individuo->inicio.x, y_atual = individuo->inicio.y;
    for(int i = 0; i < NUM_JUNTAS; i++) {
        //a cada iteração o x e y atuais do braço se atualizam
        x_atual += (cos(individuo->angulos[i]) * (COMPRIMENTO_TOTAL/NUM_JUNTAS));
        y_atual += (sin(individuo->angulos[i]) * (COMPRIMENTO_TOTAL/NUM_JUNTAS));
        //em toda iteração checo se o braço entrou em algum obstaculo, usando uma função que detecta essa colisao do proprio SDL
        //caso tenha entrado, é dada uma pontuação negativa e a função retorna. Quero evitar essa situação ao máximo.
        //aproveito também para já calcular a menor distância que acontece entre uma junta e um obstaculo.
        if(XYparaIJ(y_atual) < NUM_SQUARES && XYparaIJ(x_atual) < NUM_SQUARES && XYparaIJ(y_atual) >= 0 && XYparaIJ(x_atual) >= 0) {
            if(obstaculos[XYparaIJ(y_atual)][XYparaIJ(x_atual)] == 1){
                individuo->distanciaDestino = 99999999; 
                individuo->menorDistancia = 0;
                return;
            } else {
                if(obstaculos[XYparaIJ(y_atual)][XYparaIJ(x_atual)] > menor_distancia) menor_distancia = obstaculos[XYparaIJ(y_atual)][XYparaIJ(x_atual)];
            }
        } else {
            individuo->distanciaDestino = 99999999; 
            individuo->menorDistancia = 0;
            return;
        }
        
    }
    individuo->menorDistancia = menor_distancia;
    
    SDL_Point final = {x_atual, y_atual};
    individuo->distanciaDestino = distancia(final, objetivo);
    //Por fim, o individuo recebe a pontuação calculada.
    //individuo->pontuacao = pontuacao;
}

void mutaIndividuo(Individuo* individuo, int mutacao) {
    for(int i = 0; i < mutacao; i++) {
        individuo->angulos[(rand()%NUM_JUNTAS)] = (rand() % 361) * (6.28318530718/360.0);
    }
}

int temVazio(int** obstaculos) {
    for(int i = 0; i < NUM_SQUARES; i++) {
        for(int j = 0; j < NUM_SQUARES; j++) {
            if(obstaculos[i][j] == 0) return 1;
        }
    }
    return 0;
}

void mostraIndividuo(Tela* tela, Individuo* individuo, int r, int g, int b) {
    int x_atual = individuo->inicio.x, y_atual = individuo->inicio.y;
    for(int i = 0; i < NUM_JUNTAS; i++) {
        SDL_SetRenderDrawColor(tela->renderer, r, g, b, 255);
        SDL_RenderDrawLine(tela->renderer, x_atual, y_atual, x_atual + (cos(individuo->angulos[i]) * (COMPRIMENTO_TOTAL/NUM_JUNTAS)), y_atual + (sin(individuo->angulos[i]) * (COMPRIMENTO_TOTAL/NUM_JUNTAS)));
        x_atual += (cos(individuo->angulos[i]) * (COMPRIMENTO_TOTAL/NUM_JUNTAS));
        y_atual += (sin(individuo->angulos[i]) * (COMPRIMENTO_TOTAL/NUM_JUNTAS));
        SDL_Point aux = {x_atual, y_atual};
        SDL_SetRenderDrawColor(tela->renderer, 0, 0, 0, 255);
        if(i != NUM_JUNTAS-1) desenhaCirculo(tela, aux, 3);
    }
}

int lerInput(int* mutacao, SDL_Point* objetivo, int* mostra_pop)
{
	SDL_Event event;
    int pause = 0;
	while (SDL_PollEvent(&event) || pause)
	{
		switch (event.type)
		{
			case SDL_QUIT:
				exit(0);
				break;
            
            case SDL_KEYDOWN: {
                SDL_Keycode keyPressed = event.key.keysym.sym;
                if(keyPressed == SDLK_z) *mutacao += 1;
                else if ((keyPressed == SDLK_x) && (*mutacao > 1)) *mutacao -= 1;
                else if (keyPressed == SDLK_g) return 2;
                else if (keyPressed == SDLK_s) *mostra_pop = !(*mostra_pop);
                else if (keyPressed == SDLK_p) pause = !pause;
                break;
            }
            case SDL_MOUSEBUTTONDOWN:
                objetivo->x = event.button.x;
                objetivo->y = event.button.y;
                return 1;
			default:
				break;
		}
	}
    return 0;
}

void inicializaSDL(Tela* tela)
{
    srand((unsigned)time(NULL));
	if (SDL_Init(SDL_INIT_VIDEO) < 0)
	{
		exit(1);
	}

	tela->window = SDL_CreateWindow("Teclas: S para alternar a visualização G para genocídio Z e X para aumentar/diminuir mutação", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_LENGTH, SCREEN_LENGTH, 0);

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

Individuo* individuoAleatorio(SDL_Point inicio, int num_juntas) {
    Individuo* novo = (Individuo*) malloc(sizeof(Individuo));
    novo->angulos = (float*) malloc(sizeof(float)*NUM_JUNTAS);
    for(int i = 0; i < NUM_JUNTAS; i++) {
        novo->angulos[i] = ((float)(rand() % 6283184))/(1000000.0);
    }
    novo->menorDistancia = 0;
    novo->distanciaDestino = 99999999999;
    novo->inicio.x = inicio.x;
    novo->inicio.y = inicio.y;
    return novo;
}

void copiaIndividuo(Individuo* destino, Individuo* origem) {
    destino->inicio = origem->inicio;
    destino->distanciaDestino = origem->distanciaDestino;
    destino->menorDistancia = origem->menorDistancia;
    for(int i = 0; i < NUM_JUNTAS; i++) {
        destino->angulos[i] = origem->angulos[i];
    }
}

void desenhaCirculo(Tela* tela, SDL_Point ponto, int raio) {
    for (int y = -raio; y <= raio; ++y) {
        for (int x = -raio; x <= raio; ++x) {
            if (x * x + y * y <= raio * raio) {
                SDL_RenderDrawPoint(tela->renderer, ponto.x + x, ponto.y + y);
            }
        }
    }
}

int main(int argc, char* argv[]) {

    if(argc != 6) {
        printf("Erro na inicialização do programa\n");
        return 0;
    }
    NUM_JUNTAS = atoi(argv[3]);
    COMPRIMENTO_TOTAL = atoi(argv[4]);
    NUM_INDIVIDUOS = atoi(argv[5]);
    
    SCREEN_LENGTH = 640;
    NUM_SQUARES = 80;
    SQUARE_SIZE = SCREEN_LENGTH / NUM_SQUARES;
    SDL_Point inicio;//onde é guardado o ponto inicial do braço
    SDL_Point destino;

    int mostra_pop = 0;

    int taxa_mut = TAXA_MUTACAO;
    //inicializa a tela e abre a janela do programa.

    Tela tela;
    inicializaSDL(&tela);
    //inicializa a quantidade de obstáculos e o vetor de obstáculos(ponteiros de retângulos)

    //le o cenário de obstáculos
    FILE* cenario = fopen(argv[1], "rb");
    int** obstaculos = (int**) malloc(sizeof(int*) * NUM_SQUARES);
    for(int i = 0; i < NUM_SQUARES; i++) {
        obstaculos[i] = (int*) malloc(sizeof(int) * NUM_SQUARES);
    }
    for(int i = 0; i < NUM_SQUARES; i++) {
        for(int j = 0; j < NUM_SQUARES; j++) {
            fread(&(obstaculos[i][j]), sizeof(int), 1, cenario);
            if(obstaculos[i][j] == 2) {
                inicio.x = IJparaXY(j);
                inicio.y = IJparaXY(i);
            }
            if(obstaculos[i][j] == 3) {
                destino.x = IJparaXY(j);
                destino.y = IJparaXY(i);
            }
        }
    }
    fclose(cenario);
    FILE* caminho = fopen(argv[2], "rb");
    //vou criar um vetor de pontos para guardar quantos destinos haverá
    //primeiro leio o numero de destinos e depois leio cada um dos pontos
    int num_objetivos = 0;
    fread(&num_objetivos, sizeof(int), 1, caminho);
    if(num_objetivos == 0) {
        //nao há caminho possivel[
        printf("Não há caminho possível.\n");
        return 0;
    }
    SDL_Point destinos[num_objetivos];
    for(int i = num_objetivos-1; i >= 0; i--) {
        fread(&(destinos[i]), sizeof(SDL_Point), 1, caminho);
    }
    fclose(caminho);
    //o objetivo recebe o primeiro
    destino = destinos[0];
    //entender melhor essa parte para comentar, nao me lembro de quando fiz ela
    //ela pega todos os osbtaculos e vai criando uma area ao redor deles, para entender a distancia aos obstaculos, por isso os niveis
    int nivel = 1;
    while(nivel <= 3) {
        for(int i = 0; i < NUM_SQUARES; i++) {
            for(int j = 0; j < NUM_SQUARES; j++) {
                if(obstaculos[i][j] == nivel) {
                    if((i-1 >= 0) && (j-1 >= 0) && (obstaculos[i-1][j-1] == 0)) {
                        obstaculos[i-1][j-1] = nivel+1;
                    }
                    if((i-1 >= 0) && (j >= 0) && (obstaculos[i-1][j] == 0)) {
                        obstaculos[i-1][j] = nivel+1;
                    }
                    if((i-1 >= 0) && (j+1 < NUM_SQUARES) && (obstaculos[i-1][j+1] == 0)) {
                        obstaculos[i-1][j+1] = nivel+1;
                    }
                    if((i >= 0) && (j+1 < NUM_SQUARES) && (obstaculos[i][j+1] == 0)) {
                        obstaculos[i][j+1] = nivel+1;
                    }
                    if((i+1 < NUM_SQUARES) && (j+1 < NUM_SQUARES) && (obstaculos[i+1][j+1] == 0)) {
                        obstaculos[i+1][j+1] = nivel+1;
                    }
                    if((i+1 < NUM_SQUARES) && (j < NUM_SQUARES) && (obstaculos[i+1][j] == 0)) {
                        obstaculos[i+1][j] = nivel+1;
                    }
                    if((i+1 < NUM_SQUARES) && (j-1 >= 0) && (obstaculos[i+1][j-1] == 0)) {
                        obstaculos[i+1][j-1] = nivel+1;
                    }
                    if((i < NUM_SQUARES) && (j-1 >= 0) && (obstaculos[i][j-1] == 0)) {
                        obstaculos[i][j-1] = nivel+1;
                    }
                }
            }
        }
        nivel++;
    }
    //inicializa a população com individuos aleatorios partindo do inicio definido.
    Individuo* populacao[NUM_INDIVIDUOS];
    for(int i = 0; i < NUM_INDIVIDUOS; i++) {
        populacao[i] = individuoAleatorio(inicio, NUM_JUNTAS);
    }

    //inicializa o melhor de todos e já avalia ele, para que nao fique com uma pontuação aleatória.
    Individuo* melhorHistorico = (Individuo*) malloc(sizeof(Individuo));
    melhorHistorico->angulos = (float*) malloc(sizeof(float)*NUM_JUNTAS);
    avaliaIndividuo(populacao[0], obstaculos, destino);
    copiaIndividuo(melhorHistorico, populacao[0]);
    int geracoesRepetidas = 0;
    int geracao = 0;
    while(1) {
        //checa todos os inputs do usuario, inclusive o de fechar o programa
        //caso tenham se passado um numero de geracoes atualiza o destino
        if(geracao % GERACOES_POR_OBJETIVO == 0)
            if(geracao/GERACOES_POR_OBJETIVO < num_objetivos) {
                destino = destinos[geracao/GERACOES_POR_OBJETIVO];
                avaliaIndividuo(melhorHistorico, obstaculos, destino);
            }
        int input = lerInput(&taxa_mut, &destino, &mostra_pop);
        if(input == 1) {avaliaIndividuo(melhorHistorico, obstaculos, destino);}
        else if(input == 2) {
            for(int i = 0; i < NUM_INDIVIDUOS; i++) {
                populacao[i] = individuoAleatorio(inicio, NUM_JUNTAS);
            }
            copiaIndividuo(melhorHistorico, populacao[0]);
        }

        //limpa a tela
        arrumaTela(&tela);
        
        //avalia todos os individuos
        for(int i = 0; i < NUM_INDIVIDUOS; i++) {
            avaliaIndividuo(populacao[i], obstaculos, destino);
        }
        //seleciona o melhor de todos
        geracoesRepetidas++;
        for(int i = 0; i < NUM_INDIVIDUOS; i++) {
            //vou mudar essa comparação para apenas consideras as distancias obstaculos quando estiver numa determinada distancia do destino
            if(populacao[i]->distanciaDestino < DISTANCIA_MIN &&  populacao[i]->distanciaDestino < melhorHistorico->distanciaDestino) {
                copiaIndividuo(melhorHistorico, populacao[i]);
                taxa_mut = TAXA_MUTACAO;
                geracoesRepetidas = 0;
            } else if((populacao[i]->distanciaDestino < melhorHistorico->distanciaDestino && populacao[i]->menorDistancia >= melhorHistorico->menorDistancia) || (populacao[i]->menorDistancia > melhorHistorico->menorDistancia && populacao[i]->distanciaDestino <= melhorHistorico->menorDistancia)) {
                copiaIndividuo(melhorHistorico, populacao[i]);
                taxa_mut = TAXA_MUTACAO;
                geracoesRepetidas = 0;
            }
           
        }

        //mutacao variavel automatica
        if(geracoesRepetidas > GERACOES_REPETIDAS) {
            if(taxa_mut < (NUM_JUNTAS))
                taxa_mut++;
            else {//genocidio
                for(int i = 0; i < NUM_INDIVIDUOS; i++) {
                    populacao[i] = individuoAleatorio(inicio, NUM_JUNTAS);
                }
                copiaIndividuo(melhorHistorico, populacao[0]);
                taxa_mut = 1;
            }
            geracoesRepetidas = 0;
        }

        //desenha todos os individuos com uma cor definida(azul perto do ciano)
        if(mostra_pop)    
            for(int i = 0; i < NUM_INDIVIDUOS; i++) 
                mostraIndividuo(&tela, populacao[i], 19, 122, 127);
        
        //desenha o melhor de todos com uma cor vermelha
        mostraIndividuo(&tela, melhorHistorico, 255, 36, 0);

        //printf("A menor distância do melhor de todos: %f\n", melhorHistorico->menorDistancia);
        //desenha os obstáculos
        SDL_SetRenderDrawColor(tela.renderer, 0, 0, 0, 255);
        for(int i = 0; i < NUM_SQUARES; i++) {
            for(int j = 0; j < NUM_SQUARES; j++) {
                if(obstaculos[i][j] == 1) {
                    SDL_Rect rect = {j * (SCREEN_LENGTH/NUM_SQUARES), i * (SCREEN_LENGTH/NUM_SQUARES), SCREEN_LENGTH/NUM_SQUARES, SCREEN_LENGTH/NUM_SQUARES};
                    SDL_RenderFillRect(tela.renderer, &rect);
                }
            }
        }

        //desenha o objetivo 
        SDL_SetRenderDrawColor(tela.renderer, 100, 200, 100, 255);
        desenhaCirculo(&tela, destino, 7);

        //apresenta a tela desenhada ao usuário
        SDL_RenderPresent(tela.renderer);

        //muta toda a população de acordo com a taxa de mutacao atual
        for(int i = 0; i < NUM_INDIVIDUOS; i++) {
            copiaIndividuo(populacao[i], melhorHistorico);
            mutaIndividuo(populacao[i], taxa_mut);
        }
        //printf("Taxa de mutação atual: %d gerações repetidas: %d\n", taxa_mut, geracoesRepetidas);
        SDL_Delay(DELAY);
        geracao++;
    }
}
