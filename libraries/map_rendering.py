from PIL import Image, ImageDraw

INACCESSABLE = [(1,0),(5,0),(6,0),(1,1),(3,1),(6,1),(1,3),(4,3),(5,3),(0,4),(3,4),(4,4),(5,4),(1,6),(4,6)]
SPECIAL = [(0,0),(0,6),(6,6)]

def show_map(tiles_x, tiles_y, blocked_tiles, special_tiles, player_pos, id, player_agility = 0):
    #set the size of the image by multiplying it by the tiles and adding extra 100px for the borders
    width = (tiles_x*50)+100
    height = (tiles_y*50)+100
    #creating the image using PIL
    map = Image.new('RGB', (width, height), (220, 220, 220))
    draw = ImageDraw.Draw(map, 'RGB')

    #getting the mins and maxs for the tiles the player can move onto
    min_x = player_pos[0] - player_agility
    if min_x < 0:
        min_x = 0
    max_x = player_pos[0] + player_agility
    if max_x > tiles_x-1:
        max_x = tiles_x-1
    min_y = player_pos[1] - player_agility
    if min_y < 0:
        min_y = 0
    max_y = player_pos[1] + player_agility
    if max_y > tiles_y-1:
        max_y = tiles_y-1

    #Using this the tiles the player can movee to we color yellow
    for x in range(0, tiles_x):
        for y in range(0, tiles_y):
            if min_x <= x <= max_x and min_y <= y <= max_y:
                draw.rectangle([((x * 50) + 50, (y * 50) + 50), ((x * 50) + 100, (y * 50) + 100)],(253, 253, 150))

    #Using this we color the cities red
    for tile in special_tiles:
        draw.rectangle([((tile[0]*50)+50, (tile[1]*50)+50), ((tile[0]*50)+100, (tile[1]*50)+100)], (255, 105, 97))

    #Using this we draw the lines that make the image look like tiles
    for x in range(100, width-99, 50):
        draw.line([(x, 50), (x, height-50)], (200, 200, 200), 1)
        for y in range(100, height-99, 50):
            draw.line([(50, y), (width-50, y)], (200, 200, 200), 1)

    #Using this we draw where the player is
    draw.rectangle([((player_pos[0] * 50) + 60, (player_pos[1] * 50) + 60),((player_pos[0] * 50) + 90, (player_pos[1] * 50) + 90)], (119, 221, 119))

    #Using this we draw the coordinates on the tiles
    for x in range(0, tiles_x):
        for y in range(0, tiles_y):
            if x != player_pos[0] or y != player_pos[1]:
                draw.text(((x*50)+55, (y*50)+55), str(x) + ";" + str(y), (54, 57, 63))

    #Using this we draw the borders
    draw.rectangle([(0, 0), (50, height)], (54, 57, 63))
    draw.rectangle([(0, 0), (width, 50)], (54, 57, 63))
    draw.rectangle([(width, height), (width-50, 0)], (54, 57, 63))
    draw.rectangle([(width, height), (0, height-50)], (54, 57, 63))

    #Using this we draw all the blocked tiles
    for tile in blocked_tiles:
        draw.rectangle([((tile[0]*50)+50, (tile[1]*50)+50), ((tile[0]*50)+100, (tile[1]*50)+100)], (54, 57, 63))

    #save the map in the directory
    map.save('data/players/maps/'+str(id)+'.png')
    del map

