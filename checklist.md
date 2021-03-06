[voltar](README.md)

### 1.1
    [x] Display file capaz de representar retas, polígonos e pontos
    [x] Cada objeto possui um nome
    [x] Cada objeto possui um tipo
    [x] Cada objeto possui sua lista de coordenadas
    [x] Funções de navegação 2D (movimentação do window)
    [x] Funções de Zoom (modificação do tamanho do window)

### 1.2
    [x] Translações
    [x] Escalonamentos em torno do centro do objeto
    Rotações:
        [x] Em torno do centro do mundo
        [x] Em torno do centro do objeto
        [] Em torno de um ponto qualquer (arbitrário)‏

### 1.3
    [x] Altere a representação dos objetos do mundo para suportar representação em um dos sistemas de coordenadas vistos em aula: Sistema de Coordenadas Normalizado (SCN) ou o Sistema de Coordenadas do Plano de Projeção (PPC). Agora a transformada de viewport é feita com estas coordenadas novas.

    [x] Atualize a translação e o zoom da window tendo em vista o novo sistema de coordenadas. A translação em particular deve levar em conta sempre o "para cima" do ponto de vista do usuário.

    [x] Implemente a rotação implementando o algoritmo para gerar a descrição no sistema de coordenadas escolhido.

    [x] Atualize a interface da aplicação para que o usuário possa rotacionar a window também. Como a rotação é sempre ao redor do centro da window, basta um campo para colocar o ângulo de rotação.


    [x] Crie uma classe DescritorOBJ capaz de transcrever um objeto gráfico para o formato .obj, tomando seu nome, seu tipo, seus vértices e suas arestas.

    [x] Chame o descritor para cada objeto de seu mundo.
    Assim você só precisa se preocupar com o cabeçalho do .obj. O resto de se resove através de um percurso do display file com seu descritor.

### 1.4
    [x] Clipagem de Pontos
    2 (duas) técnicas distintas de clipagem de Segmentos de Reta, à escolha, passíveis de serem intercambiadas/selecionadas pelo usuário em um checkbox.

    [x] Clipagem de Polígonos (técnica à escolha).


    [x] Faça sua Viewport ser menor do que o objeto de desenho da linguagem de programação, com uma moldura ao seu redor. Isto facilita na visualização do clipping e na detecção de erros (como visto nas transparências, link).

    [x] Implemente o clipping de pontos, retas e polígonos wireframe utilizando um dos 3 algoritmos de clipping de retas vistos em aula.

    [x] Estenda seu SGI para suportar polígonos preenchidos, utilizando as primitivas de preenchimento da sua linguagem de programação. O usuário escolhe se o polígono é em modelo de arame ou preenchido no momento de sua criação.

    [x] Implemente o clipping de polígonos preenchidos com o algoritmo de Weiler-Atherton. Para simplificar, considere apenas polígonos sem furos (mas possivelmente côncavos).

### 1.5
    [x] Crie uma Classe Curva2D

    [x] A curva deverá utilizar funções de suavização (blending functions) para se mostrar.

    [x] Um objeto Curva2D poderá conter uma ou mais curvas com continuidade no mínimo G(0).

    [x] Crie uma interface para entrar com estes dados.

    [x] Implemente o Clipping para esta curva utilizando o método descrito em aula (e nas transparências)

### 1.6
    [x] Além de Hermite/Bezier, implemente também B-Splines com Forward Differences. Para tanto estenda a sua Curva2D.

    [x] Deve ser possível ao usuário entrar com quantos pontos de controle desejar, com um mínimo de n = 4.

    [x] Devem ser desenhadas m = n - 3 curvas b-spline, utilizando-se todos os pontos, 4 a 4.

### 1.7

    [x] Implemente uma classe Ponto3D capaz de realizar as 3 transformações básicas.

    [ ] Implemente uma Classe Objeto3D para representar um Modelo de Arame com as seguintes características:
        [ ] Possui uma lista de segmentos de reta constituídos por um par de Pontos3D.
        [ ] É capaz de realizar as 3 operações básicas e também a rotação em torno de um eixo arbitrário.

    [ ] Implemente o que foi visto hoje sobre Projeção Paralela Ortogonal.
        [ ] Defina um VPN qualquer fornecendo dois pontos sobre uma reta.
        [ ] O primeiro ponto pode ser o VRP.
        Lembre-se que ao final do algoritmo o VPN deve ser (0, 0, 1), ou seja, paralelo ao eixo Z.


[voltar](README.md)
