# coding: utf-8

from os import \
    listdir as os_listdir
from re import \
    findall as re_findall
from random import choice
from pygame import \
    Surface as pg_Surface
from pygame import KEYDOWN, \
    MOUSEMOTION, MOUSEBUTTONDOWN, \
    QUIT
from pygame.mixer import \
    Sound as pg_mixer_Sound, \
    Channel as pg_mixer_Channel
from pygame.transform import \
    scale as pg_transform_scale, \
    rotate as pg_transform_rotate
from pygame.mouse import \
    get_pos as pg_mouse_get_pos
from pygame.event import \
    get as pg_event_get
from pygame.display import \
    flip as pg_display_flip
from pygame.font import \
    SysFont as pg_font_SysFont
from game_obj import Tank, \
    load_img, objs_crossed
from constants import BLACK
from config import CONFIG


def base_init():
    global dir_, tmp_height, tmp_width, \
        details, back_screen, base_main_screen, \
        body_base_screen, track_base_screen, \
        gun_base_screen, back_arrow, arrow_left, \
        arrow_right

    dir_ = 'pics/tank_components/'
    tmp_width = int(0.125 * CONFIG['RESOLUTION'][0])
    tmp_height = int(0.31944 * CONFIG['RESOLUTION'][1])

    back_screen = pg_Surface(CONFIG['RESOLUTION'])
    base_main_screen = load_img('pics/skills_menu.png', CONFIG['RESOLUTION'])

    ch_scr = load_img('pics/misc/details_choose_screen.png', CONFIG['RESOLUTION'])
    body_base_screen = [ch_scr.copy()]
    track_base_screen = [ch_scr.copy()]
    gun_base_screen = [ch_scr.copy()]

    details = {'body': [[[[] for _ in range(int(0.00391 * CONFIG['RESOLUTION'][0]), CONFIG['RESOLUTION'][0], tmp_width)]
                        for _ in range(int(0.01389 * CONFIG['RESOLUTION'][1]), CONFIG['RESOLUTION'][1], tmp_height)]],
               'track': [[[[] for _ in range(int(0.00391 * CONFIG['RESOLUTION'][0]), CONFIG['RESOLUTION'][0], tmp_width)]
                         for _ in range(int(0.01389 * CONFIG['RESOLUTION'][1]), CONFIG['RESOLUTION'][1], tmp_height)]],
               'gun': [[[[] for _ in range(int(0.00391 * CONFIG['RESOLUTION'][0]), CONFIG['RESOLUTION'][0], tmp_width)]
                       for _ in range(int(0.01389 * CONFIG['RESOLUTION'][1]), CONFIG['RESOLUTION'][1], tmp_height)]]}

    for detail in details.keys():
        sheet = 0
        if detail == 'body':
            scr = body_base_screen
        elif detail == 'track':
            scr = track_base_screen
        else:
            scr = gun_base_screen
        x = int(0.00391 * CONFIG['RESOLUTION'][0])
        y = int(0.01389 * CONFIG['RESOLUTION'][1])
        row = 0
        col = 0
        font = pg_font_SysFont('Impact', 10)

        rus_for_params = {'cost': 'Цена', 'tank_health': 'ОБ', 'tank_speed': 'ОС', 'bullet_damage': 'ОУ'}
        for detail_name in os_listdir(dir_ + detail):
            details[detail][sheet][row][col] = [detail_name, {}]
            with open(dir_ + detail + '/' + detail_name + '/params.txt') as f:
                for param in f:
                    param = param.strip().split()
                    details[detail][sheet][row][col][1][param[0]] = int(param[1])
            detail_img = load_img(dir_ + detail + '/' + detail_name + '/' + detail_name + '_anim0.png',
                                  (int(0.11719 * CONFIG['RESOLUTION'][0]), int(0.20833 * CONFIG['RESOLUTION'][1])))
            detail_img = pg_transform_scale(detail_img,
                                            (int(0.11719 * CONFIG['RESOLUTION'][0]),
                                             int(0.20833 * CONFIG['RESOLUTION'][1])))
            scr[sheet].blit(detail_img, (x, y))
            text = font.render(' '.join([rus_for_params[str(name)] + ' = ' + str(param) + ';'
                                         for name, param in details[detail][sheet][row][col][1].items()]),
                               1, BLACK)
            text = pg_transform_scale(text,
                                      (int(text.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                      int(text.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
            scr[sheet].blit(text, (x, y + int(0.22222 * CONFIG['RESOLUTION'][1])))

            x += tmp_width
            col += 1
            if x  + int(0.11719 * CONFIG['RESOLUTION'][0]) >= CONFIG['RESOLUTION'][0]:
                x = int(0.00391 * CONFIG['RESOLUTION'][0])
                col = 0
                y += tmp_height
                row += 1
                if y + int(0.20833 * CONFIG['RESOLUTION'][1]) >= CONFIG['RESOLUTION'][1]:
                    y = int(0.01389 * CONFIG['RESOLUTION'][1])
                    row = 0
                    sheet += 1
                    scr.append(ch_scr.copy())
                    details[detail].append([[[] for _ in range(int(0.00391 * CONFIG['RESOLUTION'][0]),
                                                               CONFIG['RESOLUTION'][0], tmp_width)]
                                            for _ in range(int(0.01389 * CONFIG['RESOLUTION'][1]),
                                                           CONFIG['RESOLUTION'][1], tmp_height)])

        back_arrow = load_img('pics/misc/circle_arrow.png', (int(0.03906 * CONFIG['RESOLUTION'][0]),
                                                             int(0.06944 * CONFIG['RESOLUTION'][1])))
        arrow_left = load_img('pics/misc/arrow.png',
                              (int(0.03906 * CONFIG['RESOLUTION'][0]),
                               int(0.06944 * CONFIG['RESOLUTION'][1])))
        arrow_right = pg_transform_rotate(arrow_left, 180)


def base_delete_objs():
    global dir_, tmp_height, tmp_width, \
        details, back_screen, base_main_screen, \
        body_base_screen, track_base_screen, \
        gun_base_screen, back_arrow

    del dir_, tmp_height, tmp_width, \
        details, back_screen, base_main_screen, \
        body_base_screen, track_base_screen, \
        gun_base_screen, back_arrow


def open_base(player, window, clock):
    sheet = 0
    final_details = {'body': ['body0', {'tank_health': 50, 'cost': 100}],
                     'gun': ['gun0', {'bullet_damage': 25, 'cost': 100}],
                     'track': ['track0', {'tank_speed': 1, 'cost': 100}]}
    params = {'cost': 0, 'bullet_damage': 0, 'tank_health': 0, 'tank_speed': 0}

    track_image = load_img(dir_ + 'track/' + final_details['track'][0] +
                           '/' + final_details['track'][0] + '_anim0.png')
    gun_image = load_img(dir_ + 'gun/' + final_details['gun'][0] +
                         '/' + final_details['gun'][0] + '_anim0.png')
    body_image = load_img(dir_ + 'body/' + final_details['body'][0] +
                          '/' + final_details['body'][0] + '_anim0.png')

    for param in params.keys():
        for detail in final_details.values():
            detail = detail[1]
            try:
                params[param] += detail[param]
            except KeyError:
                pass

    segoe_font30 = pg_font_SysFont('Segoe Script', 30)

    cost_text = segoe_font30.render(str(params['cost']), 1, BLACK)
    tank_health_text = segoe_font30.render(str(params['tank_health']), 1, BLACK)
    bullet_damage_text = segoe_font30.render(str(params['bullet_damage']), 1, BLACK)
    tank_speed_text = segoe_font30.render(str(params['tank_speed']), 1, BLACK)
    player_money_text = segoe_font30.render(str(player.money), 1, BLACK)

    cost_text = pg_transform_scale(cost_text,
                                   (int(cost_text.get_size()[0] /
                                        1280 * CONFIG['RESOLUTION'][0]),
                                    int(cost_text.get_size()[1] /
                                        720 * CONFIG['RESOLUTION'][1])))
    tank_health_text = pg_transform_scale(tank_health_text,
                                          (int(tank_health_text.get_size()[0] /
                                               1280 * CONFIG['RESOLUTION'][0]),
                                           int(tank_health_text.get_size()[1] /
                                               720 * CONFIG['RESOLUTION'][1])))
    bullet_damage_text = pg_transform_scale(bullet_damage_text,
                                            (int(bullet_damage_text.get_size()[0] /
                                                 1280 * CONFIG['RESOLUTION'][0]),
                                             int(bullet_damage_text.get_size()[1] /
                                                 720 * CONFIG['RESOLUTION'][1])))
    tank_speed_text = pg_transform_scale(tank_speed_text,
                                         (int(tank_speed_text.get_size()[0] /
                                              1280 * CONFIG['RESOLUTION'][0]),
                                          int(tank_speed_text.get_size()[1] /
                                              720 * CONFIG['RESOLUTION'][1])))
    player_money_text = pg_transform_scale(player_money_text,
                                         (int(player_money_text.get_size()[0] /
                                              1280 * CONFIG['RESOLUTION'][0]),
                                          int(player_money_text.get_size()[1] /
                                              720 * CONFIG['RESOLUTION'][1])))

    screen = 'main_base'
    mouse_pos = (0, 0)
    sounds = ['music/morse_get.wav', 'music/morse_send.wav']
    channel = pg_mixer_Channel(0)
    sound = pg_mixer_Sound(choice(sounds))
    sound.set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))
    channel.play(sound)
    back_music = pg_mixer_Sound('music/base_menu_music.wav')
    back_music.play(-1)
    back_music.set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))
    while True:
        for event in pg_event_get():
            if event.type == QUIT:
                raise SystemExit
            if event.type == MOUSEMOTION:
                mouse_pos = pg_mouse_get_pos()
            if event.type == MOUSEBUTTONDOWN:
                if screen == 'main_base':
                    if objs_crossed(mouse_pos, (1, 1),
                                    (int(0.04297 * CONFIG['RESOLUTION'][0]),
                                     int(0.10139 * CONFIG['RESOLUTION'][1])),
                                    (int(0.09219 * CONFIG['RESOLUTION'][0]),
                                     int(0.16389 * CONFIG['RESOLUTION'][1]))):
                        screen = 'track'
                        sheet = 0
                    elif objs_crossed(mouse_pos, (1, 1),
                                      (int(0.77422 * CONFIG['RESOLUTION'][0]),
                                       int(0.58333 * CONFIG['RESOLUTION'][1])),
                                      (int(0.09219 * CONFIG['RESOLUTION'][0]),
                                       int(0.16389 * CONFIG['RESOLUTION'][1]))):
                        screen = 'body'
                        sheet = 0
                    elif objs_crossed(mouse_pos, (1, 1),
                                      (int(0.78594 * CONFIG['RESOLUTION'][0]),
                                       int(0.10556 * CONFIG['RESOLUTION'][1])),
                                      (int(0.09219 * CONFIG['RESOLUTION'][0]),
                                       int(0.16389 * CONFIG['RESOLUTION'][1]))):
                        screen = 'gun'
                        sheet = 0
                    elif objs_crossed(mouse_pos, (1, 1),
                                      (int(0.37969 * CONFIG['RESOLUTION'][0]),
                                       int(0.78333 * CONFIG['RESOLUTION'][1])),
                                      (int(0.19687 * CONFIG['RESOLUTION'][0]),
                                       int(0.06111 * CONFIG['RESOLUTION'][1]))):
                        sound.stop()
                        channel.stop()
                        back_music.stop()
                        if params['cost'] > player.money:
                            print('not enough money')  # todo print
                            continue
                        elif params['tank_speed'] <= 0:
                            print('negative speed')  # todo print
                            continue
                        else:
                            player.money -= params['cost']
                        final = {'track': {}, 'gun': {}, 'body': {}, 'bullet': {}}
                        pattern = r'([a-zA-Z\d]*?_anim(\d*?)\.png)'

                        for detail in ('track', 'gun', 'body'):
                            last_details = os_listdir(dir_ + detail + '/' + final_details[detail][0])
                            if 'bullet' in last_details:
                                bullets_lst = os_listdir(dir_ + detail + '/' + final_details[detail][0] + '/bullet')
                                for det in re_findall(pattern, ' '.join(bullets_lst)):
                                    final['bullet'][int(det[1])] = det[0]
                                final['bullet'] = [dir_ + detail + '/' + final_details[detail][0] + '/' + 'bullet/' +
                                                   x[1] for x in sorted(final['bullet'].items())]
                            last_details = re_findall(pattern, ' '.join(last_details))
                            for det in last_details:
                                final[detail][int(det[1])] = det[0]
                            final[detail] = [dir_ + detail + '/' + final_details[detail][0] + '/' +
                                             x[1] for x in sorted(final[detail].items())]

                        return Tank(player,
                                    params['tank_speed'],
                                    params['tank_health'],
                                    params['bullet_damage'],
                                    final['bullet'],
                                    [final['track'], final['gun'], final['body']])

                    elif objs_crossed(mouse_pos, (1, 1),
                                      (0, CONFIG['RESOLUTION'][1] - back_arrow.get_size()[1]), back_arrow.get_size()):
                        sound.stop()
                        channel.stop()
                        back_music.stop()
                        return

                else:
                    if mouse_pos[0] % tmp_width < int(0.00781 * CONFIG['RESOLUTION'][0]) or \
                                            mouse_pos[1] % tmp_height < int(0.01389 * CONFIG['RESOLUTION'][1]):
                        continue
                    col = mouse_pos[0] // tmp_width
                    row = mouse_pos[1] // tmp_height
                    if details[screen][sheet][row][col]:
                        final_details[screen] = details[screen][sheet][row][col]

                        params = {'cost': 0, 'bullet_damage': 0, 'tank_health': 0, 'tank_speed': 0}
                        for param in params.keys():
                            for detail in final_details.values():
                                detail = detail[1]
                                try:
                                    params[param] += detail[param]
                                except KeyError:
                                    pass

                        cost_text = segoe_font30.render(str(params['cost']), 1, BLACK)
                        tank_health_text = segoe_font30.render(str(params['tank_health']), 1, BLACK)
                        bullet_damage_text = segoe_font30.render(str(params['bullet_damage']), 1, BLACK)
                        tank_speed_text = segoe_font30.render(str(params['tank_speed']), 1, BLACK)

                        cost_text = pg_transform_scale(cost_text,
                                                       (int(cost_text.get_size()[0] /
                                                           1280 * CONFIG['RESOLUTION'][0]),
                                                       int(cost_text.get_size()[1] /
                                                           720 * CONFIG['RESOLUTION'][1])))
                        tank_health_text = pg_transform_scale(tank_health_text,
                                                              (int(tank_health_text.get_size()[0] /
                                                                  1280 * CONFIG['RESOLUTION'][0]),
                                                              int(tank_health_text.get_size()[1] /
                                                                  720 * CONFIG['RESOLUTION'][1])))
                        bullet_damage_text = pg_transform_scale(bullet_damage_text,
                                                                (int(bullet_damage_text.get_size()[0] /
                                                                    1280 * CONFIG['RESOLUTION'][0]),
                                                                int(bullet_damage_text.get_size()[1] /
                                                                    720 * CONFIG['RESOLUTION'][1])))
                        tank_speed_text = pg_transform_scale(tank_speed_text,
                                                             (int(tank_speed_text.get_size()[0] /
                                                                 1280 * CONFIG['RESOLUTION'][0]),
                                                             int(tank_speed_text.get_size()[1] /
                                                                 720 * CONFIG['RESOLUTION'][1])))

                        screen = 'main_base'

                        track_image = load_img(dir_ + 'track/' + final_details['track'][0] +
                                               '/' + final_details['track'][0] + '_anim0.png')
                        gun_image = load_img(dir_ + 'gun/' + final_details['gun'][0] +
                                             '/' + final_details['gun'][0] + '_anim0.png')
                        body_image = load_img(dir_ + 'body/' + final_details['body'][0] +
                                              '/' + final_details['body'][0] + '_anim0.png')

                    elif objs_crossed(mouse_pos, (1, 1),
                                      (0, CONFIG['RESOLUTION'][1] - arrow_left.get_size()[1]),
                                      arrow_left.get_size()) and sheet > 0:
                        sheet -= 1
                    elif objs_crossed(mouse_pos, (1, 1), (arrow_left.get_size()[0],
                                                          CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]),
                                      arrow_right.get_size()) and sheet < len(details[screen]) - 1:
                        sheet += 1

            if event.type == KEYDOWN:
                # if event.key == K_ESCAPE:
                pass

        clock.tick(CONFIG['FPS_LIMIT'])

        if not channel.get_busy():
            sound = pg_mixer_Sound(choice(sounds))
            sound.set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))
            channel.play(sound)

        back_screen.fill(BLACK)

        if screen == 'main_base':
            # Обновление фона
            back_screen.blit(base_main_screen, (0, 0))

            # Обновление частей танка
            back_screen.blit(track_image, (int(0.45859 * CONFIG['RESOLUTION'][0]),
                                           int(0.59306 * CONFIG['RESOLUTION'][1])))
            back_screen.blit(gun_image, (int(0.45859 * CONFIG['RESOLUTION'][0]),
                                         int(0.59306 * CONFIG['RESOLUTION'][1])))
            back_screen.blit(body_image, (int(0.45859 * CONFIG['RESOLUTION'][0]),
                                          int(0.59306 * CONFIG['RESOLUTION'][1])))
            back_screen.blit(track_image, (int(0.06953 * CONFIG['RESOLUTION'][0]),
                                           int(0.14861 * CONFIG['RESOLUTION'][1])))
            back_screen.blit(gun_image, (int(0.8125 * CONFIG['RESOLUTION'][0]),
                                         int(0.15278 * CONFIG['RESOLUTION'][1])))
            back_screen.blit(body_image, (int(0.80078 * CONFIG['RESOLUTION'][0]),
                                          int(0.63056 * CONFIG['RESOLUTION'][1])))

            # Обновление текста
            back_screen.blit(cost_text, (int(0.49453 * CONFIG['RESOLUTION'][0]),
                                         int(0.41111 * CONFIG['RESOLUTION'][1])))
            back_screen.blit(tank_health_text, (int(0.49453 * CONFIG['RESOLUTION'][0]),
                                                int(0.46111 * CONFIG['RESOLUTION'][1])))
            back_screen.blit(tank_speed_text, (int(0.49453 * CONFIG['RESOLUTION'][0]),
                                               int(0.36111 * CONFIG['RESOLUTION'][1])))
            back_screen.blit(bullet_damage_text, (int(0.49453 * CONFIG['RESOLUTION'][0]),
                                                  int(0.31111 * CONFIG['RESOLUTION'][1])))
            back_screen.blit(player_money_text, (int(0.49453 * CONFIG['RESOLUTION'][0]),
                                                 int(0.26111 * CONFIG['RESOLUTION'][1])))

            back_screen.blit(back_arrow, (0, CONFIG['RESOLUTION'][1] - back_arrow.get_size()[1]))

        elif screen == 'track':
            back_screen.blit(track_base_screen[sheet], (0, 0))
            if sheet > 0:
                back_screen.blit(arrow_left, (0, CONFIG['RESOLUTION'][1] - arrow_left.get_size()[1]))
            if sheet < len(details[screen]) - 1:
                back_screen.blit(arrow_right, (arrow_left.get_size()[0],
                                               CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]))

        elif screen == 'gun':
            back_screen.blit(gun_base_screen[sheet], (0, 0))
            if sheet > 0:
                back_screen.blit(arrow_left, (0, CONFIG['RESOLUTION'][1] - arrow_left.get_size()[1]))
            if sheet < len(details[screen]) - 1:
                back_screen.blit(arrow_right, (arrow_left.get_size()[0],
                                               CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]))

        elif screen == 'body':
            back_screen.blit(body_base_screen[sheet], (0, 0))
            if sheet > 0:
                back_screen.blit(arrow_left, (0, CONFIG['RESOLUTION'][1] - arrow_left.get_size()[1]))
            if sheet < len(details[screen]) - 1:
                back_screen.blit(arrow_right, (arrow_left.get_size()[0],
                                               CONFIG['RESOLUTION'][1] - arrow_right.get_size()[1]))

        window.blit(back_screen, (0, 0))
        pg_display_flip()


# Тест меню базы
if __name__ == '__main__':
    from pygame.display import set_mode
    from game_obj import Player
    from pygame.mixer import init as in1
    test_window = set_mode(CONFIG['RESOLUTION'])
    test_player = Player()
    base_init()
    in1()
    open_base(test_player, test_window)
