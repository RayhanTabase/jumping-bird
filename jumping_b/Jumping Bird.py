import pygame,sys,random,time


pygame.init()

WINDOW_WIDTH  = 512
WINDOW_HEIGHT = 288

WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (255,0,0)
BLUE  = (0,0,255)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Jumping Bird')
SCREEN.fill(WHITE)
BACKGROUND = pygame.image.load('background.png')
GROUND = pygame.image.load('ground.png')
BACKGROUND_SCROLL = 0
GROUND_SCROLL = 0
SCROLL_SPEED_background = 0.5
SCROLL_SPEED_ground = 1

GRAVITY_SPEED = 1.7
GRAVITY = GRAVITY_SPEED
PIPE_IMAGE = pygame.image.load('pipe.png')
PIPE_WIDTH = PIPE_IMAGE.get_width()
PIPE_HEIGHT = PIPE_IMAGE.get_height()
PIPE_SCROLL = -2
Spawn_timer = 0
spawn_limit = 80
jump_height = -28 + -GRAVITY

PIPE_GAP = 80

class Pipe:
    def __init__(self):
        self.image_bottom = PIPE_IMAGE
        self.image_top = pygame.transform.flip(PIPE_IMAGE,False,True)
        self.x = WINDOW_WIDTH 
        self.y = random.randint( int(WINDOW_HEIGHT/3),   int(WINDOW_HEIGHT/1.3)) 
        self.y_top = - (WINDOW_HEIGHT - self.y + PIPE_GAP)
        self.width = PIPE_WIDTH
        self.height = PIPE_HEIGHT
    
    def update(self):
        self.x = self.x + PIPE_SCROLL
        
    def draw(self):
        SCREEN.blit(self.image_bottom,(self.x,self.y))
        SCREEN.blit(self.image_top,(self.x,self.y_top))
        
class Bird:
    def __init__(self):
        self.image = pygame.image.load('bird.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = WINDOW_WIDTH/2 - (self.width/2)
        self.y = WINDOW_HEIGHT/2 - (self.height/2)
    
    def draw(self):
        SCREEN.blit(self.image,(self.x,self.y))

    def update(self):
        global GRAVITY
        self.y = self.y + GRAVITY  
      
    def collision(self,pipe):
        mercy_spce = 7
        
        if self.x + self.width < pipe.x + mercy_spce:
            return False
        if self.y + self.height< pipe.y + mercy_spce and self.y > pipe.y_top + pipe.height -mercy_spce :
            return False
        
        if self.x > pipe.x + pipe.width - mercy_spce :
            return False
        if self.y  > pipe.y + pipe.height and self.y + self.height < pipe.y_top :
            return False
        
        return True


score_sound = pygame.mixer.Sound('score.wav')    
jump_sound  = pygame.mixer.Sound('jump.wav')
hurt_sound  = pygame.mixer.Sound('hurt.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')   
# music = pygame.mixer.music.load('marios_way.mp3')
         
clock = pygame.time.Clock()

Score = 0
High_Score=[] 

font=pygame.font.Font('flappy.ttf',40)
font1 = pygame.font.Font('flappy.ttf',20)
Title = True
Playing = False
Loose = False
Counter = False
Count = 1
# pygame.mixer.music.play(-1)
while True:
    clock.tick(60)

    if Title:
        bird = Bird()
        Pipe_Sprite = []
        if BACKGROUND_SCROLL > 413:
            BACKGROUND_SCROLL = 0
        if GROUND_SCROLL > 413:
            GROUND_SCROLL = 0
        BACKGROUND_SCROLL= BACKGROUND_SCROLL + SCROLL_SPEED_background
        GROUND_SCROLL    = GROUND_SCROLL  + SCROLL_SPEED_ground
        SCREEN.blit(BACKGROUND,(-BACKGROUND_SCROLL,0))
        SCREEN.blit(GROUND,(-GROUND_SCROLL,WINDOW_HEIGHT-16))

        SCORE_MESSAGE = font.render(('Score: ' + str(Score)),True,WHITE)
        SCREEN.blit(SCORE_MESSAGE,(20,20))

        if Counter == False:

            Play_Message = font1.render('Press P to Play',True,WHITE)
            Quit_Message = font1.render('Press ESCAPE to Quit',True,WHITE)

            SCREEN.blit(Play_Message,(WINDOW_WIDTH/2 -40,WINDOW_HEIGHT/2))
            SCREEN.blit(Quit_Message,(WINDOW_WIDTH/2 -40,WINDOW_HEIGHT/2+40))

            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_p:
                        Counter = True
                        
                        
                    if e.key ==pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        elif Counter == True:
            
            Count_Message = font.render(str(int(Count)),True,WHITE)
            SCREEN.blit(Count_Message,(WINDOW_WIDTH/2 - 40, WINDOW_HEIGHT/2 - 40))
            
            Count = Count + 0.04
        
        if int(Count) > 3:
                Title=False
                Playing=True
                Counter = False
                Count = 1
                Score = 0
            
        pygame.display.flip()

    elif Playing:
       
        if Spawn_timer == spawn_limit:
            pipe = Pipe()
            Pipe_Sprite.append(pipe)

        jump = False
        
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    jump_sound.play()
                    jump = True
                    
                elif e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    jump = False

        if jump == True:
                    GRAVITY = GRAVITY + jump_height 
                    
        else:
            GRAVITY = GRAVITY_SPEED

        bird.update()
        for pipe in Pipe_Sprite:
            pipe.update()
        
        if BACKGROUND_SCROLL > 413:
            BACKGROUND_SCROLL = 0
        if GROUND_SCROLL > 413:
            GROUND_SCROLL = 0
        BACKGROUND_SCROLL= BACKGROUND_SCROLL + SCROLL_SPEED_background
        GROUND_SCROLL    = GROUND_SCROLL  + SCROLL_SPEED_ground
        SCREEN.blit(BACKGROUND,(-BACKGROUND_SCROLL,0))
    
        if bird.y > WINDOW_HEIGHT:
           Loose = True
           Playing = False
           hurt_sound.play()
        
        for pipe in Pipe_Sprite:
            
            if pipe.x > - (pipe.width):
                pipe.draw()
                
                if bird.x == pipe.x + pipe.width + 1  :
                    Score = Score +  1
                    score_sound.play()
                
                if bird.collision(pipe):
                    Loose = True
                    Playing = False 
                   
                    explosion_sound.play()
                    
                    hurt_sound.play()
            
        SCREEN.blit(GROUND,(-GROUND_SCROLL,WINDOW_HEIGHT-16))
        bird.draw()

        SCORE_MESSAGE = font.render(('Score: ' + str(Score)),True,WHITE)
        SCREEN.blit(SCORE_MESSAGE,(20,20))
        
        pygame.display.flip()

        Spawn_timer = Spawn_timer + 1
        
        if Spawn_timer >spawn_limit:
            Spawn_timer = 0
            
        for pipe in Pipe_Sprite:
            if pipe.x < - (pipe.width):
                Pipe_Sprite.remove(pipe)
    elif Loose:
        time.sleep(1)
        Title = True
        Playing = False
        Loose = False
                
        
        


