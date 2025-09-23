from Pages.page import Page

import pygame
import pygameUI

import csv

from SimulationTabs.projectile_input_tab import ProjectileInput
from SimulationTabs.object_tab import ObjectTab
from SimulationTabs.InteractiveMode.interactive_mode_tab import InteractiveMode
from SimulationTabs.scene_object_properties_tab import SceneObjectProperties
from SimulationTabs.save_project_tab import SaveProject
from SimulationTabs.graph import GraphDataInput


class SimulatorPage(Page):
    def __init__(self, simulation):
        super().__init__()
        self.__simulation = simulation  # aggregation
        self.__interactive_mode = InteractiveMode(simulation, simulation.username)  # composition
        self.__graph_input = GraphDataInput(simulation)  # composition
        self.__screen = pygame.display.set_mode((self._WIDTH, self._HEIGHT))
        self.__initUI()
        self.__show_save_button()
        self.settings_window.set_simulation(simulation)
        self.settings_window.simulation = simulation

        self.object_data = {}   # for CSV

    def __initUI(self):
        super()._initUI()
        self.buttons = []

        self.pause_resume_button = pygameUI.IconButton((64, 734), 81, 81,
                                                       "Images/Simulator/Icons/ResumeIcon.svg",
                                                       function=self.__pause_resume)
        self.buttons.append(self.pause_resume_button)

        self.restart_button = pygameUI.IconButton((154, 744), 61, 61,
                                                  "Images/Simulator/Icons/RestartIcon.svg", function=self.__restart)
        self.buttons.append(self.restart_button)

        self.redo_button = pygameUI.IconButton((1110, 30), 51, 51, "Images/Simulator/Icons/RedoIcon.svg",
                                               function=self.__redo_action)
        self.buttons.append(self.redo_button)

        self.undo_button = pygameUI.IconButton((1030, 20), 71, 71, "Images/Simulator/Icons/UndoIcon.svg",
                                               function=self.__undo_action)
        self.buttons.append(self.undo_button)

        self.object_tab_button = pygameUI.TextButton((self._WIDTH // 2 - 50, self._HEIGHT - 50), 100, 50,
                                                     "Objects tab", "white", 18,
                                                     function=self.__show_object_tab)
        self.buttons.append(self.object_tab_button)

        self.scene_object_properties_button = pygameUI.TextButton((180, 40), 200, 50, "Scene/Object Properties",
                                                                  (111, 212, 255), 22,
                                                                  function=self.__show_properties)
        self.buttons.append(self.scene_object_properties_button)

        self.interactive_mode_button = pygameUI.TextButton((390, 40), 200, 50, "Interactive Mode",
                                                           (96, 220, 137), 22,
                                                           function=self.__show_interactive_mode)
        self.buttons.append(self.interactive_mode_button)

        self.interactive_mode_icon = pygameUI.IconButton((395, 50), 30, 30,
                                                         "Images/Simulator/Icons/InteractiveIcon.png")
        self.buttons.append(self.interactive_mode_icon)

        self.display_graph_button = pygameUI.TextButton((1200, 40), 200, 50, "Display graph", (111, 212, 255), 22,
                                                        function=self.__toggle_graph)
        self.buttons.append(self.display_graph_button)

        self.simulator_settings_button = pygameUI.IconButton((1450, 734), 81, 81,
                                                             "Images/Simulator/Icons/SettingsIcon.png",
                                                             self._toggle_settings)  # using superclass method
        self.buttons.append(self.simulator_settings_button)

        self.scale_image = pygame.image.load("Images/Simulator/Scale.png")
        self.positive_direction_image = pygame.image.load("Images/Simulator/Positive direction.png")

    def __show_save_button(self):
        if self.__simulation.username != "Guest":
            self.save_button = pygameUI.TextButton((0, 0), 75, 25, "Save project", "#d1dbe3", 16,
                                                   function=self.__save_project)
            self.buttons.append(self.save_button)

    def __show_cannon_buttons(self, cannon, projectile, position_x):
        self.projectile_input_button = pygameUI.TextButton((position_x, 700), 175, 25, "Input angle/initial velocity",
                                                           "#d1dbe3", 16,
                                                           function=lambda: self.__show_projectile_input(cannon,
                                                                                                         projectile))
        self.buttons.append(self.projectile_input_button)

        self.reload_button = pygameUI.TextButton((position_x + 180, 700), 100, 25, "Reload cannon", "#d1dbe3", 16,
                                                 function=lambda: self.__reload_cannon(cannon, projectile))
        self.buttons.append(self.reload_button)

    def __show_projectile_input(self, cannon, projectile):
        self.projectile_input = ProjectileInput(self.__simulation, cannon, projectile)
        self.projectile_input.show()
        self.__show_message_box("Rotate the cannon and choose an initial velocity")

    def __reload_cannon(self, cannon, projectile):
        self.__simulation.reload_cannon(cannon, projectile)

    def __show_save_as_csv_button(self):
        self.save_as_csv_button = pygameUI.TextButton((1200, 875), 200, 20, "Save as CSV", "grey", 26, "black",
                                                      function=self.__save_as_csv)
        self.buttons.append(self.save_as_csv_button)

    def __hide_save_as_csv_button(self):
        if hasattr(self, 'save_as_csv_button'):
            self.buttons.remove(self.save_as_csv_button)
            del self.save_as_csv_button

    def __save_project(self):
        self.save_project = SaveProject(self.__simulation)
        self.save_project.show()

    def __undo_action(self):
        self.__simulation.undo_action()

    def __redo_action(self):
        self.__simulation.redo_action()

    def __show_message_box(self, text):
        self.message_box = pygameUI.TextButton((0, 0), 0, 40, text, "black", 24, font_colour="white")
        text_surface = self.message_box.font.render(self.message_box.text, True, self.message_box.font_colour)
        text_width, text_height = text_surface.get_size()
        self.message_box.width = text_width + 25
        self.message_box.pos = (self._WIDTH // 2 - text_width // 2, 125)
        self.buttons.append(self.message_box)

        pygame.time.set_timer(pygame.USEREVENT, 10000)  # timer to remove message box after 10 seconds

    def __pause_resume(self):
        if self.__simulation.resume:  # pausing
            self.__simulation.resume = False
            self.pause_resume_button.image_path = "Images/Simulator/Icons/ResumeIcon.svg"
        else:  # resuming
            self.__simulation.resume = True
            self.pause_resume_button.image_path = "Images/Simulator/Icons/PauseIcon.svg"

            self.__simulation.save_state(self.__simulation.state_file)
        self.pause_resume_button.update_image()

    def __restart(self):
        self.__simulation.resume = False
        self.pause_resume_button.image_path = "Images/Simulator/Icons/ResumeIcon.svg"
        self.pause_resume_button.update_image()
        self.__simulation.load_state(self.__simulation.state_file)
        self.__show_message_box("Simulation restarted")

        self.object_data = {}

    def __show_object_tab(self):
        self.objects_tab = ObjectTab(self.__simulation)
        self.objects_tab.show()
        self.__show_message_box("Choose where to place the object")

    def __toggle_graph(self):
        self.__graph_input.graph.toggle_graph()
        if self.__graph_input.graph.show_graph:
            # If the graph is currently shown, hide it and reset the data
            self.__hide_save_as_csv_button()
            self.objects_data = {}
            self.__graph_input.hide()
        else:
            # If the graph is not shown, create new graph input objects and a new graph
            self.__graph_input = GraphDataInput(self.__simulation)
            self.__graph_input.graph.toggle_graph()
            self.__graph_input.show()
            self.__show_save_as_csv_button()

    def __save_as_csv(self):
        filename = "object_data.csv"
        fieldnames = ["Object", "Height", "Velocity", "Vertical velocity", "Horizontal velocity", "Kinetic energy",
                      "Gravitational potential energy"]

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for obj, data in self.object_data.items():
                writer.writerow({"Object": obj, **data})

    def __show_properties(self):
        self.scene_object_properties = SceneObjectProperties(self.__simulation)
        self.scene_object_properties.show()

    def __show_interactive_mode(self):
        self.__interactive_mode.show()

    def _grid(self):  # overriding method in superclass
        self.py_surface.fill((180, 206, 222))

        if self.settings_window.show_grid:
            for x in range(0, self._WIDTH, 50):
                pygame.draw.line(self.py_surface, (43, 90, 179), (x, 0), (x, self._HEIGHT))
            for y in range(0, self._HEIGHT, 50):
                pygame.draw.line(self.py_surface, (43, 90, 179), (0, y), (self._WIDTH, y))

    def run(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # space can be used to resume/pause
                        self.__pause_resume()
                    elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            self.__redo_action()    # control shift z redoes an action
                        else:
                            self.__undo_action()    # control z undoes an action
                elif event.type == pygame.USEREVENT:
                    if hasattr(self, "message_box"):
                        self.buttons.remove(self.message_box)   # remove message box after 10 seconds
                        del self.message_box
                for button in self.buttons:
                    button.clicked(event)

            self._grid()
            self.__simulation.window.blit(self.py_surface, (0, 0))  # draw the background

            self.__simulation.window.blit(self.scale_image, (1450, 50))
            self.__simulation.window.blit(self.positive_direction_image, (50, 50))

            for obj in self.__simulation.objects:
                obj.draw()

            for obj in self.__simulation.models:
                obj.draw()

            if self.__graph_input.graph.show_graph and self.__graph_input.object_selected is not None:
                pygame.draw.rect(self.__simulation.window, "white", (990, 665, 420, 220))  # border
                data = self.__simulation.get_graph_data(self.__graph_input.object_selected)
                data = data[self.__graph_input.variable]
                self.__graph_input.graph.update_plot(data)
                self.__graph_input.graph.draw_on(self.__simulation.window)

                if self.__simulation.resume:
                    object_data = self.__simulation.get_graph_data(self.__graph_input.object_selected)
                    self.object_data.setdefault(self.__graph_input.object_selected, []).append(object_data)

            # if resumed, update simulation
            if self.__simulation.resume:
                self.__simulation.space.step(self.__simulation.DT)
                # csv file

            for button in self.buttons:
                button.draw(self.__simulation.window)

            for obj in self.__simulation.models:
                if obj.__class__.__name__ == "Cannon":
                    if not obj.show_cannon_buttons:
                        projectile = self.__simulation.cannon_projectile_mapping[obj]
                        self.__show_cannon_buttons(obj, projectile, obj.position_x + 100)
                        obj.show_cannon_buttons = True

            for obj in self.__simulation.objects:   # for each object in the scene
                if obj.show_velocity_vectors:
                    self.__simulation.draw_velocity_vectors(obj)
                if obj.show_force_vectors:
                    self.__simulation.draw_force_vectors(obj)
                obj.body.force = (0, 0)  # continuously clear and apply force
                self.__simulation.apply_force(obj, (obj.force_x, obj.force_y))

                # if object tunnelling occurs
                if obj.body.position[0] < 0 or obj.body.position[0] > self.__simulation.WIDTH or \
                        obj.body.position[1] < 0 or obj.body.position[1] > self.__simulation.HEIGHT:
                    self.__simulation.delete_object(obj, False)     # do not add action to undo/redo list

            pygame.display.flip()
            clock.tick(self.__simulation.FPS)

        pygame.quit()  # if not running
