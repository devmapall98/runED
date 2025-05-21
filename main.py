import os
import sys
import time
import atexit
import ctypes
# import signal
import asyncio

from libs.setup import update, setup
from libs.classes import conf, debug, app, game, utils
from libs.consts import paths as p
from libs.consts import consts as c

from colorama import init as colorama_init
colorama_init()
from colorama import Fore as fg
from colorama import Style as st
########################################################################################

splashScreen = (
		f'{fg.LIGHTWHITE_EX}{st.BRIGHT}'
		f'                                  8888888888 8888888b.  \n'
		f'                                  888        888  "Y88b \n'
		f'                                  888        888    888 \n'
		f'        888d888 888  888 88888b.  8888888    888    888 \n'
		f'        888P"   888  888 888 "88b 888        888    888 \n'
		f'        888     888  888 888  888 888        888    888 \n'
		f'        888     Y88b 888 888  888 888        888  .d88P \n'
		f'        888      "Y88888 888  888 8888888888 8888888P"  \n'
		f'        \n{st.RESET_ALL}'
		f'=============================================================== \n'
		f' Version: {fg.LIGHTWHITE_EX}{c.VERSION['full']}{st.RESET_ALL}\n'
		f' Author:  @devmapall98 \n'
		f' License: UNLICENSE \n'
		f' GitHub:  {fg.LIGHTBLUE_EX}https://github.com/{c.GIT_REPO} {st.RESET_ALL}\n'
		f'=============================================================== \n'
)
print(splashScreen)

#=======================================================================================
# d8b          d8b 888    
# Y8P          Y8P 888    
#                  888    
# 888 88888b.  888 888888 
# 888 888 "88b 888 888    
# 888 888  888 888 888    
# 888 888  888 888 Y88b.  
# 888 888  888 888  "Y888

VR_STATUS = c.VR_STATUS

setup.run(setup.check())

# Set variables
apps 				= conf.load('apps')
settings 			= conf.load('settings')
vrSettings 			= conf.load('vrSettings')
vrMode				= settings['vrCompatible']

# Make list of enabled apps to run
enabledApps 		= conf.filter('apps','enabled')

# Make list of apps to run in VR based on `enabledApps`
vrApps 				= conf.filter('apps','vr')

if settings['checkUpdatesAtStartup']:
	# Check if the update file exists and if it is older than 1 day
	if os.path.exists(p.UPDATE):
		with open(p.UPDATE, 'r') as f:
			last_check = int(f.read())
		if time.time() - last_check > 86400*settings['checkUpdatesInterval']: # 86400 seconds = 1 day
			with open(p.UPDATE, 'w') as f:
				f.write(str(int(time.time())))
			# Check for updates
			status = update.check(update.getRelease(c.GIT_REPO), c.VERSION, c.GIT_REPO)
			if not status:
				os.remove(p.UPDATE)
	else:
		with open(p.UPDATE, 'w') as f:
			f.write(str(int(time.time())))
			# Check for updates
			status = update.check(update.getRelease(c.GIT_REPO), c.VERSION, c.GIT_REPO)
		if not status:
			os.remove(p.UPDATE)
#//
#=======================================================================================



#=======================================================================================
#
#  .d888                            888    d8b                            
# d88P"                             888    Y8P                            
# 888                               888                                   
# 888888 888  888 88888b.   .d8888b 888888 888  .d88b.  88888b.  .d8888b  
# 888    888  888 888 "88b d88P"    888    888 d88""88b 888 "88b 88K      
# 888    888  888 888  888 888      888    888 888  888 888  888 "Y8888b. 
# 888    Y88b 888 888  888 Y88b.    Y88b.  888 Y88..88P 888  888      X88 
# 888     "Y88888 888  888  "Y8888P  "Y888 888  "Y88P"  888  888  88888P' 

# Run apps depending on vrMode
def run_apps() -> list[ dict[str, bool] ]:
	"""
	***ASYNCHRONOUS, REMEMBER TO AWAIT()*** \n
	Runs all apps from `.yaml` config based on conditions: \n
	- Is VR running?\n
	- Is the setting for different app set for VR True?\n
	- Is the app `enabled` in config?
	"""
	startedApps = list(())
	if VR_STATUS:
		if vrMode:
			for i in vrApps:
				if i['enabled']:
					utils.uprint(i['name'] + " is starting.", 'debug')
					startedApps.append(asyncio.run(app.run(i)))
		else:
			for i in enabledApps:
				utils.uprint(i['name'] + " is starting.", 'debug')
				startedApps.append(asyncio.run(app.run(i)))
	else:
		for i in enabledApps:
			utils.uprint(i['name'] + " is starting.", 'debug')
			startedApps.append(asyncio.run(app.run(i)))

	return startedApps
#//

# Run on app exit
def exit_handler() -> None:
	"""
	Kills all tracked(`enabled`), running apps before terminating runED.
	"""
	if VR_STATUS:
		if vrMode:
			for i in vrApps:
				if i['enabled']:
					if app.check(i):
						app.kill(i)
		else:
			for i in enabledApps:
				if app.check(i):
					app.kill(i)
	else:
		for i in enabledApps:
			if app.check(i):
				app.kill(i)
	# for i in apps:
	# 	if app.check(i):
	# 		app.kill(i)
	utils.uprint('Apps closed.')
	debug.pause(breathe = True)
#//
#=======================================================================================






















#=======================================================================================
#=======================================================================================
#=======================================================================================
#
#                        d8b          
#                        Y8P          
#                                    
# 88888b.d88b.   8888b.  888 88888b.  
# 888 "888 "88b     "88b 888 888 "88b 
# 888  888  888 .d888888 888 888  888 
# 888  888  888 888  888 888 888  888 
# 888  888  888 "Y888888 888 888  888
def main() -> None:
	run_apps() # Run apps
	game.setup(VR_STATUS) # Set up stuff for VR

	asyncio.run(game.launch(VR_STATUS)) # Run Elite Dangerous

	game.awaitGameStart(c.GAME_EXE) # Await game start
	game.awaitGameEnd(c.GAME_EXE) # Await game finish

	debug.pause('GAME CLOSED', True)
#//
#=======================================================================================
#=======================================================================================
#=======================================================================================



























































#=======================================================================================
#
#               888               d8b          
#               888               Y8P          
#               888                            
#  8888b.   .d88888 88888b.d88b.  888 88888b.  
#     "88b d88" 888 888 "888 "88b 888 888 "88b 
# .d888888 888  888 888  888  888 888 888  888 
# 888  888 Y88b 888 888  888  888 888 888  888 
# "Y888888  "Y88888 888  888  888 888 888  888

# Check elevation status and run the program with admin rights if needed
def is_admin() -> bool:
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

# # Handle Ctrl+C gracefully
# def signal_handler(signum, frame) -> None:
# 	print(frame, 'debug')
# 	print(signum, 'debug')
# 	utils.uprint('Ctrl+C detected. Shutting down...', 'warn')
# 	sys.exit(0)
# #//

def start() -> None:
	# signal.signal(signal.SIGINT, signal_handler)
	if settings['closeAppsOnExit']:
		atexit.register(exit_handler)
	main()
	utils.uprint('runED will now close. Bye!')
	time.sleep(5)
	sys.exit(0)
#//

# Lets go
if is_admin():
	VR_STATUS = game.checkVr() # Check if VR is running
	start()
else:
	# Re-run the program with admin rights
	if settings['runElevated'] == 1:
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
	else:
		VR_STATUS = game.checkVr() # Check if VR is running
		start()
#=======================================================================================
