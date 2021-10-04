# coding: utf-8

from time import process_time as time_process_time
from pygame import \
    Surface as pg_Surface
from pygame import QUIT, \
    KEYDOWN, K_ESCAPE, \
    MOUSEBUTTONDOWN
from pygame.mixer_music import \
    load as pg_mixer_music_load, \
    play as pg_mixer_music_play
from pygame.transform import \
    scale as pg_transform_scale
from pygame.display import \
    flip as pg_display_flip
from pygame.event import \
    get as pg_event_get
from pygame.font import \
    SysFont as pg_font_SysFont
from game_obj import load_img
from constants import BLACK
from config import CONFIG


def tutorial(window, level, clock):
    from Base_menu import base_main_screen, body_base_screen
    pg_mixer_music_load('music/ingame_music.wav')
    pg_mixer_music_play(-1)

    tutor_screen = pg_Surface(CONFIG['RESOLUTION'])
    text_place = load_img('pics/misc/tutor_line.png', (CONFIG['RESOLUTION'][0], int(0.13889 * CONFIG['RESOLUTION'][1])))
    cap = load_img('pics/misc/captain.png', (int(0.06563 * CONFIG['RESOLUTION'][0]),
                                             int(0.13611 * CONFIG['RESOLUTION'][1])))
    tutor_font = pg_font_SysFont('Impact', 25)
    text = [
        'Привет! Добро пожаловать в обучение! Здесь ты научишься управлять своей армией.',
        'Перед тобой - карта уровня. Здесь будут разворачиваться военные действия.',
        'Чтобы победить, надо уничтожить все базы соперников.',
        'Существуют 6 типов блоков на уровне: Земля, Камень, Вода, Шахта, Песок и База. Расскажу о каждом из них.',
        'Земля - это блок, по которому ты можешь передвигать свои танки, а Камень - по которому нельзя.',
        'Вода - блок, по которому могут передвигаться лишь пули.',
        'Из шахты можно забрать золото для сооружения новых танков. Песок - разрушаемый блок.',
        'Ну и база. На базе можно создать танки.',
        'Это меню создания танка. Чтобы создать танк надо нажать на любой из квадратов.',
        'При нажатии на одно из комплектующих танка оно выбирается.',
        'Ну и для выхода из данного меню, нажимай на стрелку в нижнем левом углу.',
        'Управлять танком довольно просто: нажимаешь на кнопку, которая обозначает нужную команду.',
        '(Эти кнопки можно изменить в настройках)',
        'А теперь вперед в бой!'
    ]
    text = [tutor_font.render(txt, 1, BLACK) for txt in text]
    text = [pg_transform_scale(txt, (int(txt.get_size()[0] / 1280 * CONFIG['RESOLUTION'][0]),
                                     int(txt.get_size()[1] / 720 * CONFIG['RESOLUTION'][1]))) for txt in text]
    stage = 0
    while True:
        for event in pg_event_get():
            if event.type == QUIT:
                raise SystemExit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                else:
                    stage += 1
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                stage += 1

        if stage >= len(text):
            return

        clock.tick(CONFIG['FPS_LIMIT'])

        tutor_screen.fill(BLACK)

        if 0 <= stage <= 7 or stage > 10:
            level.draw(tutor_screen, 0, 0, time_process_time())
        elif stage == 10 or stage == 8:
            tutor_screen.blit(base_main_screen, (0, 0))
        elif stage == 9:
            tutor_screen.blit(body_base_screen[0], (0, 0))

        tutor_screen.blit(text_place, (0, CONFIG['RESOLUTION'][1] - int(0.13889 * CONFIG['RESOLUTION'][1])))
        tutor_screen.blit(text[stage], (0, CONFIG['RESOLUTION'][1] - int(0.13889 * CONFIG['RESOLUTION'][1])))
        tutor_screen.blit(cap, (CONFIG["RESOLUTION"][0] - cap.get_size()[0],
                                CONFIG["RESOLUTION"][1] - cap.get_size()[1]))
        window.blit(tutor_screen, (0, 0))
        pg_display_flip()


if __name__ == '__main__':
    from pygame.display import set_mode
    from pygame.time import Clock
    from pygame.font import init as in1
    from levels import L6
    from game_obj import Level, init_objs_png
    from pygame.mixer import init as in2
    from Base_menu import base_init

    wind = set_mode((1280, 720))
    in1()
    in2()
    init_objs_png()
    base_init()

    tutorial(wind, Level(L6), Clock())
