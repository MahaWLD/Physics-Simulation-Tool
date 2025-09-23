import pygame
import pymunk
import pymunk.pygame_util
import math

from abc import ABC, abstractmethod


class Object(ABC):  # abstract class -
    # prevents a user from creating an object of that class
    # ensures abstract methods are overridden in a child class
    def __init__(self, space, window, pos, elasticity, friction, obj_type):
        self.space = space
        self.window = window
        self.draw_options = pymunk.pygame_util.DrawOptions(window)
        self.pos = pos
        self.elasticity = elasticity
        self.friction = friction
        self.obj_type = obj_type
        self.body = None
        self.shape = None

    # different implementations of the create shape method demonstrates polymorphism
    @abstractmethod
    def create_shape(self):  # has a declaration but not an implementation
        pass

    def delete_shape(self):
        if self.body:
            self.space.remove(self.body, self.shape)

    @abstractmethod
    def draw(self):
        self.space.debug_draw(self.draw_options)


class Ball(Object):
    count = 0  # class variable shared among all its instances

    def __init__(self, space, window, pos, elasticity, friction, radius, mass):
        super().__init__(space, window, pos, elasticity, friction, "object")
        Ball.count += 1
        self.name = f"Ball {Ball.count}"
        self.radius = radius
        self.mass = mass  # in kg
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.force_x = 0
        self.force_y = 0
        self.show_velocity_vectors = True
        self.show_force_vectors = False

    def create_shape(self):
        self.body.position = self.pos
        self.shape.mass = int(self.mass)
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction
        self.space.add(self.body, self.shape)

    def draw(self):
        self.space.debug_draw(self.draw_options)

    def toggle_velocity_vectors(self):
        self.show_velocity_vectors = not self.show_velocity_vectors

    def toggle_force_vectors(self):
        self.show_force_vectors = not self.show_force_vectors


class Block(Object):
    count = 0

    def __init__(self, space, window, pos, elasticity, friction, size, mass):
        super().__init__(space, window, pos, elasticity, friction, "object")
        Block.count += 1
        self.name = f"Block {Block.count}"
        self.size = size
        self.mass = mass
        self.body = pymunk.Body()
        self.shape = pymunk.Poly.create_box(self.body, self.size,
                                            radius=2)  # adds a border, even a curved edge when made large
        self.force_x = 0
        self.force_y = 0
        self.show_velocity_vectors = True
        self.show_force_vectors = False

    def create_shape(self):
        self.body.position = self.pos
        self.shape.mass = self.mass
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction
        self.space.add(self.body, self.shape)

    def draw(self):
        self.space.debug_draw(self.draw_options)

    def toggle_velocity_vectors(self):
        self.show_velocity_vectors = not self.show_velocity_vectors

    def toggle_force_vectors(self):
        self.show_force_vectors = not self.show_force_vectors


class Platform(Object):
    def __init__(self, space, window, pos, elasticity, friction, size):
        super().__init__(space, window, pos, elasticity, friction, "model")
        self.name = "Platform"
        self.size = size
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Poly.create_box(self.body, self.size)

    def create_shape(self):
        self.body.position = self.pos
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction
        self.space.add(self.body, self.shape)

    def draw(self):
        self.space.debug_draw(self.draw_options)


class Boundary(Object):
    def __init__(self, space, window, pos, elasticity, friction, size, name):
        super().__init__(space, window, pos, elasticity, friction, "model")
        self.name = name
        self.size = size
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Poly.create_box(self.body, self.size)

    def create_shape(self):
        self.body.position = self.pos
        self.shape.elasticity = self.elasticity
        self.shape.friction = self.friction
        self.space.add(self.body, self.shape)

    def draw(self):
        self.space.debug_draw(self.draw_options)


class Cannon(Object):
    count = 0

    def __init__(self, space, window, position_x):
        super().__init__(space, window, (position_x, 450), None, None, "model")
        Cannon.count += 1
        self.name = f"Cannon {Cannon.count}"
        self.default_image = pygame.image.load("Images/Simulator/Models/Cannon.png")
        self.image = self.default_image
        image_width = self.image.get_width()
        self.position_x = position_x - (image_width // 2)
        self.angle = 0
        self.show_cannon_buttons = False

    def create_shape(self):
        pass

    def rotate_cannon(self, angle):
        self.image = self.default_image  # reset image
        self.angle = angle
        centred_image = self.image.copy()
        centred_image_rect = centred_image.get_rect()

        # image will rotate about the centre
        pivot_x, pivot_y = centred_image_rect.center

        angle_rad = math.radians(self.angle)

        # rotate anti-clockwise from the horizontal positive
        sin_theta = math.sin(-angle_rad)
        cos_theta = math.cos(-angle_rad)

        # rotation matrix
        rotation_matrix = [
            [cos_theta, -sin_theta],
            [sin_theta, cos_theta]
        ]

        # create a surface for the rotated image with transparency
        rotated_rect = centred_image.get_rect()
        rotated_image = pygame.Surface(rotated_rect.size, pygame.SRCALPHA)

        for x in range(centred_image.get_width()):
            for y in range(centred_image.get_height()):
                # find rotated coordinates
                rotated_x = (x - pivot_x) * rotation_matrix[0][0] + (y - pivot_y) * rotation_matrix[0][1]
                rotated_x += pivot_x
                rotated_x = int(round(rotated_x))
                rotated_y = (x - pivot_x) * rotation_matrix[1][0] + (y - pivot_y) * rotation_matrix[1][1]
                rotated_y += pivot_y
                rotated_y = int(round(rotated_y))

                pixel_colour = centred_image.get_at((x, y))
                rotated_image.set_at((rotated_x, rotated_y), pixel_colour)

        self.image = rotated_image

    def draw(self):
        self.window.blit(self.image, (self.position_x, 450))


class Projectile(Ball):
    count = 0

    def __init__(self, space, window, pos, elasticity, friction, radius, mass):
        super().__init__(space, window, pos, elasticity, friction, radius, mass)
        Projectile.count += 1
        self.name = f"Projectile {Projectile.count}"
