import pygame
import random

# Constants are generally all capitals and separate from most other code.
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

WINDOW_TITLE = "Project Golf"
FRAME_RATE = 60.0
IDEAL_FRAME_TIME = 1.0 / FRAME_RATE

COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)


# This is technically not needed. Python uses DUCK TYPING.
#  DUCK TYPING means that if an object has a function, you can call it.
# This is here to see that anything that is drawable, and interactable
#  should have these functions, and to provide and error message
#  when you forget to implement these functions.
class GameObject:
    # This is a class variable. Each instance of "GameObject" or derivative
    #  will see the same copy of this.
    GameObjects = []

    def __init__(self):
        # Keep track of all the game objects
        # Notice I reference by the class name.
        GameObject.GameObjects.append(self)

        # Used to order drawing!
        self.ZIndex = 0

    def handle_input(self, events, environment):
        # If you forget to override this function, this will print.
        print("\'handle_input\' function not implemented for " + self.__class__.__name__ + "!")

    def step(self, environment):
        # If you forget to override this function, this will print.
        print("\'step\' function not implemented for " + self.__class__.__name__ + "!")

    def draw(self, draw_context):
        # If you forget to override this function, this will print.
        print("\'draw\' function not implemented for " + self.__class__.__name__ + "!")


# I'm drawing these as squares because its easy.
class Ball(GameObject):
    def __init__(self, x=0, y=0):
        # Calls the GameObject constructor (aka "init" function)
        super().__init__()

        # Have a size.
        self.width = random.randint(15, 50)
        self.height = random.randint(15, 50)

        # Starting position.
        self.x = x
        self.y = y

        # Starting velocity.
        self.velocity_x = 0
        self.velocity_y = 0

    def handle_input(self, events, environment):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                # See if we got clicked on.
                if (click_pos[0] - self.width) < self.x < click_pos[0] \
                        and click_pos[1] - self.height < self.y < click_pos[1]:
                    self.velocity_x = random.randint(0, 3)
                    self.velocity_y = random.randint(0, 3)

    def step(self, environment):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Turn around if we are out of bounds.
        if self.x < 0 or self.x + self.width > DISPLAY_WIDTH:
            self.velocity_x *= -1

        if self.y < 0 or self.y + self.height > DISPLAY_HEIGHT:
            self.velocity_y *= -1

    def draw(self, draw_context):
        rect_tuple = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(draw_context, COLOR_BLUE, rect_tuple, 0)


class GenericInputObject(GameObject):
    def __init__(self):
        # Calls the GameObject constructor (aka "init" function)
        super().__init__()

    def handle_input(self, events, environment):
        # Check if any buttons have been pressed
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Ball(random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT))
                elif event.key == pygame.K_ESCAPE:
                    environment.Running = False
            elif event.type == pygame.QUIT:
                environment.Running = False

    def step(self, environment):
        # Do nothing but override the function so we don't get
        # the error message from GameObject.
        pass

    def draw(self, draw_context):
        # Do nothing but override the function so we don't get
        # the error message from GameObject.
        pass


class Engine:
    # In this example, the "Engine" itself is the environment
    # object but it doesn't have to be that way.
    def __init__(self, draw_context):
        self.draw_context = draw_context
        self.Running = True

    def start(self):
        # This gets created and add to the list of game objects in its constructor (aka 'init')
        GenericInputObject()

    def handle_input(self):
        # Check if any buttons have been pressed
        events = pygame.event.get()
        for game_object in GameObject.GameObjects:
            game_object.handle_input(events, self)

    def step(self):
        # Perform the step function for all game objects.
        for game_object in GameObject.GameObjects:
            game_object.step(self)

    def draw(self):
        # Erase the background
        self.draw_context.fill(COLOR_WHITE)

        # Perform the draw function for all the game objects.
        for game_object in GameObject.GameObjects:
            game_object.draw(self.draw_context)

        pygame.display.update()


def main():
    # Press SPACE to create a block ('Ball' object).
    # Click on the ball object to start it moving.

    pygame.init()

    resolution = (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    game_display = pygame.display.set_mode(resolution)
    pygame.display.set_caption(WINDOW_TITLE)

    clock = pygame.time.Clock()

    # Start the game engine.
    game = Engine(game_display)
    game.start()

    clock.tick()
    while True:
        game.handle_input()
        game.step()
        game.draw()

        if not game.Running:
            break

        clock.tick(FRAME_RATE)

        # BELOW IS EDUCATIONAL!
        # This is the gist of what 'tick' is doing
        # tick() without any arguments, only returns the time since the last tick() call.
        #
        # frame_time = clock.tick()
        #
        # next_frame_delay = IDEAL_FRAME_TIME - frame_time
        # if next_frame_delay > 0:
        #    clock.wait(next_frame_delay)  # Multi-process friendly
        #    # clock.delay(next_frame_delay) More accurate but blocks the processor.


if __name__ == "__main__":
    main()

