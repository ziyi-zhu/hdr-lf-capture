import os

from merge import merge_light_field

#path = os.path.join('home', 'pi', 'Pictures', 'capture')
path = 'capture'

merge_light_field(path, 'SonyA7r1', 3)