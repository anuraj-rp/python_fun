from os.path import join, dirname
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

class Robot(object):

    def __init__(self):
        # Initial position is (0, 0)
        self.x = 0
        self.y = 0

    def __str__(self):
        return "Robot position is {}, {}.".format(self.x, self.y)

    def interpret(self, model):
        for c in model.commands:
            if c.__class__.__name__ == "InitialCommand":
                print("Setting position to: {}, {}".format(c.x, c.y))
                self.x = c.x
                self.y = c.y
            else:
                dir = c.direction
                print("Going {} for {} step(s).".format(dir, c.steps))

                move = {
                        "up": (0, 1),
                        "down": (0, -1),
                        "left": (-1, 0),
                        "right":(1, 0)
                        }[dir]
                self.x += c.steps * move[0]
                self.y += c.steps * move[1]

            print(self)

def move_command_processor(move_cmd):
    if move_cmd.steps == 0:
        move_cmd.steps = 1


def main():
    this_folder = dirname(__file__)
    robot_mm = metamodel_from_file(join(this_folder, 'robot.tx'), debug=False)
    robot_mm.register_obj_processors({'MoveCommand': move_command_processor})

    robot_model = robot_mm.model_from_file(join(this_folder, 'program.rbt'))
    robot = Robot()
    robot.interpret(robot_model)

if __name__ == "__main__":
    main()
