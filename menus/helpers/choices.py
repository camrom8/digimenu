from django.utils.translation import gettext as _

NONE = 'Only size'
EXTRA_SMALL = 'Extra small'
SMALL = 'Small'
MEDIUM = 'medium'
LARGE = 'Large'
EXTRA_LARGE = 'Extra Large'
COMBO = 'combo'

SIZES = [
    (NONE, _('Only size')),
    (SMALL, _('Small')),
    (EXTRA_SMALL, _('Extra small')),
    (MEDIUM, _('medium')),
    (LARGE, _('Large')),
    (EXTRA_LARGE, _('Extra large')),
    (COMBO, _('Combo')),
]
