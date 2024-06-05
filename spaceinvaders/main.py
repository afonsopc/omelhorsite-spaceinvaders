import variables
import platform
import datetime
import asyncio
import random
import pygame
import time
import sys

class Game:
    def __init__(self):
        # Get time
        self.start_time = time.time()
        # Pygame Init
        pygame.init()
        pygame.font.init()
        pygame.display.init()
        pygame.mixer.init()
        # Display
        self.display = pygame.display.set_mode(variables.SCREEN_RESOLUTION)
        pygame.display.set_caption(variables.TITLE)
        # Full screen
        self.fullscreen_on = False
        self.fullscreen_time_since_last_f11 = 0
        self.fullscreen_timeout = variables.FULLSCREEN_TIMEOUT
        # Statistics
        self.statistics_time_text = variables.STATISTICS_TIME_TEXT
        self.statistics_lifes_text = variables.STATISTICS_LIFES_TEXT
        self.statistics_points_text = variables.STATISTICS_POINTS_TEXT
        self.statistics_kills_text = variables.STATISTICS_KILLS_TEXT
        self.statistics_font_size = variables.STATISTICS_FONT_SIZE
        self.statistics_margin = variables.STATISTICS_MARGIN
        self.statistics_time_margin_top = variables.STATISTICS_TIME_MARGIN_TOP
        self.statistics_lifes_margin_top = variables.STATISTICS_LIFES_MARGIN_TOP
        self.statistics_points_margin_top = variables.STATISTICS_POINTS_MARGIN_TOP
        self.statistics_kills_margin_top = variables.STATISTICS_KILLS_MARGIN_TOP
        self._statistics_font = variables.STATISTICS_FONT
        self.statistics_font = pygame.font.Font(self._statistics_font, self.statistics_font_size)
        # Buy Lifes
        self.buy_lifes_text = variables.BUY_LIFES_TEXT
        self.buy_lifes_margin = variables.BUY_LIFES_MARGIN
        self.buy_lifes_cost = variables.BUY_LIFES_COST
        self.buy_lifes_margin_top = variables.BUY_LIFES_MARGIN_TOP
        self.buy_lifes_font_size = variables.BUY_LIFES_FONT_SIZE
        self._buy_lifes_font = variables.BUY_LIFES_FONT
        self.buy_lifes_font = pygame.font.Font(self._buy_lifes_font, self.buy_lifes_font_size)
        self.buy_lifes_color = variables.BUY_LIFES_COLOR
        self.buy_lifes_timeout = variables.BUY_LIFES_TIMEOUT
        self.buy_lifes_time_since_last_purchase = 0
        # Background Music
        self.background_music = variables.BACKGROUND_MUSIC
        self.background_music_volume = variables.BACKGROUND_MUSIC_VOLUME
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(loops=-1)
        # Music Toggle
        self._music_toggle_font = variables.MUSIC_TOGGLE_FONT
        self.music_toggle_font_size = variables.MUSIC_TOGGLE_FONT_SIZE
        self.music_toggle_font = pygame.font.Font(self._music_toggle_font, self.music_toggle_font_size)
        self.music_toggle_pos = variables.MUSIC_TOGGLE_POS
        self.music_toggle_state = False
        self.music_toggle_on_text = variables.MUSIC_TOGGLE_ON_TEXT
        self.music_toggle_off_text = variables.MUSIC_TOGGLE_OFF_TEXT
        # Game OVER text
        self.game_over = False
        self.game_over_game_over_text = variables.GAME_OVER_GAME_OVER_TEXT
        self.game_over_retry_text = variables.GAME_OVER_RETRY_TEXT
        self.game_over_send_score_text = variables.GAME_OVER_SEND_SCORE_TEXT
        self._game_over_font = variables.GAME_OVER_FONT
        self.game_over_font_size = variables.GAME_OVER_FONT_SIZE
        self.game_over_game_over_pos = variables.GAME_OVER_GAME_OVER_POS
        self.game_over_color = variables.GAME_OVER_COLOR
        self.game_over_font = pygame.font.Font(self._game_over_font, self.game_over_font_size)
        # Game OVER subtext
        self._game_over_subtext_font = variables.GAME_OVER_SUBTEXT_FONT
        self.game_over_subtext_font_size = variables.GAME_OVER_SUBTEXT_FONT_SIZE
        self.game_over_subtext_font = pygame.font.Font(self._game_over_subtext_font, self.game_over_subtext_font_size)
        self.game_over_retry_pos =  variables.GAME_OVER_RETRY_POS
        self.game_over_send_score_pos = variables.GAME_OVER_SEND_SCORE_POS
        self.game_over_send_score_font_size = variables.GAME_OVER_SEND_SCORE_FONT_SIZE
        self.game_over_send_score_font = pygame.font.Font(self._game_over_subtext_font, self.game_over_send_score_font_size)
        # Send score
        self.send_score_timeout = variables.SEND_SCORE_TIMEOUT
        self.time_since_last_sent_score = 0
        self.sent_score = False
        # Clock
        self.clock = pygame.time.Clock()
        # Background
        self.bg_res = variables.BACKGROUND_RESOLUTION
        self.bg_img = pygame.image.load(variables.BACKGROUND_IMAGE).convert()
        self.bg_img = pygame.transform.scale(self.bg_img, self.bg_res)
        # Player
        self.player_kills = 0
        self.player_lifes = variables.PLAYER_LIFES
        self.player_laser_velocity = variables.PLAYER_LASER_VELOCITY
        self.player_velocity = variables.PLAYER_VELOCITY
        self.player_points = 0
        self.player_shots = []
        self.player_shot_timeout = variables.PLAYER_SHOT_TIMEOUT
        self.player_shot_time_since_last_shot = 0
        self.player_pos = variables.PLAYER_STARTING_POS
        self.player_res = variables.PLAYER_RESOLUTION
        self.player_laser_resolution = variables.PLAYER_LASER_RESOLUTION
        self.player_img = pygame.image.load(variables.PLAYER_IMAGE).convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, self.player_res)
        self.player_laser_img = pygame.image.load(variables.PLAYER_LASER_IMAGE)
        self.player_laser_img = pygame.transform.scale(self.player_laser_img, self.player_laser_resolution)
        # Enemies
        self.enemies_lifes = variables.ENEMIES_LIFES
        self.enemies_percentages = variables.ENEMIES_PERCENTAGES
        self.enemies = {"enemy_1":[], "enemy_2":[], "enemy_3":[], "enemy_4":[], "enemy_5":[]}
        self.enemies_res = variables.ENEMIES_RESOLUTION
        self.enemies_laser_resolution = variables.ENEMIES_LASER_RESOLUTION
        self.enemies_spawn_timeout = variables.ENEMIES_SPAWN_TIMEOUT
        self.enemies_time_since_last_spawn = variables.ENEMIES_SPAWN_TIMEOUT
        self.enemies_shots = []
        self.enemies_time_since_last_shot = 0
        self.enemies_shot_timeout = variables.ENEMIES_SHOT_TIMEOUT
        self.enemies_laser_velocity = variables.ENEMIES_LASER_VELOCITY
        self.enemies_velocity = variables.ENEMIES_VELOCITY
        self.enemies_points = variables.ENEMIES_POINTS
        # Enemy 1
        self.enemy_1_img = pygame.image.load(variables.ENEMY_1_IMAGE).convert_alpha()
        self.enemy_1_img = pygame.transform.scale(self.enemy_1_img, self.enemies_res)
        self.enemy_1_img = pygame.transform.rotate(self.enemy_1_img, 180)
        self.enemy_1_laser_img = pygame.image.load(variables.ENEMY_1_LASER_IMAGE).convert_alpha()
        self.enemy_1_laser_img = pygame.transform.scale(self.enemy_1_laser_img, self.enemies_laser_resolution)
        self.enemy_1_laser_img = pygame.transform.rotate(self.enemy_1_laser_img, 180)
        # Enemy 2
        self.enemy_2_img = pygame.image.load(variables.ENEMY_2_IMAGE).convert_alpha()
        self.enemy_2_img = pygame.transform.scale(self.enemy_2_img, self.enemies_res)
        self.enemy_2_img = pygame.transform.rotate(self.enemy_2_img, 180)
        self.enemy_2_laser_img = pygame.image.load(variables.ENEMY_2_LASER_IMAGE).convert_alpha()
        self.enemy_2_laser_img = pygame.transform.scale(self.enemy_2_laser_img, self.enemies_laser_resolution)
        self.enemy_2_laser_img = pygame.transform.rotate(self.enemy_2_laser_img, 180)
        # Enemy 3
        self.enemy_3_img = pygame.image.load(variables.ENEMY_3_IMAGE).convert_alpha()
        self.enemy_3_img = pygame.transform.scale(self.enemy_3_img, self.enemies_res)
        self.enemy_3_img = pygame.transform.rotate(self.enemy_3_img, 180)
        self.enemy_3_laser_img = pygame.image.load(variables.ENEMY_3_LASER_IMAGE).convert_alpha()
        self.enemy_3_laser_img = pygame.transform.scale(self.enemy_3_laser_img, self.enemies_laser_resolution)
        self.enemy_3_laser_img = pygame.transform.rotate(self.enemy_3_laser_img, 180)
        # Enemy 4
        self.enemy_4_img = pygame.image.load(variables.ENEMY_4_IMAGE).convert_alpha()
        self.enemy_4_img = pygame.transform.scale(self.enemy_4_img, self.enemies_res)
        self.enemy_4_img = pygame.transform.rotate(self.enemy_4_img, 180)
        self.enemy_4_laser_img = pygame.image.load(variables.ENEMY_4_LASER_IMAGE).convert_alpha()
        self.enemy_4_laser_img = pygame.transform.scale(self.enemy_4_laser_img, self.enemies_laser_resolution)
        self.enemy_4_laser_img = pygame.transform.rotate(self.enemy_4_laser_img, 180)
        # Enemy 5
        self.enemy_5_img = pygame.image.load(variables.ENEMY_5_IMAGE).convert_alpha()
        self.enemy_5_img = pygame.transform.scale(self.enemy_5_img, self.enemies_res)
        self.enemy_5_img = pygame.transform.rotate(self.enemy_5_img, 180)
        self.enemy_5_laser_img = pygame.image.load(variables.ENEMY_5_LASER_IMAGE).convert_alpha()
        self.enemy_5_laser_img = pygame.transform.scale(self.enemy_5_laser_img, self.enemies_laser_resolution)
        self.enemy_5_laser_img = pygame.transform.rotate(self.enemy_5_laser_img, 180)
        # Sounds
        self.shoot_sounds = variables.SHOOT_SOUNDS
        self.hit_sounds = variables.HIT_SOUNDS
        self.kill_sounds = variables.KILL_SOUNDS
        self.life_sounds = variables.LIFE_SOUNDS
        self.menu_sounds = variables.MENU_SOUNDS
        self.die_sounds = variables.DIE_SOUNDS
        self.hurt_sounds = variables.HURT_SOUNDS
        self.send_score_sounds = variables.SEND_SCORE_SOUNDS
        self.sound_effects_volume = variables.SOUND_EFFECTS_VOLUME
        # Cheats
        self.cheats = False
        # Joysticks
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    def play_random_sound(self, sound_list):
        sound = random.choice(sound_list)
        sound_mixer = pygame.mixer.Sound(sound)
        sound_mixer.set_volume(self.sound_effects_volume)
        sound_mixer.play()
        print("Playing sound: ", sound)

    def draw_background(self):
        self.display.blit(self.bg_img, (0, 0))

    def player_inputs(self):
        keys = pygame.key.get_pressed()

        player_pos_original = self.player_pos
        velocity = self.player_velocity * self.deltatime

        # Joystick moviment
        for joystick in self.joysticks:
            if joystick.get_init():
                if joystick.get_numaxes() >= 2:
                    x_axis = joystick.get_axis(0)
                    y_axis = joystick.get_axis(1)
                    if abs(x_axis) >= 0.1:
                        self.player_pos = (self.player_pos[0]+(x_axis*700)*velocity, self.player_pos[1])
                    if abs(y_axis) >= 0.1:
                        self.player_pos = (self.player_pos[0], self.player_pos[1]+(y_axis*700)*velocity)
                if joystick.get_button(0):
                    if time.time() - self.player_shot_time_since_last_shot >= self.player_shot_timeout:
                        self.player_shots.append((self.player_pos, True))
                        self.play_random_sound(self.shoot_sounds)
                        self.player_shot_time_since_last_shot = time.time()
                if joystick.get_button(1):
                    if time.time() - self.buy_lifes_time_since_last_purchase >= self.buy_lifes_timeout:
                        self.buy_lifes()
                        self.buy_lifes_time_since_last_purchase = time.time()


        for _ in range(len(keys)):
            if keys[pygame.K_b] and time.time() - self.buy_lifes_time_since_last_purchase >= self.buy_lifes_timeout:
                self.buy_lifes()
                self.buy_lifes_time_since_last_purchase = time.time()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.player_pos = (self.player_pos[0], self.player_pos[1]-velocity)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.player_pos = (self.player_pos[0], self.player_pos[1]+velocity)
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.player_pos = (self.player_pos[0]-velocity, self.player_pos[1])
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.player_pos = (self.player_pos[0]+velocity, self.player_pos[1])
            if keys[pygame.K_SPACE]:
                if time.time() - self.player_shot_time_since_last_shot >= self.player_shot_timeout:
                    self.player_shots.append((self.player_pos, True))
                    self.play_random_sound(self.shoot_sounds)
                    self.player_shot_time_since_last_shot = time.time()
            if keys[pygame.K_PERIOD]:
                self.player_shot_timeout = 0.1
                self.cheats = True
            # if keys[pygame.K_F11]:
            #     if time.time() - self.fullscreen_time_since_last_f11 >= self.fullscreen_timeout:
            #         pygame.display.toggle_fullscreen()
            #         self.fullscreen_time_since_last_f11 = time.time()
        if self.player_pos[0]+self.player_res[0] >= self.bg_res[0] or self.player_pos[0] <= 0:
            self.player_pos = (player_pos_original[0], self.player_pos[1])
        if self.player_pos[1]+self.player_res[1] >= self.bg_res[1] or self.player_pos[1] <= 0:
            self.player_pos = (self.player_pos[0], player_pos_original[1])

    def player_shoot(self):
        modified_list = []
        velocity = self.player_laser_velocity * self.deltatime
        for idx, shot in enumerate(self.player_shots):
            if shot[1]:
                y = shot[0][1]-velocity
                if y > 0:
                    shot = ((shot[0][0], y), True)
                    self.display.blit(self.player_laser_img, shot[0])
                    modified_list.append(shot)
        self.player_shots = modified_list

    def draw_player(self):
        self.display.blit(self.player_img, self.player_pos)

    def enemies_move(self):
        modified_dictionary = {"enemy_1":[], "enemy_2":[], "enemy_3":[], "enemy_4":[], "enemy_5":[]}
        velocity = self.enemies_velocity * self.deltatime
        for enemy_type, enemies in self.enemies.items():
            for enemy_values in enemies:
                pos = enemy_values[0]
                lifes = enemy_values[1]
                new_pos = (pos[0], pos[1]+velocity)
                if pos[1] <= self.bg_res[1]:
                    modified_dictionary[enemy_type].append((new_pos, lifes))
                else:
                    self.player_points -= 1
        self.enemies = modified_dictionary

    def enemies_update(self):
        if time.time() - self.enemies_time_since_last_spawn >= self.enemies_spawn_timeout:
            self.spawn_enemies()
            self.enemies_time_since_last_spawn = time.time()
        if time.time() - self.enemies_time_since_last_shot >= self.enemies_shot_timeout:
            try:
                enemy_type = random.choice(list(self.enemies.keys()))
                enemy = random.choice(self.enemies[enemy_type])
                enemy_pos = enemy[0]
                self.enemy_shoot(enemy_pos, enemy_type)
                self.enemies_time_since_last_shot = time.time()
            except:
                pass
        for enemy_type, enemies in self.enemies.items():
            for enemy_values in enemies:
                enemy_pos = enemy_values[0]
                if enemy_type == "enemy_1":
                    self.display.blit(self.enemy_1_img, enemy_pos)
                elif enemy_type == "enemy_2":
                    self.display.blit(self.enemy_2_img, enemy_pos)
                elif enemy_type == "enemy_3":
                    self.display.blit(self.enemy_3_img, enemy_pos)
                elif enemy_type == "enemy_4":
                    self.display.blit(self.enemy_4_img, enemy_pos)
                elif enemy_type == "enemy_5":
                    self.display.blit(self.enemy_5_img, enemy_pos)

    def enemies_shots_update(self):
        modified_list = []
        velocity = self.enemies_laser_velocity * self.deltatime
        for idx, shot in enumerate(self.enemies_shots):
            if shot[1] == "enemy_1":
                image = self.enemy_1_laser_img
            elif shot[1] == "enemy_2":
                image = self.enemy_2_laser_img
            elif shot[1] == "enemy_3":
                image = self.enemy_3_laser_img
            elif shot[1] == "enemy_4":
                image = self.enemy_4_laser_img
            elif shot[1] == "enemy_5":
                image = self.enemy_5_laser_img
            if shot[0][1] <= self.bg_res[1] and shot[2]:
                modified_shot = ((shot[0][0], shot[0][1]+velocity), shot[1], True)
                modified_list.append(modified_shot)
                self.display.blit(image, modified_shot[0])
        self.enemies_shots = modified_list

    def enemy_shoot(self, enemy_pos, enemy_type):
        shot = (enemy_pos, enemy_type, True)
        self.enemies_shots.append(shot)
        self.play_random_sound(self.shoot_sounds)
        print("Enemy shot: ", enemy_type)

    def spawn_enemies(self):
        enemies = list(self.enemies_percentages.keys())
        probabilities = list(self.enemies_percentages.values())
        random_enemy = random.choices(enemies, weights=probabilities, k=1)[0]

        x_pos = random.uniform(variables.ENEMIES_SPAWN_AREA_X[0], variables.ENEMIES_SPAWN_AREA_X[1])
        self.enemies[random_enemy].append(((x_pos, -variables.ENEMIES_RESOLUTION[1]), self.enemies_lifes[random_enemy]))
        print("Spawned enemy: ", random_enemy)

    def check_hits(self):
        modified_enemies = {"enemy_1":[], "enemy_2":[], "enemy_3":[], "enemy_4":[], "enemy_5":[]}
        if len(self.player_shots) == 0:
            modified_shots = self.player_shots
            modified_enemies = self.enemies
        else:
            for enemy_type, enemies in self.enemies.items():
                for idx_enemy, enemy_values in enumerate(enemies):
                    has_been_shot = False
                    pos = enemy_values[0]
                    lifes = enemy_values[1]
                    for idx_shot, shot in enumerate(self.player_shots):
                        x_check = shot[0][0]+self.enemies_laser_resolution[0]//2 < pos[0]+self.enemies_res[0] and shot[0][0]-self.enemies_laser_resolution[0]//2 > pos[0]-self.enemies_res[0]
                        y_check = shot[0][1]+self.enemies_laser_resolution[1]//2 < pos[1]+self.enemies_res[1] and shot[0][1]-self.enemies_laser_resolution[1]//2 > pos[1]-self.enemies_res[1]
                        if x_check and y_check:
                            self.player_shots[idx_shot] = ((0, 0), False)
                            has_been_shot = True
                    if has_been_shot:
                        self.play_random_sound(self.hit_sounds)
                        lifes -= 1
                        if lifes <= 0:
                            self.player_points += self.enemies_points[enemy_type]
                            self.player_kills += 1
                            self.play_random_sound(self.kill_sounds)
                        else:
                            modified_enemies[enemy_type].append((pos, lifes))
                    else:
                        modified_enemies[enemy_type].append((pos, lifes))
        modified_enemies_shots = []
        for idx_shot, shot in enumerate(self.enemies_shots):
            x_check = shot[0][0]+self.player_laser_resolution[0]//2 < self.player_pos[0]+self.player_res[0] and shot[0][0]-self.player_laser_resolution[0]//2 > self.player_pos[0]-self.player_res[0]
            y_check = shot[0][1]+self.player_laser_resolution[1]//2 < self.player_pos[1]+self.player_res[1] and shot[0][1]-self.player_laser_resolution[1]//2 > self.player_pos[1]-self.player_res[1]
            if x_check and y_check:
                self.player_lifes -= 1
                self.play_random_sound(self.hurt_sounds)
            else:
                modified_enemies_shots.append(shot)
        self.enemies_shots = modified_enemies_shots
        self.enemies = modified_enemies

    def add_time_difficulty(self):
        time_boost = 0
        time_since_start = time.time() - self.start_time
        if time_since_start <= 120:
            time_boost = time_since_start / 15000
            self.enemies_spawn_timeout = variables.ENEMIES_SPAWN_TIMEOUT - (time_since_start/200)
            self.enemies_shot_timeout = variables.ENEMIES_SHOT_TIMEOUT - (time_since_start/500)

        elif time_since_start <= 240:
            time_boost = time_since_start / 18000
            self.enemies_spawn_timeout = variables.ENEMIES_SPAWN_TIMEOUT - (time_since_start/500)
            self.enemies_shot_timeout = variables.ENEMIES_SHOT_TIMEOUT - (time_since_start/800)
        elif time_since_start <= 3060:
            time_boost = time_since_start / 18000
            self.enemies_spawn_timeout = variables.ENEMIES_SPAWN_TIMEOUT - (time_since_start/1000)
            self.enemies_shot_timeout = variables.ENEMIES_SHOT_TIMEOUT - (time_since_start/1300)
        else:
            self.enemies_spawn_timeout = variables.ENEMIES_SPAWN_TIMEOUT - (time_since_start/5000)
            self.enemies_shot_timeout = variables.ENEMIES_SHOT_TIMEOUT - (time_since_start/8000)
        
        if self.enemies_spawn_timeout <= 1.5 and self.enemies_shot_timeout <= 0.5:
            self.player_shot_timeout = 0.3
        if self.enemies_spawn_timeout <= 1 and self.enemies_shot_timeout <= 0.3:
            self.player_shot_timeout = 0.2
        elif self.enemies_spawn_timeout <= 0 and self.enemies_shot_timeout <= 0:
            self.player_shot_timeout = 0.1
        self.enemies_velocity += time_boost
        self.enemies_laser_velocity += time_boost

    def draw_statistics(self):
        time_text = self.statistics_font.render(self.statistics_time_text.format(self.playing_time_formated), False, (255, 255, 255))
        self.display.blit(time_text, (self.statistics_margin, self.statistics_time_margin_top))
        if len(str(self.player_lifes)) >= 10:
            lifes = "∞"
        else:
            lifes = self.player_lifes
        lifes_text = self.statistics_font.render(self.statistics_lifes_text.format(lifes), False, (255, 255, 255))
        self.display.blit(lifes_text, (self.statistics_margin, self.statistics_lifes_margin_top))
        points_text = self.statistics_font.render(self.statistics_points_text.format(self.player_points), False, (255, 255, 255))
        self.display.blit(points_text, (self.statistics_margin, self.statistics_points_margin_top))
        kills_text = self.statistics_font.render(self.statistics_kills_text.format(self.player_kills), False, (255, 255, 255))
        self.display.blit(kills_text, (self.statistics_margin, self.statistics_kills_margin_top))

    def draw_buy_lifes(self):
        buy_lifes_text = self.buy_lifes_font.render(self.buy_lifes_text.format(self.buy_lifes_cost), False, self.buy_lifes_color)
        self.display.blit(buy_lifes_text, (self.statistics_margin, self.buy_lifes_margin_top))

    def buy_lifes(self):
        if self.player_points >= self.buy_lifes_cost:
            self.player_points -= self.buy_lifes_cost
            self.player_lifes += 1
            self.play_random_sound(self.life_sounds)
            print("Bought life... 🚀🚀🚀🚀")

    async def send_score(self, money, kills, time):
        print("Sending score... 🚀")
        platform.window.sendScore(
            money,
            kills,
            time,
        )
    

    def game_over_screen(self):
        retry = None
        self.draw_background()
        self.draw_statistics()
        self.draw_music_toggle()
        game_over_game_over_text = self.game_over_font.render(self.game_over_game_over_text, True, (255, 255, 255))
        game_over_game_over_rect = game_over_game_over_text.get_rect(center=self.game_over_game_over_pos)
        self.display.blit(game_over_game_over_text, game_over_game_over_rect)
        game_over_retry_text = self.game_over_subtext_font.render(self.game_over_retry_text, True, (255, 255, 255))
        game_over_retry_rect = game_over_retry_text.get_rect(center=self.game_over_retry_pos)
        self.display.blit(game_over_retry_text, game_over_retry_rect)
        if not self.sent_score:
            game_over_send_score_text = self.game_over_send_score_font.render(self.game_over_send_score_text, True, (255, 255, 255))
            game_over_send_score_rect = game_over_send_score_text.get_rect(center=self.game_over_send_score_pos)
            self.display.blit(game_over_send_score_text, game_over_send_score_rect)

        # Joystick support
        for joystick in self.joysticks:
            if joystick.get_init():
                if joystick.get_button(0):
                    self.player_pos = variables.PLAYER_STARTING_POS
                    self.player_shots = []
                    self.player_points = 0
                    self.player_kills = 0
                    self.player_lifes = variables.PLAYER_LIFES
                    self.start_time = time.time()
                    self.enemies = {"enemy_1":[], "enemy_2":[], "enemy_3":[]}
                    self.enemies_shots = []
                    self.game_over = False
                    self.enemies_velocity = variables.ENEMIES_VELOCITY
                    self.enemies_laser_velocity = variables.ENEMIES_LASER_VELOCITY
                    retry = True

        keys = pygame.key.get_pressed()
        for _ in range(len(keys)):
            if keys[pygame.K_g]:
                if not self.sent_score and time.time() - self.time_since_last_sent_score >= self.send_score_timeout:
                    asyncio.create_task(self.send_score(
                        self.player_points,
                        self.player_kills,
                        self.playing_time,
                    ))
                    self.play_random_sound(self.send_score_sounds)
                    self.sent_score = True
                    self.time_since_last_sent_score = time.time()
            if keys[pygame.K_RETURN]:
                self.player_pos = variables.PLAYER_STARTING_POS
                self.player_shots = []
                self.player_points = 0
                self.player_kills = 0
                self.player_lifes = variables.PLAYER_LIFES
                self.start_time = time.time()
                self.enemies = {"enemy_1":[], "enemy_2":[], "enemy_3":[]}
                self.enemies_shots = []
                self.game_over = False
                self.enemies_velocity = variables.ENEMIES_VELOCITY
                self.enemies_laser_velocity = variables.ENEMIES_LASER_VELOCITY
                retry = True

        if retry:
            self.play_random_sound(self.menu_sounds)

        pygame.display.update()
        return retry

    def draw_music_toggle(self):
        if self.music_toggle_state:
            text = self.music_toggle_on_text
        else:
            text = self.music_toggle_off_text
        music_toggle_icon = self.music_toggle_font.render(text, True, (255, 255, 255))
        self.display.blit(music_toggle_icon, self.music_toggle_pos)

    def toggle_music_toggle(self):
        print("Toggling music...")
        self.music_toggle_state = not self.music_toggle_state
        if self.music_toggle_state:
            pygame.mixer.music.set_volume(self.background_music_volume)
        else:
            pygame.mixer.music.set_volume(0)


    def frame(self):
        running = True
        # Tick clock and get deltatime
        clock_tick = self.clock.tick(variables.FPS)
        self.deltatime = clock_tick / 1000
        # Make the close button work
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x_check = event.pos[0] >= self.music_toggle_pos[0]
                y_check = event.pos[1] <= self.music_toggle_font_size
                if x_check and y_check:
                    self.toggle_music_toggle()

        if self.game_over:
            retry = self.game_over_screen()
            if type(retry) is bool:
                running = retry
            return running
        # Time 
        self.playing_time = time.time() - self.start_time
        self.playing_time_formated = datetime.timedelta(seconds=int(self.playing_time))
        # Game logic
        self.draw_background()
        self.player_inputs()
        self.player_shoot()
        self.enemies_shots_update()
        self.enemies_update()
        self.check_hits()
        self.enemies_move()
        self.draw_player()
        self.add_time_difficulty()
        self.draw_statistics()
        self.draw_music_toggle()
        # print(f"Spawn Timeout: {self.enemies_spawn_timeout:.2f}")
        # print(f"Shot Timeout: {self.enemies_shot_timeout:.2f}")
        # print(f"Player Shot Timeout: {self.player_shot_timeout:.2f}")
        # print(self.clock)
        if self.player_points >= self.buy_lifes_cost:
            self.draw_buy_lifes()
            self.able_to_buy_lifes = True
        else:
            self.able_to_buy_lifes = False
        if self.player_lifes <= 0:
            self.play_random_sound(self.die_sounds)
            self.game_over = True
            self.sent_score = False
        # Update Display
        pygame.display.update()
        return running


async def main():
    game = Game()
    running = True
    while running:
        running = game.frame()
        await asyncio.sleep(0)
    print("Game Over!")
    sys.exit()

asyncio.run(main())