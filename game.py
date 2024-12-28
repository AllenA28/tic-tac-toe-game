
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 800))
clock = pygame.time.Clock()
running = True
dt = 0
TILE_SIZE = screen.get_width()/3
TILE_MARKERS=['','X','O']
font = pygame.font.SysFont('Helvetica', 720//3, bold=True, italic=False)
instrfont = pygame.font.SysFont('Helvetica', 50, bold=True, italic=False)
winner = ['tie', 'player 1', 'player 2']

#honestly this one was probably not needed, just for fun
class Board:
    def __init__(self, color):
        self.color = color
        self.tiles = []
        for i in range(3):
            self.tiles.append([])
            for j in range(3):
                self.tiles[i].append(Tile(TILE_SIZE, (j, i)))


#each tile is basically it's own object with properties like coords, length, and the marker it shows
class Tile:
    def __init__(self, length, coords):
        self.length = length
        self.yval = coords[1] *self.length
        self.xval = coords[0]* self.length
        self.marker = TILE_MARKERS[0]
        self.rect = pygame.Rect(self.xval, self.yval, self.length, self.length)
    
    def render (self, screen):
        pygame.draw.rect(screen, 'green', self.rect)
        pygame.draw.rect(screen, 'black', self.rect, round(self.length / 30))
        screen.blit(font.render(self.marker, True, 'black'), (self.xval+25, self.yval+25))


def get_clicked_tile(mouse_pos, board):
    '''
    this returns the tile that was clicked, requires mouse position and the board
    '''
    for row in board.tiles:
        for tile in row:
            if tile.rect.collidepoint(mouse_pos):
                return tile
    return None


def check_winner():
    '''
like the method name says, it checks for a winner, it scanns the board for win conditions
returns a boolean determining if someone won the game, changes the global variables for 
message, and the start and endpoint of the winning line
    '''
    global message,spoint,epoint

    for item in 'XO':
        #check for three in a row
        for row in range(3):
            if all(board.tiles[row][col].marker == item for col in range(3)):
                spoint = (0,row*TILE_SIZE+TILE_SIZE/2)
                epoint = (TILE_SIZE*3-(TILE_SIZE/30),row*TILE_SIZE+ TILE_SIZE/2)
                message = f'Player {TILE_MARKERS.index(item)} wins by Row!'
                return True

        #check for three in a column
        for col in range(3):
            if all(board.tiles[row][col].marker == item for row in range(3)):
                message = f'Player {TILE_MARKERS.index(item)} wins by Column!'
                spoint = (col*TILE_SIZE+TILE_SIZE/2,0)
                epoint = (col*TILE_SIZE+ TILE_SIZE/2,TILE_SIZE*3-(TILE_SIZE/30))
                return True

        #Check the diagonals
        if (board.tiles[0][0].marker == board.tiles[1][1].marker == board.tiles[2][2].marker == item):
            message = f'Player {TILE_MARKERS.index(item)} wins by Diagonal!'
            spoint = board.tiles[0][0].rect.topleft
            epoint = board.tiles[2][2].rect.bottomright
            return True
        if (board.tiles[0][2].marker == board.tiles[1][1].marker == board.tiles[2][0].marker == item):
            message = f'Player {TILE_MARKERS.index(item)} wins by Diagonal!'
            spoint = board.tiles[0][2].rect.topright
            epoint = board.tiles[2][0].rect.bottomleft
            return True
            
    return False

board = Board('blue')
players = (1,2)
player = players[0]
count=0
game_over = False

while running:
################################### inputs #########################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                #this allows for restarting the game
                for row in range(3):
                    for col in range(3):
                        board.tiles[row][col].marker = TILE_MARKERS[0]
                        count =0
                        player = players[0]
                        game_over = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pos = pygame.mouse.get_pos()
            tile = get_clicked_tile(pos, board)
            tile.marker = TILE_MARKERS[player]
            if check_winner():
                count+=1
                player = players[count %2]
                game_over = True
            count+=1
            player = players[count %2]
            



    ################################# Display stuff ##############################
    screen.fill('black')

    draw = False
    if count == 9 and not check_winner():
        message = 'It\'s a draw!'
        draw = True
        game_over = True
    
    for row in board.tiles:
        for tile in row:
            tile.render(screen)

    #things for game over
    if game_over:
        screen.blit(instrfont.render(message, True, 'white'), (14, 720))
        if not draw:
            pygame.draw.line(screen, 'blue', spoint, epoint, 20)
    else:
        screen.blit(instrfont.render(f'Player {player}, your move', True, 'white'), (14, 720))
    


    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
