import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP :(0, -5),
    pg.K_DOWN :(0, 5),
    pg.K_LEFT :(-5, 0),
    pg.K_RIGHT :(5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectか爆弾Rect
    戻り値:判定結果タプル（横方向、縦方向）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH <rct.right:   #横方向にはみ出ていたら
        yoko = False
    if rct.top < 0  or HEIGHT < rct.bottom:  #縦方向にはみ出ていたら
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:    #演習1
    gg_img = pg.Surface((WIDTH, HEIGHT))
    gg_img.set_alpha(100)   #透明度の設定
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GameOver",   #文章の表示
            True, (255,255,255))
    gg_img.blit(txt, [400, 325])
    ck_img = pg.image.load("fig/8.png")
    gg_img.blit(ck_img, [350,325])
    gg_img.blit(ck_img, [700,325])
    screen.blit(gg_img, [0, 0])
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:   #演習2
    bb_imgs =[]
    for r in range(1, 11):   #画像の大きさのリスト
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]    #加速度のリスト

    return bb_imgs, bb_accs







def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    clock = pg.time.Clock()
    bb_rct = bb_img.get_rect() #爆弾rect
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    bb_imgs, bb_accs = init_bb_imgs() 



    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        if bb_rct.colliderect(kk_rct):  #こうかとんと爆弾の衝突判定
            gameover(screen) # ゲームオーバー 
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        
        avx = vx * bb_accs[min(tmr//500, 9)]   #横方向の加速度の実装
        avy = vy * bb_accs[min(tmr//500, 9)]   #縦方向の加速度の実装
        bb_rct.move_ip(avx , avy)   #vx,vyをavx,avyに変更
        yoko, tate =check_bound(bb_rct)
        if not yoko:  #横方向にはみ出ていたら 
            vx *= -1
        if not tate:  #縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  #爆弾描画


        bb_img = bb_imgs[min(tmr//500, 9)]   #爆弾の拡大率の変更

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
