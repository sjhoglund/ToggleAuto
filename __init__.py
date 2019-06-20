# -*- coding: utf-8 -*-
import time

from modules.kettle import *

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi

@cbpi.step
class ToggleAuto(StepBase):
    '''
    Just put the decorator @cbpi.step on top of a method
    '''
    # Properties
    temp = Property.Number("Temperature", configurable=True, description="Target Temperature of HLT")
    kettle = StepProperty.Kettle("Kettle", description="Set this to your HLT")
    toggle_type = Property.Select("Toggle Type", options=["On", "Off"])

    def init(self):
        '''
        Initialize Step. This method is called once at the beginning of the step
        :return:
        '''
        #self.notify("props", cbpi.cache.get("kettle")[int(self.kettle)].state, timeout=None)
        self.set_target_temp(self.temp, self.kettle)
        kettle_state = kettle = cbpi.cache.get("kettle")[int(self.kettle)].state
        if kettle_state is False and self.toggle_type == "On":
            Kettle2View().toggle(int(self.kettle))
            self.notify("Kettle Update", "Auto is on. Starting the next step.", timeout=None)
            self.next()
        else:
            if kettle_state is False and self.toggle_type == "Off":
                self.notify("Kettle Error", "Auto is already off, please adjust your brew step!", type="danger", timeout=None)
            else:
                if kettle_state is True:
                    if self.toggle_type == "On":
                        self.notify("Kettle Error", "Auto is already on, please adjust your brew step!", type="danger", timeout=None)
                    else:
                        Kettle2View().toggle(int(self.kettle))
                        self.notify("Kettle Update", "Auto is Off. Starting the next step.", timeout=None)
                        self.next()
