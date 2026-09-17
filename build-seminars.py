#!/usr/bin/env python3
"""Generate seminare.htm and one page per seminar from index.html's own chrome.

The head, icon sprite, header, mobile sheet, footer and script are lifted from
index.html at build time rather than copied by hand, so five pages cannot drift
apart. Edit SEMINARS below and re-run when the real dates arrive:

    python3 build-seminars.py
"""
import io, re, sys

SEMINARS = [
    dict(slug='seminar-pse-einfuehrung',
         title='Psychosomatische Energetik — ein Einführungsabend',
         short='Psychosomatische Energetik',
         when='Donnerstag, 12. November 2026', time='19–21 Uhr', dur='2 Stunden',
         img='assets/clean/1021.jpg', imgw=167, imgh=206,
         alt='Hände der Heilpraktikerin bei der Testung am Arm',
         teaser='Was die Testung zeigt, wie ein seelischer Konflikt sichtbar wird und warum Sie dafür nichts erzählen müssen.',
         body=['Psychosomatische Energetik arbeitet mit der Annahme, dass hinter vielen '
               'körperlichen Beschwerden ein seelischer Konflikt steht, der Lebensenergie '
               'bindet. An diesem Abend zeige ich, wie die Testung abläuft und was sie '
               'sichtbar macht.',
               'Sie müssen nichts von sich erzählen und nichts mitbringen. Wer möchte, '
               'kann sich im Anschluss selbst testen lassen.'],
         points=['Wie die Testung praktisch abläuft',
                 'Was die vier Konfliktebenen bedeuten',
                 'Womit anschließend behandelt wird',
                 'Zeit für Ihre Fragen']),
    dict(slug='seminar-blutwerte',
         title='Ihre Blutwerte lesen lernen',
         short='Blutwerte lesen lernen',
         when='Samstag, 28. November 2026', time='10–14 Uhr', dur='4 Stunden',
         img='assets/clean/1019.jpg', imgw=167, imgh=206,
         alt='Blutröhrchen für die ganzheitliche Laboranalyse',
         teaser='42 bis 70 Werte ergeben ein Bild. An diesem Vormittag lernen Sie, worauf ich schaue und was die Zahlen über Ihren Stoffwechsel sagen.',
         body=['Ein Laborbefund ist kein Urteil, sondern ein Zwischenstand. Wir gehen '
               'gemeinsam durch die Werte, die in einer ganzheitlichen Analyse '
               'zusammengehören, und ich zeige, welche Zusammenhänge mir auffallen.',
               'Bringen Sie vorhandene eigene Befunde gerne mit — wir schauen anonym '
               'und nur, soweit Sie das möchten.'],
         points=['Welche Werte zusammen gelesen werden',
                 'Warum „normal" nicht immer unauffällig heißt',
                 'Schilddrüse, Eisen, Vitamin D im Zusammenhang',
                 'Eigene Befunde können mitgebracht werden']),
    dict(slug='seminar-klangschalen',
         title='Klangschalen für zu Hause',
         short='Klangschalen für zu Hause',
         when='Samstag, 16. Januar 2027', time='10–13 Uhr', dur='3 Stunden',
         img='assets/clean/ruhe.jpg', imgw=251, imgh=145,
         alt='Handtuch und ätherische Öle, Sinnbild für Ruhe und Regeneration',
         teaser='Grundlagen der Klangschalenarbeit zum Mitmachen — Haltung, Anschlag und ein paar einfache Abläufe für den eigenen Alltag.',
         body=['Klang wirkt über den Körper, nicht über das Gespräch. Deshalb ist dieser '
               'Vormittag vor allem praktisch: Sie hören, probieren und spüren selbst.',
               'Schalen sind vorhanden. Bequeme Kleidung und eine Decke sind alles, was '
               'Sie mitbringen müssen.'],
         points=['Anschlag, Haltung und Klangführung',
                 'Zwei einfache Abläufe für zu Hause',
                 'Worauf bei eigenen Schalen zu achten ist',
                 'Schalen werden gestellt']),
    dict(slug='seminar-kinder-staerken',
         title='Kinder stärken — ein Abend für Eltern',
         short='Kinder stärken',
         when='Mittwoch, 4. Februar 2027', time='19–21 Uhr', dur='2 Stunden',
         img='assets/clean/kinder.jpg', imgw=133, imgh=202,
         alt='Kinderhände und Erwachsenenhände halten gemeinsam ein Herz',
         teaser='Unruhe, Konzentration, Rückzug: was Kinder brauchen, wie PSE bei ihnen wirkt und was Sie zu Hause tun können.',
         body=['Kinder reagieren auf Psychosomatische Energetik oft besonders schnell, '
               'weil bei ihnen noch wenig überlagert ist. Dieser Abend richtet sich an '
               'Eltern, nicht an die Kinder selbst.',
               'Es geht um Beobachten statt Bewerten — und darum, wann eine ärztliche '
               'Abklärung der richtige erste Schritt ist.'],
         points=['Unruhe, Schlaf und Konzentration einordnen',
                 'Wie die Testung bei Kindern abläuft',
                 'Was Sie zu Hause unterstützen können',
                 'Wann zuerst ärztlich abgeklärt wird']),
]

src = io.open('index.html', encoding='utf-8').read()

def between(a, b, inclusive_b=True):
    i = src.index(a); j = src.index(b, i)
    return src[i:j + (len(b) if inclusive_b else 0)]

STYLE_LINK = '<link rel="stylesheet" href="site.css">'
HEAD_TOP = src[:src.index(STYLE_LINK) + len(STYLE_LINK)]
SPRITE   = between('<svg width="0"', '</svg>')
CHROME   = src[src.index('<header class="bar"'):src.index('<main')]      # header + mobile sheet
FOOTER   = between('<footer class="foot"', '</footer>')
SCRIPT   = src[src.rfind('<script>'):src.rindex('</script>') + len('</script>')]

# index.html's head carries a long documentation comment about the homepage's
# design decisions — and that comment contains a sample <title> of its own, so a
# naive "replace the first <title>" hits the wrong one. Strip the comment first:
# it does not belong on a seminar page either way, and then only one title is left.
def head(title):
    h = re.sub(r'<!--.*?-->\s*', '', HEAD_TOP, count=1, flags=re.S)
    h, n = re.subn(r'<title>.*?</title>', '<title>%s</title>' % title, h, flags=re.S)
    if n != 1:
        sys.exit('expected exactly one <title> after stripping the comment, found %d' % n)
    return h

NOTE = ('<p class="semnote">Die hier gezeigten Termine sind <strong>Beispiele für die '
        'Gestaltung</strong>. Echte Seminartermine und Preise trägt die Praxis vor dem '
        'Livegang ein.</p>')

def page(title, body):
    return '%s\n%s\n\n%s<main>\n%s</main>\n\n%s\n\n%s\n' % (
        head(title), SPRITE, CHROME, body, FOOTER, SCRIPT)

# ---------------------------------------------------------------- index page
rows = []
for s in SEMINARS:
    rows.append('''        <li class="semrow">
          <div class="semrow__when">
            <span class="semrow__date">%(when)s</span>
            <span class="semrow__time">%(time)s · %(dur)s</span>
          </div>
          <div class="semrow__what">
            <h2><a href="%(slug)s.htm">%(title)s</a></h2>
            <p>%(teaser)s</p>
            <span class="semrow__go">Details und Platz buchen <svg class="ico"><use href="#i-arrow"/></svg></span>
          </div>
        </li>''' % s)

index_body = '''  <section class="section" id="seminare">
    <div class="wrap stack" style="gap:16px">
      <span class="eyebrow">Seminare</span>
      <h1>Kommende Termine</h1>
      <p class="lede">In kleinen Gruppen erkläre ich die Methoden, mit denen ich arbeite —
        verständlich, ohne Vorkenntnisse und mit genug Zeit für Ihre Fragen.</p>
    </div>
    <div class="wrap">
      %s
      <ul class="semlist">
%s
      </ul>
    </div>
  </section>
''' % (NOTE, '\n'.join(rows))

io.open('seminare.htm', 'w', encoding='utf-8').write(page('Seminare | Naturheilpraxis Cornelia Dinger', index_body))

# --------------------------------------------------------------- detail pages
for s in SEMINARS:
    points = '\n'.join('            <li><svg class="ico"><use href="#i-check"/></svg>%s</li>' % t
                       for t in s['points'])
    paras = '\n'.join('          <p>%s</p>' % t for t in s['body'])
    body = '''  <section class="section tint-2 semhead">
    <div class="wrap stack" style="gap:14px">
      <a class="semback" href="seminare.htm"><svg class="ico"><use href="#i-arrow"/></svg>Alle Seminare</a>
      <span class="eyebrow">Seminar</span>
      <h1>%(title)s</h1>
      <p class="lede">%(teaser)s</p>
      <dl class="semfacts">
        <div><span class="semfact__ico"><svg class="ico"><use href="#i-calendar"/></svg></span>
          <span class="semfact__t"><dt>Termin</dt><dd>%(when)s</dd></span></div>
        <div><span class="semfact__ico"><svg class="ico"><use href="#i-clock"/></svg></span>
          <span class="semfact__t"><dt>Uhrzeit</dt><dd>%(time)s, %(dur)s</dd></span></div>
        <div><span class="semfact__ico"><svg class="ico"><use href="#i-pin"/></svg></span>
          <span class="semfact__t"><dt>Ort</dt><dd>Praxis, Schubertstraße 7, Bad Schönborn</dd></span></div>
        <div><span class="semfact__ico"><svg class="ico"><use href="#i-euro"/></svg></span>
          <span class="semfact__t"><dt>Gebühr</dt><dd><span class="price--slot">Betrag einsetzen</span></dd></span></div>
      </dl>
    </div>
  </section>

  <section class="section">
    <div class="wrap semdetail">
      <div class="semdetail__text">
%(paras)s
        <figure class="semshot" style="--shot:%(shot)dpx">
          <img src="%(img)s" alt="%(alt)s" width="%(imgw)d" height="%(imgh)d" loading="lazy" decoding="async">
        </figure>
        <h3>Worum es geht</h3>
        <ul class="incl semincl">
%(points)s
        </ul>

        <div class="semteacher">
          <figure class="sem__portrait semportrait--inline">
            <img src="assets/clean/cornelia.jpg" alt="Cornelia Dinger, Heilpraktikerin" width="392" height="482" loading="lazy" decoding="async">
          </figure>
          <p class="semteacher__t"><b>Cornelia Dinger</b>Heilpraktikerin. Sie hält das Seminar selbst.</p>
        </div>
      </div>

      <form class="panel sembook" id="booking">
        <div class="fbody">
          <h3>Platz buchen</h3>
          <p class="sembook__lead">Vier Angaben genügen. Sie erhalten eine Bestätigung,
            bevor etwas verbindlich wird.</p>
          <div class="row2">
            <div class="field"><label for="b-first">Vorname</label><input id="b-first" name="firstname" type="text" autocomplete="given-name" required></div>
            <div class="field"><label for="b-last">Nachname</label><input id="b-last" name="lastname" type="text" autocomplete="family-name" required></div>
          </div>
          <div class="field"><label for="b-mail">E-Mail</label><input id="b-mail" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="b-tel">Telefon</label><input id="b-tel" name="tel" type="tel" autocomplete="tel" required></div>
          <label class="check">
            <input type="checkbox" name="consent" required>
            <span>Ich bin damit einverstanden, dass meine Angaben zur Bearbeitung meiner Anmeldung gespeichert werden. <a href="datenschutz.htm">Datenschutzerklärung</a></span>
          </label>
          <button class="btn btn--primary" type="submit" style="width:100%%">Platz buchen <svg class="ico"><use href="#i-arrow"/></svg></button>
          <p class="appt__foot">Ihre Anmeldung ist noch keine Zusage — ich bestätige Ihren Platz persönlich.</p>
        </div>
        <div class="sent" role="status">
          <svg class="ico"><use href="#i-check"/></svg>
          <h3 style="font-size:1.3rem">Vielen Dank für Ihre Anmeldung.</h3>
          <p style="color:var(--body)">Ich melde mich persönlich bei Ihnen und bestätige Ihren Platz. Wenn es dringend ist, erreichen Sie mich unter <a href="tel:+491711242717">0171 124 27 17</a>.</p>
          <p class="appt__foot">Entwurf: im Livebetrieb an das Praxis-Postfach angebunden.</p>
        </div>
      </form>
    </div>
  </section>
''' % dict(s, paras=paras, points=points, shot=s['imgw']*2)
    io.open(s['slug'] + '.htm', 'w', encoding='utf-8').write(
        page('%s | Naturheilpraxis Cornelia Dinger' % s['short'], body))

print('wrote seminare.htm and %d seminar pages' % len(SEMINARS))
for s in SEMINARS:
    print('  ', s['slug'] + '.htm')
