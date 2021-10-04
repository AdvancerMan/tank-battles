# coding: utf-8

from os import \
    listdir as os_listdir
from os.path import \
    join as os_path_join
from random import choice, randrange
from pygame import \
    Surface as pg_Surface, \
    error as pg_error, \
    PixelArray as pg_PixelArray
from pygame.mixer import \
    Sound as pg_mixer_Sound
from pygame.font import \
    init as pg_font_init, \
    SysFont as pg_font_SysFont
from pygame.transform import \
    rotate as pg_transform_rotate, \
    scale as pg_transform_scale
from pygame.image import \
    load as pg_image_load
from config import CONFIG
from constants import RIGHT, LEFT, \
    DOWN, UP, BLACK, WHITE


def init_objs_png():
    global blow, BlockUnD_png, Base_png, \
        BlockD_png, Mine_png, Dirt_png, \
        MiniMenu_png, Water_png, move_sound, \
        art_png, antiart_png, fire_skill_png

    _dir_ = 'pics/blow/blow'
    _blow_details = ['1.1', '1.2', '1.3',
                     '2.1', '2.2', '2.3',
                     '3.1', '3.2', '3.3',
                     '4.1', '4.2', '4.3']
    _pics_func = lambda x: load_img(_dir_ + x + '.png')
    blow = [_pics_func(x) for x in _blow_details]

    BlockUnD_png = load_img('pics/blocks/block_und.png')
    Base_png = [load_img('pics/blocks/base/' + png) for png in os_listdir('pics/blocks/base')]
    Mine_png = {int(png[4:-4]): load_img('pics/blocks/mine/' + png) for png in os_listdir('pics/blocks/mine')}
    BlockD_png = load_img('pics/blocks/block_d.png')
    Dirt_png = load_img('pics/blocks/dirt.png')
    Water_png = [load_img('pics/blocks/water/' + png) for png in os_listdir('pics/blocks/water')]

    MiniMenu_png = load_img('pics/misc/mini_menu.png', (100, 150))

    move_sound = pg_mixer_Sound(file='music/tank_move.wav')

    art_png = load_img('pics/skills/static_objects/artillery/artillery.png', (100, 100))
    antiart_png = load_img('pics/skills/static_objects/antiartgun/antiartgun.png', (100, 100))
    fire_skill_png = load_img('pics/skills/fire.png', (100, 100))


def del_objs_png():
    global blow, BlockUnD_png, Base_png, \
        BlockD_png, Mine_png, Dirt_png, \
        MiniMenu_png, Water_png, move_sound, \
        art_png, antiart_png, fire_skill_png

    del blow, BlockUnD_png, Base_png, \
        BlockD_png, Mine_png, Dirt_png, \
        MiniMenu_png, Water_png, move_sound, \
        art_png, antiart_png, fire_skill_png


def load_img(path, params=(CONFIG['OBJ_WIDTH'], CONFIG['OBJ_HEIGHT']),
             change_size=True, raise_error=False):
    path = os_path_join(*path.split('/'))
    try:
        img = pg_image_load(path)
        if change_size:
            img = pg_transform_scale(img, params)
    except:
        if raise_error:
            raise pg_error
        img = pg_Surface(params)
        img.fill(WHITE)
    else:
        pix_ar = pg_PixelArray(img)
        pix_ar.replace((0, 0, 0), (1, 0, 0))
        img = pix_ar.make_surface()
    img = img.convert_alpha(img)
    return img


def objs_crossed(obj1_pos, obj1_size, obj2_pos, obj2_size, cycle=True):
    obj1_cross = False
    for pos in (obj1_pos, (obj1_pos[0], obj1_pos[1] + obj1_size[1]),
                (obj1_pos[0] + obj1_size[0], obj1_pos[1] + obj1_size[1]), (obj1_pos[0], obj1_pos[1])):
        obj1_cross1 = obj2_pos[0] <= pos[0] < obj2_pos[0] + obj2_size[0]
        obj1_cross2 = obj2_pos[1] <= pos[1] < obj2_pos[1] + obj2_size[1]
        obj1_cross = obj1_cross1 and obj1_cross2 or obj1_cross

    obj2_cross = 0

    if cycle:
        obj2_cross = objs_crossed(obj2_pos, obj2_size, obj1_pos, obj1_size, False)
    return obj1_cross or obj2_cross


class FPSForPics:
    def __init__(self, fps, number_of_frames=1):
        self.last_frame_time = 0
        self.frame_now = 0
        self.frames_number = number_of_frames
        self.spf = 1 / fps

    def frame(self, time):
        if time > self.last_frame_time + self.spf:
            self.frame_now += 1
            self.last_frame_time = time
            if self.frame_now >= self.frames_number:
                self.frame_now = 0
        return self.frame_now


class TanksError(BaseException):
    pass


class SkillsLine:
    def __init__(self):
        self.surf = pg_Surface((int(0.15625 * CONFIG['RESOLUTION'][0]), CONFIG['RESOLUTION'][1]))
        self.image = load_img('pics/misc/skills_line.png', (int(0.15625 * CONFIG['RESOLUTION'][0]),
                                                            CONFIG['RESOLUTION'][1]))
        self.x = CONFIG['RESOLUTION'][0]
        self.y = 0
        self.skills = {1: {(50, 100): (art_png,
                                       'Artillery'),
                           (50, 200): (antiart_png,
                                       'AntiArtGun'),
                           (50, 300): (fire_skill_png,
                                       'Fire!')}}
        self.sheet_number = 1

    def update(self, updating=None, mouse_pos=None):
        if updating is not None:
            if updating:
                if self.x - CONFIG['SKILLS_LINE_SPEED'] > CONFIG['RESOLUTION'][0] - self.surf.get_size()[0]:
                    self.x -= CONFIG['SKILLS_LINE_SPEED']
                else:
                    self.x = CONFIG['RESOLUTION'][0] - self.surf.get_size()[0]
            else:
                if self.x + CONFIG['SKILLS_LINE_SPEED'] < CONFIG['RESOLUTION'][0]:
                    self.x += CONFIG['SKILLS_LINE_SPEED']
                else:
                    self.x = CONFIG['RESOLUTION'][0]
        else:
            for pos, skill in self.skills[self.sheet_number].items():
                if objs_crossed(mouse_pos, (1, 1), pos, skill[0].get_size()):
                    return pg_transform_scale(skill[0], (CONFIG['OBJ_WIDTH'], CONFIG['OBJ_HEIGHT'])), skill[1]

    def draw(self, surf):
        self.surf.fill(BLACK)

        self.surf.blit(self.image, (0, 0))
        for pos, skill in self.skills[self.sheet_number].items():
            self.surf.blit(skill[0], pos)
        surf.blit(self.surf, (self.x, self.y))


class Field:
    def __init__(self, field_image, font, size, pos, prompt_text, prompt_color=WHITE, restart_game=False):
        self.res = restart_game
        self.image = pg_transform_scale(field_image, size)
        self.size = size
        self.prompt_txt_pos = pos
        self.text_image = None
        self.txt_img_pos = (0, 0)
        self.font = font
        self.prompt_txt_img = font.render(str(prompt_text), 1, prompt_color)
        self.prompt_txt_img = pg_transform_scale(self.prompt_txt_img,
                                                 (int(self.prompt_txt_img.get_size()[0] / 1280 *
                                                      CONFIG['RESOLUTION'][0]),
                                                  int(self.prompt_txt_img.get_size()[1] / 720 *
                                                      CONFIG['RESOLUTION'][1])))
        self.pos = (pos[0] + self.prompt_txt_img.get_size()[0] + int(0.01563 * CONFIG['RESOLUTION'][0]),
                    pos[1] + self.prompt_txt_img.get_size()[1] // 2 - size[1] // 2)
        if restart_game:
            self.res_text = pg_font_SysFont('Impact', 32)\
                .render('Для вступления изменений в силу необходимо перезапустить игру', 1, prompt_color)
            self.res_text = pg_transform_scale(self.res_text,
                                               (int(self.res_text.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                                int(self.res_text.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))

    def update(self, text, txt_color):
        if text == '':
            text = ' '
        self.text_image = self.font.render(str(text), 1, txt_color)
        self.text_image = pg_transform_scale(self.text_image, (int(self.text_image.get_size()[0] / 1280 *
                                                                   CONFIG['RESOLUTION'][0]),
                                                               int(self.text_image.get_size()[1] / 720 *
                                                                   CONFIG['RESOLUTION'][1])))
        self.txt_img_pos = (self.pos[0] + self.size[0] // 2 - self.text_image.get_size()[0] // 2,
                            self.pos[1] + self.size[1] // 2 - self.text_image.get_size()[1] // 2)

    def draw(self, surf):
        surf.blit(self.prompt_txt_img, self.prompt_txt_pos)
        surf.blit(self.image, self.pos)
        surf.blit(self.text_image, self.txt_img_pos)

        if self.res:
            surf.blit(self.res_text, (self.prompt_txt_pos[0],
                                      self.prompt_txt_pos[1] + self.prompt_txt_img.get_size()[1] -
                                      int(0.02778 * CONFIG['RESOLUTION'][1])))


class Slider:
    def __init__(self, line_image, slider_image, font, pos, value_borders, start_value, prompt_text, prompt_color=WHITE):
        self.prompt_txt_img = font.render(prompt_text, 1, prompt_color)
        self.prompt_txt_img = pg_transform_scale(self.prompt_txt_img,
                                                 (int(self.prompt_txt_img.get_size()[0] / 1280 *
                                                      CONFIG['RESOLUTION'][0]),
                                                  int(self.prompt_txt_img.get_size()[1] / 720 *
                                                      CONFIG['RESOLUTION'][1])))
        self.prompt_txt_pos = pos

        self.line_image = pg_transform_scale(line_image,
                                             (int(line_image.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                              int(line_image.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
        self.line_pos = (pos[0] + self.prompt_txt_img.get_size()[0] + int(0.01563 * CONFIG['RESOLUTION'][0]),
                         pos[1] + self.prompt_txt_img.get_size()[1] // 2 - self.line_image.get_size()[1] // 2)
        self.line_size = self.line_image.get_size()

        self.slider_image = pg_transform_scale(slider_image,
                                               (int(slider_image.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                                int(slider_image.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
        self.slider_size = self.slider_image.get_size()
        self.moving = False

        self.pixel2value = {}
        self.value2pixel = {}
        all_pixels = self.line_image.get_size()[0] - self.slider_size[0]
        all_values = list(range(value_borders[0], value_borders[1] + 1))
        k = len(all_values) / all_pixels
        for pixel in range(all_pixels + 1):
            value = pixel * k
            if value >= len(all_values) != 1:
                value -= 1
            self.pixel2value[pixel + self.line_pos[0]] = all_values[int(value)]
            self.value2pixel[all_values[int(value)]] = (pixel + self.line_pos[0],
                                                        self.line_pos[1] + self.line_image.get_size()[1] // 2 -
                                                        self.slider_size[1] // 2)

        while start_value not in self.value2pixel.keys():
            start_value -= 1
            if start_value <= value_borders[0]:
                start_value = value_borders[0]
        self.slider_pos = self.value2pixel[start_value]

        self.slider_x_pos = self.slider_pos[0]

    def update(self, mouse_pos):
        """
        to update self.moving must be on
        :param mouse_pos: mouse's position
        :return: value
        """
        if self.moving:
            self.slider_x_pos = mouse_pos[0]
            if self.line_pos[0] + self.slider_size[0] // 2 <= self.slider_x_pos < \
                                    self.line_pos[0] + self.line_image.get_size()[0] - self.slider_size[0] // 2:
                self.slider_pos = (self.slider_x_pos - self.slider_size[0] // 2, self.slider_pos[1])
            elif self.slider_x_pos < self.line_pos[0] + self.slider_size[0] // 2:
                self.slider_pos = (self.line_pos[0], self.slider_pos[1])
            elif self.slider_x_pos > self.line_pos[0] + self.line_image.get_size()[0] - self.slider_size[0] // 2:
                self.slider_pos = (self.line_pos[0] + self.line_image.get_size()[0] - self.slider_size[0],
                                   self.slider_pos[1])
        else:
            self.slider_x_pos = self.slider_pos[0]

        return self.pixel2value[self.slider_pos[0]]

    def draw(self, surf):
        surf.blit(self.prompt_txt_img, self.prompt_txt_pos)
        surf.blit(self.line_image, self.line_pos)
        surf.blit(self.slider_image, self.slider_pos)


class Switcher:
    def __init__(self, switcher_images, font, pos, is_on, prompt_text, prompt_color=WHITE):
        self.prompt_txt_img = font.render(prompt_text, 1, prompt_color)
        self.prompt_txt_img = pg_transform_scale(self.prompt_txt_img,
                                                 (int(self.prompt_txt_img.get_size()[0] / 1280 *
                                                      CONFIG['RESOLUTION'][0]),
                                                  int(self.prompt_txt_img.get_size()[1] / 720 *
                                                      CONFIG['RESOLUTION'][1])))
        self.prompt_txt_pos = pos

        self.switcher_images = []
        for img in switcher_images:
            img = pg_transform_scale(img, (int(img.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                           int(img.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
            self.switcher_images.append(img)
        self.switcher_pos = (pos[0] + self.prompt_txt_img.get_size()[0] + int(0.01563 * CONFIG['RESOLUTION'][0]),
                             pos[1] + self.prompt_txt_img.get_size()[1] // 2 - self.switcher_images[0].get_size()[1] // 2)
        self.switcher_size = self.switcher_images[0].get_size()
        self.on = is_on
        self.image = self.switcher_images[int(is_on)]

    def update(self):
        """
        to update change self.on to True or False
        """
        self.image = self.switcher_images[int(self.on)]
        return self.on

    def draw(self, surf):
        surf.blit(self.prompt_txt_img, self.prompt_txt_pos)
        surf.blit(self.image, self.switcher_pos)


class Player:
    def __init__(self, number=1):
        self.money = CONFIG['START_PLAYER_MONEY']
        self.tanks_pos = {}
        self.base_pos = ()
        self.action = None
        self.number = number
        self.statuses = ['У игрока закончились ходы.', 'Игрок еще может ходить.', 'Игрок ходит.']
        self.name = 'Игрок ' + str(number)  # todo активные скиллы


class MiniMenu:
    def __init__(self, params, x_and_y, borders):
        pg_font_init()
        inf = []  # todo обновление инфы
        text_font = pg_font_SysFont('Impact', 12)
        for name, param in params.items():
            inf.append(text_font.render(name + ': ' + str(param), 1, WHITE))
        text_space = 20 * len(inf)
        self.height = (150 * text_space) // 130
        self.borders_space = self.height - text_space
        self.y = self.borders_space
        self.img = pg_transform_scale(MiniMenu_png.copy(), (100, self.height))
        self.lower_border = pg_Surface((100, self.borders_space))
        self.lower_border.set_colorkey(BLACK)
        self.lower_border.blit(self.img, (0, 0))
        y = self.borders_space // 2
        for text in inf:
            self.img.blit(text, (20, y))
            y += 20

        x = y = 0
        if x_and_y[0] + 100 > borders[0]:
            x = x_and_y[0] + 100 - borders[0]
        if x_and_y[1] + self.height > borders[1]:
            y = x_and_y[1] + self.height - borders[1]
        self.pos = (x_and_y[0] - x, x_and_y[1] - y)

        self.image = pg_Surface((100, self.y))
        self.image.fill(BLACK)
        self.image.blit(self.img, (0, 0))
        self.image.blit(self.lower_border, (0, self.y - self.borders_space // 2))

    def update(self, opened):
        if opened and self.y < self.height:
            self.y += CONFIG['MINI_MENU_SPEED']
            if self.y > self.height:
                self.y = self.height
        elif not opened:
            self.y -= CONFIG['MINI_MENU_SPEED']
            if self.y <= self.borders_space:
                return None

        self.image = pg_Surface((100, self.y))
        self.image.fill(BLACK)
        self.image.blit(self.img, (0, 0))
        self.image.blit(self.lower_border, (0, self.y - self.borders_space // 2))
        return False

    def draw(self, surf):
        surf.blit(self.image, self.pos)


class Tank:
    def __init__(self, team, speed, health, bullet_damage, bullet, details):
        self.x = 0
        self.y = 0
        self.team = team
        self.direction = 'right'
        self.health = health
        self.points_bag = speed
        self.pts = 0
        self.menu = None
        self.menu_opened = False
        self.bullet = {'right': [], 'up': [], 'left': [], 'down': []}
        for i in (('right', RIGHT), ('up', UP),
                  ('left', LEFT), ('down', DOWN)):
            for bul in bullet:
                self.bullet[i[0]].append(pg_transform_rotate(load_img(bul, change_size=False), i[1]))
        self.bullet_dmg = bullet_damage
        self.image = pg_Surface((CONFIG['OBJ_WIDTH'], CONFIG['OBJ_HEIGHT']))
        self.image.set_colorkey(BLACK)
        details.append(['pics/tank_components/teams/player' +
                        str((team.number - 1) % len(os_listdir('pics/tank_components/teams')) + 1) +
                        '.png'])
        for detail_indx in range(len(details)):
            for path_indx in range(len(details[detail_indx])):
                path = details[detail_indx][path_indx]
                details[detail_indx][path_indx] = load_img(path)
        self.details = details
        self.frames = [0, 0, 0, 0]
        self.angle = 0
        self.destruct = False

    def update(self, lvl, action=None, tanks_list=None):
        if tanks_list is None:
            tanks_list = []
        if self.health <= 0:
            if len(self.frames) == 4:
                sound = pg_mixer_Sound('music/explosion.wav')
                sound.play()
                sound.set_volume(CONFIG['SOUNDS_VOLUME'] / 1000 * int(CONFIG['SOUNDS_ON']))
                del sound
                self.frames.append(-1)
                self.details.append(blow)
                self.destruct = True
            self.frames[4] += 1
            if self.frames[4] >= len(self.details[4]):
                return None
            else:
                return False

        info = {'right': ((self.x + CONFIG['OBJ_WIDTH'], self.y), 0, 0),
                'left': ((self.x - CONFIG['OBJ_WIDTH'], self.y), 1, 0),
                'down': ((self.x, self.y + CONFIG['OBJ_HEIGHT']), 2, 1),
                'up': ((self.x, self.y - CONFIG['OBJ_HEIGHT']), 3, 1)}

        if action is None:
            if self.x % CONFIG['OBJ_WIDTH'] != 0:
                if (self.x + CONFIG['TANKS_SPEED'] * ((-1) ** (info[self.direction][1] % 2))) // \
                        CONFIG['OBJ_WIDTH'] != self.x // CONFIG['OBJ_WIDTH']:

                    # Если движется вправо
                    if (-1) ** (info[self.direction][1] % 2) + 1:
                        self.x = ((self.x + CONFIG['TANKS_SPEED'] * ((-1) ** (info[self.direction][1] % 2))) //
                                  CONFIG['OBJ_WIDTH']) * CONFIG['OBJ_WIDTH']
                    else:
                        self.x = self.x - self.x % CONFIG['OBJ_WIDTH']
                else:
                    self.x += CONFIG['TANKS_SPEED'] * ((-1) ** (info[self.direction][1] % 2))
            elif self.y % CONFIG['OBJ_HEIGHT'] != 0:
                if (self.y + CONFIG['TANKS_SPEED'] * ((-1) ** (info[self.direction][1] % 2))) // \
                        CONFIG['OBJ_HEIGHT'] != self.y // CONFIG['OBJ_HEIGHT']:

                    # Если движется вверх
                    if (-1) ** (info[self.direction][1] % 2) + 1:
                        self.y = ((self.y + CONFIG['TANKS_SPEED'] * ((-1) ** (info[self.direction][1] % 2))) //
                                  CONFIG['OBJ_HEIGHT']) * CONFIG['OBJ_HEIGHT']
                    else:
                        self.y = self.y - self.y % CONFIG['OBJ_HEIGHT']
                else:
                    self.y += CONFIG['TANKS_SPEED'] * ((-1) ** (info[self.direction][1] % 2))
            else:
                return False  # ((-1) ** (info[self.direction][1] % 2))
            for frame in range(len(self.frames)):
                self.frames[frame] += 1
                if self.frames[frame] >= len(self.details[frame]):
                    self.frames[frame] = 0
            return False

        if lvl is None:
            return False

        action = self.team.action
        self.pts -= 1
        tanks_list = [i[0] for i in tanks_list]
        place = lvl.objs_place
        all_objs_pos = []
        for i in lvl.ingame_objs.values():
            for j in list(i.keys()):
                all_objs_pos.append(j)
        params = [lvl.params[i] * lvl.obj_params[i] for i in (0, 1)]

        if action == 'shoot':
            sound = pg_mixer_Sound('music/tank_shot.wav')
            sound.play()
            sound.set_volume(CONFIG['SOUNDS_VOLUME'] / 1000 * int(CONFIG['SOUNDS_ON']))
            del sound
            return Bullet(info[self.direction][0][0],
                          info[self.direction][0][1],
                          self.direction,
                          self.bullet, self.bullet_dmg)

        else:
            info = info[action]
            block = info[0]
            anim = info[1]
            param = info[2]
            # Если танк повернут не в сторону действия
            if self.direction != action:
                self.direction = action
                angles = {'right': RIGHT, 'up': UP, 'down': DOWN, 'left': LEFT}
                self.angle = angles[action]
            else:
                for frame in range(len(self.frames)):
                    self.frames[frame] += 1
                    if self.frames[frame] >= len(self.details[frame]):
                        self.frames[frame] = 0
                if block in tanks_list:
                    self.pts += 1
                    return True
                sound = move_sound
                sound.play()
                sound.set_volume(CONFIG['SOUNDS_VOLUME'] / 1000 * int(CONFIG['SOUNDS_ON']))
                if param:
                    if 0 <= (self.y + CONFIG['OBJ_HEIGHT'] * ((-1) ** (anim % 2))) < params[param]:
                        if type(place[block]) == Dirt and block not in all_objs_pos:
                            self.y += CONFIG['TANKS_SPEED'] * ((-1) ** (anim % 2))
                        elif type(place[block]) == Mine:
                            sound = pg_mixer_Sound(file='music/mine_gold_drop.wav')
                            sound.play()
                            sound.set_volume(CONFIG['SOUNDS_VOLUME'] / 1000 * int(CONFIG['SOUNDS_ON']))
                            del sound
                            self.team.money += place[block].money
                            place[block].money = 0
                            place[block].check_image()

                else:
                    if 0 <= self.x + CONFIG['OBJ_WIDTH'] * ((-1) ** (anim % 2)) < params[param]:
                        if type(place[block]) == Dirt and block not in all_objs_pos:
                            self.x += CONFIG['TANKS_SPEED'] * ((-1) ** (anim % 2))
                        elif type(place[block]) == Mine:
                            sound = pg_mixer_Sound(file='music/mine_gold_drop.wav')
                            sound.play()
                            sound.set_volume(CONFIG['SOUNDS_VOLUME'] / 1000 * int(CONFIG['SOUNDS_ON']))
                            del sound
                            self.team.money += place[block].money
                            place[block].money = 0
                            place[block].check_image()
        return False

    def draw(self, surf, cam_x, cam_y):
        if -cam_x - CONFIG['OBJ_WIDTH'] <= self.x <= -cam_x + CONFIG['RESOLUTION'][0] \
                and -cam_y - CONFIG['OBJ_HEIGHT'] <= self.y <= -cam_y + CONFIG['RESOLUTION'][1]:
            self.image.fill(BLACK)
            for i in range(len(self.details)):
                self.image.blit(pg_transform_rotate(self.details[i][self.frames[i]], self.angle), (0, 0))
            surf.blit(self.image, (self.x, self.y))


class Bullet:
    def __init__(self, x, y, direction, bullet_img, bullet_dmg):
        self.health = 1
        self.pos = (x, y)
        self.frame = 0
        self.image = bullet_img[direction]
        self.image_size = self.image[0].get_size()
        self.damage = bullet_dmg
        self.direction = {'right': (1, 0),
                          'up': (0, -1),
                          'left': (-1, 0),
                          'down': (0, 1)}[direction]
        x_space = (CONFIG['OBJ_WIDTH'] - self.image_size[0]) // 2
        y_space = (CONFIG['OBJ_HEIGHT'] - self.image_size[1]) // 2
        if direction == 'right' or direction == 'left':
            y += y_space
            if direction == 'left':
                x += 50 - self.image_size[0]
        elif direction == 'down' or direction == 'up':
            x += x_space
            if direction == 'up':
                y += 50 - self.image_size[0]
        self.x = x
        self.y = y
        self.true_pos = (x, y)

    def check_collide(self, tanks_dict, objs_dict):
        try:
            tanks_dict[self.pos]
        except KeyError:
            try:
                block_type = type(objs_dict[self.pos])
                if block_type == Dirt or block_type == Water:
                    # Если позиция свободна
                    return True, None
                elif block_type == Base or block_type == BlockD:
                    # Если позиция занята базой или разрушаемым блоком
                    return False, True
            except KeyError:
                pass
            # Если позиция занята блоком или находится за экраном
            return False, False
        else:
            # Если на позиции танк
            return False, True

    def update(self, tanks_dict, objs_dict):
        if self.health <= 0:
            del self
            return None
        # Проверяем позицию, на которой находится пуля
        collide = self.check_collide(tanks_dict, objs_dict)
        # Если путь свободен
        if collide[0]:
            self.x += CONFIG['BULLETS_SPEED'] * self.direction[0]
            self.y += CONFIG['BULLETS_SPEED'] * self.direction[1]
            self.true_pos = (self.x, self.y)
            self.pos = (((self.true_pos[0] + self.image_size[0] *
                          int(bool(self.direction[0] + 1))) // CONFIG['OBJ_WIDTH']) * CONFIG['OBJ_WIDTH'],
                        ((self.true_pos[1] + self.image_size[1] *
                          int(bool(self.direction[1] + 1))) // CONFIG['OBJ_HEIGHT']) * CONFIG['OBJ_HEIGHT'])
            collide = self.check_collide(tanks_dict, objs_dict)
        # Если врезался
        if collide[1] is not None:
            if collide[1]:
                # Если врезался в танк, пулю или базу
                return True
            else:
                # Если врезался в блок
                del self
                return None
        return False

    def draw(self, surf, cam_x, cam_y):
        if -cam_x - CONFIG['OBJ_WIDTH'] <= self.true_pos[0] <= -cam_x + CONFIG['RESOLUTION'][0] \
                and -cam_y - CONFIG['OBJ_HEIGHT'] <= self.true_pos[1] <= -cam_y + CONFIG['RESOLUTION'][1]:
            surf.blit(self.image[self.frame], self.true_pos)
        self.frame += 1
        if self.frame >= len(self.image):
            self.frame = 0


class StaticGunWithField:
    def __init__(self, level_size, x, y, action_range, image, health):
        self.pos = (x, y)
        self.image = image
        self.health = health

        self.action_positions = {self.pos}
        last_level = [self.pos]
        next_level = []
        for _ in range(action_range):
            for pos in last_level:
                for k in ((0, -1), (-1, 0),
                          (0, 1), (1, 0)):
                    new_pos = (pos[0] + CONFIG['OBJ_WIDTH'] * k[0],
                               pos[1] + CONFIG['OBJ_HEIGHT'] * k[1])
                    if new_pos[0] < 0 or new_pos[0] >= level_size[0] or \
                       new_pos[1] < 0 or new_pos[1] >= level_size[1]:
                        continue
                    elif new_pos not in self.action_positions:
                        self.action_positions.add(new_pos)
                        next_level.append(new_pos)
            last_level = [i for i in next_level]

    def draw(self, surf):
        surf.blit(self.image, self.pos)


class Artillery(StaticGunWithField):
    def __init__(self, level_size, x, y, action_range, image, health, damage):
        super(Artillery, self).__init__(level_size, x, y, action_range, image, health)
        self.damage = damage


class AntiArtGun(StaticGunWithField):
    def __init__(self, level_size, x, y, action_range, image, health, defend_power):
        super(AntiArtGun, self).__init__(level_size, x, y, action_range, image, health)
        self.defend_power = defend_power


class Texture:
    def __init__(self, img, health):
        self.image = img
        self.health = health
        self.animated = False


class Base(Texture):
    def __init__(self, team=1):
        png = Base_png[(team - 1) % len(os_listdir('pics/blocks/base'))]
        super(Base, self).__init__(png.copy(), CONFIG['BASE_HEALTH'])
        self.anim_destr = blow
        self.frame = 0


class BlockUnD(Texture):
    def __init__(self):
        super(BlockUnD, self).__init__(BlockUnD_png.copy(), 999999999)


class BlockD(Texture):
    def __init__(self):
        super(BlockD, self).__init__(BlockD_png.copy(), CONFIG['BLOCK_HEALTH'])
        self.anim_destr = blow
        self.frame = 0


class Mine(Texture):
    def __init__(self):
        super(Mine, self).__init__(None, 1000)
        self.images = {gold: png.copy() for gold, png in Mine_png.items()}
        self.money = CONFIG['START_MINE_MONEY']
        self.check_image()

    def check_image(self):
        img = None
        for img_num in sorted(self.images.keys()):
            if img_num <= self.money:
                img = self.images[img_num]
            else:
                break
        self.image = img

    def update(self):
        self.money += randrange(CONFIG['MINE_MONEY_PER_TURN_FROM'],
                                CONFIG['MINE_MONEY_PER_TURN_TO'] + 1)
        self.check_image()


class Dirt(Texture):
    def __init__(self):
        super(Dirt, self).__init__(Dirt_png.copy(), 999999999)


class Water(Texture):
    def __init__(self):
        super(Water, self).__init__([img.copy() for img in Water_png], 999999999)
        self.frame = FPSForPics(10, len(self.image))
        self.animated = True


_objs = {
    '=': BlockUnD,
    '-': BlockD,
    'D': Dirt,
    'B': Base,
    'M': Mine,
    'W': Water
}


class Level:
    def __init__(self, level):
        self.objs_place = {}
        self.player_count = 0
        for line in level:
            self.player_count += line.count('B')
        self.ingame_objs = {i + 1: {} for i in range(self.player_count)}
        self.players_base = {}
        x = [i for i in range(1, self.player_count + 1)]
        self.obj_params = (CONFIG['OBJ_WIDTH'], CONFIG['OBJ_HEIGHT'])
        self.params = (len(level[0]), len(level))
        self.image = pg_Surface((self.params[0] * self.obj_params[0],
                                self.params[1] * self.obj_params[1]))
        self.size = self.image.get_size()
        self.level = [[None for _ in range(self.params[0])] for _ in range(self.params[1])]
        row_number, column_number = 0, 0
        for row in level:
            for col in row:
                coord = (column_number * CONFIG['OBJ_WIDTH'], row_number * CONFIG['OBJ_HEIGHT'])
                if col == 'B':
                    ch = choice(x)
                    self.players_base[ch] = coord
                    self.objs_place[coord] = \
                        self.level[row_number][column_number] = _objs[col](ch)
                    x.pop(x.index(ch))
                else:
                    self.objs_place[coord] = \
                        self.level[row_number][column_number] = _objs[col]()
                column_number += 1
            row_number += 1
            column_number = 0

    def draw(self, surf, cam_x, cam_y, globaltime, additional_blocks_covering=None):
        if additional_blocks_covering is None:
            additional_blocks_covering = {}
        destruct = False
        self.image.fill(BLACK)
        for pos, obj in list(self.objs_place.items()):
            if -cam_x - CONFIG['OBJ_WIDTH'] <= pos[0] <= -cam_x + CONFIG['RESOLUTION'][0] \
                    and -cam_y - CONFIG['OBJ_HEIGHT'] <= pos[1] <= -cam_y + CONFIG['RESOLUTION'][1]:
                if obj.health <= 0:
                    if obj.frame != len(obj.anim_destr):
                        destruct = True
                        obj.image.blit(obj.anim_destr[obj.frame], (0, 0))
                        obj.frame += 1
                    else:
                        obj = Dirt()
                        self.objs_place[pos] = obj
                if obj.animated:
                    img = obj.image[obj.frame.frame(globaltime)]
                else:
                    img = obj.image
                self.image.blit(img, pos)
                if pos in additional_blocks_covering.keys():
                    for image in additional_blocks_covering[pos]:
                        self.image.blit(image, pos)

        surf.blit(self.image, (0, 0))
        return destruct
