# -*- coding: utf-8 -*-
"""Телефон: ролик во весь экран, текст поверх него через секунду."""
import io

p = 'index.html'
s = io.open(p, encoding='utf-8').read()

# ---------- 1. Разметка первого экрана на телефоне ----------
БЫЛО_CSS = """        /* Ролик 16:9 на вертикальном экране обрезался так, что от дома
           оставалось 26% ширины. Даём видео собственную полосу сверху —
           кадр отдаляется, дом виден целиком, текст уходит под него. */
        .hero {
          display: block;
          min-height: 0;
        }

        .hero__media {
          position: relative;
          inset: auto;
          /* Ролик почти квадратный: при высоте около ширины экрана
             он показывается целиком, без обрезки по бокам */
          height: 108vw;
          min-height: 320px;
          max-height: 440px;
        }

        /* Сверху гасим только шапку, снизу — полосу под заголовком.
           Середину кадра не трогаем, иначе дом уходит в темноту. */
        .hero__media::after {
          background:
            linear-gradient(to bottom, rgba(11, 13, 18, 0.72), transparent 18%),
            linear-gradient(to top, var(--bg) 6%, rgba(11, 13, 18, 0.78) 26%, transparent 56%);
        }

        /* Текст заезжает на фотографию, а не начинается под ней */
        .hero__inner {
          position: relative;
          z-index: 2;
          max-width: none;
          gap: 13px;
          margin-top: -135px;
          padding-block: 0 26px;
        }"""

СТАЛО_CSS = """        /* Ролик занимает весь экран, текст лежит поверх него.
           Квадратный кадр при этом обрезается по бокам — это плата
           за то, что текст на видео, а не под ним. */
        .hero {
          display: grid;
          align-items: end;
          min-height: 100svh;
        }

        .hero__media {
          position: absolute;
          inset: 0;
        }

        /* Низ затемняем плотно: под текстом кадр ещё движется,
           и без этого белые буквы теряются в светлом проёме */
        .hero__media::after {
          background:
            linear-gradient(to bottom, rgba(11, 13, 18, 0.72), transparent 16%),
            linear-gradient(to top, var(--bg) 4%, rgba(11, 13, 18, 0.88) 34%, rgba(11, 13, 18, 0.4) 62%, transparent 82%);
        }

        .hero__inner {
          position: relative;
          z-index: 2;
          max-width: none;
          gap: 13px;
          margin-top: 0;
          padding-block: 0 30px;
        }"""

assert БЫЛО_CSS in s, 'мобильный первый экран'
s = s.replace(БЫЛО_CSS, СТАЛО_CSS, 1)

# ---------- 2. Текст появляется через секунду ----------
БЫЛО_JS = """        var телефон = window.matchMedia('(max-width: 760px)').matches
        видео.src = телефон ? 'media/intro-mob.webm' : 'media/intro.webm'
        видео.poster = телефон ? 'media/hero-start-mob.jpg' : 'media/hero-start.jpg'"""

СТАЛО_JS = """        var телефон = window.matchMedia('(max-width: 760px)').matches
        видео.src = телефон ? 'media/intro-mob.webm' : 'media/intro.webm'
        видео.poster = телефон ? 'media/hero-start-mob.jpg' : 'media/hero-start.jpg'

        // На телефоне текст выходит поверх ещё идущего ролика через секунду.
        // На компьютере он ждёт конца: там ролик — отдельная сцена,
        // а на телефоне человек не готов смотреть пять секунд в пустой экран.
        if (телефон) {
          видео.addEventListener('playing', function () {
            setTimeout(показатьТекст, 1000)
          }, { once: true })
        }"""

assert БЫЛО_JS in s
s = s.replace(БЫЛО_JS, СТАЛО_JS, 1)

# ---------- 3. Разделяем «показать текст» и «погасить ролик» ----------
БЫЛО_ОТКР = """        function открыть() {
          if (показано) return
          показано = true
          экран.setAttribute('data-готово', '1')
          if (видео) videoГасим()
        }

        function videoГасим() {
          видео.classList.add('off')
          setTimeout(function () { try { видео.pause() } catch (e) {} }, 600)
        }"""

СТАЛО_ОТКР = """        // Текст и ролик разведены: на телефоне текст выходит раньше,
        // а ролик продолжает идти и замирает на последнем кадре
        function показатьТекст() {
          if (показано) return
          показано = true
          экран.setAttribute('data-готово', '1')
        }

        function погасить() {
          if (!видео) return
          видео.classList.add('off')
          setTimeout(function () { try { видео.pause() } catch (e) {} }, 600)
        }

        function открыть() {
          показатьТекст()
          погасить()
        }"""

assert БЫЛО_ОТКР in s
s = s.replace(БЫЛО_ОТКР, СТАЛО_ОТКР, 1)

io.open(p, 'w', encoding='utf-8').write(s)
print('текст переведён поверх ролика')
