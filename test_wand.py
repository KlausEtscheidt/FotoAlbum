p = r'C:\Users\Klaus\Pictures\testpics\1960_01.tif'
from wand.image import Image
from wand.display import display

with Image(filename=p) as img:
    # img.crop(left=34, top=99, width=755, height=37)
    # img.auto_level()
    # img.negate()
    # img.threshold(threshold=0.70)
    # img.save(filename='stockhold_processed.png')
    img.rotate()
    display(img)
    input()