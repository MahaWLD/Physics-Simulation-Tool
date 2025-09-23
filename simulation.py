import pygame.mouse
import pymunk.pygame_util
import os
from datetime import datetime
import json

from database import cursor, db
from undo_redo import UndoRedoList
from simulation_objects import *


class Simulation:
    def __init__(self, width, height, window, username):
        self.WIDTH, self.HEIGHT = width, height
        self.window = window
        self.space = pymunk.Space()
        self.username = username
        pygame.init()
        pygame.display.set_caption("Physics Simulation Tool")

        # pause by default
        self.resume = False

        # default FPS and time step
        self.FPS = 60
        self.DT = 1 / self.FPS

        # for pixel to metres and vice versa conversions
        self.__PIXELS_PER_METRE = 50

        # initialise gravitational acceleration
        gravitational_acceleration = self.get_gravitational_acceleration("Earth")
        self.space.gravity = (0, self.__metres_to_pixels(gravitational_acceleration))

        # undo redo list
        self.__undo_redo_list = UndoRedoList()

        # to store current objects and models in the scene
        self.objects = []
        self.models = []

        self.__PLATFORM_HEIGHT = 250

        # create boundaries
        self.__create_preset_objects()

        self.state_file = "simulation_state.json"
        if not os.path.exists(self.state_file):  # if file does not exist
            with open(self.state_file, "w") as f:  # create file
                json.dump({}, f)  # initialises the file with an empty object

        self.save_state(self.state_file)

        self.cannon_projectile_mapping = {}

    def __metres_to_pixels(self, metres):
        return metres * self.__PIXELS_PER_METRE

    def __pixels_to_metres(self, pixels):
        return pixels / self.__PIXELS_PER_METRE

    @staticmethod
    def __resolve_vectors(vector_magnitude, angle_in_degrees):
        angle_in_rad = math.radians(angle_in_degrees)
        vector_x = vector_magnitude * math.cos(angle_in_rad)
        vector_y = vector_magnitude * math.sin(angle_in_rad)
        return vector_x, vector_y

    @staticmethod
    def __combine_vectors(vector_x, vector_y):
        combined = math.sqrt(vector_x ** 2 + vector_y ** 2)  # pythagoras
        return combined

    @staticmethod
    def apply_force(obj, force):
        obj.body.apply_force_at_world_point((force[0], force[1]), obj.body.position)

    @staticmethod
    def __apply_impulse(obj, force):
        obj.body.apply_impulse_at_world_point((force[0], force[1]), obj.body.position)

    def apply_force_to_object(self, obj, force_data, resolved):
        if resolved:
            force_x = self.__metres_to_pixels(force_data["force_x"])
            force_y = self.__metres_to_pixels(force_data["force_y"])
        else:
            force = self.__metres_to_pixels(force_data["force"])
            force_x, force_y = self.__resolve_vectors(force, -force_data["angle"])
        obj.force_x += force_x
        obj.force_y -= force_y  # makes upwards direction positive

    def __create_preset_objects(self):
        # preset object configurations
        object_configs = [
            (Platform, (self.WIDTH // 2, self.HEIGHT - 125), 0.5, 0.5, (self.WIDTH, self.__PLATFORM_HEIGHT)),
            (Boundary, (self.WIDTH // 2, 0), 0.5, 0.5, (self.WIDTH, 5), "Ceiling"),
            (Boundary, (0, self.HEIGHT // 2), 0.5, 0.5, (5, self.WIDTH), "Left wall"),
            (Boundary, (self.WIDTH, self.HEIGHT // 2), 0.5, 0.5, (5, self.HEIGHT), "Right wall")
        ]

        for obj_class, pos, elasticity, friction, *args in object_configs:
            obj = obj_class(self.space, self.window, pos, elasticity, friction, *args)
            obj.create_shape()

            if obj.obj_type == "object":
                self.objects.append(obj)
            else:
                self.models.append(obj)

    def add_object(self, object_data, resolved):
        if resolved:
            # impulse = mass * velocity
            impulse_x, impulse_y = (object_data["mass"] * self.__metres_to_pixels(object_data["initial_velocity_x"]),
                                    object_data["mass"] * self.__metres_to_pixels(object_data["initial_velocity_y"]))
        else:
            velocity_x, velocity_y = self.__resolve_vectors(self.__metres_to_pixels(object_data["initial_velocity"]),
                                                            object_data["velocity_angle"])
            impulse_x, impulse_y = (velocity_x * object_data["mass"],
                                    -velocity_x * object_data["mass"])

        if object_data["object"].lower() == "ball":
            # create ball
            Ball.name = Ball(self.space, self.window, object_data["position"], object_data["elasticity"],
                             object_data["friction"], self.__metres_to_pixels(object_data["radius"]),
                             object_data["mass"])
            Ball.name.create_shape()
            self.objects.append(Ball.name)
            self.__apply_impulse(Ball.name, (impulse_x, -impulse_y))  # makes upwards direction positive
            object_data = self.get_object_data(Ball.name)

            if "force_x" in object_data:
                Ball.name.force_x += object_data["force_x"]
                Ball.name.force_y += object_data["force_y"]
                Ball.name.body.angle = object_data["angle"]

        elif object_data["object"].lower() == "block":
            # create block
            Block.name = Block(self.space, self.window, object_data["position"], object_data["elasticity"],
                               object_data["friction"],
                               (self.__metres_to_pixels(object_data["width"]),
                                self.__metres_to_pixels(object_data["height"])), object_data["mass"])
            Block.name.create_shape()
            self.objects.append(Block.name)
            self.__apply_impulse(Block.name, (impulse_x, impulse_y))
            object_data = self.get_object_data(Block.name)

            if "force_x" in object_data:
                Block.name.force_x += object_data["force_x"]
                Block.name.force_y += object_data["force_y"]
                Block.name.body.angle = object_data["angle"]

        # append action to undo_redo_list
        self.__undo_redo_list.append("add object", object_data)
        self.__undo_redo_list.display()

    def delete_object(self, obj, add_to_undo_list):
        object_data = self.get_object_data(obj)
        if add_to_undo_list:
            self.__undo_redo_list.append("delete object", object_data)
            self.__undo_redo_list.display()
        obj.delete_shape()
        self.objects.remove(obj)

    @staticmethod
    def get_mouse_position():
        mouse_clicked = False
        while not mouse_clicked:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
        return pygame.mouse.get_pos()

    def add_cannon(self, position_x):
        # create cannon
        Cannon.name = Cannon(self.space, self.window, position_x)
        self.models.append(Cannon.name)

        # create projectile
        Projectile.name = Projectile(self.space, self.window, (position_x, self.HEIGHT - self.__PLATFORM_HEIGHT - 35),
                                     0.5, 0.5, 35, 50)
        Projectile.name.create_shape()
        self.objects.append(Projectile.name)

        # map projectile to cannon
        self.cannon_projectile_mapping[Cannon.name] = Projectile.name  # hash table

    def launch_projectile(self, projectile, angle, initial_velocity):
        initial_velocity = self.__metres_to_pixels(initial_velocity)
        velocity_x, velocity_y = self.__resolve_vectors(initial_velocity, angle)
        velocity_y = -velocity_y  # upwards is the positive direction
        impulse_x, impulse_y = (projectile.mass * velocity_x,
                                projectile.mass * velocity_y)
        self.__apply_impulse(projectile, (impulse_x, impulse_y))

    def reload_cannon(self, cannon, projectile):
        # reposition projectile
        projectile.body.position = (cannon.position_x + 100, self.HEIGHT - self.__PLATFORM_HEIGHT - 35)

    def save_state(self, filename):
        # a list to store the data for each object
        objects_data = []

        # save position, velocity and angle of each object
        for obj in self.objects:
            obj_data = {
                "object_name": obj.name,
                "position": obj.body.position,
                "velocity": obj.body.velocity,
                "angle": obj.body.angle
            }
            objects_data.append(obj_data)

        # write the list of object data to a JSON file
        with open(filename, "w") as f:
            json.dump(objects_data, f, indent=4)  # serialisation

    def load_state(self, filename):
        with open(filename, "r") as f:
            objects_data = json.load(f)  # deserialization

        for obj_data in objects_data:
            # find the object with the corresponding name or identifier
            for obj in self.objects:
                if obj.name == obj_data["object_name"]:
                    # update the object's position and velocity
                    obj.body.position = obj_data["position"]
                    obj.body.velocity = obj_data["velocity"]
                    obj.body.angle = obj_data["angle"]
                    break  # once the object is found and updated, exit the loop

        self.space.step(self.DT)

    def undo_action(self):
        action, data = self.__undo_redo_list.undo()
        if action:
            if action == "add object":
                self.__undo_add_object(data)
                print("[Undo successful]")
            elif action == "delete object":
                self.__undo_delete_object(data)
                print("[Undo successful]")

    def __undo_add_object(self, object_data):
        obj = object_data["object"]
        obj.delete_shape()
        self.objects.remove(obj)

    def __undo_delete_object(self, object_data):
        self.add_object_back(object_data)

    def redo_action(self):
        action, data = self.__undo_redo_list.redo()
        if action:
            if action == "add object":
                self.__undo_delete_object(data)
                print("[Redo successful]")
            elif action == "delete object":
                self.__undo_add_object(data)
                print("[Redo successful]")

    def add_object_back(self, object_data):
        if object_data["object_type"] == "Ball":
            # create ball
            Ball.name = Ball(self.space, self.window, object_data["position"], object_data["elasticity"],
                             object_data["friction"], object_data["radius"], object_data["mass"])
            Ball.name.create_shape()
            self.objects.append(Ball.name)

        elif object_data["object_type"] == "Block":
            # create block
            Block.name = Block(self.space, self.window, object_data["position"], object_data["elasticity"],
                               object_data["friction"],
                               (object_data["width"], object_data["height"]), object_data["mass"])
            Block.name.create_shape()
            self.objects.append(Block.name)

    @staticmethod
    def get_object_data(obj):
        obj_data = {
            "object": obj,
            "object_name": obj.name,
            "object_type": obj.__class__.__name__,
            "position": obj.body.position,
            "mass": obj.body.mass,
            "initial_velocity_x": obj.body.velocity[0],
            "initial_velocity_y": obj.body.velocity[1],
            "angle": obj.body.angle,
            "elasticity": obj.shape.elasticity,
            "friction": obj.shape.friction
        }
        if obj_data["object_type"] == "Ball":
            obj_data["radius"] = obj.radius
        elif obj_data["object_type"] == "Block":
            obj_data["width"] = obj.size[0]
            obj_data["height"] = obj.size[1]
        return obj_data

    def get_graph_data(self, obj):
        obj_data = {
            "Height": round(self.__calculate_height(obj), 2),
            "Velocity": round(self.__calculate_velocity(obj), 2),
            "Vertical velocity": round(self.__pixels_to_metres(obj.body.velocity[1]), 2),
            "Horizontal velocity": round(self.__pixels_to_metres(obj.body.velocity[0]), 2),
            "Kinetic energy": round(self.__calculate_kinetic_energy(obj), 2),
            "Gravitational potential energy": round(self.__calculate_gravitational_potential_energy(obj), 2)
        }
        return obj_data

    def __calculate_height(self, obj):
        height = self.HEIGHT - self.__PLATFORM_HEIGHT - obj.body.position[1]
        if obj.__class__.__name__ == "Ball":
            height -= obj.radius
        elif obj.__class__.__name__ == "Block":
            height -= obj.size[1] // 2
        return self.__pixels_to_metres(height)

    def __calculate_velocity(self, obj):
        velocity = self.__combine_vectors(obj.body.velocity[0], obj.body.velocity[1])
        return self.__pixels_to_metres(velocity)

    def __calculate_kinetic_energy(self, obj):
        velocity = self.__calculate_velocity(obj)
        ke = 1 / 2 * obj.shape.mass * velocity ** 2
        return ke

    def __calculate_gravitational_potential_energy(self, obj):
        height = self.__calculate_height(obj)
        g = self.__pixels_to_metres(self.space.gravity[1])
        gpe = obj.shape.mass * g * height
        return gpe

    def __draw_vectors(self, obj, vector, scale_factor, colour, units):
        vector_x = vector[0]
        vector_y = vector[1]

        SCALE_FACTOR = scale_factor

        # define coordinates for the endpoints of the vector stored in tuples
        horizontal_end_pos = (obj.body.position[0] + vector_x * SCALE_FACTOR, obj.body.position[1])
        vertical_end_pos = (obj.body.position[0], obj.body.position[1] + vector_y * SCALE_FACTOR)

        # draw vectors
        pygame.draw.line(self.window, colour, obj.body.position, horizontal_end_pos, 5)
        pygame.draw.line(self.window, colour, obj.body.position, vertical_end_pos, 5)

        # arrowheads
        arrowhead_size = 10
        if vector_x > 0.0001 or vector_x < 0.0001:
            # object does not appear to be moving or have a force exerted upon it
            # at a velocity or force smaller than this
            if vector_x > 0.0001:
                horizontal_arrowhead_points = [(horizontal_end_pos[0], horizontal_end_pos[1] - arrowhead_size),
                                               (horizontal_end_pos[0] + arrowhead_size, horizontal_end_pos[1]),
                                               (horizontal_end_pos[0], horizontal_end_pos[1] + arrowhead_size)]
            else:
                horizontal_arrowhead_points = [(horizontal_end_pos[0], horizontal_end_pos[1] - arrowhead_size),
                                               (horizontal_end_pos[0] - arrowhead_size, horizontal_end_pos[1]),
                                               (horizontal_end_pos[0], horizontal_end_pos[1] + arrowhead_size)]

            pygame.draw.polygon(self.window, colour, horizontal_arrowhead_points)

            font = pygame.font.SysFont("Calibre", 28)  # font and font size
            text = font.render(f"{abs(vector_x):.2f} {units}", True, "dark blue")  # show value to 2 decimal places
            text_rect = text.get_rect(center=(horizontal_end_pos[0] + 20, horizontal_end_pos[1]))
            self.window.blit(text, text_rect)

        # same logic for the vector in the y-direction
        if vector_y > 0.0001 or vector_y < 0.0001:
            if vector_y > 0.0001:
                vertical_arrowhead_points = [(vertical_end_pos[0] - arrowhead_size, vertical_end_pos[1]),
                                             (vertical_end_pos[0], vertical_end_pos[1] + arrowhead_size),
                                             (vertical_end_pos[0] + arrowhead_size, vertical_end_pos[1])]
            else:
                vertical_arrowhead_points = [(vertical_end_pos[0] - arrowhead_size, vertical_end_pos[1]),
                                             (vertical_end_pos[0], vertical_end_pos[1] - arrowhead_size),
                                             (vertical_end_pos[0] + arrowhead_size, vertical_end_pos[1])]
            pygame.draw.polygon(self.window, colour, vertical_arrowhead_points)

            font = pygame.font.SysFont("Calibre", 28)
            text = font.render(f"{abs(vector_y):.2f} {units}", True, "dark blue")
            text_rect = text.get_rect(center=(horizontal_end_pos[0], vertical_end_pos[1] + 20))
            self.window.blit(text, text_rect)

    def draw_velocity_vectors(self, obj):
        velocity = self.__pixels_to_metres(obj.body.velocity)
        self.__draw_vectors(obj, velocity, 10, "blue", "m/s")

    def draw_force_vectors(self, obj):
        # draw any forces that have been applied on the object
        force = (self.__pixels_to_metres(obj.force_x), self.__pixels_to_metres(obj.force_y))
        self.__draw_vectors(obj, force, 0.1, "red", "N")

        # draw the weight force acting on the object
        weight = (0, obj.shape.mass * self.__pixels_to_metres(self.space.gravity[1]))  # W = mg
        self.__draw_vectors(obj, weight, 0.1, "grey", "N")

    def edit_gravitational_acceleration(self, acceleration):
        self.space.gravity = (0, self.__metres_to_pixels(acceleration))

    @staticmethod
    def edit_object_properties(obj, data):
        if hasattr(obj, "mass"):
            obj.shape.mass = data["mass"]
        if hasattr(obj, "elasticity"):
            obj.shape.elasticity = data["elasticity"]
        if hasattr(obj, "friction"):
            obj.shape.friction = data["friction"]

    @staticmethod
    def get_gravitational_acceleration(planet):
        gravitational_accelerations = {
            "Earth": 9.8,
            "Moon": 1.6,
            "Mars": 3.7,
            "Jupiter": 23.1
        }
        return gravitational_accelerations[planet]

    def change_fps(self, fps):
        self.FPS = fps
        self.DT = 1 / self.FPS

    def set_to_default_fps(self):
        self.FPS = 60
        self.DT = 1 / self.FPS

    def save_as_project(self, project_name):
        query = "SELECT * FROM SavedProjects WHERE project_name = %s AND userID = %s"
        cursor.execute(query, (project_name, self.username))
        existing_project = cursor.fetchone()

        if existing_project:
            # update existing record
            update_query = "UPDATE SavedProjects SET FPS = %s, date_created = %s WHERE " \
                           "project_name = %s AND userID = %s"
            cursor.execute(update_query, (self.FPS, datetime.now(), project_name, self.username))
            db.commit()
            print("[Updated project]")

            project_id = existing_project[0]
        else:
            # insert new record
            insert_query = "INSERT INTO SavedProjects (project_name, userID, FPS, date_created) " \
                           "VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (project_name, self.username, self.FPS, datetime.now()))
            db.commit()
            print("[Saved project]")

            project_id = cursor.lastrowid

        self.save_objects(project_id)

    def save_objects(self, project_id):
        try:
            # Delete existing objects associated with the project
            delete_query = "DELETE FROM Objects WHERE projectID = %s"
            cursor.execute(delete_query, (project_id,))
            db.commit()
            print("[Deleted existing objects]")

            # Insert objects
            insert_ball_query = "INSERT INTO Objects (object_name, projectID, object_type, " \
                                "position_x, position_y, velocity_x, velocity_y, force_x, force_y, " \
                                "angle, mass, friction, elasticity, radius) " \
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            insert_block_query = "INSERT INTO Objects (object_name, projectID, object_type, " \
                                 "position_x, position_y, velocity_x, velocity_y, force_x, force_y, " \
                                 "angle, mass, friction, elasticity, width, height) " \
                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            for obj in self.objects:
                try:
                    if obj.__class__.__name__ == "Ball":
                        cursor.execute(insert_ball_query, (
                            obj.name, project_id, "Ball",
                            obj.body.position[0], obj.body.position[1],
                            obj.body.velocity[0], obj.body.velocity[1],
                            obj.force_x, obj.force_y,
                            obj.body.angle, obj.body.mass,
                            obj.shape.friction, obj.shape.elasticity,
                            self.__pixels_to_metres(obj.radius)
                        ))
                        db.commit()
                        print("[Inserted object]", obj.name)
                    elif obj.__class__.__name__ == "Block":
                        cursor.execute(insert_block_query, (
                            obj.name, project_id, "Block",
                            obj.body.position[0], obj.body.position[1],
                            obj.body.velocity[0], obj.body.velocity[1],
                            obj.force_x, obj.force_y,
                            obj.body.angle, obj.body.mass,
                            obj.shape.friction, obj.shape.elasticity,
                            self.__pixels_to_metres(obj.size[0]), self.__pixels_to_metres(obj.size[1])
                        ))
                        db.commit()
                        print("[Inserted object]", obj.name)
                except Exception as e:
                    db.rollback()
                    print("Error inserting object:", e)

            # Insert cannons
            insert_cannon_query = "INSERT INTO Objects (object_name, projectID, object_type, position_x) " \
                                  "VALUES(%s, %s, %s, %s)"
            for cannon in self.models:
                if isinstance(cannon, Cannon):
                    try:
                        cursor.execute(insert_cannon_query, (cannon.name, project_id, 'Cannon', cannon.position_x))
                        db.commit()
                        print("[Inserted cannon]", cannon.name)
                    except Exception as e:
                        db.rollback()
                        print("Error inserting cannon:", e)

            print("[Objects saved successfully]")
        except Exception as e:
            print("Error saving objects:", e)

    def load_project(self, project_name):
        try:
            query = '''
                SELECT o.object_name, o.object_type, o.position_x, o.position_y,
                o.velocity_x, o.velocity_y, o.force_x, o.force_y, o.angle, o.mass, o.friction, o.elasticity,
                o.radius, o.width, o.height
            FROM Objects o
            JOIN SavedProjects sp ON o.projectID = sp.projectID
            WHERE sp.project_name = %s AND sp.userID = %s
            '''

            cursor.execute(query, (project_name, self.username))

            # fetch the project data
            project_data = cursor.fetchall()

            # data processing
            for row in project_data:
                object_name, object_type, position_x, position_y, velocity_x, velocity_y, force_x, force_y, angle, \
                mass, friction, elasticity, radius, width, height = row

                object_data = {
                    "object_name": object_name,
                    "object": object_type,
                    "position": (position_x, position_y),
                    "initial_velocity_x": velocity_x,
                    "initial_velocity_y": velocity_y,
                    "force_x": force_x,
                    "force_y": force_y,
                    "angle": angle,
                    "mass": mass,
                    "friction": friction,
                    "elasticity": elasticity,
                    "radius": radius,
                    "width": width,
                    "height": height
                }

                if object_type == "Ball" or object_type == "Block":
                    self.add_object(object_data, resolved=True)
                elif object_type == "Cannon":
                    self.add_cannon(position_x)

            print("[Project loaded successfully]")

        except Exception as e:
            print("Error loading project:", e)
