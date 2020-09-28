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
CHACHOS = "menus/losChachos.html"
XLARGE4 = "menus/details7.html"
XLARGE5 = "menus/details8.html"
XLARGE6 = "menus/details9.html"
PORTICO = "menus/portico.html"
MARGARITA = "menus/margarita.html"
CIELOBISTRO = "menus/cieloBistro.html"
PORTO1 = "menus/portoAlto1.html"
PORTO2 = "menus/portoAlto2.html"

TEMPLATES = [
    (SLIDES, _('Small')),
    (TABS, _('Medium')),
    (TABSb, _('Medium B')),
    (FULL, _('large')),
    (XLARGE, _('X-large')),
    (XLARGE2, _('X-large 2')),
    (CHACHOS, _('Los Chachos')),
    (XLARGE4, _('Don_pedrito')),
    (XLARGE5, _('Margarita')),
    (XLARGE6, _('Portico OLD')),
    (PORTICO, _('Portico')),
    (MARGARITA, _('Pizza Margarita')),
    (CIELOBISTRO, _('Cielo Bistro')),
    (PORTO1, _('Porto 1')),
    (PORTO2, _('Porto 2')),
]
