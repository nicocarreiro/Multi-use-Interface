#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <X11/Xlib.h>
#include <X11/keysym.h>

#define WIDTH  400
#define HEIGHT 300
#define BUFFER_SIZE 100

int readfile() {
    char filename[] = "mapConfig.txt";
    char buffer[BUFFER_SIZE];

    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Erro ao abrir o arquivo %s\n", filename);
        return 0;
    }

    // Ler o número do arquivo
    if (fgets(buffer, BUFFER_SIZE, file) == NULL) {
        fprintf(stderr, "Erro ao ler o número do arquivo %s\n", filename);
        fclose(file);
        return 0;
    }

    // Converter o número para inteiro
    int number = atoi(buffer);

    // Fechar o arquivo
    fclose(file);

    return number;
}

void drawNumber(Display *display, Window window, int number) {
    // Obter o número da tela
    int screen = DefaultScreen(display);
    
    // Obter o contexto gráfico da janela
    GC gc = DefaultGC(display, screen);
    
    // Preencher a janela com uma cor sólida
    XSetForeground(display, gc, WhitePixel(display, screen)); // Cor branca
    XFillRectangle(display, window, gc, 0, 0, WIDTH, HEIGHT);
    
    // Definir a cor do texto para preto
    XSetForeground(display, gc, BlackPixel(display, screen)); // Cor preta
    
    // Converter o número para uma string
    char number_str[BUFFER_SIZE];
    snprintf(number_str, BUFFER_SIZE, "%d", number);

    // Desenhar o número na janela
    XDrawString(display, window, gc,
                50, 50, number_str, strlen(number_str));
}


int main() {
    Display *display;
    Window window;
    XEvent event;
    int screen;
    
    // Inicializar a conexão com o display X11
    display = XOpenDisplay(NULL);
    if (display == NULL) {
        fprintf(stderr, "Cannot open display\n");
        return 1;
    }

    // Obter o número da tela
    screen = DefaultScreen(display);

    // Criar a janela
    window = XCreateSimpleWindow(display, RootWindow(display, screen),
                                  10, 10, WIDTH, HEIGHT, 1,
                                  BlackPixel(display, screen),
                                  WhitePixel(display, screen));

    // Selecionar eventos de exposição e eventos de teclado para a janela
    XSelectInput(display, window, ExposureMask | KeyPressMask);

    // Mapear a janela na tela
    XMapWindow(display, window);

    int number = readfile(); // Ler o número inicial do arquivo
    drawNumber(display, window, number); // Desenhar o número inicial na janela

    // Loop principal
    while (1) {
        // Aguardar por um evento
        XNextEvent(display, &event);

        // Se o evento for de exposição, redesenhar o número na janela
        if (event.type == Expose) {
            drawNumber(display, window, number);
        }

        // Se o evento for de pressionar uma tecla
        if (event.type == KeyPress) {
            // Obter a tecla pressionada
            KeySym key = XLookupKeysym(&event.xkey, 0);
            char ascii_char = (char) key;

            // Se 'u' for pressionado, ler o número do arquivo novamente
            if (ascii_char == 'u') {
                number = readfile();
                drawNumber(display, window, number); // Redesenhar o número na janela
            } 
            // Se 'e' for pressionado, sair do loop e encerrar o programa
            else if (ascii_char == 'e') {
                break;
            }
        }
    }

    // Fechar a conexão com o display X11
    XCloseDisplay(display);

    return 0;
}
