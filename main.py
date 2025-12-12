import pygame, sys
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    # delta_time
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroidField = AsteroidField()

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # fill and update
        screen.fill("black")
        for el in updatable:
            el.update(dt)
        for el in drawable:
            el.draw(screen)
        # draw shots
        for el in shots:
            el.update(dt)
            el.draw(screen)
            #print(f"Shot coords: ({el.position.x}, {el.position.y})")
        
        # collision check player asteroid
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        # collion check asteroid shot
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

        # cleanup shots out of bounds
        for shot in shots:
            if shot.position.x < 0 or shot.position.x > SCREEN_WIDTH:
                shot.kill()
            if shot.position.y < 0 or shot.position.y > SCREEN_HEIGHT:
                shot.kill()




        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
