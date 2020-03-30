# coding: utf-8

from pygame import \
    Surface as pg_Surface
from pygame import KEYDOWN, \
    K_ESCAPE, QUIT, K_TAB, \
    MOUSEBUTTONDOWN, MOUSEMOTION, \
    MOUSEBUTTONUP
from pygame.font import \
    init as pg_font_init, \
    SysFont as pg_font_SysFont
from pygame.transform import \
    scale as pg_transform_scale, \
    rotate as pg_transform_rotate
from pygame.display import \
    flip as pg_display_flip
from pygame.mouse import \
    get_pos as pg_mouse_get_pos
from pygame.event import \
    get as pg_event_get
from game_obj import load_img, \
    BlockD, BlockUnD, \
    Dirt, Base, Mine, Water, \
    _objs as objs, Field, objs_crossed
from levels import level_dict_
from Menu import loading_screen
from config import CONFIG
from constants import BLACK
from levels_extractor import levels_writing


def init_editor():
    global _objs, blocks_menu_image, \
        blocks_pos, editor_window, \
        setting_menu_image, create_text, \
        rename_text, delete_text, exit_text, \
        load_text, game_name_text, prompt_text, \
        gn_text_pos, pr_text_pos, cr_text_pos, \
        lo_text_pos, ren_text_pos, del_text_pos, \
        ex_text_pos, cr_text_size, lo_text_size, \
        ren_text_size, del_text_size, ex_text_size, \
        set_size_text, sets_text_pos, back_text, \
        back_text_size, field_sets1, field_sets2, \
        start_create_text, sc_text_pos, sc_text_size, \
        x_field, y_field, x_space, y_space, \
        level_choose_text, lch_text_pos, \
        arrow_right, arrow_left, arrow_left_pos, \
        arrow_right_pos, set_font, naming_window, \
        rename_field, rename_field_text

    pg_font_init()

    _objs = {
        BlockUnD: '=',
        BlockD: '-',
        Dirt: 'D',
        Base: 'B',
        Mine: 'M',
        Water: 'W'
    }

    set_font = pg_font_SysFont('Impact', 48)
    big_set_font = pg_font_SysFont('Impact', 72)
    small_set_font = pg_font_SysFont('Impact', 25)

    game_name_text = big_set_font.render('Танковые баталии', 1, BLACK)
    prompt_text = small_set_font.render('Редактор уровней', 1, BLACK)
    create_text = set_font.render('Создать уровень', 1, BLACK)
    load_text = set_font.render('Загрузить уровень', 1, BLACK)
    rename_text = set_font.render('Переименовать уровень', 1, BLACK)
    delete_text = set_font.render('Удалить уровень', 1, BLACK)
    exit_text = set_font.render('Выйти', 1, BLACK)
    back_text = set_font.render('Вернуться', 1, BLACK)

    set_size_text = set_font.render('Выберите размер своего уровня', 1, BLACK)
    start_create_text = big_set_font.render('Создать уровень', 1, BLACK)

    level_choose_text = set_font.render('Выбор уровня', 1, BLACK)

    game_name_text = pg_transform_scale(game_name_text, (int(0.45703 * CONFIG['RESOLUTION'][0]),
                                                         int(0.12361 * CONFIG['RESOLUTION'][1])))
    prompt_text = pg_transform_scale(prompt_text, (int(0.15547 * CONFIG['RESOLUTION'][0]),
                                                   int(0.04444 * CONFIG['RESOLUTION'][1])))
    create_text = pg_transform_scale(create_text, (int(0.27891 * CONFIG['RESOLUTION'][0]),
                                                   int(0.08333 * CONFIG['RESOLUTION'][1])))
    load_text = pg_transform_scale(load_text, (int(0.30547 * CONFIG['RESOLUTION'][0]),
                                               int(0.08333 * CONFIG['RESOLUTION'][1])))
    rename_text = pg_transform_scale(rename_text, (int(0.40156 * CONFIG['RESOLUTION'][0]),
                                                   int(0.08333 * CONFIG['RESOLUTION'][1])))
    delete_text = pg_transform_scale(delete_text, (int(0.27891 * CONFIG['RESOLUTION'][0]),
                                                   int(0.08333 * CONFIG['RESOLUTION'][1])))
    exit_text = pg_transform_scale(exit_text, (int(0.10938 * CONFIG['RESOLUTION'][0]),
                                               int(0.08333 * CONFIG['RESOLUTION'][1])))
    back_text = pg_transform_scale(back_text, (int(0.17188 * CONFIG['RESOLUTION'][0]),
                                               int(0.08333 * CONFIG['RESOLUTION'][1])))

    set_size_text = pg_transform_scale(set_size_text, (int(0.53281 * CONFIG['RESOLUTION'][0]),
                                                       int(0.08333 * CONFIG['RESOLUTION'][1])))
    start_create_text = pg_transform_scale(start_create_text, (int(0.41563 * CONFIG['RESOLUTION'][0]),
                                                               int(0.12361 * CONFIG['RESOLUTION'][1])))

    level_choose_text = pg_transform_scale(level_choose_text, (int(0.23125 * CONFIG['RESOLUTION'][0]),
                                                               int(0.08333 * CONFIG['RESOLUTION'][1])))

    gn_text_pos = (int(0.27188 * CONFIG['RESOLUTION'][0]),
                   int(0.06944 * CONFIG['RESOLUTION'][1]))
    pr_text_pos = (int(0.42266 * CONFIG['RESOLUTION'][0]),
                   int(0.17361 * CONFIG['RESOLUTION'][1]))
    cr_text_pos = (int(0.39063 * CONFIG['RESOLUTION'][0]),
                   int(0.27778 * CONFIG['RESOLUTION'][1]))
    lo_text_pos = (int(0.39063 * CONFIG['RESOLUTION'][0]),
                   int(0.41667 * CONFIG['RESOLUTION'][1]))
    ren_text_pos = (int(0.39063 * CONFIG['RESOLUTION'][0]),
                    int(0.55556 * CONFIG['RESOLUTION'][1]))
    del_text_pos = (int(0.39063 * CONFIG['RESOLUTION'][0]),
                    int(0.69444 * CONFIG['RESOLUTION'][1]))
    ex_text_pos = (int(0.39063 * CONFIG['RESOLUTION'][0]),
                   int(0.83333 * CONFIG['RESOLUTION'][1]))

    sets_text_pos = (int(0.23359 * CONFIG['RESOLUTION'][0]),
                     int(0.27778 * CONFIG['RESOLUTION'][1]))
    sc_text_pos = (int(0.54688 * CONFIG['RESOLUTION'][0]),
                   int(0.55556 * CONFIG['RESOLUTION'][1]))

    lch_text_pos = (int(0.38438 * CONFIG['RESOLUTION'][0]),
                    int(0.20833 * CONFIG['RESOLUTION'][1]))

    cr_text_size = create_text.get_size()
    lo_text_size = load_text.get_size()
    ren_text_size = rename_text.get_size()
    del_text_size = delete_text.get_size()
    ex_text_size = exit_text.get_size()
    back_text_size = back_text.get_size()
    sc_text_size = start_create_text.get_size()

    editor_window = pg_Surface(CONFIG['RESOLUTION'])
    setting_menu_image = load_img('pics/edit_set_menu.png', CONFIG['RESOLUTION'])
    blocks_menu_image = load_img('pics/editor_blocks_menu.png', CONFIG['RESOLUTION'])
    x_space = int(0.03906 * CONFIG['RESOLUTION'][0])
    y_space = int(0.06944 * CONFIG['RESOLUTION'][1])
    x_block_space = int(0.11719 * CONFIG['RESOLUTION'][0])
    y_block_space = int(0.20833 * CONFIG['RESOLUTION'][1])
    x_field = x_block_space + x_space
    y_field = y_block_space + y_space
    x = x_space
    y = y_space
    blocks_pos = {}
    for obj in _objs.keys():
        img = obj().image
        if type(img) == list:
            img = img[0]
        blocks_menu_image.blit(pg_transform_scale(img, (x_block_space,
                                                                y_block_space)),
                               (x, y))
        blocks_pos[(x, y)] = obj
        x += x_field
        if x + x_block_space > CONFIG['RESOLUTION'][0]:
            x = x_space
            y += y_field

    f_img = load_img('pics/misc/field.png', change_size=False)
    field_sets1 = Field(f_img.copy(), set_font, (int(0.07813 * CONFIG['RESOLUTION'][0]),
                                                 int(0.06944 * CONFIG['RESOLUTION'][1])),
                        (int(0.07813 * CONFIG['RESOLUTION'][0]),
                         int(0.48611 * CONFIG['RESOLUTION'][1])), 'Ширина в блоках: ', BLACK)
    field_sets2 = Field(f_img.copy(), set_font, (int(0.07813 * CONFIG['RESOLUTION'][0]),
                                                 int(0.06944 * CONFIG['RESOLUTION'][1])),
                        (int(0.07813 * CONFIG['RESOLUTION'][0]),
                         int(0.69444 * CONFIG['RESOLUTION'][1])), 'Высота в блоках: ', BLACK)

    arrow_left = load_img('pics/misc/arrow.png')
    arrow_left = pg_transform_scale(arrow_left, (int(0.03906 * CONFIG['RESOLUTION'][0]),
                                                 int(0.06944 * CONFIG['RESOLUTION'][1])))
    arrow_right = pg_transform_rotate(arrow_left.copy(), 180)
    arrow_left_pos = (int(0.07812 * CONFIG['RESOLUTION'][0]),
                      int(0.83333 * CONFIG['RESOLUTION'][1]))
    arrow_right_pos = (int(0.11719 * CONFIG['RESOLUTION'][0]),
                       int(0.83333 * CONFIG['RESOLUTION'][1]))

    naming_window = load_img('pics/misc/OK_notOK_window.png',
                             (int(0.40625 * CONFIG['RESOLUTION'][0]),
                              int(0.41667 * CONFIG['RESOLUTION'][1])))
    rename_field_text = set_font.render('Имя уровня:', 1, BLACK)
    rename_field_text = pg_transform_scale(rename_field_text, (int(rename_field_text.get_size()[0] /
                                                                   1280 * CONFIG['RESOLUTION'][0]),
                                                               int(rename_field_text.get_size()[1] /
                                                                   720 * CONFIG['RESOLUTION'][1])))
    rename_field = Field(f_img.copy(), set_font,
                         (int(0.32812 * CONFIG['RESOLUTION'][0]),
                          int(0.08333 * CONFIG['RESOLUTION'][1])),
                         (CONFIG['RESOLUTION'][0] // 2 - int(0.32812 * CONFIG['RESOLUTION'][0]) // 2 -
                          int(0.01563 * CONFIG['RESOLUTION'][0]),
                          CONFIG['RESOLUTION'][1] // 2 - naming_window.get_size()[1] // 2 +
                          rename_field_text.get_size()[1] + int(0.05972 * CONFIG['RESOLUTION'][1])),
                         '', BLACK)


def del_editor_objs():
    global _objs, blocks_menu_image, \
        blocks_pos, editor_window, \
        setting_menu_image, create_text, \
        rename_text, delete_text, exit_text, \
        load_text, game_name_text, prompt_text, \
        gn_text_pos, pr_text_pos, cr_text_pos, \
        lo_text_pos, ren_text_pos, del_text_pos, \
        ex_text_pos, cr_text_size, lo_text_size, \
        ren_text_size, del_text_size, ex_text_size, \
        set_size_text, sets_text_pos, back_text, \
        back_text_size, field_sets1, field_sets2, \
        start_create_text, sc_text_pos, sc_text_size, \
        x_field, y_field, x_space, y_space, \
        level_choose_text, lch_text_pos, \
        arrow_right, arrow_left, arrow_left_pos, \
        arrow_right_pos, set_font, naming_window, \
        rename_field, rename_field_text

    del _objs, blocks_menu_image, \
        blocks_pos, editor_window, \
        setting_menu_image, create_text, \
        rename_text, delete_text, exit_text, \
        load_text, game_name_text, prompt_text, \
        gn_text_pos, pr_text_pos, cr_text_pos, \
        lo_text_pos, ren_text_pos, del_text_pos, \
        ex_text_pos, cr_text_size, lo_text_size, \
        ren_text_size, del_text_size, ex_text_size, \
        set_size_text, sets_text_pos, back_text, \
        back_text_size, field_sets1, field_sets2, \
        start_create_text, sc_text_pos, sc_text_size, \
        x_field, y_field, x_space, y_space, \
        level_choose_text, lch_text_pos, \
        arrow_right, arrow_left, arrow_left_pos, \
        arrow_right_pos, set_font, naming_window, \
        rename_field, rename_field_text


def editor(window, clock):
    global level_dict_

    loading_screen(window)
    init_editor()
    params = (10, 10)

    mouse_pos = pg_mouse_get_pos()
    block = BlockUnD
    tmp_block = None

    editing = True
    blocks_menu = False
    creating = False
    field_sets1_writing = False
    field_sets2_writing = False
    rename_field_writing = False
    naming_window_on = False
    level = None
    lvl_key = 1
    screen = 'setting'
    while editing:
        for event in pg_event_get():
            if event.type == QUIT:
                raise SystemExit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if screen == 'editor' and not naming_window_on:
                        naming_window_on = True
                        with open('levels.py', encoding='utf-8-sig') as f:
                            last_line = [i for i in f][-1]
                            if 'L' not in last_line:
                                number = '1'
                            else:
                                number = last_line[last_line.find('L') + 1:]
                                number = str(int(number) + 1)
                            level_name = "Уровень " + number
                    elif naming_window_on:
                        pass
                    else:
                        screen = 'setting'
                elif event.key == K_TAB and screen == 'editor' and not naming_window_on:
                    blocks_menu = not blocks_menu

                if field_sets1_writing:
                    if 48 <= event.key <= 57:
                        param = int(str(params[0]) + chr(event.key))
                        if param > 99:
                            param = 99
                        params = (param, params[1])
                elif field_sets2_writing:
                    if 48 <= event.key <= 57:
                        param = int(str(params[1]) + chr(event.key))
                        if param > 99:
                            param = 99
                        params = (params[0], param)

                if rename_field_writing:
                    if event.key == 8 and len(level_name) > 0:
                        level_name = level_name[:-1]
                    elif len(level_name) <= 16 and 32 <= event.key <= 126:
                        level_name += chr(event.key)

            if event.type == MOUSEMOTION:
                mouse_pos = pg_mouse_get_pos()

            if event.type == MOUSEBUTTONDOWN:
                if screen == 'editor':
                    if event.button == 1:
                        if blocks_menu:
                            blocks_menu = False
                            try:
                                block = blocks_pos[(mouse_pos[0] // x_field * x_field + x_space,
                                                    mouse_pos[1] // y_field * y_field + y_space)]
                            except KeyError:
                                pass
                        else:
                            creating = not naming_window_on
                    elif event.button == 3:
                        if not blocks_menu:
                            creating = True
                            tmp_block = block
                            block = Dirt
                elif screen == 'setting':
                    if event.button == 1:
                        if objs_crossed(mouse_pos, (1, 1), cr_text_pos, cr_text_size):
                            screen = 'set_lvl_size'

                        elif objs_crossed(mouse_pos, (1, 1), lo_text_pos, lo_text_size):
                            screen = 'load_lvl'
                            lvl_key = 1

                        elif objs_crossed(mouse_pos, (1, 1), ren_text_pos, ren_text_size):
                            screen = 'rename_lvl'
                            lvl_key = 1

                        elif objs_crossed(mouse_pos, (1, 1), del_text_pos, del_text_size):
                            screen = 'del_lvl'
                            lvl_key = 1

                        elif objs_crossed(mouse_pos, (1, 1), ex_text_pos, ex_text_size):
                            del_editor_objs()
                            return
                else:
                    if event.button == 1:
                        if objs_crossed(mouse_pos, (1, 1), ex_text_pos, back_text_size):
                            screen = 'setting'

                if screen == 'set_lvl_size':
                    if event.button == 1:
                        if objs_crossed(mouse_pos, (1, 1), field_sets1.pos, field_sets1.size):
                            field_sets1_writing = True
                            field_sets2_writing = False
                            params = (0, params[1])
                        elif objs_crossed(mouse_pos, (1, 1), field_sets2.pos, field_sets2.size):
                            field_sets2_writing = True
                            field_sets1_writing = False
                            params = (params[0], 0)
                        else:
                            field_sets1_writing = False
                            field_sets2_writing = False

                        if objs_crossed(mouse_pos, (1, 1), sc_text_pos, sc_text_size):
                            screen = 'editor'
                            params_res = (params[0] * CONFIG['OBJ_WIDTH'], params[1] * CONFIG['OBJ_HEIGHT'])
                            camera_x = CONFIG['RESOLUTION'][0] // 2 - params_res[0] // 2
                            camera_y = CONFIG['RESOLUTION'][1] // 2 - params_res[1] // 2
                            editor_screen = pg_Surface(params_res)
                            blocks = [[Dirt() for _ in range(params[0])] for _ in range(params[1])]

                elif screen == 'del_lvl' or screen == 'load_lvl' or screen == 'rename_lvl':
                    if event.button == 1:
                        levels = sorted(level_dict_.keys())

                        x = int(0.03906 * CONFIG['RESOLUTION'][0])
                        y = int(0.27778 * CONFIG['RESOLUTION'][1])
                        cycle_lvl_key = 1
                        for lvl in levels:
                            lvl_text = lvl
                            lvl = set_font.render(lvl, 1, BLACK)
                            size = (int((lvl.get_size()[0] / 1280) * CONFIG['RESOLUTION'][0]),
                                    int((lvl.get_size()[1] / 720) * CONFIG['RESOLUTION'][1]))
                            if y + size[1] > ex_text_pos[1]:
                                y = int(0.27778 * CONFIG['RESOLUTION'][1])
                                cycle_lvl_key += 1
                            if cycle_lvl_key == lvl_key:
                                if objs_crossed(mouse_pos, (1, 1), (x, y), size):
                                    level = lvl_text
                                    screen += '2'
                            y += int(0.13889 * CONFIG['RESOLUTION'][1])

                        if lvl_key > 1 and objs_crossed(mouse_pos, (1, 1), arrow_left_pos, arrow_left.get_size()):
                            lvl_key -= 1

                        elif lvl_key < cycle_lvl_key and \
                                objs_crossed(mouse_pos, (1, 1), arrow_right_pos, arrow_right.get_size()):
                            lvl_key += 1
                if naming_window_on:
                    if event.button == 1:

                        if objs_crossed(mouse_pos, (1, 1),
                                        (CONFIG['RESOLUTION'][0] // 2 - naming_window.get_size()[0] // 2 +
                                             int(0.06875 * CONFIG['RESOLUTION'][0]),
                                         CONFIG['RESOLUTION'][1] // 2 - naming_window.get_size()[1] // 2 +
                                             int(0.30972 * CONFIG['RESOLUTION'][1])),
                                        (int(0.09062 * CONFIG['RESOLUTION'][0]),
                                         int(0.04583 * CONFIG['RESOLUTION'][1]))):
                            if screen == 'editor':
                                blocks = [''.join([_objs[type(block)] for block in row]) for row in blocks]
                                with open('levels.py', 'a', encoding='utf-8-sig') as f:
                                    f.write('\nL' + number + ' = ' + repr(blocks)
                                            .replace(']', '\n]').replace(' ', '\n    ').replace('[', '[\n    '))
                                    if len(level_name) == 0:
                                        level_name = ' '
                                    f.write("\n\nlevel_dict_['" + level_name + "'] = L" + number + "\n")
                                level_dict_['Уровень ' + number] = blocks
                            elif screen == 'rename_lvl':
                                if level_name != level:
                                    level_dict_[level_name] = level_dict_[level]
                                    del level_dict_[level]
                                    levels_writing(level_dict_)

                            naming_window_on = False
                            screen = 'setting'

                        elif objs_crossed(mouse_pos, (1, 1),
                                          (CONFIG['RESOLUTION'][0] // 2 - naming_window.get_size()[0] // 2 +
                                               int(0.24297 * CONFIG['RESOLUTION'][0]),
                                           CONFIG['RESOLUTION'][1] // 2 - naming_window.get_size()[1] // 2 +
                                               int(0.30972 * CONFIG['RESOLUTION'][1])),
                                          (int(0.09062 * CONFIG['RESOLUTION'][0]),
                                           int(0.04583 * CONFIG['RESOLUTION'][1]))):
                            naming_window_on = False

                        elif objs_crossed(mouse_pos, (1, 1), rename_field.pos, rename_field.size):
                            rename_field_writing = True
                            level_name = ''
                        else:
                            rename_field_writing = False

                    elif event.button == 3:
                        screen = 'setting'
                        rename_field_writing = False
                        naming_window_on = False

            if event.type == MOUSEBUTTONUP:
                if screen == 'editor':
                    if event.button == 1:
                        creating = False
                    elif event.button == 3:
                        block = tmp_block
                        creating = False

        clock.tick(CONFIG['FPS_LIMIT'])

        if creating:
            block_pos = (mouse_pos[0] - camera_x, mouse_pos[1] - camera_y)
            block_pos = (block_pos[0] // CONFIG['OBJ_WIDTH'], block_pos[1] // CONFIG['OBJ_HEIGHT'])

            try:
                if not (block_pos[0] < 0 or block_pos[1] < 0):
                    blocks[block_pos[1]][block_pos[0]] = block()
            except IndexError:
                pass

        if screen == 'load_lvl2':
            blocks = []
            for row in range(len(level_dict_[level])):
                blocks.append([])
                for col in level_dict_[level][row]:
                    blocks[row].append(objs[col]())
            screen = 'editor'
            params_res = (len(blocks[0]) * CONFIG['OBJ_WIDTH'], len(blocks) * CONFIG['OBJ_HEIGHT'])
            camera_x = CONFIG['RESOLUTION'][0] // 2 - params_res[0] // 2
            camera_y = CONFIG['RESOLUTION'][1] // 2 - params_res[1] // 2
            editor_screen = pg_Surface(params_res)

        elif screen == 'rename_lvl2':
            naming_window_on = True
            screen = 'rename_lvl'
            level_name = level

        elif screen == 'del_lvl2':
            screen += 'setting'  # todo Точно удалить? Окошко

            del level_dict_[level]
            levels_writing(level_dict_)

        editor_window.fill(BLACK)

        if screen == 'editor':
            if not blocks_menu:
                if mouse_pos[0] <= 5 and camera_x < 0:
                    if camera_x <= -CONFIG['CAMERA_SPEED']:
                        camera_x += CONFIG['CAMERA_SPEED']
                    else:
                        camera_x = 0
                elif mouse_pos[0] >= CONFIG['RESOLUTION'][0] - 5 and camera_x - CONFIG['RESOLUTION'][0] > -params_res[0]:
                    if camera_x - CONFIG['RESOLUTION'][0] <= -params_res[0] + CONFIG['CAMERA_SPEED']:
                        camera_x = -params_res[0] + CONFIG['RESOLUTION'][0]
                    else:
                        camera_x -= CONFIG['CAMERA_SPEED']

                if mouse_pos[1] <= 5 and camera_y < 0:
                    if camera_y <= -CONFIG['CAMERA_SPEED']:
                        camera_y += CONFIG['CAMERA_SPEED']
                    else:
                        camera_y = 0
                elif mouse_pos[1] >= CONFIG['RESOLUTION'][1] - 5 and camera_y - CONFIG['RESOLUTION'][1] > -params_res[1]:
                    if camera_y - CONFIG['RESOLUTION'][1] <= -params_res[1] + CONFIG['CAMERA_SPEED']:
                        camera_y = -params_res[1] + CONFIG['RESOLUTION'][1]
                    else:
                        camera_y -= CONFIG['CAMERA_SPEED']
                editor_screen.fill(BLACK)
                for row in range(len(blocks)):
                    for col in range(len(blocks[row])):
                        if blocks[row][col].animated:
                            editor_screen.blit(blocks[row][col].image[0],
                                               (col * CONFIG['OBJ_WIDTH'], row * CONFIG['OBJ_HEIGHT']))
                        else:
                            editor_screen.blit(blocks[row][col].image,
                                               (col * CONFIG['OBJ_WIDTH'], row * CONFIG['OBJ_HEIGHT']))
                editor_window.blit(editor_screen, (camera_x, camera_y))
            else:
                editor_window.blit(blocks_menu_image, (0, 0))
        else:
            creating = False
            editor_window.blit(setting_menu_image, (0, 0))
            editor_window.blit(game_name_text, gn_text_pos)
            editor_window.blit(prompt_text, pr_text_pos)
            if screen == 'setting':
                editor_window.blit(exit_text, ex_text_pos)
            else:
                editor_window.blit(back_text, ex_text_pos)

        if screen == 'setting':
            editor_window.blit(create_text, cr_text_pos)
            editor_window.blit(load_text, lo_text_pos)
            editor_window.blit(rename_text, ren_text_pos)
            editor_window.blit(delete_text, del_text_pos)

        elif screen == 'set_lvl_size':
            field_sets1.update(str(params[0]), BLACK)
            field_sets2.update(str(params[1]), BLACK)

            editor_window.blit(set_size_text, sets_text_pos)
            editor_window.blit(start_create_text, sc_text_pos)
            field_sets1.draw(editor_window)
            field_sets2.draw(editor_window)

        elif screen == 'rename_lvl' or screen == 'del_lvl' or screen == 'load_lvl':
            editor_window.blit(level_choose_text, lch_text_pos)

            levels = sorted(level_dict_.keys())

            x = int(0.03906 * CONFIG['RESOLUTION'][0])
            y = int(0.27778 * CONFIG['RESOLUTION'][1])
            cycle_lvl_key = 1
            for lvl in levels:
                lvl = set_font.render(lvl, 1, BLACK)
                size = (int((lvl.get_size()[0] / 1280) * CONFIG['RESOLUTION'][0]),
                        int((lvl.get_size()[1] / 720) * CONFIG['RESOLUTION'][1]))
                lvl = pg_transform_scale(lvl, size)
                if y + size[1] > ex_text_pos[1]:
                    y = int(0.27778 * CONFIG['RESOLUTION'][1])
                    cycle_lvl_key += 1
                if cycle_lvl_key == lvl_key:
                    editor_window.blit(lvl, (x, y))
                y += int(0.13889 * CONFIG['RESOLUTION'][1])

            if lvl_key > 1:
                editor_window.blit(arrow_left, arrow_left_pos)
            if lvl_key < cycle_lvl_key:
                editor_window.blit(arrow_right, arrow_right_pos)

        if naming_window_on:
            editor_window.blit(naming_window, (CONFIG['RESOLUTION'][0] // 2 - naming_window.get_size()[0] // 2,
                                               CONFIG['RESOLUTION'][1] // 2 - naming_window.get_size()[1] // 2))

            editor_window.blit(rename_field_text,
                               (CONFIG['RESOLUTION'][0] // 2 - naming_window.get_size()[0] // 2 +
                                int(0.03828 * CONFIG['RESOLUTION'][0]),
                                CONFIG['RESOLUTION'][1] // 2 - naming_window.get_size()[1] // 2 +
                                int(0.05972 * CONFIG['RESOLUTION'][1])))
            rename_field.update(level_name, BLACK)
            rename_field.draw(editor_window)

        window.blit(editor_window, (0, 0))
        pg_display_flip()


if __name__ == '__main__':
    from pygame import FULLSCREEN
    from pygame.time import Clock
    from pygame.display import set_mode
    from pygame.mixer import init as in1
    from game_obj import init_objs_png
    from Menu import loading_screen_init
    wind = set_mode(CONFIG['RESOLUTION'])  # , FULLSCREEN)
    in1()
    init_objs_png()
    loading_screen_init()
    editor(wind, Clock())
