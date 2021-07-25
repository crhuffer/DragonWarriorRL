import datetime

from inputs import get_gamepad


# TODO: try to come up with a better name for this.

class HumanPresser:
    '''Provides a set of methods that allows a human to control the emulator and to update the model and Q-table as if
    the bot made the choices of actions. The method names picked for brevity to make it less verbose to use in an
    interactive interpreter.'''

    def __init__(self, actor):
        self.actor = actor

    def w(self, laststepwassuccessful=True, printtiming=True):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname['up'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()

    def a(self, laststepwassuccessful=True, printtiming=True):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname['left'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()

    def s(self, laststepwassuccessful=True, printtiming=True):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname['down'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()

    def d(self, laststepwassuccessful=True, printtiming=True):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname['right'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()

    def stairs(self, laststepwassuccessful=True, printtiming=True):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname['menucol0row2'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()

    def door(self, laststepwassuccessful=True, printtiming=True):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname['menucol1row2'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()

    def take(self, laststepwassuccessful=True, printtiming=True):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname['menucol1row3'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()

    def attack(self, laststepwassuccessful=True, printtiming=True):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname['menucol0row0'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()

    def b(self, laststepwassuccessful=True, printtiming=True):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname['B'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()

    def menu(self, columnnumber, rownumber):
        self.actor.doaction(self.actor.env.dict_comboactionsindextoname[f'menucol{columnnumber}row{rownumber}'])
        self.actor.dopostprocessingfrompreviousstep(dolearning=False)
        self.actor.env.render()


# %%

list_codestoignore = ['ABS_X', 'ABS_Y', 'ABS_RX', 'ABS_RY', 'SYN_REPORT', 'ABS_RZ', 'ABS_Z']
s = HumanPresser(actor=actor)

# %%

list_events = []
duration = datetime.timedelta(seconds=60 * 10)
now = datetime.datetime.now()
while datetime.datetime.now() < now + duration:
    events = get_gamepad()
    for event in events:
        if event.code not in list_codestoignore:
            if event.state != 0:
                print(event.ev_type, event.code, event.state)
                list_events.append([event.ev_type, event.code, event.state])
                # MessageBeep()
                if event.code == 'ABS_HAT0X':
                    if event.state == -1:
                        s.a()
                    else:
                        s.d()
                elif event.code == 'ABS_HAT0Y':
                    if event.state == -1:
                        s.w()
                    else:
                        s.s()

                elif event.code == 'BTN_THUMBR':
                    s.menu(1, 0)
                elif event.code == 'BTN_TR':
                    s.menu(1, 1)
                elif event.code == 'BTN_NORTH':
                    s.menu(1, 2)
                elif event.code == 'BTN_EAST':
                    s.menu(1, 3)

                elif event.code == 'BTN_THUMBL':
                    s.menu(0, 0)
                elif event.code == 'BTN_TL':
                    s.menu(0, 1)
                elif event.code == 'BTN_WEST':
                    s.menu(0, 2)
                elif event.code == 'BTN_SOUTH':
                    s.menu(0, 3)

                elif event.code == 'BTN_SELECT':
                    env.pressbutton('A')
                elif event.code == 'BTN_START':
                    env.pressbutton('B')

# %%

for index in range(1000):
    agent.learn()
agent.save_model()

# %%


# %%

# import inputs
#
# gamepad = inputs.devices.gamepads[0]
# gamepad.set_vibration(1, 0, 1000)
# %%


# # %%
#
# list_events = []
# duration = datetime.timedelta(seconds=10)
# now = datetime.datetime.now()
# while datetime.datetime.now() < now + duration:
#     events = get_gamepad()
#     for event in events:
#         print(event.ev_type, event.code, event.state)
#         list_events.append([event.ev_type, event.code, event.state])
#
#
# # %%
# import pandas as pd
# df = pd.DataFrame(list_events, columns=['eventtype', 'code', 'state'])
#
# # %%
#
# df['eventtype'].value_counts()
# df['code'].value_counts()
# df['state'].value_counts()
#
# # list_codestoignore = df['code'].unique()
# df.loc[:, ['code', 'state']].value_counts()

# %%

# dict_controllertohumanpresser = dict()
# dict_controllertohumanpresser['BTN_SOUTH']
# %%


# %%

if __name__ == '__main__':
    # The actor should already be set up using at least parts of run_dragon_warrior.py
    s = HumanPresser(actor=actor)

    # %%

    env.pressbutton('A')
    env.pressbutton('left')
    env.pressbutton('right')
    env.pressbutton('up')
    env.pressbutton('down')
    env.pressbutton('B')

    # %%

    s.d()
    s.take()
    s.d()
    s.take()
    s.d()
    [s.d() for index in range(3)]
    s.w()
    [s.w() for index in range(3)]
    s.a()
    s.a()
    s.take()
    s.d()
    s.d()
    s.s()
    [s.s() for index in range(5)]
    s.a()
    [s.a() for index in range(5)]
    s.s()
    s.door()
    s.s()
    s.s()
    s.d()
    [s.d() for index in range(5)]
    s.stairs()
    s.d()
    s.d()
    s.s()
    [s.s() for index in range(8)]
    s.a()
    [s.s() for index in range(6)]
