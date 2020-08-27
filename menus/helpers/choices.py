from django.utils.translation import gettext as _

NONE = _('Unique')
EXTRA_SMALL = _('x-Small')
SMALL = _('Small')
MEDIUM = _('Medium')
LARGE = _('Large')
EXTRA_LARGE = _('x-Large')
COMBO = _('Meal')
PERSONAL = _('Personal')
MEDIANA = _('Mediana')
FAMILIAR = _('Familiar')
SHOT = _('Shot')
MEDIA = _('Media')
BOTELLA = _('Botella')
T30CM = _('30cm')
T50CM = _('50cm')

SIZES = [
    (NONE, _('Only')),
    (EXTRA_SMALL, _('Extra small')),
    (SMALL, _('Small')),
    (MEDIUM, _('Medium')),
    (LARGE, _('Large')),
    (EXTRA_LARGE, _('Extra large')),
    (COMBO, _('Meal')),
    (PERSONAL, _('Personal')),
    (MEDIANA, _('Mediana')),
    (FAMILIAR, _('Familiar')),
    (SHOT, _('Shot')),
    (SHOT, _('Media')),
    (T50CM, _('50cm')),
    (T30CM, _('30cm')),
]
SLIDES = "menus/details.html"
TABS = "menus/details2.html"
TABSb = "menus/details2b.html"
FULL = "menus/details3.html"
XLARGE = "menus/details4.html"
XLARGE2 = "menus/details5.html"
XLARGE3 = "menus/details6.html"
XLARGE4 = "menus/details7.html"
XLARGE5 = "menus/details8.html"
XLARGE6 = "menus/details9.html"
STANDARD = "menus/details10.html"
STANDARD2 = "menus/details11.html"
STANDARD3 = "menus/details12.html"

TEMPLATES = [
    (SLIDES, _('Small')),
    (TABS, _('Medium')),
    (TABSb, _('Medium B')),
    (FULL, _('large')),
    (XLARGE, _('X-large')),
    (XLARGE2, _('X-large 2')),
    (XLARGE3, _('Los_chachos')),
    (XLARGE4, _('Don_pedrito')),
    (XLARGE5, _('Margarita')),
    (XLARGE6, _('Portico')),
    (STANDARD, _('Portico_2')),
    (STANDARD2, _('Margarita_2')),
    (STANDARD3, _('Cielo_bistro')),
]
