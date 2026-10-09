
import pygame
import math

from .graph import Graph
from .simulation import Simulation


class Visualizer:
    """Display the graph and navigate through simulation history."""

    def __init__(
        self,
        graph: Graph,
        simulation: Simulation
    ) -> None:

        self.graph = graph
        self.simulation = simulation

        pygame.init()

        # 1900, 1000
        self.screen = pygame.display.set_mode((2800, 1200))
        pygame.display.set_caption("Fly-in")

        self.clock = pygame.time.Clock()

        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

        self.font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 38)

        # Index of the snapshot currently displayed.
        self.history_index = 0

        # Automatic playback.
        self.playing = False
        self.playback_delay = 500
        self.playback_timer = 0
        self.message_turn = False

        # Smooth movement between consecutive snapshots.
        self.animation_duration = 500.0  # milliseconds
        self.animation_elapsed = self.animation_duration
        self.animating = False

        self.animation_start_positions = {}
        self.animation_end_positions = {}

        self.calculate_transform()

    def calculate_transform(self) -> None:

        zones = list(self.graph.zones.values())

        if not zones:
            return

        min_x = min(zone.x for zone in zones)
        max_x = max(zone.x for zone in zones)

        min_y = min(zone.y for zone in zones)
        max_y = max(zone.y for zone in zones)

        # Prevent division by zero for single-row/column graphs.
        graph_width = max(max_x - min_x, 1)
        graph_height = max(max_y - min_y, 1)

        screen_width, screen_height = self.screen.get_size()

        margin = 120

        available_width = screen_width - 2 * margin
        available_height = screen_height - 2 * margin

        self.scale = min(
            available_width / graph_width,
            available_height / graph_height
        )

        self.offset_x = (
            screen_width - graph_width * self.scale
        ) / 2 - min_x * self.scale

        self.offset_y = (
            screen_height - graph_height * self.scale
        ) / 2 - min_y * self.scale

    def screen_position(self, zone):

        x = zone.x * self.scale + self.offset_x
        y = zone.y * self.scale + self.offset_y

        return int(x), int(y)

    def current_snapshot(self):
        """Return the snapshot selected by the history index."""

        if not self.simulation.history:
            return {}, {}, {}, {}

        self.history_index = max(
            0,
            min(
                self.history_index,
                len(self.simulation.history) - 1
            )
        )

        return self.simulation.history[self.history_index]

    def draw(self) -> None:

        self.screen.fill((30, 30, 30))

        snapshot = self.current_snapshot()

        drones_by_zone, drones_on_links, zone_counts, link_counts = (
            snapshot
        )

        self.draw_connections(link_counts)
        self.draw_zones(zone_counts)
        positions = self.get_animated_positions()
        self.draw_drones(positions)
        self.draw_turn()
        self.draw_controls()

        pygame.display.flip()

    def draw_connections(self, link_counts) -> None:

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

            # Display connection usage.
            count = link_counts.get(
                (connection.zone1, connection.zone2),
                link_counts.get(
                    (connection.zone2, connection.zone1),
                    0
                )
            )

            mid_x = (pos1[0] + pos2[0]) // 2
            mid_y = (pos1[1] + pos2[1]) // 2

            label = self.small_font.render(
                f"{count}/{connection.capacity}",
                True,
                (210, 210, 210)
            )

            self.screen.blit(
                label,
                (mid_x + 5, mid_y - 20)
            )

    def draw_zones(self, zone_counts) -> None:

        for zone in self.graph.zones.values():

            position = self.screen_position(zone)
            color = self.resolve_color(zone.color)

            pygame.draw.circle(
                self.screen,
                color,
                position,
                23
            )

            # Zone name.
            name = self.font.render(
                zone.name,
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                name,
                (
                    position[0] - name.get_width() // 2,
                    position[1] - 48
                )
            )

            # Occupancy / capacity.
            count = zone_counts.get(zone.name, 0)

            capacity_text = self.small_font.render(
                f"{count}/{zone.max_drones}",
                True,
                (255, 255, 255)
            )

            self.screen.blit(
                capacity_text,
                (
                    position[0] - capacity_text.get_width() // 2,
                    position[1] + 29
                )
            )

    def resolve_color(self, color_name: str) -> tuple[int, int, int]:

        try:
            color = pygame.Color(color_name)
            return color.r, color.g, color.b

        except (ValueError, TypeError):
            return 200, 200, 200

    def draw_drones(self, positions) -> None:
        """Draw drones at their interpolated pixel positions."""

        for drone_id, (x, y) in positions.items():
            radius = 13

            pygame.draw.circle(
                self.screen,
                (255, 190, 60),
                (x, y),
                radius
            )

            label = self.small_font.render(
                drone_id,
                True,
                (20, 20, 20)
            )

            label_rect = label.get_rect(center=(x, y))
            self.screen.blit(label, label_rect)

    def draw_turn(self) -> None:

        total_turns = max(
            len(self.simulation.history) - 1,
            0
        )

        text = self.title_font.render(
            f"Turn: {self.history_index} / {total_turns}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(text, (30, 25))

        status = "PLAYING" if self.playing else "PAUSED"

        status_text = self.font.render(
            status,
            True,
            (100, 230, 150) if self.playing else (220, 220, 220)
        )

        self.screen.blit(status_text, (30, 70))

    def draw_controls(self) -> None:

        _, height = self.screen.get_size()

        controls = (
            "LEFT: Previous turn   "
            "RIGHT: Next turn   "
            "SPACE: Play/Pause   "
            "UP: First turn   "
            "DOWN: Last recorded turn   "
            "Q: Exit"
        )

        text = self.small_font.render(
            controls,
            True,
            (190, 190, 190)
        )

        self.screen.blit(
            text,
            (30, height - 35)
        )

    def next_turn(self) -> None:
        """Advance one turn and animate the movement."""

        if self.animating:
            return

        old_positions = self.get_drone_positions(
            self.current_snapshot()
        )
        old_index = self.history_index

        # Navigate through recorded history first.
        if self.history_index < len(self.simulation.history) - 1:
            self.history_index += 1

        else:
            # Calculate the next simulation turn.
            moved = self.simulation.simulate_turn()

            if not moved:
                self.playing = False
                return

            self.history_index = len(self.simulation.history) - 1

        # Animate only if the displayed state changed.
        if self.history_index != old_index:
            self.start_transition(old_positions)

        # Report completion only once.
        if (
            self.simulation.all_finished()
            and not self.message_turn
        ):
            print(
                f"\nSimulation finished in "
                f"{self.simulation.turn} turns."
            )

            self.message_turn = True
            self.playing = False

    def previous_turn(self) -> None:
        """Go back one turn and animate backwards."""

        if self.animating or self.history_index <= 0:
            return

        old_positions = self.get_drone_positions(
            self.current_snapshot()
        )

        self.history_index -= 1

        self.start_transition(old_positions)

    def run(self) -> None:

        # Ensure the initial snapshot exists.
        if not self.simulation.history:
            self.simulation.initialize_drones()
            self.simulation.history.append(
                self.simulation.capture_snapshot()
            )

        self.history_index = 0

        running = True

        while running:
            # Time elapsed since the previous frame.
            dt = self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT:
                        self.next_turn()

                    elif event.key == pygame.K_LEFT:
                        self.playing = False
                        self.previous_turn()

                    elif event.key == pygame.K_SPACE:
                        self.playing = not self.playing

                    elif event.key == pygame.K_UP:
                        self.playing = False
                        if not self.animating:
                            old_positions = self.get_drone_positions(
                                self.current_snapshot()
                            )
                            self.history_index = 0
                            self.start_transition(old_positions)

                    elif event.key == pygame.K_DOWN:
                        self.playing = False
                        if not self.animating:
                            old_positions = self.get_drone_positions(
                                self.current_snapshot()
                            )
                            self.history_index = (
                                len(self.simulation.history) - 1
                            )
                            self.start_transition(old_positions)

                    elif event.key == pygame.K_q:
                        running = False

            # Update the animation.
            if self.animating:
                self.animation_elapsed += dt

                if self.animation_elapsed >= self.animation_duration:
                    self.animation_elapsed = self.animation_duration
                    self.animating = False

            # Automatic playback.
            if self.playing and not self.animating:
                self.playback_timer += dt

                if self.playback_timer >= self.playback_delay:
                    self.next_turn()
                    self.playback_timer = 0

            self.draw()

        pygame.quit()

    def get_drone_positions(self, snapshot):
        """Calculate pixel positions for every drone in a snapshot."""

        drones_by_zone, drones_on_links, _, _ = snapshot
        positions = {}

        # Drones inside zones.
        for zone_name, drone_ids in drones_by_zone.items():
            zone = self.graph.zones.get(zone_name)

            if zone is None:
                continue

            cx, cy = self.screen_position(zone)
            total = len(drone_ids)

            for index, drone_id in enumerate(drone_ids):
                angle = 2 * math.pi * index / max(total, 1)
                radius = 35

                positions[drone_id] = (
                    int(cx + math.cos(angle) * radius),
                    int(cy + math.sin(angle) * radius)
                )

        # Drones travelling along connections.
        for (zone1_name, zone2_name), drone_ids in drones_on_links.items():
            zone1 = self.graph.zones.get(zone1_name)
            zone2 = self.graph.zones.get(zone2_name)

            if zone1 is None or zone2 is None:
                continue

            x1, y1 = self.screen_position(zone1)
            x2, y2 = self.screen_position(zone2)

            total = len(drone_ids)

            for index, drone_id in enumerate(drone_ids):
                fraction = (index + 1) / (total + 1)

                positions[drone_id] = (
                    int(x1 + (x2 - x1) * fraction),
                    int(y1 + (y2 - y1) * fraction)
                )

        return positions

    def start_transition(self, start_positions):
        """Animate drones from one snapshot to another."""

        end_positions = self.get_drone_positions(
            self.current_snapshot()
        )

        # Include all drones present in either snapshot.
        all_ids = set(start_positions) | set(end_positions)

        self.animation_start_positions = {}
        self.animation_end_positions = {}

        for drone_id in all_ids:
            start = start_positions.get(
                drone_id,
                end_positions.get(drone_id, (0, 0))
            )

            end = end_positions.get(
                drone_id,
                start
            )

            self.animation_start_positions[drone_id] = start
            self.animation_end_positions[drone_id] = end

        self.animation_elapsed = 0.0
        self.animating = True

    def get_animated_positions(self):
        """Interpolate drone positions during a transition."""

        if not self.animating:
            return self.get_drone_positions(
                self.current_snapshot()
            )

        t = min(
            self.animation_elapsed / self.animation_duration,
            1.0
        )

        # Smooth acceleration and deceleration.
        t = t * t * (3 - 2 * t)

        positions = {}

        for drone_id, (x0, y0) in self.animation_start_positions.items():
            x1, y1 = self.animation_end_positions[drone_id]

            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t

            positions[drone_id] = (round(x), round(y))

        return positions
