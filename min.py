from ursina import *

app = Ursina()
cube=Entity(
    model="cube",
    texture="white_cube",
    scale=2,
    rotation=(0,0,65),
    collider="box",
    )
cube = Entity(model='cube',color=hsv(300,1,1),scale=2,collider='box')
def spin():
    cube.animate('rotation_y', cube.rotation_y+360, duration=2,curve=curve.in_out_expo)
cube.on_click = spin
EditorCamera()
app.run()