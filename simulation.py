from Box2D.examples.framework import (Framework, Keys, main)
from Box2D import (b2DistanceJointDef, b2EdgeShape, b2FixtureDef,
                   b2PolygonShape, b2CircleShape, b2RevoluteJointDef, b2_pi)
import Box2D
from random import randint

class PhySimulation(Framework):
    name = "PhySimulation"
    description = "A simple sandbox simulation made with Box2D Framework"
    bodies = []
    shift_moused = False
    moused = False

    def __init__(self):
        super(PhySimulation, self).__init__()
        ground = self.world.CreateBody(shapes=b2EdgeShape(vertices=[(-40, 0), (40, 0)]))

    def MouseDown(self, p):
        super(PhySimulation, self).MouseDown(p)
        if not self.shift_moused:
            self.moused = True
            if not self.mouseJoint:
                size = randint(1, 4)
                size = size if not size == 4 else 0.5
                fixture = b2FixtureDef(shape=b2PolygonShape(box=(size, size)), density=1, friction=0.4)
                self.bodies.append(self.world.CreateDynamicBody(position=p, fixtures=fixture))
            else:
                pass
        else:
            pass
        self.moused = False

    def ShiftMouseDown(self, p):
        if not self.moused:
            self.shift_moused = True
            if not self.mouseJoint:
                size = randint(0, 3)
#            size = size if not size == 3 else 0.5
                fixture = b2FixtureDef(shape=b2CircleShape(radius=size), density=1, friction=0.4)
                self.bodies.append(self.world.CreateDynamicBody(position=p, fixtures=fixture))
            else:
                pass
        else:
            pass
        self.shift_moused = False
main(PhySimulation)

