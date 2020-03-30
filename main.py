# coding: utf-8

""" todo list
акт скиллы:
пушкоблок
лазер
авиаудар

туман войны
активные скиллы
лазер
выбор кнопки меню на клавишу
меню реализация выбора на кнопки клавиатуры в меню

масштабирование карты

сетевая игра

ворота
лава

нейтральные силы

другие ресурсы помимо золота (железо, нефть, резина)

уровни сложности

Сейчас:
артиллерия
зенитка
"""
try:
    from traceback import format_exc
    from random import randrange
    from time import process_time as time_process_time
    from pygame import \
        Surface as pg_Surface,\
        init as pg_init, \
        quit as pg_quit
    from pygame import KEYDOWN, \
        K_ESCAPE, K_TAB, QUIT, \
        FULLSCREEN, MOUSEMOTION, \
        MOUSEBUTTONDOWN
    from pygame.mixer_music import \
        load as pg_mixer_music_load, \
        play as pg_mixer_music_play, \
        pause as pg_mixer_music_pause, \
        unpause as pg_mixer_music_unpause, \
        set_volume as pg_mixer_music_set_volume
    from pygame.mixer import \
        init as pg_mixer_init, \
        Sound as pg_mixer_Sound
    from pygame.mouse import \
        get_pos as pg_mouse_get_pos
    from pygame.transform import \
        scale as pg_transform_scale
    from pygame.font import \
        init as pg_font_init, \
        SysFont as pg_font_SysFont, \
        quit as pg_font_quit
    from pygame.time import \
        Clock as pg_time_Clock
    from pygame.display import \
        set_mode as pg_display_set_mode, \
        set_caption as pg_display_set_caption, \
        flip as pg_display_flip
    from pygame.event import \
        get as pg_event_get
    from config import CONFIG
    from Menu import loading_screen_init, \
        loading_screen, main_menu, \
        win_screen_func
    from game_obj import init_objs_png, \
        Player, TanksError, Base, \
        Bullet, Dirt, Mine, \
        load_img, MiniMenu, \
        objs_crossed, Artillery, \
        AntiArtGun, SkillsLine, \
        BlockUnD, BlockD
    from Base_menu import \
        open_base, base_init
    from constants import BLACK, \
        WHITE, STANDARD_CONTROLS, \
        RIGHT, LEFT, DOWN, UP
except ImportError:
    with open('importLog.txt', 'w', encoding='utf-8-sig') as f:
        try:
            from traceback import format_exc
            f.write(format_exc())
        except ImportError:
            f.write("Can't import traceback module")
    exit(1)

def main():
    # Инициализация PyGame
    pg_init()
    pg_font_init()
    pg_mixer_init()

    # Создание окна
    if CONFIG['FULLSCREEN_ON']:
        window = pg_display_set_mode(CONFIG['RESOLUTION'], FULLSCREEN)
    else:
        window = pg_display_set_mode(CONFIG['RESOLUTION'])
    pg_display_set_caption('Танковые баталии')
    loading_screen_init()
    loading_screen(window)
    pg_display_flip()

    # Создание строки состояния
    information_line = pg_Surface((CONFIG['RESOLUTION'][0],
                                   int(0.05556 * CONFIG['RESOLUTION'][1])))
    inf_line_img = load_img('pics/misc/inf_line.png', (CONFIG['RESOLUTION'][0],
                                                       int(0.05556 * CONFIG['RESOLUTION'][1])))
    inf_font = pg_font_SysFont('Impact', 25)
    inf_y = -information_line.get_size()[1]

    # Небольшой подгруз файлов в оперативную память
    init_objs_png()
    red_field = load_img('pics/misc/red_field.png')
    green_field = load_img('pics/misc/green_field.png')
    base_init()
    pg_mixer_music_load('music/menu_music.mp3')
    pg_mixer_music_play(-1)
    pg_mixer_music_set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))

    # Создание меню активных умений
    skills_menu = SkillsLine()

    # Выход в меню
    game_on, level, window = main_menu(False, window, pg_time_Clock())

    " Характерные для каждого уровня значения "
    if game_on:
        screen = pg_Surface(level.size)
        pg_mixer_music_load('music/ingame_music.mp3')
        pg_mixer_music_play(-1)
        pg_mixer_music_set_volume(CONFIG['MUSIC_VOLUME']/ 1000 * int(CONFIG['MUSIC_ON']))
        all_objs_on_level = {}
        static_objs = {i: {} for i in range(1, level.player_count + 1)}
        bullets_dict = {}
        players = {}
        fire_level_covering = {}
        menus = []
        skill_todo = ()
        controls = {i: j for i, j in list(sorted(CONFIG['CONTROLS'].items()))[:level.player_count]}
        turn = randrange(1, level.player_count + 1)

        for pl_n in range(1, level.player_count + 1):
            if pl_n not in controls.keys():
                controls[pl_n] = STANDARD_CONTROLS[1]
            pl = Player(pl_n)
            players[pl_n] = pl
            pl.base_pos = level.players_base[pl_n]
        status = 0
        inf_text = inf_font.render('Ходит ' + players[turn].name + ' игрок. Его золото: '
                                   + str(players[turn].money) + '. ' + players[turn].statuses[status], 1, WHITE)
        inf_text = pg_transform_scale(inf_text,(int(inf_text.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                                int(inf_text.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
        cl = pg_time_Clock()
        base_blocked = True
        updating = False
        inform = False
        mouse_pos = pg_mouse_get_pos()
        camera_x = CONFIG['RESOLUTION'][0] // 2 - level.size[0] // 2
        camera_y = CONFIG['RESOLUTION'][1] // 2 - level.size[1] // 2

    ''' Цикл игры '''
    while game_on:
        " Блок проверки действий игрока "
        for event in pg_event_get():

            # Нажатие на кнопку клавиатуры
            if event.type == KEYDOWN:
                # Нажатие на клавишу Escape
                if event.key == K_ESCAPE:
                    # Открытие меню
                    pg_mixer_music_load('music/menu_music.mp3')
                    pg_mixer_music_play(-1)
                    pg_mixer_music_set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))
                    game_on, new_lvl, window = main_menu(True, window, cl)
                    pg_mixer_music_load('music/ingame_music.mp3')
                    pg_mixer_music_play(-1)
                    pg_mixer_music_set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))
                    # Если начата новая игра
                    if new_lvl is not None:
                        level = new_lvl
                        screen = pg_Surface(level.size)

                        all_objs_on_level = {}
                        static_objs = {i: {} for i in range(1, level.player_count + 1)}
                        bullets_dict = {}
                        players = {}
                        fire_level_covering = {}
                        menus = []
                        skill_todo = ()
                        controls = {i: j for i, j in list(sorted(CONFIG['CONTROLS'].items()))[:level.player_count]}
                        turn = randrange(1, level.player_count + 1)
                        for pl_n in range(1, level.player_count + 1):
                            if pl_n not in controls.keys():
                                controls[pl_n] = STANDARD_CONTROLS[1]
                            pl = Player(pl_n)
                            players[pl_n] = pl
                            pl.base_pos = level.players_base[pl_n]
                        status = 0
                        inf_text = inf_font.render('Ходит ' + players[turn].name + ' игрок. Его золото: '
                                                   + str(players[turn].money) + '. '
                                                   + players[turn].statuses[status], 1, WHITE)
                        inf_text = pg_transform_scale(inf_text,(int(inf_text.get_size()[0] / 1280 *
                                                                    CONFIG['RESOLUTION'][0]),
                                                                int(inf_text.get_size()[1] / 720 *
                                                                    CONFIG['RESOLUTION'][1])))
                        mouse_pos = pg_mouse_get_pos()
                        inf_y = -information_line.get_size()[1]
                        skills_menu = SkillsLine()
                        updating = False
                        camera_x = CONFIG['RESOLUTION'][0] // 2 - level.size[0] // 2
                        camera_y = CONFIG['RESOLUTION'][1] // 2 - level.size[1] // 2
                        del new_lvl

                # Если нажата клавиша TAB
                if event.key == K_TAB:
                    # Инверсия логической переменной inform
                    inform = not inform

                # Если игрок управляет танками
                if not updating:
                    for k_name, key in controls[turn].items():
                        if event.key == key:
                            try:
                                players[turn].action = k_name
                            except KeyError:
                                del controls[turn]
                                break

            # Передвижение курсора мыши
            if event.type == MOUSEMOTION:
                mouse_pos = pg_mouse_get_pos()

            # Нажатие на кнопку мыши
            if event.type == MOUSEBUTTONDOWN:

                # Обработка нажатия на кнопки активных умений
                skl_upd = skills_menu.update(mouse_pos=(mouse_pos[0] - skills_menu.x, mouse_pos[1]))
                if skl_upd is not None:
                    skill_todo = skl_upd
                    if 'Fire!' in skill_todo:
                        if fire_level_covering:
                            continue
                        for static_obj in static_objs[turn].values():
                            if type(static_obj) == Artillery:
                                for block in static_obj.action_positions:
                                    if block in fire_level_covering.keys():
                                        fire_level_covering[block].append(red_field.copy())
                                    else:
                                        fire_level_covering[block] = [red_field.copy()]
                            elif type(static_obj) == AntiArtGun:
                                for block in static_obj.action_positions:
                                    if block in fire_level_covering.keys():
                                        fire_level_covering[block].append(green_field.copy())
                                    else:
                                        fire_level_covering[block] = [green_field.copy()]

                        skill_todo = ()
                elif skill_todo:
                    if objs_crossed(mouse_pos, (1, 1), (skills_menu.x, skills_menu.y), skills_menu.image.get_size()):
                        skill_todo = ()
                    else:
                        art_pos = (mouse_pos[0] - camera_x,
                                   mouse_pos[1] - camera_y)
                        art_pos = (art_pos[0] - art_pos[0] % CONFIG['OBJ_WIDTH'],
                                   art_pos[1] - art_pos[1] % CONFIG['OBJ_HEIGHT'])
                        if type(level.objs_place[art_pos]) == BlockUnD:
                            if skill_todo[1] == 'Artillery' and players[turn].money >= 500:
                                static_objs[turn][art_pos] = Artillery(level.size, art_pos[0], art_pos[1], 4,
                                                                       skill_todo[0], 200, 50)  # todo health and dmg and cost
                                players[turn].money -= 500
                            elif skill_todo[1] == 'AntiArtGun' and players[turn].money >= 500:
                                static_objs[turn][art_pos] = AntiArtGun(level.size, art_pos[0], art_pos[1], 4,
                                                                        skill_todo[0], 200, 1)  # todo health and dmg and cost
                                players[turn].money -= 500
                        skill_todo = ()
                else:
                    art_pos = (mouse_pos[0] - camera_x,
                               mouse_pos[1] - camera_y)
                    art_pos = (art_pos[0] - art_pos[0] % CONFIG['OBJ_WIDTH'],
                               art_pos[1] - art_pos[1] % CONFIG['OBJ_HEIGHT'])
                    if art_pos in fire_level_covering.keys():
                        dmg = 0
                        defend_power = 1
                        tmp = {}
                        for objs in static_objs.values():
                            for pos, obj in objs.items():
                                tmp[pos] = obj
                                if type(obj) == AntiArtGun and art_pos in obj.action_positions:
                                    defend_power += obj.defend_power
                        for art in static_objs[turn].values():
                            if type(art) == Artillery and art_pos in art.action_positions:
                                dmg += art.damage
                        if art_pos in all_objs_on_level.keys():
                            all_objs_on_level[art_pos].health -= dmg // defend_power
                        elif art_pos in tmp.keys():
                            tmp[pos].health -= dmg // defend_power
                            if tmp[pos].health <= 0:
                                for ind in range(len(static_objs.values())):
                                    if pos in list(static_objs.values())[ind].keys():
                                        del list(static_objs.values())[ind][pos]
                                        break
                                del tmp[pos]
                        else:
                            if type(level.objs_place[art_pos]) == Base or type(level.objs_place[art_pos]) == BlockD:
                                level.objs_place[art_pos].health -= dmg // defend_power
                        del tmp
                    fire_level_covering = {}


            # Нажатие на "крестик"
            if event.type == QUIT:
                game_on = False

        # Измеряем fps и устанавливаем его лимит
        cl.tick(CONFIG['FPS_LIMIT'])
        fps_now = cl.get_fps()

        globaltime = time_process_time()

        " Блок обновления событий "

        # Обновление пуль
        bullets_list = list(bullets_dict.items())
        for obj_pos, obj in bullets_list:
            try:
                bullets_dict[obj_pos]
            except KeyError:
                continue
            pos = (obj_pos[0] + obj.direction[0] * CONFIG['OBJ_WIDTH'],
                   obj_pos[1] + obj.direction[1] * CONFIG['OBJ_HEIGHT'])
            try:
                bullets_dict[pos]
            except KeyError:
                pass
            else:
                if pos in bullets_list:
                    bullets_list.append((obj_pos, obj))
                    continue
            upd = obj.update(all_objs_on_level, level.objs_place)
            del bullets_dict[obj_pos]
            if upd:
                try:
                    # Если попал в танк
                    all_objs_on_level[obj.pos].health -= obj.damage
                except KeyError:
                    # Если попал в блок
                    level.objs_place[obj.pos].health -= obj.damage
                    continue
                if all_objs_on_level[obj.pos].update(None) is None:
                    # Если танк взорвали
                    for pl_n, pl in players.items():
                        if obj.pos in pl.tanks_pos.keys():
                            break
                    else:
                        # Если у танка нет хозяина
                        raise TanksError('unknown tank died')
                    del pl.tanks_pos[obj.pos]
                    del level.ingame_objs[pl_n][obj.pos]
                    del all_objs_on_level[obj.pos]
                del obj
            elif upd is None:
                del obj
            else:
                bullets_dict[obj.pos] = obj

        # Если базу игрока разрушили
        for pl_n, pl in list(players.items()):
            if type(level.objs_place[pl.base_pos]) != Base:
                sound = pg_mixer_Sound('music/explosion.wav').play()
                sound.set_volume(CONFIG['SOUNDS_VOLUME'] / 1000 * int(CONFIG['SOUNDS_ON']))
                del sound
                del players[pl_n]
                for pos in level.ingame_objs[pl_n]:
                    del all_objs_on_level[pos]
                del level.ingame_objs[pl_n]

        new_turn = False
        # Проверка существования игрока
        while True:
            try:
                players[turn]
            except KeyError:
                turn += 1
                if turn > level.player_count and not new_turn:
                    new_turn = True
                    turn = 1
                    # Обовление шахт
                    for block in level.objs_place.values():
                        if type(block) == Mine:
                            block.update()
            else:
                break

        pl = players[turn]
        pl_n = pl.number
        # Если игрок ничего не делал
        if pl.action is None:
            pass

        # Если игрок закончил ход
        elif pl.action == 'turn_end' and not bullets_dict:
            pl.money += randrange(CONFIG['PLAYER_MONEY_PER_TURN_FROM'], CONFIG['PLAYER_MONEY_PER_TURN_TO'] + 1)
            turn += 1

            new_turn = False
            # Проверка существования игрока
            while True:
                try:
                    players[turn]
                except KeyError:
                    turn += 1
                    if turn > level.player_count and not new_turn:
                        new_turn = True
                        turn = 1
                        # Обовление шахт
                        for block in level.objs_place.values():
                            if type(block) == Mine:
                                block.update()
                else:
                    break

            # Обновление очков передвижения танков
            for tank in players[turn].tanks_pos.values():
                tank.pts = tank.points_bag

        # Если игрок управляет танками
        elif pl.action != 'base' and not bullets_dict:
            tmp = 0
            tanks_list = list(pl.tanks_pos.items())
            for tank_pos, tank in tanks_list:
                # Если у танка нет очков передвижения
                if tank.pts == 0:
                    continue
                # Обновляем танки
                upd = tank.update(level, 'action', tanks_list[tmp:])
                if upd:
                    # Если танк стреляет
                    if type(upd) == Bullet:
                        collide = upd.check_collide(all_objs_on_level,
                                                    level.objs_place)
                        # Если пуля сразу столкнулась с объектом
                        if collide[1]:
                            try:
                                # Если пуля попала в танк
                                all_objs_on_level[upd.pos].health -= upd.damage
                            except KeyError:
                                # Если пуля попала в блок
                                level.objs_place[upd.pos].health -= upd.damage
                        # Если путь свободен
                        elif collide[0]:
                            bullets_dict[(upd.x, upd.y)] = upd
                    else:
                        tanks_list.append((tank_pos, tank))

                else:
                    # Если танк еще существует
                    if upd is not None:
                        # Меняем позицию танка во всех словарях
                        del pl.tanks_pos[tank_pos]
                        del level.ingame_objs[pl_n][tank_pos]
                        del all_objs_on_level[tank_pos]
                        pl.tanks_pos[(tank.x, tank.y)] = tank
                        level.ingame_objs[pl_n][(tank.x, tank.y)] = tank
                        all_objs_on_level[(tank.x, tank.y)] = tank

                tmp += 1

        # Если игрок открыл меню базы
        elif pl.action == 'base':
            # Ищем свободное место вокруг базы
            for pos in (
                    (pl.base_pos[0] + CONFIG['OBJ_WIDTH'], pl.base_pos[1]),
                    (pl.base_pos[0] - CONFIG['OBJ_WIDTH'], pl.base_pos[1]),
                    (pl.base_pos[0], pl.base_pos[1] + CONFIG['OBJ_HEIGHT']),
                    (pl.base_pos[0], pl.base_pos[1] - CONFIG['OBJ_HEIGHT']),
            ):
                try:
                    # Если на позиции блок грязи
                    if type(level.objs_place[pos]) == Dirt:
                        try:
                            # Свободна ли позиция?
                            all_objs_on_level[pos]
                        except KeyError:
                            # Позиция свободна
                            base_blocked = False
                            break
                except KeyError:
                    pass
            else:
                # Если база заблокирована
                print('Player', pl_n, 'has no place near base!')  # todo print

            if not base_blocked:
                # Открываем меню базы
                pg_mixer_music_pause()
                new_tank = open_base(pl, window, cl)
                pg_mixer_music_unpause()
                # Если создан новый танк
                if new_tank is not None:
                    new_tank.x, new_tank.y = pos
                    new_tank.direction = {
                    (pl.base_pos[0] + CONFIG['OBJ_WIDTH'], pl.base_pos[1]): 'right',
                    (pl.base_pos[0] - CONFIG['OBJ_WIDTH'], pl.base_pos[1]): 'left',
                    (pl.base_pos[0], pl.base_pos[1] + CONFIG['OBJ_HEIGHT']): 'down',
                    (pl.base_pos[0], pl.base_pos[1] - CONFIG['OBJ_HEIGHT']): 'up'
                    }[pos]
                    new_tank.angle = {'right': RIGHT, 'up': UP, 'down': DOWN, 'left': LEFT}[new_tank.direction]
                    level.ingame_objs[pl_n][pos] = new_tank
                    pl.tanks_pos[pos] = new_tank
                    all_objs_on_level[pos] = new_tank
                    del new_tank

        base_blocked = True
        pl.action = None

        updating = False
        status = 0
        for tank_pos, tank in list(all_objs_on_level.items()):
            # Если танк еще в движении
            tank.update(None, 'check')
            if tank.x % CONFIG['OBJ_WIDTH'] != 0 or tank.y % CONFIG['OBJ_HEIGHT'] != 0 or tank.destruct:
                updating = True
                upd = tank.update(None)
                for player in players.values():
                    try:
                        del player.tanks_pos[tank_pos]
                    except KeyError:
                        pass
                    else:
                        del level.ingame_objs[player.number][tank_pos]
                        break
                del all_objs_on_level[tank_pos]
                # Если танк еще существует
                if upd is not None:
                    # Меняем позицию танка во всех словарях
                    pl.tanks_pos[(tank.x, tank.y)] = tank
                    level.ingame_objs[pl_n][(tank.x, tank.y)] = tank
                    all_objs_on_level[(tank.x, tank.y)] = tank

            tank.menu_opened = False
            if tank_pos in players[turn].tanks_pos.keys():
                if objs_crossed(mouse_pos, (1, 1),
                                (tank_pos[0] + camera_x, tank_pos[1] + camera_y),
                                (CONFIG['OBJ_WIDTH'], CONFIG['OBJ_HEIGHT'])):
                    if not tank.menu:
                        tank.menu_opened = True
                        tank.menu = MiniMenu({'HP': tank.health, 'MP': tank.pts, 'Dmg': tank.bullet_dmg},
                                             (mouse_pos[0] - camera_x, mouse_pos[1] - camera_y), level.size)
                        menus.append(tank.menu)
                    else:
                        tank.menu_opened = True

                if tank.pts > 0:
                    status = 1

            # Обновление МиниМеню
            try:
                if tank.menu.update(tank.menu_opened) is None:
                    menus.remove(tank.menu)
                    tank.menu = None
            except AttributeError:
                pass

        # Если игрок еще ходит
        if updating:
            status = 2

        # Если на карте осталась 1 база
        if len(list(players.keys())) == 1:
            # Открытие меню и победного окна
            pg_mixer_music_load('music/menu_music.mp3')
            pg_mixer_music_play(-1)
            pg_mixer_music_set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))
            game_on, new_lvl, window = win_screen_func(window, cl)
            # Если начата новая игра
            if new_lvl is not None:
                pg_mixer_music_load('music/ingame_music.mp3')
                pg_mixer_music_play(-1)
                pg_mixer_music_set_volume(CONFIG['MUSIC_VOLUME'] / 1000 * int(CONFIG['MUSIC_ON']))
                level = new_lvl
                screen = pg_Surface(level.size)

                all_objs_on_level = {}
                static_objs = {i: {} for i in range(1, level.player_count + 1)}
                bullets_dict = {}
                players = {}
                fire_level_covering = {}
                menus = []
                skill_todo = ()
                controls = {i: j for i, j in list(sorted(CONFIG['CONTROLS'].items()))[:level.player_count]}
                turn = randrange(1, level.player_count + 1)
                for pl_n in range(1, level.player_count + 1):
                    if pl_n not in controls.keys():
                        controls[pl_n] = STANDARD_CONTROLS[1]
                    pl = Player(pl_n)
                    players[pl_n] = pl
                    pl.base_pos = level.players_base[pl_n]
                status = 0
                inf_text = inf_font.render('Ходит ' + players[turn].name + ' игрок. Его золото: '
                                           + str(players[turn].money) + '. '
                                           + players[turn].statuses[status], 1, WHITE)
                inf_text = pg_transform_scale(inf_text,(int(inf_text.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                                        int(inf_text.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
                mouse_pos = pg_mouse_get_pos()
                inf_y = -information_line.get_size()[1]
                skills_menu = SkillsLine()
                updating = False
                camera_x = CONFIG['RESOLUTION'][0] // 2 - level.size[0] // 2
                camera_y = CONFIG['RESOLUTION'][1] // 2 - level.size[1] // 2
                del new_lvl

        # Обновление строки состояния
        skills_menu.update(inform)
        if inform:
            if inf_y + CONFIG['INFORMATION_LINE_SPEED'] < 0:
                inf_y += CONFIG['INFORMATION_LINE_SPEED']
            else:
                inf_y = 0

            if bullets_dict:
                status = 2

            inf_text = inf_font.render('Ходит ' + players[turn].name + ' игрок. Его золото: '
                                       + str(players[turn].money) + '. ' + players[turn].statuses[status], 1, WHITE)
            inf_text = pg_transform_scale(inf_text,(int(inf_text.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                                    int(inf_text.get_size()[1] / 720 * CONFIG['RESOLUTION'][1])))
        else:
            if inf_y - CONFIG['INFORMATION_LINE_SPEED'] > -information_line.get_size()[1]:
                inf_y -= CONFIG['INFORMATION_LINE_SPEED']
            else:
                inf_y = -information_line.get_size()[1]

        # Обновление камеры
        if mouse_pos[0] <= 5 and camera_x < 0:
            if camera_x <= -CONFIG['CAMERA_SPEED']:
                camera_x += CONFIG['CAMERA_SPEED']
            else:
                camera_x = 0
        elif mouse_pos[0] >= CONFIG['RESOLUTION'][0] - 5 and camera_x - CONFIG['RESOLUTION'][0] > -level.size[0]:
            if camera_x - CONFIG['RESOLUTION'][0] <= -level.size[0] + CONFIG['CAMERA_SPEED']:
                camera_x = -level.size[0] + CONFIG['RESOLUTION'][0]
            else:
                camera_x -= CONFIG['CAMERA_SPEED']

        if mouse_pos[1] <= 5 and camera_y < 0:
            if camera_y <= -CONFIG['CAMERA_SPEED']:
                camera_y += CONFIG['CAMERA_SPEED']
            else:
                camera_y = 0
        elif mouse_pos[1] >= CONFIG['RESOLUTION'][1] - 5 and \
             camera_y - CONFIG['RESOLUTION'][1] > -level.size[1]:
            if camera_y - CONFIG['RESOLUTION'][1] <= -level.size[1] + CONFIG['CAMERA_SPEED']:
                camera_y = -level.size[1] + CONFIG['RESOLUTION'][1]
            else:
                camera_y -= CONFIG['CAMERA_SPEED']

        " Блок прорисовки экрана "
        window.fill(BLACK)
        screen.fill(BLACK)
        information_line.fill(BLACK)
        updating = level.draw(screen, camera_x, camera_y, globaltime, fire_level_covering) or updating
        for obj in all_objs_on_level.values():
            obj.draw(screen, camera_x, camera_y)
        for stat_objs in static_objs.values():
            for obj in stat_objs.values():
                obj.draw(screen)
        for obj in bullets_dict.values():
            obj.draw(screen, camera_x, camera_y)
        for menu in menus:
            menu.draw(screen)
        information_line.blit(inf_line_img, (0, 0))
        information_line.blit(inf_text, (0, 0))

        if game_on:
            window.blit(screen, (camera_x, camera_y))
            skills_menu.draw(window)
            window.blit(information_line, (0, inf_y))
            pg_display_flip()

    # Выход из PyGame
    pg_font_quit()
    pg_quit()

if __name__ == '__main__':
    try:
        main()
    except:
        with open('log.txt', 'w', encoding='utf-8-sig') as f:
            f.write(format_exc())
