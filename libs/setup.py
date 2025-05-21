import os
import sys
import yaml
import time
import requests
import subprocess

from libs.classes import utils, debug
from libs.consts import paths as p
from libs.consts import consts as c

from colorama import init as colorama_init
colorama_init()
from colorama import Fore as fg
from colorama import Style as st

# No file or directory logging, no job header or summary, no class or size info, no progress info, include same files, include tweaked files
# and only copy files that are newer or have different size.
robocopyArgs = '/NFL /NDL /NJH /NJS /nc /ns /np /IS /IT /IM'

escape_dict = {
	'\a':r'\a',
	'\b':r'\b',
	'\\c':r'\c',
	'\f':r'\f',
	'\n':r'\n',
	'\r':r'\r',
	'\t':r'\t',
	'\v':r'\v',
	'\'':r'\'',
	'\"':r'\"'
}
########################################################################################

class update():
	def check(latest_release_dict, VERSION, GIT_REPO) -> None:
		if latest_release_dict is None:
			return False
		if latest_release_dict['major'] > VERSION['major'] \
			or latest_release_dict['minor'] > VERSION['minor'] \
			or latest_release_dict['patch'] > VERSION['patch']:
			print(
				f'{st.RESET_ALL}{fg.LIGHTGREEN_EX} A new version of runED is available!{st.RESET_ALL}\n'
				f'{st.RESET_ALL}{fg.LIGHTWHITE_EX} Your version: {fg.LIGHTYELLOW_EX}'
				f'{latest_release_dict["channel"]}/{VERSION["major"]}.{VERSION["minor"]}.{VERSION["patch"]}{st.RESET_ALL}\n'
				f'{st.RESET_ALL}{fg.LIGHTWHITE_EX} Latest version: {fg.LIGHTGREEN_EX}{st.BRIGHT}'
				f'{VERSION["channel"]}/{latest_release_dict["major"]}.{latest_release_dict["minor"]}.{latest_release_dict["patch"]}{st.RESET_ALL}\n'
				f'{st.RESET_ALL}{fg.LIGHTWHITE_EX} You can find it here: \n{fg.LIGHTBLUE_EX}'
				f'     https://github.com/{GIT_REPO}/releases/latest {st.RESET_ALL}\n'
			)
			print('=============================================================== \n\n\n')
			return False
		else:
			print(
				f'{st.RESET_ALL}{fg.LIGHTWHITE_EX} You are using the latest version of runED.\n{st.RESET_ALL}'
			)
			print('=============================================================== \n\n\n')
			return True
	#//

	def getRelease(GIT_REPO) -> str | None:
		try:
			response = requests.get(f'https://api.github.com/repos/{GIT_REPO}/releases/latest')
			if response.status_code != 200:
				utils.uprint(f'Error when checking for updates: HTTP/{response.status_code}', 'error')
				return None
			else:
				latest_release_str = response.json()['tag_name'].split('/')[-1]
				latest_release = {
					'major'  : latest_release_str.split('.')[0],
					'minor'  : latest_release_str.split('.')[1],
					'patch'  : latest_release_str.split('.')[2],
					'channel': response.json()['tag_name'].split('/')[0],
				}
				return latest_release
		except requests.RequestException as e:
			utils.uprint(f'Error when checking for updates: {e}','error')
			return None
	#//
#//

class setup():
	def __raw(text) -> str  | None:
		"""Returns a raw string from user input"""
		new_string=''
		for char in text:
			try: 
				new_string += escape_dict[char]
			except KeyError: 
				new_string += char
		return new_string
	#//

	def getUserInput(title, prompt) -> str | None:
		"""Get user input and return it as a string"""
		utils.uprint(f'{title}')
		return input(prompt)
	#//

	def getUserInputRaw(title, prompt) -> str | None:
		"""Get user input and return it as a raw string"""
		utils.uprint(f'{title}')
		return setup.__raw(input(prompt))
	#//

	def check() -> dict[str, bool]:
		"""Check if the config file and ed-options-backup folder exist"""
		configExists = os.path.isfile(p.CONFIG)
		edOptionsExists = os.path.isdir(p.ED_OPTIONS_BACKUP)
		return {'config': configExists, p.ED_OPTIONS_BACKUP: edOptionsExists}
	#//

	def run(checked) -> None:
		if not checked['config']:

			utils.uprint(
				'Hi! Since this is the first time you have started runED we have a few things to configure.',
				'info'
			)
			utils.uprint(
				'This setup will have 3 parts:\n'
				'                               '
				f'{st.RESET_ALL}{st.DIM}1. {st.RESET_ALL}'
				f'{fg.LIGHTWHITE_EX}{st.BRIGHT}Main Settings\n'
				'                               '
				f'{st.RESET_ALL}{st.DIM}2. {st.RESET_ALL}'
				f'{fg.LIGHTWHITE_EX}{st.BRIGHT}Applications {st.RESET_ALL}{fg.LIGHTGREEN_EX}{st.DIM}(required){st.RESET_ALL}\n'
				'                               '
				f'{st.RESET_ALL}{st.DIM}3. {st.RESET_ALL}'
				f'{fg.LIGHTWHITE_EX}{st.BRIGHT}Elite Dangerous Options {st.RESET_ALL}{fg.LIGHTBLUE_EX}{st.DIM}(VR related settings - optional){st.RESET_ALL}'
				'\n',
				'info'
			)
			utils.uprint(
				'Follow the instructions. runED will exit after setup is completed.',
				'info'
			)
			utils.uprint(
				f'{st.RESET_ALL}{st.BRIGHT}{fg.LIGHTWHITE_EX}You will have to relaunch it MANUALLY.\n{st.RESET_ALL}'
				f'{st.RESET_ALL}{st.DIM}                           If you want to change the settings later, you can do so by editing the config file.{st.RESET_ALL}\n'
				f'{st.DIM}                           You can find it in "{p.CONFIG}".{st.RESET_ALL}',
				'warn'
			)
			outnull = input(
				f'                           {st.RESET_ALL}Press {fg.YELLOW}<{fg.LIGHTGREEN_EX}ENTER{st.RESET_ALL}{fg.YELLOW}>{st.RESET_ALL} to start setup...\n'
			)

			# Handle invalid input and reset variables
			def handle_invalid_input(default_value, message, reset_value=None):
				"""
				Handles invalid input by printing a message and returning a default value or a tuple of default and reset values.
				"""
				utils.uprint(message, 'info')
				return default_value if reset_value is None else (default_value, reset_value)
			#//

			#### PRE SETUP ####
			defaultSettings = False
			while defaultSettings not in ['y', 'Y', 'n', 'N']:
				print('\n')
				if defaultSettings == '72756E4544':
					utils.uprint(
						'Here are the defaults:\n'
						f'                           - Check for updates at startup: {st.RESET_ALL}{fg.LIGHTGREEN_EX}True{st.RESET_ALL}\n'
						f'                           - Check for updates interval: {st.RESET_ALL}{fg.LIGHTGREEN_EX}every month{st.RESET_ALL}\n'
						f'                           - Separate VR profile: {st.RESET_ALL}{fg.LIGHTRED_EX}False{st.RESET_ALL}\n'
						f'                           - Run elevated: {st.RESET_ALL}{fg.LIGHTRED_EX}False{st.RESET_ALL}\n'
						f'                           - Close launched apps on exit: {st.RESET_ALL}{fg.LIGHTRED_EX}False{st.RESET_ALL}\n'
						f'                           - Game start timeout: {st.RESET_ALL}{fg.LIGHTBLUE_EX}30{st.RESET_ALL} seconds\n',
						'info'
					)

				defaultSettings = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTGREEN_EX}Setup 1 - Main Settings - {st.BRIGHT}DEFAULTS{st.RESET_ALL}',
					f'Do you want to use the default settings?\n'
					f'{st.RESET_ALL}{st.DIM}This skips most of the setup, but you\'ll still be asked to set up at least one app to use runED.{st.RESET_ALL}\n'
					f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes, '
					f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no, and '
					f'{fg.YELLOW}"{fg.LIGHTBLUE_EX}show{fg.YELLOW}"{st.RESET_ALL} to show the default settings: '
				)

				match defaultSettings:
					case 'y' | 'Y':
						utils.uprint(f'You selected: {fg.BLUE}Yes{st.RESET_ALL}', 'info')
					case 'n' | 'N':
						utils.uprint(f'You selected: {fg.BLUE}No{st.RESET_ALL}', 'info')
					case 'show' | 'SHOW' | 'Show' | 's' | 'S':
						defaultSettings = '72756E4544'
						print('\n')
						print('\n')
						print('\n')
					case _:
						defaultSettings = handle_invalid_input(
							False, 'Invalid input, please try again.'
						)
			if defaultSettings in ['y', 'Y']:
				defaultSettings = True
			else:
				defaultSettings = False
			###################

			##### SETUP 1 #####
			# 1
			if not defaultSettings:
				checkUpdatesAtStartup = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTGREEN_EX}Setup 1 - Main Settings - Step 1 of 6{st.RESET_ALL}',
					f'Check for updates on startup?\n'
					f'{st.RESET_ALL}{st.DIM}Default is True.{st.RESET_ALL}\n'
					f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes or '
					f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no: '
				)
				if checkUpdatesAtStartup not in ['y', 'Y', 'n', 'N']:
					checkUpdatesAtStartup = handle_invalid_input(
						False, f'Invalid input, using default value "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".'
					)
				else:
					checkUpdatesAtStartup = checkUpdatesAtStartup in ['y', 'Y']
					utils.uprint(f'You selected: {fg.BLUE}{"Yes" if checkUpdatesAtStartup else "No"}{st.RESET_ALL}', 'info')

				# 2
				if checkUpdatesAtStartup:
					print('\n')
					checkUpdatesInterval = setup.getUserInput(
						f'{st.RESET_ALL}{fg.LIGHTGREEN_EX}Setup 1 - Main Settings - Step 2 of 6{st.RESET_ALL}',
						'How often do you want to check for updates?\n'
						f'{st.RESET_ALL}{st.DIM}Default is 7 (every 7 days).{st.RESET_ALL}\n'
						f'Type a {fg.CYAN}number of days{st.RESET_ALL} to wait between update checks: '
					)
					if not checkUpdatesInterval.isdigit():
						checkUpdatesInterval = handle_invalid_input(
							0, f'Invalid input, using default value of {st.RESET_ALL}{fg.LIGHTMAGENTA_EX}7 days{st.RESET_ALL}.'
						)
					else:
						checkUpdatesInterval = int(checkUpdatesInterval)
						utils.uprint(f'You selected: {fg.BLUE}{checkUpdatesInterval}{st.RESET_ALL} {fg.CYAN}days{st.RESET_ALL}', 'info')
				else:
					print('\n')
					utils.uprint(
						f'{st.RESET_ALL}{fg.LIGHTGREEN_EX}Setup 1 - Main Settings - Step 2 of 6{st.RESET_ALL}'
					)
					utils.uprint(
						'Skipping Step 2 based on previous input.',
						'info'
					)
					checkUpdatesInterval = 7

				# 3
				print('\n')
				vrCompatible = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTGREEN_EX}Setup 1 - Main Settings - Step 3 of 6{st.RESET_ALL}',
					f'Do you want to run different lists of apps for VR and desktop gaming?\n'
					f'{st.RESET_ALL}{st.DIM}Default is False.{st.RESET_ALL}\n'
					f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes or '
					f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no: '
				)
				if vrCompatible not in ['y', 'Y', 'n', 'N']:
					vrCompatible = handle_invalid_input(False, f'Invalid input, using default value "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".')
				else:
					vrCompatible = vrCompatible in ['y', 'Y']
					utils.uprint(f'You selected: {fg.BLUE}{"Yes" if vrCompatible else "No"}{st.RESET_ALL}', 'info')

				# 4
				print('\n')
				runElevated = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTGREEN_EX}Setup 1 - Main Settings - Step 4 of 6{st.RESET_ALL}',
					f'Do you need to use runED with admin privileges?\n'
					f'{st.RESET_ALL}{fg.LIGHTBLACK_EX}This might be needed for some apps. {st.BRIGHT}Don\'t use this if you don\'t need this.{st.RESET_ALL}\n'
					f'{st.RESET_ALL}{st.DIM}Default is False.{st.RESET_ALL}\n'
					f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes or '
					f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no: '
				)
				if runElevated not in ['y', 'Y', 'n', 'N']:
					runElevated = handle_invalid_input(False, f'Invalid input, using default value "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".')
				else:
					runElevated = runElevated in ['y', 'Y']
					utils.uprint(f'You selected: {fg.BLUE}{"Yes" if runElevated else "No"}{st.RESET_ALL}', 'info')

				# 5
				print('\n')
				closeAppsOnExit = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTGREEN_EX}Setup 1 - Main Settings - Step 5 of 6{st.RESET_ALL}',
					f'Close all applications when runED exits?\n'
					f'{st.RESET_ALL}{st.DIM}runED will attempt to close only the apps it launched itself.{st.RESET_ALL}\n'
					f'{st.RESET_ALL}{st.DIM}Default is False.{st.RESET_ALL}\n'
					f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes or '
					f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no: '
				)
				if closeAppsOnExit not in ['y', 'Y', 'n', 'N']:
					closeAppsOnExit = handle_invalid_input(False, f'Invalid input, using default value "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".')
				else:
					closeAppsOnExit = closeAppsOnExit in ['y', 'Y']
					utils.uprint(f'You selected: {fg.BLUE}{"Yes" if closeAppsOnExit else "No"}{st.RESET_ALL}', 'info')

				# 6
				print('\n')
				gameStartTimeout = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTGREEN_EX}Setup 1 - Main Settings - Step 6 of 6{st.RESET_ALL}',
					f'How long should runED give Elite to launch before timing out?\n'
					f'{st.RESET_ALL}{st.DIM}If Elite doesn\'t launch in time try increasing this in the config file found in {p.CONFIG}".{st.RESET_ALL}\n'
					f'{st.RESET_ALL}{st.DIM}Default is 60 seconds.{st.RESET_ALL}\n'
					f'Type the desired time in {fg.CYAN}seconds{st.RESET_ALL}: '
				)
				if not gameStartTimeout.isnumeric():
					gameStartTimeout = handle_invalid_input(
						60,
						f'Invalid input, using default value of {st.RESET_ALL}{fg.LIGHTMAGENTA_EX}60 seconds{st.RESET_ALL}.'
					)
				else:
					gameStartTimeout = int(gameStartTimeout)
					utils.uprint(f'You selected: {fg.BLUE}{int(gameStartTimeout)}{st.RESET_ALL} {fg.CYAN}seconds{st.RESET_ALL}', 'info')
			else:
				utils.uprint(
					f'Skipping {st.RESET_ALL}{fg.LIGHTGREEN_EX}Setup 1 - Main Settings{st.RESET_ALL} based on previous input.',
					'info'
				)
				checkUpdatesAtStartup = True
				checkUpdatesInterval = 7
				vrCompatible = False
				runElevated = False
				closeAppsOnExit = False
				gameStartTimeout = 60
			###################

			print('\n')
			print('\n')
			print('\n')

			##### SETUP 2 #####
			# 1
			appName = setup.getUserInput(
				f'{st.RESET_ALL}{fg.LIGHTBLUE_EX}Setup 2 - Applications - Step 1 of 4{st.RESET_ALL}',
				f'{st.BRIGHT}runED needs at least one application to manage.{st.RESET_ALL}\n'
				f'{st.RESET_ALL}{fg.LIGHTBLUE_EX}Name of the app{st.RESET_ALL} you want to run: '
			)
			if not appName or not appName.isalnum() or appName == '':
				appName = handle_invalid_input(
					'App1',
					f'No name entered, using default name "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}App1{st.RESET_ALL}."'
				)
			else:
				gameStartTimeout = int(gameStartTimeout)
				utils.uprint(f'You selected: {fg.BLUE}{appName}{st.RESET_ALL}', 'info')

			# 2
			appPath = ''
			i = 0
			while appPath == '' or not appPath or not os.path.isfile(appPath):
				print('\n')
				if appPath == '' and i > 0 or not os.path.isfile(appPath) and i > 0:
					utils.uprint(f'{st.RESET_ALL}{fg.LIGHTWHITE_EX}Path not entered or invalid. This step is {st.BRIGHT}required.{st.RESET_ALL}', 'warn')
				appPath = setup.getUserInputRaw(
					f'{st.RESET_ALL}{fg.LIGHTBLUE_EX}Setup 2 - Applications - Step 2 of 4{st.RESET_ALL}',
					f'{st.RESET_ALL}{st.BRIGHT}{fg.LIGHTWHITE_EX}Path{st.RESET_ALL} to the application executable: '
				)
				i += 1

			# 3
			if closeAppsOnExit:
				print('\n')
				appForceKill = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTBLUE_EX}Setup 2 - Applications - Step 3 of 4{st.RESET_ALL}',
					f'When closing this app, should runED force-kill it? (necessary for some apps)\n'
					f'{st.RESET_ALL}{st.DIM}Default is False.{st.RESET_ALL}\n'
					f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes or '
					f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no: '
				)
				if appForceKill not in ['y', 'Y', 'n', 'N']:
					appForceKill = handle_invalid_input(
						False,
						f'Invalid input, using default value "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".'
					)
				else:
					appForceKill = appForceKill in ['y', 'Y']
					utils.uprint(f'You selected: {fg.BLUE}{"Yes" if appForceKill else "No"}{st.RESET_ALL}', 'info')
			else:
				print('\n')
				utils.uprint(
					f'Skipping {st.RESET_ALL}{fg.LIGHTBLUE_EX}Setup 2 - Applications - Step 3 of 4{st.RESET_ALL} based on previous input: "do not close apps on runEDexit"',
					'info'
				)
				appForceKill = False

			if vrCompatible:
				# 4
				print('\n')
				appVr = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTBLUE_EX}Setup 2 - Applications - Step 4 of 4{st.RESET_ALL}',
					f'Run this app when you play in VR?\n'
					f'{st.RESET_ALL}{st.DIM}Default is False.{st.RESET_ALL}\n'
					f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes or '
					f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no: '
				)
				if appVr not in ['y', 'Y', 'n', 'N']:
					appVr = handle_invalid_input(
						False,
						f'Invalid input, using default value "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".'
					)
				else:
					appVr = appVr in ['y', 'Y']
					utils.uprint(f'You selected: {fg.BLUE}{"Yes" if appVr else "No"}{st.RESET_ALL}', 'info')
			else:
				print('\n')
				utils.uprint(
					f'Skipping {st.RESET_ALL}{fg.LIGHTBLUE_EX}Setup 2 - Applications - Step 4 of 4{st.RESET_ALL} based on previous input: "no different lists of apps for VR and desktop gaming".',
					'info'
				)
				appVr = False
			###################

			
			print('\n')
			print('\n')
			print('\n')

			##### SETUP 3 #####
			if vrCompatible:
				# 1
				print('\n')
				edOptionsFolderCopy = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTYELLOW_EX}Setup 3 - Elite Dangerous Options - Step 1{st.RESET_ALL}',
					f'Do you use different graphics settings for VR and desktop gaming?\n'
					f'Next couple of steps will help you automate this.\n'
					f'{st.RESET_ALL}{st.DIM}Default is False.{st.RESET_ALL}\n'
					f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes or '
					f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no: '
				)
				if edOptionsFolderCopy == 'y' or edOptionsFolderCopy == 'Y':
					edOptionsFolderCopy = True
				elif edOptionsFolderCopy == 'n' or edOptionsFolderCopy == 'N':
					edOptionsFolderCopy = False
				else:
					edOptionsFolderCopy = False
					utils.uprint(f'Invalid input, using default value "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".', 'warn')
				utils.uprint(f'You selected: {fg.BLUE}{"Yes" if edOptionsFolderCopy else "No"}{st.RESET_ALL}', 'info')

				# 2
				if edOptionsFolderCopy:
					print('\n')
					edGraphicsOptionsDefaultPath = 'C:\\Users\\YOUR_USERNAME\\AppData\\Local\\Frontier Developments\\Elite Dangerous\\Options\\Graphics'
					edOptionsFolderPath = setup.getUserInputRaw(
						f'{st.RESET_ALL}{fg.LIGHTYELLOW_EX}Setup 3 - Elite Dangerous Options - Step 2{st.RESET_ALL}',
						f'Path to the Elite Dangerous graphics options folder\n'
						f'(located at: "{st.RESET_ALL}{st.BRIGHT}{edGraphicsOptionsDefaultPath}{st.RESET_ALL}"): '
					)

					if edOptionsFolderPath == '' or not (edOptionsFolderPath.split('\\')[-1] == 'Graphics' and os.path.isdir(edOptionsFolderPath)):
						edOptionsFolderCopy, edOptionsFolderPath = handle_invalid_input(
							False,
							f'Invalid path or no path entered, reverting previous step to "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".'
							)
						return

					if os.path.isdir(p.ED_OPTIONS_BACKUP):
						utils.uprint(
							f'runED just checked and the backup folder already exists at '
							f'"{st.RESET_ALL}{st.BRIGHT}{fg.LIGHTGREEN_EX}{p.ED_OPTIONS_BACKUP}{st.RESET_ALL}".\nNo need to create it again.',
							'info'
							)
						return

					
					print('\n')
					utils.uprint(
						f'To use this feature you\'ll need to follow below instructions {st.BRIGHT}carefully{st.RESET_ALL}.',
						'info'
					)
					utils.uprint(
						f'{st.RESET_ALL}{st.BRIGHT}{fg.LIGHTWHITE_EX}If this step fails, the option of swapping the settings automatically will be '
						f'{fg.LIGHTRED_EX}disabled{st.RESET_ALL}{st.BRIGHT}{fg.LIGHTWHITE_EX}.{st.RESET_ALL}',
						'warn'
					)
					outnull = input(f'{st.RESET_ALL}Press {fg.YELLOW}<{fg.LIGHTGREEN_EX}ENTER{st.RESET_ALL}{fg.YELLOW}>{st.RESET_ALL} when you are ready to continue...\n')

					utils.uprint(
						f'{st.RESET_ALL}{st.DIM}1. {st.RESET_ALL}'
						f'{fg.LIGHTWHITE_EX}Open Elite Dangerous and set the graphical settings you want to use for {st.BRIGHT}desktop{st.NORMAL} play.{st.RESET_ALL}\n'
						f'{st.RESET_ALL}{st.DIM}                  2. {st.RESET_ALL}'
						f'{fg.LIGHTWHITE_EX}Close Elite Dangerous.{st.RESET_ALL}',
					)
					setAndClosed1 = input(
						f'{st.RESET_ALL}                  After you\'re done, please type {fg.LIGHTMAGENTA_EX}SET AND CLOSED{st.RESET_ALL} to continue: '
					)
					if setAndClosed1 not in ['SET AND CLOSED', 'set and closed', 'Set and Closed']:
						edOptionsFolderCopy, edOptionsFolderPath = handle_invalid_input(
							False,
							f'Invalid input, reverting previous step to "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".'
						)
						return
					print('\n')
					utils.uprint('runED will now copy the desktop play settings to its backup folder. Standby...', 'info')
					subprocess.Popen(f"robocopy \"{edOptionsFolderPath}\" \"{p.ED_OPTIONS_BACKUP}\\nonvr-ed-options\" \"*\" {robocopyArgs}")
					time.sleep(5)
					utils.uprint(f'{st.RESET_ALL}{st.BRIGHT}{fg.LIGHTGREEN_EX}runED has copied the desktop play settings.{st.RESET_ALL}', 'info')
					time.sleep(3)
					graphicsOptionsSavedNonVr = True

					print('\n')
					utils.uprint(
						f'{st.RESET_ALL}{st.DIM}1. {st.RESET_ALL}'
						f'{fg.LIGHTWHITE_EX}Open Elite Dangerous and set the graphical settings you want to use for {st.BRIGHT}VR{st.NORMAL}.{st.RESET_ALL}\n'
						f'{st.RESET_ALL}{st.DIM}                  2. {st.RESET_ALL}'
						f'{fg.LIGHTWHITE_EX}Close Elite Dangerous.{st.RESET_ALL}'
					)
					setAndClosed2 = input(
						f'{st.RESET_ALL}                  After you\'re done, please type {fg.LIGHTMAGENTA_EX}SET AND CLOSED{st.RESET_ALL} to continue: '
					)
					if setAndClosed2 not in ['SET AND CLOSED', 'set and closed', 'Set and Closed']:
						edOptionsFolderCopy, edOptionsFolderPath = handle_invalid_input(
							False,
							f'Invalid input, reverting previous step to "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".'
						)
						return
					print('\n')
					utils.uprint('runED will now copy the VR settings to its backup folder. Standby...', 'info')
					subprocess.Popen(f"robocopy \"{edOptionsFolderPath}\" \"{p.ED_OPTIONS_BACKUP}\\vr-ed-options\" \"*\" {robocopyArgs}")
					time.sleep(5)
					utils.uprint(f'{st.RESET_ALL}{st.BRIGHT}{fg.LIGHTGREEN_EX}runED has copied the VR settings.{st.RESET_ALL}', 'info')
					time.sleep(3)
					graphicsOptionsSavedVr = True
					edOptionsFolderCopy = True
					print('\n')

				else:
					edOptionsFolderPath = False
					graphicsOptionsSavedNonVr = False
					graphicsOptionsSavedVr = False

				# 3
				print('\n')
				oculusCheck = setup.getUserInput(
					f'{st.RESET_ALL}{fg.LIGHTYELLOW_EX}Setup 3 - Elite Dangerous Options - Step 3{st.RESET_ALL}',
					f'Are you using Oculus as your VR headset?\n'
					f'{st.RESET_ALL}{st.DIM}Default is False.{st.RESET_ALL}\n'
					f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes or '
					f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no: '
				)
				if oculusCheck not in ['y', 'Y', 'n', 'N']:
					oculusASWoff, oculusCLIpath = handle_invalid_input(
						False,
						f'Invalid input, using default value "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".'
					)
				# 4
				elif oculusCheck in ['y', 'Y']:
					utils.uprint(f'You selected: {fg.BLUE}{"Yes" if oculusCheck in ["y", "Y"] else "No"}{st.RESET_ALL}', 'info')
					print('\n')
					oculusASWoff = setup.getUserInput(
						f'{st.RESET_ALL}{fg.LIGHTYELLOW_EX}Setup 3 - Elite Dangerous Options - Step 4{st.RESET_ALL}',
						f'Do you want to disable ASW after the game starts?\n'
						f'{st.RESET_ALL}{st.DIM}Default is False.{st.RESET_ALL}\n'
						f'Type {fg.YELLOW}"{fg.LIGHTGREEN_EX}Y{fg.YELLOW}"{st.RESET_ALL} for yes or '
						f'{fg.YELLOW}"{fg.LIGHTRED_EX}N{fg.YELLOW}"{st.RESET_ALL} for no: '
					)
					if oculusASWoff not in ['y', 'Y', 'n', 'N']:
						oculusASWoff = handle_invalid_input(
							False,
							f'Invalid input, using default value "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".'
						)
						return
					else:
						oculusASWoff = oculusASWoff in ['y', 'Y']
						utils.uprint(f'You selected: {fg.BLUE}{"Yes" if oculusASWoff else "No"}{st.RESET_ALL}', 'info')
					# 5
					print('\n')
					oculusCLIpath = setup.getUserInputRaw(
						f'{st.RESET_ALL}{fg.LIGHTYELLOW_EX}Setup 3 - Elite Dangerous Options - Step 5{st.RESET_ALL}',
						f'Path to the Oculus CLI executable (by default located at:'
						f'"{st.RESET_ALL}{st.BRIGHT}C:\\Program Files\\Oculus\\Support\\oculus-diagnostics\\OculusDebugToolCLI.exe{st.RESET_ALL}"): '
					)
					if oculusCLIpath == '' or not os.path.isfile(oculusCLIpath):
						oculusASWoff, oculusCLIpath = handle_invalid_input(
							False,
							f'Invalid path or no path entered, reverting previous step to "{st.RESET_ALL}{fg.LIGHTMAGENTA_EX}False{st.RESET_ALL}".'
						)
						return
				else:
					oculusASWoff = False
					oculusCLIpath = False
			else:
				utils.uprint(
					f'Skipping {st.RESET_ALL}{fg.LIGHTYELLOW_EX}Setup 3 - Elite Dangerous Options{st.RESET_ALL} based on previous input: "no vr play".',
					'info'
				)
				edOptionsFolderCopy = False
				edOptionsFolderPath = False
				graphicsOptionsSavedNonVr = False
				graphicsOptionsSavedVr = False
				oculusASWoff = False
				oculusCLIpath = False
				if not os.path.isdir(p.ED_OPTIONS_BACKUP):
					os.makedirs(p.ED_OPTIONS_BACKUP)
					if os.path.isdir(p.ED_OPTIONS_BACKUP) and not os.path.isdir(f'{p.ED_OPTIONS_BACKUP}\\nonvr-ed-options'):
						os.makedirs(f'{p.ED_OPTIONS_BACKUP}\\nonvr-ed-options')
					if os.path.isdir(p.ED_OPTIONS_BACKUP) and not os.path.isdir(f'{p.ED_OPTIONS_BACKUP}\\vr-ed-options'):
						os.makedirs(f'{p.ED_OPTIONS_BACKUP}\\vr-ed-options')

			##################

			print('\n')
			print('\n')
			print('\n')
			utils.uprint('Done! This is the end of the setup.', 'info')
			utils.uprint('runED will now create the configuration file.', 'info')
			utils.uprint('Standby...', 'info')
			time.sleep(2)

			VERSION = c.VERSION

			confContent = {
				'apps': [
					{
						'enabled': 					True,
						'forceKill': 				appForceKill,
						'name': 					appName,
						'path': 					appPath,
						'vr': 						appVr
					}
				],
				'settings': {
					'checkUpdatesAtStartup': 		checkUpdatesAtStartup,
					'checkUpdatesInterval': 		checkUpdatesInterval,
					'closeAppsOnExit': 				closeAppsOnExit,
					'gameStartTimeout': 			gameStartTimeout,
					'runElevated': 					runElevated,
					'vrCompatible': 				vrCompatible,
				},
				'vrSettings': {
					'edOptionsFolderCopy': 			edOptionsFolderCopy,
					'edOptionsFolderPath': 			edOptionsFolderPath,
					'oculusASWoff': 				oculusASWoff,
					'oculusCLIpath': 				oculusCLIpath,
					'graphicsOptionsSavedNonVr': 	graphicsOptionsSavedNonVr,
					'graphicsOptionsSavedVr': 		graphicsOptionsSavedVr
				}
			}

			with open(p.CONFIG, 'w') as f:
				yaml.safe_dump(confContent, f)

			utils.uprint(f'{st.RESET_ALL}{fg.LIGHTGREEN_EX}Configuration file created successfully.{st.RESET_ALL}', 'info')
			utils.uprint(f'runED will now exit. Please relaunch it {st.RESET_ALL}{st.BRIGHT}{fg.LIGHTWHITE_EX}manually{st.RESET_ALL}.', 'info')
			time.sleep(5)
			input(f'{st.RESET_ALL}Press {fg.YELLOW}<{fg.LIGHTGREEN_EX}ENTER{st.RESET_ALL}{fg.YELLOW}>{st.RESET_ALL} to EXIT...\n')
			debug.pause(breathe = True)
			sys.exit(0)
	#//
#//
