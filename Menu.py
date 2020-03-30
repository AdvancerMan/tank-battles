# coding: utf-8

from re import findall
from time import process_time as time_process_time
from pygame import \
    Surface as pg_Surface, \
    error as pg_error
from pygame import \
    QUIT, KEYDOWN, MOUSEMOTION, \
    K_ESCAPE, K_UP, K_DOWN, K_w, \
    K_s, MOUSEBUTTONDOWN, MOUSEBUTTONUP, \
    FULLSCREEN
from pygame.mixer_music import \
    set_volume as pg_mixer_music_set_volume
from pygame.display import \
    set_mode as pg_display_set_mode, \
    flip as pg_display_flip
from pygame.transform import \
    rotate as pg_transform_rotate, \
    scale as pg_transform_scale
from pygame.mouse import \
    get_pos as pg_mouse_get_pos
from pygame.event import \
    get as pg_event_get
from pygame.font import \
    SysFont as pg_font_SysFont
import levels
from config import CONFIG
from game_obj import Level, \
    load_img, Field, Slider, \
    Switcher, objs_crossed, \
    FPSForPics
from tutorial import tutorial
from constants import BLACK, WHITE, \
    GREEN, YELLOW, PURPLE, KEYS_DICT, \
    STANDARD_INGAME_CONST


def file_writing(information):
    vars_pattern = r"'(.+?)': (.+),"
    with open('config.py', encoding='utf-8-sig') as f:
        file = {}
        for line in f:
            line = line.strip()
            var = findall(vars_pattern, line)
            if var:
                file[var[0][0]] = var[0][1]

    with open('config.py', 'w', encoding='utf-8-sig') as f:
        f.write('# coding: utf-8\n"""\nConfig file.\n"""\n')
        f.write('CONFIG = {\n')
        controls_pattern = r"(\d+?): " \
                           r"{" \
                           r"'(.+?)': (\d+?), " \
                           r"'(.+?)': (\d+?), " \
                           r"'(.+?)': (\d+?), " \
                           r"'(.+?)': (\d+?), " \
                           r"'(.+?)': (\d+?), " \
                           r"'(.+?)': (\d+?), " \
                           r"'(.+?)': (\d+?)" \
                           r"}"
        tmp = {}
        try:
            for i in findall(controls_pattern, file['CONTROLS']):
                tmp[int(i[0])] = {i[j]: int(i[j + 1]) for j in range(1, 15, 2)}
            file['CONTROLS'] = tmp
        except KeyError:
            print('FILE ERROR.')
            raise SystemExit
        try:
            tmp = information['CONTROLS'].items()
        except KeyError:
            pass
        else:
            for player, controls in tmp:
                try:
                    file['CONTROLS'][player]
                except KeyError:
                    file['CONTROLS'][player] = {}
                for k_name, key in controls.items():
                    file['CONTROLS'][player][k_name] = key
        for line in file.keys():
            if line not in information.keys():
                out = file[line]
                if type(out) is not str:
                    out = str(out)
            else:
                if line == 'CONTROLS':
                    for k in information[line].keys():
                        for ctrl_k in information[line][k].keys():
                            file[line][k][ctrl_k] = information[line][k][ctrl_k]
                    out = str(file[line])
                else:
                    out = str(information[line])

            f.write('    ' + "'" + line + "': " + out + ',\n')
        f.write('}\n')


def menu_init():
    global menu_screen, menu_screen_image, mm_pf_render, \
        mm_sf_render, mm_qf_render, \
        mm_nf_render, s_pf_render, s_sf_render, \
        s_qf_render, s_nf_render, s2_pf_render, \
        s2_sf_render, s2_qf_render, s2_nf_render, \
        arrow_left, arrow_right, \
        mm_pf_pos, mm_sf_pos, mm_qf_pos, mm_nf_pos, \
        s_pf_pos, s_sf_pos, s_qf_pos, s_nf_pos, \
        s2_pf_pos, s2_sf_pos, s2_qf_pos, s2_nf_pos, \
        mm_pf_size, mm_sf_size, mm_qf_size, \
        s_pf_size, s_sf_size, s_qf_size, \
        s2_pf_size, s2_sf_size, s2_qf_size, \
        contr_qf_pos, impact_font70, pl_n_text_pos, \
        field, right_field, left_field, down_field, \
        up_field, shoot_field, base_field, turn_end_field, \
        music_slider, music_switcher, res_wid_field, \
        res_hei_field, base_oz_field, block_oz_field, \
        money_pl_field, money_mine_field, money_mine_from_field, \
        money_mine_to_field, money_pl_from_field, \
        money_pl_to_field, fps_limit_field, sounds_slider, \
        cam_spd_slider, tank_spd_slider, bul_spd_slider, \
        inf_l_spd_slider, skl_l_spd_slider, mini_mn_spd_slider, \
        fullscreen_switcher, sounds_switcher, umolch_render, mn_anim_spd_slider
    menu_screen = pg_Surface(CONFIG['RESOLUTION'])
    tmp = {}
    try:
        with open('pics/main_screen/moving.txt') as f:
            for line in f:
                line = line.strip()
                line = line.split()
                if line[1] == 'right':
                    tmp[int(line[0])] = int(line[2])
                elif line[1] == 'left':
                    tmp[int(line[0])] = -int(line[2])
    except FileNotFoundError:
        pass
    x = 1
    menu_screen_image = []
    while True:
        try:
            img = load_img('pics/main_screen/' + str(x) + '.png', change_size=False, raise_error=True)
            img = pg_transform_scale(img, (int(img.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                           int(img.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
        except pg_error:
            if x == 1:
                menu_screen_image = [[load_img('none', CONFIG['RESOLUTION']), 0, CONFIG['RESOLUTION'][0], 0]]
            break
        else:
            if x in tmp.keys():
                y = -1
                if tmp[x] < 0:
                    y = 1
                menu_screen_image.append([img, 0, img.get_size()[0] * y, tmp[x]])
            else:
                menu_screen_image.append([img, 0, img.get_size()[0], 0])
            x += 1
    del tmp

    impact_font80 = pg_font_SysFont('Impact', 80)
    impact_font70 = pg_font_SysFont('Impact', 70)

    # Создание SurfaceType для текстов
    mm_pf_render = impact_font80.render('Играть', 1, WHITE)
    mm_sf_render = impact_font70.render('Настройки', 1, WHITE)
    mm_qf_render = impact_font80.render('Выйти', 1, WHITE)
    mm_nf_render = impact_font80.render('Танковые баталии', 1, GREEN)
    s_pf_render = impact_font80.render('Редактор уровней', 1, WHITE)
    s_sf_render = impact_font70.render('Настройка параметров', 1, WHITE)
    s_qf_render = impact_font80.render('Вернуться', 1, WHITE)
    s_nf_render = impact_font80.render('Танковые баталии', 1, YELLOW)
    s2_pf_render = impact_font80.render('Управление', 1, WHITE)
    s2_sf_render = impact_font70.render('Другое', 1, WHITE)
    s2_qf_render = impact_font80.render('Вернуться', 1, WHITE)
    s2_nf_render = impact_font80.render('Танковые баталии', 1, PURPLE)
    umolch_render = impact_font70.render('По умолчанию', 1, WHITE)

    # Подгонка размера текстов под разрешение экрана
    mm_pf_render = pg_transform_scale(mm_pf_render, (int(0.17891 * CONFIG['RESOLUTION'][0]),
                                                     int(0.13611 * CONFIG['RESOLUTION'][1])))
    mm_sf_render = pg_transform_scale(mm_sf_render, (int(0.25391 * CONFIG['RESOLUTION'][0]),
                                                     int(0.11944 * CONFIG['RESOLUTION'][1])))
    mm_qf_render = pg_transform_scale(mm_qf_render, (int(0.18044 * CONFIG['RESOLUTION'][0]),
                                                     int(0.13611 * CONFIG['RESOLUTION'][1])))
    mm_nf_render = pg_transform_scale(mm_nf_render, (int(0.50938 * CONFIG['RESOLUTION'][0]),
                                                     int(0.13611 * CONFIG['RESOLUTION'][1])))
    s_pf_render = pg_transform_scale(s_pf_render, (int(0.49375 * CONFIG['RESOLUTION'][0]),
                                                   int(0.13611 * CONFIG['RESOLUTION'][1])))
    s_sf_render = pg_transform_scale(s_sf_render, (int(0.54531 * CONFIG['RESOLUTION'][0]),
                                                   int(0.11944 * CONFIG['RESOLUTION'][1])))
    s_qf_render = pg_transform_scale(s_qf_render, (int(0.28359 * CONFIG['RESOLUTION'][0]),
                                                   int(0.13611 * CONFIG['RESOLUTION'][1])))
    s_nf_render = pg_transform_scale(s_nf_render, (int(0.50938 * CONFIG['RESOLUTION'][0]),
                                                   int(0.13611 * CONFIG['RESOLUTION'][1])))
    s2_pf_render = pg_transform_scale(s2_pf_render, (int(0.32578 * CONFIG['RESOLUTION'][0]),
                                                     int(0.13611 * CONFIG['RESOLUTION'][1])))
    s2_sf_render = pg_transform_scale(s2_sf_render, (int(0.16328 * CONFIG['RESOLUTION'][0]),
                                                     int(0.11944 * CONFIG['RESOLUTION'][1])))
    s2_qf_render = pg_transform_scale(s2_qf_render, (int(0.28359 * CONFIG['RESOLUTION'][0]),
                                                     int(0.13611 * CONFIG['RESOLUTION'][1])))
    s2_nf_render = pg_transform_scale(s2_nf_render, (int(0.50938 * CONFIG['RESOLUTION'][0]),
                                                     int(0.13611 * CONFIG['RESOLUTION'][1])))
    umolch_render = pg_transform_scale(umolch_render, (int(umolch_render.get_size()[0] / 1280 *
                                                           CONFIG['RESOLUTION'][0]),
                                                       int(umolch_render.get_size()[1] / 720 *
                                                           CONFIG['RESOLUTION'][1])))

    # Подгонка их позиции под разрешение
    mm_pf_pos = (int(0.41016 * CONFIG['RESOLUTION'][0]),
                 int(0.25417 * CONFIG['RESOLUTION'][1]))
    mm_sf_pos = (int(0.37266 * CONFIG['RESOLUTION'][0]),
                 int(0.48333 * CONFIG['RESOLUTION'][1]))
    mm_qf_pos = (int(0.40938 * CONFIG['RESOLUTION'][0]),
                 int(0.6875 * CONFIG['RESOLUTION'][1]))
    mm_nf_pos = (int(0.24531 * CONFIG['RESOLUTION'][0]),
                 int(0))
    s_pf_pos = (int(0.25313 * CONFIG['RESOLUTION'][0]),
                int(0.25417 * CONFIG['RESOLUTION'][1]))
    s_sf_pos = (int(0.22734 * CONFIG['RESOLUTION'][0]),
                int(0.48333 * CONFIG['RESOLUTION'][1]))
    s_qf_pos = (int(0.35781 * CONFIG['RESOLUTION'][0]),
                int(0.6875 * CONFIG['RESOLUTION'][1]))
    s_nf_pos = (int(0.24531 * CONFIG['RESOLUTION'][0]),
                int(0))
    s2_pf_pos = (int(0.33671 * CONFIG['RESOLUTION'][0]),
                 int(0.25417 * CONFIG['RESOLUTION'][1]))
    s2_sf_pos = (int(0.41875 * CONFIG['RESOLUTION'][0]),
                 int(0.48333 * CONFIG['RESOLUTION'][1]))
    s2_qf_pos = (int(0.35781 * CONFIG['RESOLUTION'][0]),
                 int(0.6875 * CONFIG['RESOLUTION'][1]))
    s2_nf_pos = (int(0.24531 * CONFIG['RESOLUTION'][0]),
                 int(0))
    contr_qf_pos = (int(0.35781 * CONFIG['RESOLUTION'][0]),
                    int(0.83333 * CONFIG['RESOLUTION'][1]))

    pl_n_text_pos = (int(0.66406 * CONFIG['RESOLUTION'][0]),
                     int(0.83333 * CONFIG['RESOLUTION'][1]))

    mm_pf_size = mm_pf_render.get_size()
    mm_sf_size = mm_sf_render.get_size()
    mm_qf_size = mm_qf_render.get_size()
    s_pf_size = s_pf_render.get_size()
    s_sf_size = s_sf_render.get_size()
    s_qf_size = s_qf_render.get_size()
    s2_pf_size = s2_pf_render.get_size()
    s2_sf_size = s2_sf_render.get_size()
    s2_qf_size = s2_qf_render.get_size()

    arrow_left = load_img('pics/misc/arrow.png', (int(0.03906 * CONFIG['RESOLUTION'][0]),
                                                  int(0.06944 * CONFIG['RESOLUTION'][1])))
    arrow_right = arrow_left.copy()
    arrow_right = pg_transform_rotate(arrow_right, 180)

    field = load_img('pics/misc/field.png', change_size=False)
    up_field = Field(field.copy(), impact_font70, (int(0.23438 * CONFIG['RESOLUTION'][0]),
                                                   int(0.08333 * CONFIG['RESOLUTION'][1])),
                     (int(20), int(100)), 'Вверх: ', WHITE)
    left_field = Field(field.copy(), impact_font70, (int(0.23438 * CONFIG['RESOLUTION'][0]),
                                                     int(0.08333 * CONFIG['RESOLUTION'][1])),
                       (int(20), int(170)), 'Влево: ', WHITE)
    down_field = Field(field.copy(), impact_font70, (int(0.23438 * CONFIG['RESOLUTION'][0]),
                                                     int(0.08333 * CONFIG['RESOLUTION'][1])),
                       (int(20), int(240)), 'Вниз: ', WHITE)
    right_field = Field(field.copy(), impact_font70, (int(0.23438 * CONFIG['RESOLUTION'][0]),
                                                      int(0.08333 * CONFIG['RESOLUTION'][1])),
                        (int(20), int(310)), 'Вправо: ', WHITE)
    shoot_field = Field(field.copy(), impact_font70, (int(0.23438 * CONFIG['RESOLUTION'][0]),
                                                      int(0.08333 * CONFIG['RESOLUTION'][1])),
                        (int(20), int(380)), 'Стрелять: ', WHITE)
    base_field = Field(field.copy(), impact_font70, (int(0.23438 * CONFIG['RESOLUTION'][0]),
                                                     int(0.08333 * CONFIG['RESOLUTION'][1])),
                       (int(20), int(450)), 'Открыть базу: ', WHITE)
    turn_end_field = Field(field.copy(), impact_font70, (int(0.23438 * CONFIG['RESOLUTION'][0]),
                                                         int(0.08333 * CONFIG['RESOLUTION'][1])),
                           (int(20), int(520)), 'Завершить ход: ', WHITE)

    res_wid_field = Field(field.copy(), impact_font70, (int(0.15625 * CONFIG['RESOLUTION'][0]),
                                                        int(0.08333 * CONFIG['RESOLUTION'][1])),
                          (int(0.01562 * CONFIG['RESOLUTION'][0]),
                           int(0.13889 * CONFIG['RESOLUTION'][1])),
                          'Ширина экрана', WHITE, True)
    res_hei_field = Field(field.copy(), impact_font70, (int(0.15625 * CONFIG['RESOLUTION'][0]),
                                                        int(0.08333 * CONFIG['RESOLUTION'][1])),
                          (int(0.01562 * CONFIG['RESOLUTION'][0]),
                           int(0.27778 * CONFIG['RESOLUTION'][1])),
                          'Высота экрана', WHITE, True)
    base_oz_field = Field(field.copy(), impact_font70, (int(0.19531 * CONFIG['RESOLUTION'][0]),
                                                        int(0.08333 * CONFIG['RESOLUTION'][1])),
                          (int(0.01562 * CONFIG['RESOLUTION'][0]),
                           int(0.41667 * CONFIG['RESOLUTION'][1])),
                          'ОЗ базы', WHITE)
    block_oz_field = Field(field.copy(), impact_font70, (int(0.19531 * CONFIG['RESOLUTION'][0]),
                                                         int(0.08333 * CONFIG['RESOLUTION'][1])),
                           (int(0.01562 * CONFIG['RESOLUTION'][0]),
                            int(0.55556 * CONFIG['RESOLUTION'][1])),
                           'ОЗ блоков', WHITE)
    money_pl_field = Field(field.copy(), impact_font70, (int(0.19531 * CONFIG['RESOLUTION'][0]),
                                                         int(0.08333 * CONFIG['RESOLUTION'][1])),
                           (int(0.01562 * CONFIG['RESOLUTION'][0]),
                            int(0.69444 * CONFIG['RESOLUTION'][1])),
                           'Стартовое золото игрока', WHITE)
    money_mine_field = Field(field.copy(), impact_font70, (int(0.19531 * CONFIG['RESOLUTION'][0]),
                                                           int(0.08333 * CONFIG['RESOLUTION'][1])),
                             (int(0.01562 * CONFIG['RESOLUTION'][0]),
                              int(0.13889 * CONFIG['RESOLUTION'][1])),
                             'Стартовое золото шахт', WHITE)
    money_mine_from_field = Field(field.copy(), impact_font70, (int(0.19531 * CONFIG['RESOLUTION'][0]),
                                                                int(0.08333 * CONFIG['RESOLUTION'][1])),
                                  (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                   int(0.27778 * CONFIG['RESOLUTION'][1])),
                                  '+ золото в шахте от', WHITE)
    money_mine_to_field = Field(field.copy(), impact_font70, (int(0.19531 * CONFIG['RESOLUTION'][0]),
                                                              int(0.08333 * CONFIG['RESOLUTION'][1])),
                                (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                 int(0.41667 * CONFIG['RESOLUTION'][1])),
                                'До', WHITE)
    money_pl_from_field = Field(field.copy(), impact_font70, (int(0.19531 * CONFIG['RESOLUTION'][0]),
                                                              int(0.08333 * CONFIG['RESOLUTION'][1])),
                                (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                 int(0.55556 * CONFIG['RESOLUTION'][1])),
                                '+ золото у игрока от', WHITE)
    money_pl_to_field = Field(field.copy(), impact_font70, (int(0.19531 * CONFIG['RESOLUTION'][0]),
                                                            int(0.08333 * CONFIG['RESOLUTION'][1])),
                              (int(0.01562 * CONFIG['RESOLUTION'][0]),
                               int(0.69444 * CONFIG['RESOLUTION'][1])),
                              'До', WHITE)
    fps_limit_field = Field(field.copy(), impact_font70, (int(0.11719 * CONFIG['RESOLUTION'][0]),
                                                          int(0.08333 * CONFIG['RESOLUTION'][1])),
                            (int(0.01562 * CONFIG['RESOLUTION'][0]),
                             int(0.13889 * CONFIG['RESOLUTION'][1])),
                            'Лимит ФПС', WHITE)

    slider_line = load_img('pics/misc/slider_line.png', change_size=False)
    slider = load_img('pics/misc/slider/slider.png', change_size=False)

    music_slider = Slider(slider_line, slider, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                               int(0.55556 * CONFIG['RESOLUTION'][1])),
                          (0, 1000), CONFIG['MUSIC_VOLUME'], 'Громкость музыки')
    sounds_slider = Slider(slider_line, slider, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                int(0.13889 * CONFIG['RESOLUTION'][1])),
                           (0, 1000), CONFIG['SOUNDS_VOLUME'], 'Громкость звуков')
    cam_spd_slider = Slider(slider_line, slider, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                 int(0.27778 * CONFIG['RESOLUTION'][1])),
                            (1, CONFIG['OBJ_WIDTH']), CONFIG['CAMERA_SPEED'], 'Скорость камеры')
    tank_spd_slider = Slider(slider_line, slider, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                  int(0.41667 * CONFIG['RESOLUTION'][1])),
                             (1, CONFIG['OBJ_WIDTH']), CONFIG['TANKS_SPEED'], 'Скорость танков')
    bul_spd_slider = Slider(slider_line, slider, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                 int(0.55556 * CONFIG['RESOLUTION'][1])),
                            (1, CONFIG['OBJ_WIDTH']), CONFIG['BULLETS_SPEED'], 'Скорость пуль')
    inf_l_spd_slider = Slider(slider_line, slider, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                   int(0.69444 * CONFIG['RESOLUTION'][1])),
                              (1, 40), CONFIG['INFORMATION_LINE_SPEED'], 'Скорость строки состояния')
    skl_l_spd_slider = Slider(slider_line, slider, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                   int(0.13889 * CONFIG['RESOLUTION'][1])),
                              (1, CONFIG['OBJ_WIDTH']), CONFIG['SKILLS_LINE_SPEED'], 'Скорость меню акт. умений')
    mini_mn_spd_slider = Slider(slider_line, slider, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                     int(0.27778 * CONFIG['RESOLUTION'][1])),
                                (1, CONFIG['OBJ_WIDTH']), CONFIG['MINI_MENU_SPEED'], 'Скорость мини-меню')
    mn_anim_spd_slider = Slider(slider_line, slider, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                     int(0.41667 * CONFIG['RESOLUTION'][1])),
                                (1, 1000), CONFIG['MENU_ANIM_SPEED'], 'Скорость анимации меню')

    switcher_images = [load_img('pics/misc/switcher/switcher_' + i + '.png', change_size=False) for i in ('off', 'on')]

    fullscreen_switcher = Switcher(switcher_images, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                    int(0.41667 * CONFIG['RESOLUTION'][1])),
                                   CONFIG['FULLSCREEN_ON'], 'Полный экран')
    music_switcher = Switcher(switcher_images, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                               int(0.69444 * CONFIG['RESOLUTION'][1])),
                              CONFIG['MUSIC_ON'], 'Музыка включена')
    sounds_switcher = Switcher(switcher_images, impact_font70, (int(0.01562 * CONFIG['RESOLUTION'][0]),
                                                                int(0.27778 * CONFIG['RESOLUTION'][1])),
                               CONFIG['SOUNDS_ON'], 'Звук включен')


def menu_del_objs():
    global menu_screen, menu_screen_image, mm_pf_render, \
        mm_sf_render, mm_qf_render, \
        mm_nf_render, s_pf_render, s_sf_render, \
        s_qf_render, s_nf_render, s2_pf_render, \
        s2_sf_render, s2_qf_render, s2_nf_render, \
        arrow_left, arrow_right, \
        mm_pf_pos, mm_sf_pos, mm_qf_pos, mm_nf_pos, \
        s_pf_pos, s_sf_pos, s_qf_pos, s_nf_pos, \
        s2_pf_pos, s2_sf_pos, s2_qf_pos, s2_nf_pos, \
        mm_pf_size, mm_sf_size, mm_qf_size, \
        s_pf_size, s_sf_size, s_qf_size, \
        s2_pf_size, s2_sf_size, s2_qf_size, \
        contr_qf_pos, impact_font70, pl_n_text_pos, \
        field, right_field, left_field, down_field, \
        up_field, shoot_field, base_field, turn_end_field, \
        music_slider, music_switcher, res_wid_field, \
        res_hei_field, base_oz_field, block_oz_field, \
        money_pl_field, money_mine_field, money_mine_from_field, \
        money_mine_to_field, money_pl_from_field, \
        money_pl_to_field, fps_limit_field, sounds_slider, \
        cam_spd_slider, tank_spd_slider, bul_spd_slider, \
        inf_l_spd_slider, skl_l_spd_slider, mini_mn_spd_slider, \
        fullscreen_switcher, sounds_switcher, umolch_render

    del menu_screen, menu_screen_image, mm_pf_render, \
        mm_sf_render, mm_qf_render, \
        mm_nf_render, s_pf_render, s_sf_render, \
        s_qf_render, s_nf_render, s2_pf_render, \
        s2_sf_render, s2_qf_render, s2_nf_render, \
        arrow_left, arrow_right, \
        mm_pf_pos, mm_sf_pos, mm_qf_pos, mm_nf_pos, \
        s_pf_pos, s_sf_pos, s_qf_pos, s_nf_pos, \
        s2_pf_pos, s2_sf_pos, s2_qf_pos, s2_nf_pos, \
        mm_pf_size, mm_sf_size, mm_qf_size, \
        s_pf_size, s_sf_size, s_qf_size, \
        s2_pf_size, s2_sf_size, s2_qf_size, \
        contr_qf_pos, impact_font70, pl_n_text_pos, \
        field, right_field, left_field, down_field, \
        up_field, shoot_field, base_field, turn_end_field, \
        music_slider, music_switcher, res_wid_field, \
        res_hei_field, base_oz_field, block_oz_field, \
        money_pl_field, money_mine_field, money_mine_from_field, \
        money_mine_to_field, money_pl_from_field, \
        money_pl_to_field, fps_limit_field, sounds_slider, \
        cam_spd_slider, tank_spd_slider, bul_spd_slider, \
        inf_l_spd_slider, skl_l_spd_slider, mini_mn_spd_slider, \
        fullscreen_switcher, sounds_switcher, umolch_render


def main_menu(ifgame, window, clock):
    global CONFIG
    loading_screen(window)
    menu_init()
    screen = 'main_menu'
    lvl_key = 1
    pl_n = 1
    cnfg_sheet = 1
    mouse_pos = pg_mouse_get_pos()

    control = None
    writing = None
    ctrl = {1: {}}
    fullscr_on = CONFIG['FULLSCREEN_ON']
    res = CONFIG['RESOLUTION']

    menu_open = True
    while menu_open:
        for event in pg_event_get():
            if event.type == QUIT:
                raise SystemExit
            if event.type == MOUSEMOTION:
                mouse_pos = pg_mouse_get_pos()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if screen == 'main_menu':
                        if ifgame:
                            menu_del_objs()
                            return True, None, window
                    elif screen == 'settings':
                        screen = 'main_menu'
                    elif screen == 'settings_2':
                        screen = 'settings'
                    elif screen == 'controls':
                        screen = 'settings_2'
                        control = None
                        file_writing({'CONTROLS': ctrl})
                    elif screen == 'level_choosing':
                        screen = 'main_menu'
                    elif screen == 'other_settings':
                        if CONFIG['MINE_MONEY_PER_TURN_FROM'] > CONFIG['MINE_MONEY_PER_TURN_TO']:
                            CONFIG['MINE_MONEY_PER_TURN_TO'] = CONFIG['MINE_MONEY_PER_TURN_FROM']
                        if CONFIG['PLAYER_MONEY_PER_TURN_FROM'] > CONFIG['PLAYER_MONEY_PER_TURN_TO']:
                            CONFIG['PLAYER_MONEY_PER_TURN_TO'] = CONFIG['PLAYER_MONEY_PER_TURN_FROM']
                        if CONFIG['BASE_HEALTH'] == 0:
                            CONFIG['BASE_HEALTH'] = 1
                        if res[0] < 100:
                            res = (100, res[1])
                        if res[1] < 100:
                            res = (res[0], 100)

                        if fullscr_on != CONFIG['FULLSCREEN_ON']:
                            if fullscr_on:
                                window = pg_display_set_mode(CONFIG['RESOLUTION'], FULLSCREEN)
                            else:
                                window = pg_display_set_mode(CONFIG['RESOLUTION'])

                        file_writing({'START_MINE_MONEY': CONFIG['START_MINE_MONEY'],
                                      'SKILLS_LINE_SPEED': CONFIG['SKILLS_LINE_SPEED'],
                                      'CAMERA_SPEED': CONFIG['CAMERA_SPEED'],
                                      'PLAYER_MONEY_PER_TURN_TO': CONFIG['PLAYER_MONEY_PER_TURN_TO'],
                                      'MINI_MENU_SPEED': CONFIG['MINI_MENU_SPEED'],
                                      'TANKS_SPEED': CONFIG['TANKS_SPEED'],
                                      'PLAYER_MONEY_PER_TURN_FROM': CONFIG['PLAYER_MONEY_PER_TURN_FROM'],
                                      'INFORMATION_LINE_SPEED': CONFIG['INFORMATION_LINE_SPEED'],
                                      'MINE_MONEY_PER_TURN_TO': CONFIG['MINE_MONEY_PER_TURN_TO'],
                                      'START_PLAYER_MONEY': CONFIG['START_PLAYER_MONEY'],
                                      'MINE_MONEY_PER_TURN_FROM': CONFIG['MINE_MONEY_PER_TURN_FROM'],
                                      'BASE_HEALTH': CONFIG['BASE_HEALTH'],
                                      'FULLSCREEN_ON': fullscr_on,
                                      'RESOLUTION': res,
                                      'BLOCK_HEALTH': CONFIG['BLOCK_HEALTH'],
                                      'BULLETS_SPEED': CONFIG['BULLETS_SPEED'],
                                      'MUSIC_ON': CONFIG['MUSIC_ON'],
                                      'FPS_LIMIT': CONFIG['FPS_LIMIT'],
                                      'MUSIC_VOLUME': CONFIG['MUSIC_VOLUME'],
                                      'SOUNDS_VOLUME': CONFIG['SOUNDS_VOLUME'],
                                      'SOUNDS_ON': CONFIG['SOUNDS_ON'],
                                      'MENU_ANIM_SPEED': CONFIG['MENU_ANIM_SPEED']})
                        CONFIG['FULLSCREEN_ON'] = fullscr_on

                        writing = None
                        sounds_slider.moving = False
                        music_slider.moving = False
                        cam_spd_slider.moving = False
                        tank_spd_slider.moving = False
                        bul_spd_slider.moving = False
                        inf_l_spd_slider.moving = False
                        skl_l_spd_slider.moving = False
                        mini_mn_spd_slider.moving = False
                        mn_anim_spd_slider.moving = False

                        screen = 'settings_2'
                if control:
                    if pl_n not in ctrl.keys():
                        ctrl[pl_n] = {}
                    ctrl[pl_n][control] = event.key
                    if pl_n not in CONFIG['CONTROLS'].keys():
                        CONFIG['CONTROLS'][pl_n] = {}
                    CONFIG['CONTROLS'][pl_n][control] = event.key
                if writing:
                    if 48 <= event.key <= 57:
                        if writing[:-1] == 'res_':
                            res = list(res)
                            res[int(writing[-1])] = (int(str(res[int(writing[-1])]) + str(event.key - 48)))
                            res = tuple(res)

                        if writing == 'base_oz':
                            new_val = int(str(CONFIG['BASE_HEALTH']) + str(event.key - 48))
                            if new_val > 100000:
                                CONFIG['BASE_HEALTH'] = 100000
                            else:
                                CONFIG['BASE_HEALTH'] = new_val

                        elif writing == 'block_oz':
                            new_val = int(str(CONFIG['BLOCK_HEALTH']) + str(event.key - 48))
                            if new_val > 100000:
                                CONFIG['BLOCK_HEALTH'] = 100000
                            else:
                                CONFIG['BLOCK_HEALTH'] = new_val

                        elif writing == 'money_pl':
                            new_val = int(str(CONFIG['START_PLAYER_MONEY']) + str(event.key - 48))
                            if new_val > 100000:
                                CONFIG['START_PLAYER_MONEY'] = 100000
                            else:
                                CONFIG['START_PLAYER_MONEY'] = new_val

                        elif writing == 'money_mine':
                            new_val = int(str(CONFIG['START_MINE_MONEY']) + str(event.key - 48))
                            if new_val > 100000:
                                CONFIG['START_MINE_MONEY'] = 100000
                            else:
                                CONFIG['START_MINE_MONEY'] = new_val

                        elif writing == 'money_mine_from':
                            new_val = int(str(CONFIG['MINE_MONEY_PER_TURN_FROM']) + str(event.key - 48))
                            if new_val > 100000:
                                CONFIG['MINE_MONEY_PER_TURN_FROM'] = 100000
                            else:
                                CONFIG['MINE_MONEY_PER_TURN_FROM'] = new_val

                        elif writing == 'money_mine_to':
                            new_val = int(str(CONFIG['MINE_MONEY_PER_TURN_TO']) + str(event.key - 48))
                            if new_val > 100000:
                                CONFIG['MINE_MONEY_PER_TURN_TO'] = 100000
                            else:
                                CONFIG['MINE_MONEY_PER_TURN_TO'] = new_val

                        elif writing == 'money_pl_from':
                            new_val = int(str(CONFIG['PLAYER_MONEY_PER_TURN_FROM']) + str(event.key - 48))
                            if new_val > 100000:
                                CONFIG['PLAYER_MONEY_PER_TURN_FROM'] = 100000
                            else:
                                CONFIG['PLAYER_MONEY_PER_TURN_FROM'] = new_val

                        elif writing == 'money_pl_to':
                            new_val = int(str(CONFIG['PLAYER_MONEY_PER_TURN_TO']) + str(event.key - 48))
                            if new_val > 100000:
                                CONFIG['PLAYER_MONEY_PER_TURN_TO'] = 100000
                            else:
                                CONFIG['PLAYER_MONEY_PER_TURN_TO'] = new_val

                        elif writing == 'fps_limit':
                            new_val = int(str(CONFIG['FPS_LIMIT']) + str(event.key - 48))
                            if new_val > 200:
                                CONFIG['FPS_LIMIT'] = 200
                            else:
                                CONFIG['FPS_LIMIT'] = new_val

            if event.type == MOUSEBUTTONDOWN:
                if screen == 'main_menu':
                    if event.button == 1:
                        if objs_crossed(mouse_pos, (1, 1), mm_pf_pos, mm_pf_size):
                            screen = 'level_choosing'
                            lvl_key = 1
                        elif objs_crossed(mouse_pos, (1, 1), mm_sf_pos, mm_sf_size):
                            screen = 'settings'
                        elif objs_crossed(mouse_pos, (1, 1), mm_qf_pos, mm_qf_size):
                            menu_open = False
                elif screen == 'level_choosing':
                    if event.button == 1:
                        key = 1
                        tmp = int(0.20833 * CONFIG['RESOLUTION'][1])
                        for name in sorted(levels.level_dict_.keys()):
                            if tmp > CONFIG['RESOLUTION'][1] - int(0.13889 * CONFIG['RESOLUTION'][1]):
                                tmp = int(0.20833 * CONFIG['RESOLUTION'][1])
                                key += 1
                            if key == lvl_key:
                                text = impact_font70.render(name, 1, WHITE)
                                if objs_crossed(mouse_pos, (1, 1), (int(0.03906 * CONFIG['RESOLUTION'][0]), tmp),
                                                (int(text.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                                 int(text.get_size()[1] / 720 * CONFIG['RESOLUTION'][1]))):
                                    loading_screen(window)
                                    menu_del_objs()
                                    level = Level(levels.level_dict_[name])
                                    if name == 'Обучение':
                                        tutorial(window, level, clock)
                                    loading_screen(window)
                                    return True, level, window

                            tmp += int(0.13889 * CONFIG['RESOLUTION'][1])

                        if lvl_key > 1:
                            if objs_crossed(mouse_pos, (1, 1),
                                            (0, CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1] -
                                                arrow_left.get_size()[1]),
                                            arrow_left.get_size()):
                                lvl_key -= 1
                        if lvl_key < key:
                            if objs_crossed(mouse_pos, (1, 1),
                                            (0, CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]),
                                            arrow_right.get_size()):
                                lvl_key += 1
                elif screen == 'settings':
                    if event.button == 1:
                        if objs_crossed(mouse_pos, (1, 1), s_pf_pos, s_pf_size):
                            editor(window, clock)
                        elif objs_crossed(mouse_pos, (1, 1), s_sf_pos, s_sf_size):
                            screen = 'settings_2'
                        elif objs_crossed(mouse_pos, (1, 1), s_qf_pos, s_qf_size):
                            screen = 'main_menu'
                elif screen == 'settings_2':
                    if event.button == 1:
                        if objs_crossed(mouse_pos, (1, 1), s2_pf_pos, s2_pf_size):
                            screen = 'controls'
                            pl_n = 1
                        elif objs_crossed(mouse_pos, (1, 1), s2_sf_pos, s2_sf_size):
                            screen = 'other_settings'
                            cnfg_sheet = 1
                        elif objs_crossed(mouse_pos, (1, 1), s2_qf_pos, s2_qf_size):
                            screen = 'settings'
                elif screen == 'controls':
                    if event.button == 1:
                        if pl_n > 1:
                            if objs_crossed(mouse_pos, (1, 1),
                                            (0, CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1] -
                                                arrow_left.get_size()[1]),
                                            arrow_left.get_size()):
                                pl_n -= 1
                        if objs_crossed(mouse_pos, (1, 1),
                                        (0, CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]),
                                        arrow_right.get_size()):
                            pl_n += 1

                        elif objs_crossed(mouse_pos, (1, 1), contr_qf_pos, s2_qf_render.get_size()):
                            file_writing({'CONTROLS': ctrl})
                            screen = 'settings_2'

                        if objs_crossed(mouse_pos, (1, 1), right_field.pos, right_field.size):
                            control = 'right'

                        elif objs_crossed(mouse_pos, (1, 1), left_field.pos, left_field.size):
                            control = 'left'

                        elif objs_crossed(mouse_pos, (1, 1), shoot_field.pos, shoot_field.size):
                            control = 'shoot'

                        elif objs_crossed(mouse_pos, (1, 1), down_field.pos, down_field.size):
                            control = 'down'

                        elif objs_crossed(mouse_pos, (1, 1), up_field.pos, up_field.size):
                            control = 'up'

                        elif objs_crossed(mouse_pos, (1, 1), base_field.pos, base_field.size):
                            control = 'base'

                        elif objs_crossed(mouse_pos, (1, 1), turn_end_field.pos, turn_end_field.size):
                            control = 'turn_end'

                        else:
                            control = None
                elif screen == 'other_settings':
                    if event.button == 1:
                        if cnfg_sheet > 1:
                            if objs_crossed(mouse_pos, (1, 1),
                                            (0, CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1] -
                                                arrow_left.get_size()[1]),
                                            arrow_left.get_size()):
                                cnfg_sheet -= 1
                        if cnfg_sheet < 5:
                            if objs_crossed(mouse_pos, (1, 1),
                                            (0, CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]),
                                            arrow_right.get_size()):
                                cnfg_sheet += 1
                        if objs_crossed(mouse_pos, (1, 1),
                                        (pl_n_text_pos[0] - int(0.00781 * CONFIG['RESOLUTION'][0]), pl_n_text_pos[1]),
                                        umolch_render.get_size()):
                            CONFIG['PLAYER_MONEY_PER_TURN_TO'] = STANDARD_INGAME_CONST['PLAYER_MONEY_PER_TURN_TO']
                            CONFIG['FPS_LIMIT'] = STANDARD_INGAME_CONST['FPS_LIMIT']
                            CONFIG['MINE_MONEY_PER_TURN_FROM'] = STANDARD_INGAME_CONST['MINE_MONEY_PER_TURN_FROM']
                            CONFIG['BASE_HEALTH'] = STANDARD_INGAME_CONST['BASE_HEALTH']
                            res = STANDARD_INGAME_CONST['RESOLUTION']
                            CONFIG['BLOCK_HEALTH'] = STANDARD_INGAME_CONST['BLOCK_HEALTH']
                            CONFIG['MINE_MONEY_PER_TURN_TO'] = STANDARD_INGAME_CONST['MINE_MONEY_PER_TURN_TO']
                            CONFIG['START_PLAYER_MONEY'] = STANDARD_INGAME_CONST['START_PLAYER_MONEY']
                            CONFIG['START_MINE_MONEY'] = STANDARD_INGAME_CONST['START_MINE_MONEY']
                            CONFIG['PLAYER_MONEY_PER_TURN_FROM'] = STANDARD_INGAME_CONST['PLAYER_MONEY_PER_TURN_FROM']
                            CONFIG['MINI_MENU_SPEED'] = STANDARD_INGAME_CONST['MINI_MENU_SPEED']
                            CONFIG['SKILLS_LINE_SPEED'] = STANDARD_INGAME_CONST['SKILLS_LINE_SPEED']
                            CONFIG['TANKS_SPEED'] = STANDARD_INGAME_CONST['TANKS_SPEED']
                            CONFIG['CAMERA_SPEED'] = STANDARD_INGAME_CONST['CAMERA_SPEED']
                            CONFIG['BULLETS_SPEED'] = STANDARD_INGAME_CONST['BULLETS_SPEED']
                            CONFIG['MUSIC_VOLUME'] = STANDARD_INGAME_CONST['MUSIC_VOLUME']
                            CONFIG['SOUNDS_VOLUME'] = STANDARD_INGAME_CONST['SOUNDS_VOLUME']
                            CONFIG['MENU_ANIM_SPEED'] = STANDARD_INGAME_CONST['MENU_ANIM_SPEED']
                            CONFIG['INFORMATION_LINE_SPEED'] = STANDARD_INGAME_CONST['INFORMATION_LINE_SPEED']
                            CONFIG['MUSIC_ON'] = STANDARD_INGAME_CONST['MUSIC_ON']
                            fullscr_on = STANDARD_INGAME_CONST['FULLSCREEN_ON']
                            CONFIG['SOUNDS_ON'] = STANDARD_INGAME_CONST['SOUNDS_ON']

                            pg_mixer_music_set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))

                            mini_mn_spd_slider.slider_pos = \
                                mini_mn_spd_slider.value2pixel[STANDARD_INGAME_CONST['MINI_MENU_SPEED']]
                            skl_l_spd_slider.slider_pos = \
                                skl_l_spd_slider.value2pixel[STANDARD_INGAME_CONST['SKILLS_LINE_SPEED']]
                            tank_spd_slider.slider_pos = \
                                tank_spd_slider.value2pixel[STANDARD_INGAME_CONST['TANKS_SPEED']]
                            cam_spd_slider.slider_pos = \
                                cam_spd_slider.value2pixel[STANDARD_INGAME_CONST['CAMERA_SPEED']]
                            bul_spd_slider.slider_pos = \
                                bul_spd_slider.value2pixel[STANDARD_INGAME_CONST['BULLETS_SPEED']]
                            music_slider.slider_pos = \
                                music_slider.value2pixel[STANDARD_INGAME_CONST['MUSIC_VOLUME']]
                            sounds_slider.slider_pos = \
                                sounds_slider.value2pixel[STANDARD_INGAME_CONST['SOUNDS_VOLUME']]
                            inf_l_spd_slider.slider_pos = \
                                inf_l_spd_slider.value2pixel[STANDARD_INGAME_CONST['INFORMATION_LINE_SPEED']]
                            mn_anim_spd_slider.slider_pos = \
                                mn_anim_spd_slider.value2pixel[STANDARD_INGAME_CONST['MENU_ANIM_SPEED']]

                            music_switcher.on = STANDARD_INGAME_CONST['MUSIC_ON']
                            fullscreen_switcher.on = STANDARD_INGAME_CONST['FULLSCREEN_ON']
                            sounds_switcher.on = STANDARD_INGAME_CONST['SOUNDS_ON']

                        if objs_crossed(mouse_pos, (1, 1), contr_qf_pos, s2_qf_render.get_size()):
                            if CONFIG['MINE_MONEY_PER_TURN_FROM'] > CONFIG['MINE_MONEY_PER_TURN_TO']:
                                CONFIG['MINE_MONEY_PER_TURN_TO'] = CONFIG['MINE_MONEY_PER_TURN_FROM']
                            if CONFIG['PLAYER_MONEY_PER_TURN_FROM'] > CONFIG['PLAYER_MONEY_PER_TURN_TO']:
                                CONFIG['PLAYER_MONEY_PER_TURN_TO'] = CONFIG['PLAYER_MONEY_PER_TURN_FROM']
                            if CONFIG['BASE_HEALTH'] == 0:
                                CONFIG['BASE_HEALTH'] = 1
                            if res[0] < 100:
                                res = (100, res[1])
                            if res[1] < 100:
                                res = (res[0], 100)

                            if fullscr_on != CONFIG['FULLSCREEN_ON']:
                                if fullscr_on:
                                    window = pg_display_set_mode(CONFIG['RESOLUTION'], FULLSCREEN)
                                else:
                                    window = pg_display_set_mode(CONFIG['RESOLUTION'])

                            file_writing({'START_MINE_MONEY': CONFIG['START_MINE_MONEY'],
                                          'SKILLS_LINE_SPEED': CONFIG['SKILLS_LINE_SPEED'],
                                          'CAMERA_SPEED': CONFIG['CAMERA_SPEED'],
                                          'PLAYER_MONEY_PER_TURN_TO': CONFIG['PLAYER_MONEY_PER_TURN_TO'],
                                          'MINI_MENU_SPEED': CONFIG['MINI_MENU_SPEED'],
                                          'TANKS_SPEED': CONFIG['TANKS_SPEED'],
                                          'PLAYER_MONEY_PER_TURN_FROM': CONFIG['PLAYER_MONEY_PER_TURN_FROM'],
                                          'INFORMATION_LINE_SPEED': CONFIG['INFORMATION_LINE_SPEED'],
                                          'MINE_MONEY_PER_TURN_TO': CONFIG['MINE_MONEY_PER_TURN_TO'],
                                          'START_PLAYER_MONEY': CONFIG['START_PLAYER_MONEY'],
                                          'MINE_MONEY_PER_TURN_FROM': CONFIG['MINE_MONEY_PER_TURN_FROM'],
                                          'BASE_HEALTH': CONFIG['BASE_HEALTH'],
                                          'FULLSCREEN_ON': fullscr_on,
                                          'RESOLUTION': res,
                                          'BLOCK_HEALTH': CONFIG['BLOCK_HEALTH'],
                                          'BULLETS_SPEED': CONFIG['BULLETS_SPEED'],
                                          'MUSIC_ON': CONFIG['MUSIC_ON'],
                                          'FPS_LIMIT': CONFIG['FPS_LIMIT'],
                                          'MUSIC_VOLUME': CONFIG['MUSIC_VOLUME'],
                                          'SOUNDS_VOLUME': CONFIG['SOUNDS_VOLUME'],
                                          'SOUNDS_ON': CONFIG['SOUNDS_ON'],
                                          'MENU_ANIM_SPEED': CONFIG['MENU_ANIM_SPEED']})
                            CONFIG['FULLSCREEN_ON'] = fullscr_on
                            screen = 'settings_2'

                        if cnfg_sheet == 1:
                            if objs_crossed(mouse_pos, (1, 1), music_slider.line_pos, music_slider.line_size):
                                music_slider.moving = True
                            if objs_crossed(mouse_pos, (1, 1),
                                            music_switcher.switcher_pos, music_switcher.switcher_size):
                                music_switcher.on = not music_switcher.on
                            if objs_crossed(mouse_pos, (1, 1),
                                            fullscreen_switcher.switcher_size, fullscreen_switcher.switcher_pos):
                                fullscreen_switcher.on = not fullscreen_switcher.on
                            if objs_crossed(mouse_pos, (1, 1), res_wid_field.pos, res_wid_field.size):
                                writing = 'res_0'
                                res = (0, res[1])
                            elif objs_crossed(mouse_pos, (1, 1), res_hei_field.pos, res_hei_field.size):
                                writing = 'res_1'
                                res = (res[0], 0)
                            else:
                                writing = None

                        elif cnfg_sheet == 2:
                            if objs_crossed(mouse_pos, (1, 1), sounds_slider.line_pos, sounds_slider.line_size):
                                sounds_slider.moving = True
                            if objs_crossed(mouse_pos, (1, 1),
                                            sounds_switcher.switcher_pos, sounds_switcher.switcher_size):
                                sounds_switcher.on = not sounds_switcher.on
                            if objs_crossed(mouse_pos, (1, 1), base_oz_field.pos, base_oz_field.size):
                                writing = 'base_oz'
                                CONFIG['BASE_HEALTH'] = 0
                            elif objs_crossed(mouse_pos, (1, 1), block_oz_field.pos, block_oz_field.size):
                                writing = 'block_oz'
                                CONFIG['BLOCK_HEALTH'] = 0
                            elif objs_crossed(mouse_pos, (1, 1), money_pl_field.pos, money_pl_field.size):
                                writing = 'money_pl'
                                CONFIG['START_PLAYER_MONEY'] = 0
                            else:
                                writing = None

                        elif cnfg_sheet == 3:
                            if objs_crossed(mouse_pos, (1, 1), money_mine_field.pos, money_mine_field.size):
                                writing = 'money_mine'
                                CONFIG['START_MINE_MONEY'] = 0
                            elif objs_crossed(mouse_pos, (1, 1), money_mine_from_field.pos, money_mine_from_field.size):
                                writing = 'money_mine_from'
                                CONFIG['MINE_MONEY_PER_TURN_FROM'] = 0
                            elif objs_crossed(mouse_pos, (1, 1), money_mine_to_field.pos, money_mine_to_field.size):
                                writing = 'money_mine_to'
                                CONFIG['MINE_MONEY_PER_TURN_TO'] = 0
                            elif objs_crossed(mouse_pos, (1, 1), money_pl_from_field.pos, money_pl_from_field.size):
                                writing = 'money_pl_from'
                                CONFIG['PLAYER_MONEY_PER_TURN_FROM'] = 0
                            elif objs_crossed(mouse_pos, (1, 1), money_pl_to_field.pos, money_pl_to_field.size):
                                writing = 'money_pl_to'
                                CONFIG['PLAYER_MONEY_PER_TURN_TO'] = 0
                            else:
                                writing = None

                        elif cnfg_sheet == 4:
                            if objs_crossed(mouse_pos, (1, 1), fps_limit_field.pos, fps_limit_field.size):
                                writing = 'fps_limit'
                                CONFIG['FPS_LIMIT'] = 0
                            else:
                                writing = None

                            if objs_crossed(mouse_pos, (1, 1), cam_spd_slider.line_pos, cam_spd_slider.line_size):
                                cam_spd_slider.moving = True
                            if objs_crossed(mouse_pos, (1, 1), tank_spd_slider.line_pos, tank_spd_slider.line_size):
                                tank_spd_slider.moving = True
                            if objs_crossed(mouse_pos, (1, 1), bul_spd_slider.line_pos, bul_spd_slider.line_size):
                                bul_spd_slider.moving = True
                            if objs_crossed(mouse_pos, (1, 1), inf_l_spd_slider.line_pos, inf_l_spd_slider.line_size):
                                inf_l_spd_slider.moving = True

                        elif cnfg_sheet == 5:
                            if objs_crossed(mouse_pos, (1, 1), skl_l_spd_slider.line_pos, skl_l_spd_slider.line_size):
                                skl_l_spd_slider.moving = True
                            if objs_crossed(mouse_pos, (1, 1), mini_mn_spd_slider.line_pos,
                                            mini_mn_spd_slider.line_size):
                                mini_mn_spd_slider.moving = True
                            if objs_crossed(mouse_pos, (1, 1), mn_anim_spd_slider.line_pos,
                                            mn_anim_spd_slider.line_size):
                                mn_anim_spd_slider.moving = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    if screen == 'other_settings':
                        music_slider.moving = False
                        sounds_slider.moving = False
                        cam_spd_slider.moving = False
                        tank_spd_slider.moving = False
                        bul_spd_slider.moving = False
                        inf_l_spd_slider.moving = False
                        skl_l_spd_slider.moving = False
                        mini_mn_spd_slider.moving = False
                        mn_anim_spd_slider.moving = False

        clock.tick(CONFIG['FPS_LIMIT'])

        for layer_ind in range(len(menu_screen_image)):
            menu_screen.blit(menu_screen_image[layer_ind][0], (menu_screen_image[layer_ind][1], 0))
            menu_screen.blit(menu_screen_image[layer_ind][0], (menu_screen_image[layer_ind][2], 0))
            anim_spd = menu_screen_image[layer_ind][3] * CONFIG['MENU_ANIM_SPEED'] / 1000
            if 0 < anim_spd < 1:
                anim_spd = 1
            elif -1 < anim_spd < 0:
                anim_spd = -1
            anim_spd = int(anim_spd)
            menu_screen_image[layer_ind][1] += anim_spd
            menu_screen_image[layer_ind][2] += anim_spd
            if abs(menu_screen_image[layer_ind][1]) >= menu_screen_image[layer_ind][0].get_size()[0]:
                y = -1
                if menu_screen_image[layer_ind][1] < 0:
                    y = 1
                menu_screen_image[layer_ind][1] += menu_screen_image[layer_ind][0].get_size()[0] * y
                menu_screen_image[layer_ind][2] += menu_screen_image[layer_ind][0].get_size()[0] * y

        if screen == 'main_menu':
            menu_screen.blit(mm_pf_render, mm_pf_pos)
            menu_screen.blit(mm_sf_render, mm_sf_pos)
            menu_screen.blit(mm_qf_render, mm_qf_pos)
            menu_screen.blit(mm_nf_render, mm_nf_pos)
        if screen == 'level_choosing':
            key = 1
            tmp = int(0.20833 * CONFIG['RESOLUTION'][1])
            for name in sorted(levels.level_dict_.keys()):
                if tmp > CONFIG['RESOLUTION'][1] - int(0.13889 * CONFIG['RESOLUTION'][1]):
                    tmp = int(0.20833 * CONFIG['RESOLUTION'][1])
                    key += 1
                if key == lvl_key:
                    lvl_text = impact_font70.render(name, 1, WHITE)
                    size = lvl_text.get_size()
                    lvl_text = pg_transform_scale(lvl_text,
                                                  (int((size[0] / 1280) * CONFIG['RESOLUTION'][0]),
                                                   int((size[1] / 720) * CONFIG['RESOLUTION'][1])))
                    menu_screen.blit(lvl_text, (int(0.03906 * CONFIG['RESOLUTION'][0]), tmp))
                tmp += int(0.13889 * CONFIG['RESOLUTION'][1])

            menu_screen.blit(s_nf_render, s_nf_pos)
            if lvl_key > 1:
                menu_screen.blit(arrow_left, (0, CONFIG['RESOLUTION'][1] - arrow_left.get_size()[1] -
                                              arrow_right.get_size()[1]))
            if lvl_key < key:
                menu_screen.blit(arrow_right, (0, CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]))
        elif screen == 'settings':
            menu_screen.blit(s_pf_render, s_pf_pos)
            menu_screen.blit(s_sf_render, s_sf_pos)
            menu_screen.blit(s_qf_render, s_qf_pos)
            menu_screen.blit(s_nf_render, s_nf_pos)
        elif screen == 'settings_2':
            menu_screen.blit(s2_pf_render, s2_pf_pos)
            menu_screen.blit(s2_sf_render, s2_sf_pos)
            menu_screen.blit(s2_qf_render, s2_qf_pos)
            menu_screen.blit(s2_nf_render, s2_nf_pos)
        elif screen == 'controls':
            pl_n_text = impact_font70.render('Игрок: ' + str(pl_n), 1, WHITE)
            pl_n_text = pg_transform_scale(pl_n_text, (int(pl_n_text.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                                       int(pl_n_text.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
            menu_screen.blit(mm_nf_render, mm_nf_pos)
            menu_screen.blit(s2_qf_render, contr_qf_pos)

            keys = []
            for key in ('right', 'left', 'down', 'up', 'shoot', 'base', 'turn_end'):
                try:
                    keys.append(KEYS_DICT[CONFIG['CONTROLS'][pl_n][key]])
                except KeyError:
                    keys.append(' ')
            right_field.update(keys[0], BLACK)
            left_field.update(keys[1], BLACK)
            down_field.update(keys[2], BLACK)
            up_field.update(keys[3], BLACK)
            shoot_field.update(keys[4], BLACK)
            base_field.update(keys[5], BLACK)
            turn_end_field.update(keys[6], BLACK)

            right_field.draw(menu_screen)
            left_field.draw(menu_screen)
            down_field.draw(menu_screen)
            up_field.draw(menu_screen)
            shoot_field.draw(menu_screen)
            base_field.draw(menu_screen)
            turn_end_field.draw(menu_screen)

            menu_screen.blit(pl_n_text, pl_n_text_pos)
            if pl_n > 1:
                menu_screen.blit(arrow_left, (0, CONFIG['RESOLUTION'][1] - arrow_left.get_size()[1] -
                                              arrow_right.get_size()[1]))
            menu_screen.blit(arrow_right, (0, CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]))
        elif screen == 'other_settings':
            menu_screen.blit(mm_nf_render, mm_nf_pos)
            menu_screen.blit(s2_qf_render, contr_qf_pos)

            if cnfg_sheet == 1:
                CONFIG['MUSIC_VOLUME'] = music_slider.update(mouse_pos)
                CONFIG['MUSIC_ON'] = music_switcher.update()
                pg_mixer_music_set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))

                fullscr_on = fullscreen_switcher.update()
                res_wid_field.update(res[0], BLACK)
                res_hei_field.update(res[1], BLACK)

                music_slider.draw(menu_screen)
                music_switcher.draw(menu_screen)
                fullscreen_switcher.draw(menu_screen)
                res_hei_field.draw(menu_screen)
                res_wid_field.draw(menu_screen)

            elif cnfg_sheet == 2:
                CONFIG['SOUNDS_VOLUME'] = sounds_slider.update(mouse_pos)
                CONFIG['SOUNDS_ON'] = sounds_switcher.update()
                base_oz_field.update(CONFIG['BASE_HEALTH'], BLACK)
                block_oz_field.update(CONFIG['BLOCK_HEALTH'], BLACK)
                money_pl_field.update(CONFIG['START_PLAYER_MONEY'], BLACK)

                sounds_slider.draw(menu_screen)
                sounds_switcher.draw(menu_screen)
                base_oz_field.draw(menu_screen)
                block_oz_field.draw(menu_screen)
                money_pl_field.draw(menu_screen)

            elif cnfg_sheet == 3:
                money_mine_field.update(CONFIG['START_MINE_MONEY'], BLACK)
                money_mine_from_field.update(CONFIG['MINE_MONEY_PER_TURN_FROM'], BLACK)
                money_mine_to_field.update(CONFIG['MINE_MONEY_PER_TURN_TO'], BLACK)
                money_pl_from_field.update(CONFIG['PLAYER_MONEY_PER_TURN_FROM'], BLACK)
                money_pl_to_field.update(CONFIG['PLAYER_MONEY_PER_TURN_TO'], BLACK)

                money_mine_field.draw(menu_screen)
                money_mine_from_field.draw(menu_screen)
                money_mine_to_field.draw(menu_screen)
                money_pl_from_field.draw(menu_screen)
                money_pl_to_field.draw(menu_screen)

            elif cnfg_sheet == 4:
                fps_limit_field.update(CONFIG['FPS_LIMIT'], BLACK)
                CONFIG['CAMERA_SPEED'] = cam_spd_slider.update(mouse_pos)
                CONFIG['TANKS_SPEED'] = tank_spd_slider.update(mouse_pos)
                CONFIG['BULLETS_SPEED'] = bul_spd_slider.update(mouse_pos)
                CONFIG['INFORMATION_LINE_SPEED'] = inf_l_spd_slider.update(mouse_pos)

                fps_limit_field.draw(menu_screen)
                cam_spd_slider.draw(menu_screen)
                tank_spd_slider.draw(menu_screen)
                bul_spd_slider.draw(menu_screen)
                inf_l_spd_slider.draw(menu_screen)

            elif cnfg_sheet == 5:
                CONFIG['SKILLS_LINE_SPEED'] = skl_l_spd_slider.update(mouse_pos)
                CONFIG['MINI_MENU_SPEED'] = mini_mn_spd_slider.update(mouse_pos)
                CONFIG['MENU_ANIM_SPEED'] = mn_anim_spd_slider.update(mouse_pos)

                skl_l_spd_slider.draw(menu_screen)
                mini_mn_spd_slider.draw(menu_screen)
                mn_anim_spd_slider.draw(menu_screen)

            menu_screen.blit(umolch_render, (pl_n_text_pos[0] - int(0.00781 * CONFIG['RESOLUTION'][0]),
                                             pl_n_text_pos[1]))

            if cnfg_sheet > 1:
                menu_screen.blit(arrow_left, (0, CONFIG['RESOLUTION'][1] - arrow_left.get_size()[1] -
                                              arrow_right.get_size()[1]))
            if cnfg_sheet < 5:
                menu_screen.blit(arrow_right, (0, CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]))

        window.blit(menu_screen, (0, 0))
        pg_display_flip()

    menu_del_objs()
    return False, None, window


def loading_screen_init():
    global load_scr

    load_scr = load_img('pics/loading_screen.png', CONFIG['RESOLUTION'])


def loading_screen(window):
    window.blit(load_scr, (0, 0))
    pg_display_flip()


def win_screen_init(window):
    global win_screen

    loading_screen(window)

    # Создание анимации окна при победе
    win_screen = []
    x = 1
    while True:
        try:
            win_screen.append(load_img('pics/end_game_screen/' + str(x) + '.png', CONFIG['RESOLUTION'],
                                       raise_error=True))
        except pg_error:
            if x == 1:
                win_screen.append(load_img('none', CONFIG['RESOLUTION']))
            break
        else:
            x += 1


def win_screen_func(window, clock):
    win_screen_init(window)
    global win_screen

    cl = time_process_time()
    x = FPSForPics(10, len(win_screen))
    font = pg_font_SysFont('Impact', 55)
    text = font.render('Этот бой был долгим, но вы сражались достойно!', 1, WHITE)
    text = pg_transform_scale(text, (int(text.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                     int(text.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
    txt_pos = (CONFIG['RESOLUTION'][0] // 2 - text.get_size()[0] // 2, int(0.03472 * CONFIG['RESOLUTION'][1]))
    while time_process_time() - 5 <= cl:
        clock.tick(CONFIG['FPS_LIMIT'])
        window.blit(win_screen[x.frame(time_process_time())], (0, 0))
        window.blit(text, txt_pos)
        pg_display_flip()

    while True:
        for event in pg_event_get():
            if event.type == QUIT:
                raise SystemExit
            if event.type == KEYDOWN:
                del win_screen
                return main_menu(False, window, clock)
        clock.tick(CONFIG['FPS_LIMIT'])
        window.blit(win_screen[x.frame(time_process_time())], (0, 0))
        window.blit(text, txt_pos)
        pg_display_flip()


from Level_editor import editor


if __name__ == '__main__':
    from pygame import init as in1
    from pygame.time import Clock
    from pygame.display import set_mode
    from pygame.font import init as in2
    from game_obj import init_objs_png
    wind = set_mode(CONFIG['RESOLUTION'])
    in1()
    in2()
    init_objs_png()
    loading_screen_init()
    menu_init()
    main_menu(False, wind, Clock())
    win_screen_func(wind, Clock())
