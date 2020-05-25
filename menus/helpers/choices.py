from django.utils.translation import gettext as _

NONE = _('U')
EXTRA_SMALL = _('XS')
SMALL = _('S')
MEDIUM = _('M')
LARGE = _('L')
EXTRA_LARGE = _('XL')
COMBO = _('Meal')

SIZES = [
    (NONE, _('Only')),
    (EXTRA_SMALL, _('Extra small')),
    (SMALL, _('Small')),
    (MEDIUM, _('Medium')),
    (LARGE, _('Large')),
    (EXTRA_LARGE, _('Extra large')),
    (COMBO, _('Meal')),
]

SLIDES = "menus/details.html"
TABS = "menus/details2.html"
FULL = "menus/details3.html"
TEMPLATES = [
    (SLIDES, _('Small')),
    (TABS, _('Medium')),
    (FULL, _('large')),
]
