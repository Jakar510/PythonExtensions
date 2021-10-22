from PythonExtensions.Json import *
from PythonExtensions.debug import *




pos = PlacePosition.Zero()
i = Size(1200, 1050)
v = Size(1280, 800)
p = PlacePosition.Zero()

print()
p.Set(-50, -50)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(-100, -100)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(-150, -150)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(-199, -199)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(-200, -200)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(-201, -201)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(-250, -250)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(-500, -500)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(-1000, -1000)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(0, 0)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(50, 50)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(100, 100)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(250, 250)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(500, 500)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)

print()
p.Set(1000, 1000)
PrettyPrint(pos=pos.Update(p, i, v, KeepInView=True), i=i, v=v, p=p)
