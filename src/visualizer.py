import pygame
import math
from .graph import Graph
from .simulation import Simulation


class Visualizer:

    def __init__(
        self,
        graph: Graph,
        simulation: Simulation
    ) -> None:

        self.graph = graph
        self.simulation = simulation

        pygame.init()

        self.screen = pygame.display.set_mode((1900, 1000))
        pygame.display.set_caption("Fly-in")

        self.clock = pygame.time.Clock()

        self.scale = 1
        self.offset_x = 0
        self.offset_y = 0

        self.font = pygame.font.Font(None, 36)

        self.calculate_transform()

    def calculate_transform(self) -> None:

        zones = list(self.graph.zones.values())

        if not zones:
            return

        min_x = min(zone.x for zone in zones)
        max_x = max(zone.x for zone in zones)

        min_y = min(zone.y for zone in zones)
        max_y = max(zone.y for zone in zones)

        graph_width = max_x - min_x
        graph_height = max_y - min_y

        screen_width, screen_height = self.screen.get_size()

        margin = 100

        available_width = screen_width - 2 * margin
        available_height = screen_height - 2 * margin

        scale_x = (
            available_width / graph_width
            if graph_width > 0
            else float("inf")
        )

        scale_y = (
            available_height / graph_height
            if graph_height > 0
            else float("inf")
        )

        self.scale = min(scale_x, scale_y)

        self.offset_x = (
            screen_width
            - graph_width * self.scale
        ) / 2 - min_x * self.scale

        self.offset_y = (
            screen_height
            - graph_height * self.scale
        ) / 2 - min_y * self.scale

    def screen_position(self, zone):

        x = zone.x * self.scale + self.offset_x
        y = zone.y * self.scale + self.offset_y

        return int(x), int(y)

    def draw(self) -> None:

        self.screen.fill((30, 30, 30))

        self.draw_connections()
        self.draw_zones()
        self.draw_drones()
        self.draw_turn()

        pygame.display.flip()

    def draw_connections(self) -> None:

        for connection in self.graph.connections:

            zone1 = self.graph.zones[connection.zone1]
            zone2 = self.graph.zones[connection.zone2]

            pos1 = self.screen_position(zone1)
            pos2 = self.screen_position(zone2)

            pygame.draw.line(
                self.screen,
                (100, 100, 100),
                pos1,
                pos2,
                5
            )

    def draw_zones(self) -> None:

        for zone in self.graph.zones.values():

            position = self.screen_position(zone)
            color = self.resolve_color(zone.color)

            pygame.draw.circle(
                self.screen,
                color,
                position,
                23
            )

    def resolve_color(self, color_name: str) -> tuple[int, int, int]:
        try:
            c = pygame.Color(color_name)
            return (c.r, c.g, c.b)
        except ValueError:
            # if the color name dosen't exist return a default color
            return (200, 200, 200)

    def draw_drones(self) -> None:

        for zone in self.graph.zones.values():

            drones = zone.drones

            if not drones:
                continue

            center_x, center_y = self.screen_position(zone)

            total = len(drones)

            for index, drone in enumerate(drones):
                angle = 2 * math.pi * index / total
                radius = 35
                x = int(center_x + math.cos(angle) * radius)
                y = int(center_y + math.sin(angle) * radius)

                pygame.draw.circle(
                    self.screen,
                    (255, 250, 250),
                    (x, y),
                    7
                )

    def draw_turn(self) -> None:

        text = self.font.render(
            f"Turn: {self.simulation.turn}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (30, 30))

    def run(self) -> None:

        self.simulation.initialize_drones()

        running = True

        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT:

                        if not self.simulation.all_finished():
                            self.simulation.simulate_turn()

            self.draw()

            self.clock.tick(60)

        pygame.quit()
