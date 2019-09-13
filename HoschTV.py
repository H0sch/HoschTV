import platform
import os
import sys
from datetime import datetime
import time
import acsys
import ac
import configparser
import csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
import keyboard
from classes import deflabel, defbutton, deftowerbox
from sim_info import info

def acMain(ac_version):
	global HTV_debug, HTV_debug_text, cars, d, p, session, t_0, N_, path
	global HTV_halo, HTV_halo_gear, HTV_halo_speed0, HTV_halo_speed1, HTV_halo_speed2, HTV_halo_throttle, HTV_halo_brake
	global HTV_tower, box

	path = "apps/python/HoschTV/"
	ac.log("HoschTV: 0")
	session = -1
	N_=50
	
	ac.initFont(0, "voxBOX", 0, 0)
	
	HTV_debug = ac.newApp("HTV Debug")
	ac.setSize(HTV_debug, 280, 500)
	HTV_debug_text = ac.addLabel(HTV_debug, "line 1 \nline 2")
	ac.setPosition(HTV_debug_text, 3, 30)
	ac.log("HoschTV: 1")
	
	path = "./apps/python/HoschTV/"
	cars = ac.getCarsCount()
	ac.log("HoschTV: 2")
	
	HTV_halo = ac.newApp("HTV Halo HUD")
	ac.setSize(HTV_halo, 1920, 676)
	ac.setTitle(HTV_halo, "")
	ac.setIconPosition(HTV_halo, 0, -10000)
	ac.setBackgroundTexture(HTV_halo, "apps/python/HoschTV/img/halo_t/back.png")
	
	HTV_tower = ac.newApp("HTV Tower")
	ac.setSize(HTV_tower, 320, 816)
	ac.setTitle(HTV_tower, "")
	ac.setIconPosition(HTV_tower, 0, -10000)
	
	ac.log("HoschTV: 2a")
	box = {}
	for i in range(24):
		box[i]= deftowerbox(HTV_tower, i)
		
	# box0 = defbutton(HTV_tower, "", 320, 34, 0, 0)
	ac.log("HoschTV: 2b")
	# ac.setBackgroundTexture(box0.btn, "apps/python/HoschTV/img/tower-back.png")
	# ac.log("HoschTV: 2c")
	# ac.drawBorder(box0.btn, 0)
	# ac.log("HoschTV: 2d")
	
	ACinfo = ac.newApp("HTV Info")
	ac.setSize(ACinfo, 400, 100)
	ac.setTitle(ACinfo, "")
	ac.setIconPosition(ACinfo, 0, -10000)
	
	# deflabel class(parent, text, size, posx, posy, font, align)
	HTV_halo_gear = deflabel(HTV_halo, "8", 170, 1120, 168, "voxbox", "center")
	HTV_halo_speed2 = deflabel(HTV_halo, "2", 67, 1075, 79, "voxbox", "center")
	HTV_halo_speed1 = deflabel(HTV_halo, "2", 67, 1120, 79, "voxbox", "center")
	HTV_halo_speed0 = deflabel(HTV_halo, "2", 67, 1165, 79, "voxbox", "center")
	ac.log("HoschTV: 3")
	# defbutton class(parent, text, sizex, sizey, posx, posy)
	HTV_halo_brake = defbutton(HTV_halo, "", 1920, 676, 0, 0)
	HTV_halo_throttle = defbutton(HTV_halo, "", 1920, 676, 0, 0)
	ac.log("HoschTV: 4")
	
	p={}
	ac.log("HoschTV: 4a")
	d={}
	ac.log("HoschTV: 4b")
	ac.log("HoschTV: cars={}".format(cars))
	for id in range(cars):
		ac.log("HoschTV: id={}".format(id))
		p[id] = int(id)
		ac.log("HoschTV: p[{}]".format(id))
		d[id] = driver(id)
		ac.log("HoschTV: d[{}]".format(id))
	ac.log("HoschTV: 5")
	

def acUpdate(dT):
	global session
	session = info.graphics.session
	
	for id in range(cars):
		if ac.getDriverName(id) != d[id].name:
			del d[id]
			d[id] = driver(id)
		driverUpdate(id)
	
	focus = ac.getFocusedCar()
	
	try:
		f()
		debug(focus)
	except Exception as e:
		ac.log("HoschTV ERROR: {}".format(e))
		ac.log("HoschTV ERROR: {}".format(sys.exc_info()))
	
	HTV_haloUpdate(focus)
	
	ac.console("HoschTV: acUpdate({}) complete".format(round(dT, 5)))

class MyException(Exception):
    pass

def f():
    raise MyException
		
def driverUpdate(id):
	if ac.isConnected(id) == 1:
		d[id].progress = round(ac.getCarState(id, acsys.CS.NormalizedSplinePosition), 3)
		d[id].speed = int(ac.getCarState(id, acsys.CS.SpeedKMH))
		d[id].gear = int(ac.getCarState(id, acsys.CS.Gear)-1)
		d[id].rpm = int(ac.getCarState(id, acsys.CS.RPM))
		d[id].lap = int(ac.getCarState(id, acsys.CS.LapCount))
		d[id].tyre = str(ac.getCarTyreCompound(id))
		
		d[id].timebest = ac.getCarState(id, acsys.CS.BestLap)/1000
		d[id].timelast = ac.getCarState(id, acsys.CS.LastLap)/1000
		d[id].pitline = int(ac.isCarInPitline(id))
		d[id].delta = round(ac.getCarState(id, acsys.CS.PerformanceMeter), 3)
		n = int(N_ * d[id].progress)
		d[id].sector[n] = round(time.time(),5)
		
		if session == 2: 
			d[id].position = ac.getCarRealTimeLeaderboardPosition(id)+1
		else: 
			d[id].position = ac.getCarLeaderboardPosition(id)
		
		pos = d[id].position
		lead = carpos(pos-1)
		m = n-1
		if m==-1: m=N_ - 1
		
		if lead:
			if session == 2:
				if d[id].position > 1:
					if ( d[id].lap == d[lead].lap or ( d[id].lap == d[lead].lap -1 and d[id].progress > d[lead].progress ) ):
						d[id].gap = round(d[id].sector[m] - d[lead].sector[m],3)
					else:
						d[id].gap = "+{}L".format(d[lead].lap - d[id].lap)
				else: 
					d[id].gap = "Lead"
			else: 
				d[id].gap = "Q"
		
		if d[id].progress > 0.85 and d[id].progress < 0.9:
			if d[id].laps <= d[id].lap:
				d[id].laps = d[id].lap + 1
				d[id].stint = d[id].stint + 1
		
		if d[id].pitline == 1 and d[id].speed == 0:
			if d[id].stint > 0:
				d[id].stints = d[id].stints + "{}[{}] ".format(d[id].tyre, d[id].stint)
				d[id].stint = int(0)
		
		if d[id].lastlap != d[id].lap:
			
		
			if session != 2:
				if d[id].timebest == d[id].timelast:
					d[id].tyre_q = d[id].tyre
			
			d[id].lastlap = d[id].lap 
	
	"""
	
	"""

def HTV_haloUpdate(focus):
	camera = ac.getCameraMode()	
	#camera 2= Center-Cam
	#camera 1= T-Cam
	
	if camera ==1 or camera ==2:
	
		gear = str(d[focus].gear)
		if gear == "0": gear = "n"
		elif gear == "-1": gear = "r"
		speed2 = int(d[focus].speed/100)
		speed1 = int(d[focus].speed/10)-(speed2*10)
		speed0 = int(d[focus].speed) - (speed1*10) - (speed2*100)
		if speed2 == 0: speed2 = ""
		if (speed1 == 0) and (speed2 == ""): speed1 = ""
		
		brake = round(20*ac.getCarState(focus, acsys.CS.Brake))
		throttle = round(20*ac.getCarState(focus, acsys.CS.Gas))
		
		if camera == 1:
			ac.setBackgroundTexture(HTV_halo, "apps/python/HoschTV/img/halo_t/back.png")
			# ac.setVisible(HTV_halo, 1)
			ac.setPosition(HTV_halo_gear.lbl, 1120, 168)
			ac.setPosition(HTV_halo_speed2.lbl, 1075, 79)
			ac.setPosition(HTV_halo_speed1.lbl, 1120, 79)
			ac.setPosition(HTV_halo_speed0.lbl, 1165, 79)
			ac.setBackgroundTexture(HTV_halo_brake.btn, "apps/python/HoschTV/img/halo_t/b{}.png".format(brake))
			ac.setBackgroundTexture(HTV_halo_throttle.btn, "apps/python/HoschTV/img/halo_t/t{}.png".format(throttle))
		elif camera == 2:
			ac.setBackgroundTexture(HTV_halo, "apps/python/HoschTV/img/halo_c/back.png")
			# ac.setVisible(HTV_halo, 1)
			ac.setPosition(HTV_halo_gear.lbl, 960, 168)
			ac.setPosition(HTV_halo_speed2.lbl, 915, 79)
			ac.setPosition(HTV_halo_speed1.lbl, 960, 79)
			ac.setPosition(HTV_halo_speed0.lbl, 1005, 79)
			ac.setBackgroundTexture(HTV_halo_brake.btn, "apps/python/HoschTV/img/halo_c/b{}.png".format(brake))
			ac.setBackgroundTexture(HTV_halo_throttle.btn, "apps/python/HoschTV/img/halo_c/t{}.png".format(throttle))
			
		ac.setText(HTV_halo_gear.lbl, str(gear))
		ac.setText(HTV_halo_speed2.lbl, str(speed2))
		ac.setText(HTV_halo_speed1.lbl, str(speed1))
		ac.setText(HTV_halo_speed0.lbl, str(speed0))

		ac.drawBorder(HTV_halo_throttle.btn, 0)
		ac.setBackgroundOpacity(HTV_halo_throttle.btn, 0)
		ac.drawBorder(HTV_halo_brake.btn, 0)
		ac.setBackgroundOpacity(HTV_halo_brake.btn, 0)
		ac.drawBorder(HTV_halo, 0)
		ac.setBackgroundOpacity(HTV_halo, 0)
			
	else:
		ac.setVisible(HTV_halo, 0)

class driver:
	def __init__(self, id):
		self.id = int(id)
		self.name = ac.getDriverName(id)
		self.progress = 0.0
		self.speed = int(0)
		self.gear = int(0)
		self.rpm = int(0)
		self.lap = int(0)
		self.lastlap = int(0)
		self.laps = int(0)
		self.tyre = ""
		self.tyre_q = ""
		self.timebest = int(0)
		self.timelast = int(0)
		self.stint = int(0)
		self.stints = ""
		self.pitline = int(0)
		self.delta = int(0)
		self.position = int(0)
		self.sector = {}
		for n in range(N_):
			self.sector[n] = 0.0
		self.gap = 0.0
		
		self.color_text = "000000"
		self.color_back = "FFFFFF"
		self.color_car = "0000FF"
		
def debug(focus):
	# n = int(N_*d[focus].progress)
	n = int(N_*d[focus].progress)-1
	if n == -1: n = N_ - 1
	txt = ""
	txt = txt + "{} (session)\n".format(session)
	txt = txt + "{} (camera)\n".format(ac.getCameraMode())
	txt = txt + "{} (id)\n".format(d[focus].id)
	# txt = txt + "{} (time)\n".format(datetime.now())
	txt = txt + "{} (time)\n".format(time.time())
	txt = txt + "{} (progress)\n".format(d[focus].progress)
	txt = txt + "{} (speed)\n".format(d[focus].speed)
	txt = txt + "{} (gear)\n".format(d[focus].gear)
	txt = txt + "{} (rpm)\n".format(d[focus].rpm)
	txt = txt + "{} (lap)\n".format(d[focus].lap)
	txt = txt + "{} (laps)\n".format(d[focus].laps)
	txt = txt + "{} (tyre)\n".format(d[focus].tyre)
	txt = txt + "{} (tyre_q)\n".format(d[focus].tyre_q)
	txt = txt + "{} (timebest)\n".format(d[focus].timebest)
	txt = txt + "{} (timelast)\n".format(d[focus].timelast)
	txt = txt + "{} (stint)\n".format(d[focus].stint)
	txt = txt + "{} (stints)\n".format(d[focus].stints)
	txt = txt + "{} (pitline)\n".format(d[focus].pitline)
	txt = txt + "{} (delta)\n".format(d[focus].delta)
	txt = txt + "{} (position)\n".format(d[focus].position)
	txt = txt + "{} (sector)\n".format(n)
	txt = txt + "{} (secor time )\n".format(d[focus].sector[n])
	txt = txt + "{} (gap)\n".format(d[focus].gap)
	ac.setText(HTV_debug_text, txt)
	ac.drawBackground(HTV_debug, 1)
	ac.drawBorder(HTV_debug, 0)
	
def carpos(pos):
	for id in range(cars):
		if d[id].position == pos:
			return d[id].id
	return
