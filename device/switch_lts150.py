
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# switch.py - Alpaca API responders for Switch
#
# Author:   Jon Holtzman < holtz@nmsu.edu >
#
# -----------------------------------------------------------------------------
# Edit History:
#   Generated by Python Interface Generator for AlpycaDevice
#
# 27-Dec-2024   Initial edit

from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                StateValue, get_request_field, to_bool
from exceptions import *        # Nothing but exception classes

logger: Logger = None

from lts150 import Stage

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 1                      # Single instance

# -----------
# DEVICE INFO
# -----------
# Static metadata not subject to configuration changes
class Switch2Metadata:
    """ Metadata describing the Switch Device. Edit for your device"""
    Name = 'Thorlabs LTS Stage'
    Version = '1.0.0'
    Description = 'LTS Stage'
    DeviceType = 'Switch'
    DeviceID = '75a88d87-15da-4d2f-94ba-612cd5bb0fea'
    Info = 'Alpaca Sample Device\nImplements ISwitch\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 3

switch_dev = None
def start_switch_device(logger: logger):
    logger = logger
    global switch_dev
    switch_dev = Stage(logger=logger)

# --------------------
# RESOURCE CONTROLLERS
# --------------------

@before(PreProcessRequest(maxdev))
class action:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandblind:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandbool:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandstring:
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class connect:
    def on_put(self, req: Request, resp: Response, devnum: int):
        try:
            # ------------------------
            ### CONNECT THE DEVICE ###
            switch_dev.connect()
            # ------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Connect failed', ex)).json

@before(PreProcessRequest(maxdev))
class connected:
    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # -------------------------------------
            is_conn = switch_dev.connected ### READ CONN STATE ###
            # -------------------------------------
            resp.text = PropertyResponse(is_conn, req).json
        except Exception as ex:
            resp.text = MethodResponse(req, DriverException(0x500, 'Switch.Connected failed', ex)).json

@before(PreProcessRequest(maxdev))
class connecting:
    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ------------------------------
            val = switch_dev.connected ## GET CONNECTING STATE ##
            # ------------------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Connecting failed', ex)).json

@before(PreProcessRequest(maxdev))
class description:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(Switch2Metadata.Description, req).json

@before(PreProcessRequest(maxdev))
class devicestate:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ----------------------
            val = []
            # val.append(StateValue('## NAME ##', ## GET VAL ##))
            # Repeat for each of the operational states per the device spec
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'switch.Devicestate failed', ex)).json


class disconnect:
    def on_put(self, req: Request, resp: Response, devnum: int):
        try:
            # ---------------------------
            ### DISCONNECT THE DEVICE ###
            switch_dev.disconnect()
            # ---------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Disconnect failed', ex)).json

@before(PreProcessRequest(maxdev))
class driverinfo:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(Switch2Metadata.Info, req).json

@before(PreProcessRequest(maxdev))
class interfaceversion:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(Switch2Metadata.InterfaceVersion, req).json

@before(PreProcessRequest(maxdev))
class driverversion():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(Switch2Metadata.Version, req).json

@before(PreProcessRequest(maxdev))
class name():
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(Switch2Metadata.Name, req).json

@before(PreProcessRequest(maxdev))
class supportedactions:
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse([], req).json  # Not PropertyNotImplemented

@before(PreProcessRequest(maxdev))
class maxswitch:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        try:
            # ----------------------
            val = switch_dev.maxswitch ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Maxswitch failed', ex)).json

@before(PreProcessRequest(maxdev))
class canwrite:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev.canwrite(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Canwrite failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitch:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev.getswitch(id) ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitch failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitchdescription:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev.get_description(id) ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitchdescription failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitchname:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev.get_name(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitchname failed', ex)).json

@before(PreProcessRequest(maxdev))
class getswitchvalue:

    def on_get(self, req: Request, resp: Response, devnum: int):
        print('getswitchvalue on_get')
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        print('req: ',req)
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev.get_value(id) 
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Getswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class minswitchvalue:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev.get_minvalue(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Minswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class maxswitchvalue:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev.get_maxvalue(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Maxswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class switchstep:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = switch_dev.get_step(id)
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Switchstep failed', ex)).json

@before(PreProcessRequest(maxdev))
class setswitch:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not  switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        print('req: ', req)
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        print(id)
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        statestr = get_request_field('State', req)      # Raises 400 bad request if missing
        try:
            state = to_bool(statestr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'State {statestr} not a valid boolean.')).json
            return

        try:
            #resp.text = MethodResponse(req, NotImplementedException()).json
            # -----------------------------
            #switch_dev.set_switch(id)
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setswitch failed', ex)).json

@before(PreProcessRequest(maxdev))
class setswitchname:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        print('req: ', req)
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        name = get_request_field('Name', req)         # Raises 400 bad request if missing
        ### INTEPRET AS NEEDED OR FAIL ###  # Raise Alpaca InvalidValueException with details!
        try:
            resp.text = MethodResponse(req,
                            MethodNotImplemented(f'setswitch not implemented.')).json
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setswitchname failed', ex)).json

@before(PreProcessRequest(maxdev))
class setswitchvalue:

    def on_put(self, req: Request, resp: Response, devnum: int):
        print('setswitchvalue on_put')
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        print('req: ',req)
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        print('setswitchvalue on_put')
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        print('setswitchvalue on_put')
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        print('setswitchvalue on_put')
        valuestr = get_request_field('Value', req)      # Raises 400 bad request if missing
        try:
            value = float(valuestr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Value {valuestr} not a valid number.')).json
            return
        print('setswitchvalue on_put')
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        print('setswitchvalue on_put')
        try:
            # -----------------------------
            switch_dev.set_value(id,value)
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setswitchvalue failed', ex)).json

@before(PreProcessRequest(maxdev))
class canasync:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = False ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Canasync failed', ex)).json

@before(PreProcessRequest(maxdev))
class statechangecomplete:

    def on_get(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # ----------------------
            val = True ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Switch.Statechangecomplete failed', ex)).json

@before(PreProcessRequest(maxdev))
class cancelasync:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Cancelasync failed', ex)).json

@before(PreProcessRequest(maxdev))
class setasync:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        statestr = get_request_field('State', req)      # Raises 400 bad request if missing
        try:
            state = to_bool(statestr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'State {statestr} not a valid boolean.')).json
            return

        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setasync failed', ex)).json

@before(PreProcessRequest(maxdev))
class setasyncvalue:

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not switch_dev.connected :
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        
        idstr = get_request_field('Id', req)      # Raises 400 bad request if missing
        try:
            id = int(idstr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id {idstr} not a valid integer.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        valuestr = get_request_field('Value', req)      # Raises 400 bad request if missing
        try:
            value = float(valuestr)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Value {valuestr} not a valid number.')).json
            return
        if id < 0 or id > switch_dev.maxswitch -1 :
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Id " + idstr + " not in range.')).json
            return

        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Switch.Setasyncvalue failed', ex)).json

