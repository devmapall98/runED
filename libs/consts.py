import os

class consts():
	"""
	This class contains the constants used in the application.
	"""
	CHANNEL			= 'Release'
	SEMVER			= '0.9.9'
	VERSION 		= {
		'channel': CHANNEL,
		'full': f'{CHANNEL}/{SEMVER}',
		'major': SEMVER.split('.')[0],
		'minor': SEMVER.split('.')[1],
		'patch': SEMVER.split('.')[2],
		'semver': SEMVER,
	}
	GAME_EXE		= 'EliteDangerous64.exe'
	VR_STATUS		= False
	GIT_REPO		= 'devmapall98/runED'
#//

class paths():
	"""
	This class contains the paths used in the application.
	"""
	CONF_PATH = f"{os.environ['APPDATA']}\\runED"
	CONF_NAME = 'config.yaml'
	CONFIG = f"{os.environ['APPDATA']}\\runED\\{CONF_NAME}"
	UPDATE = f"{os.environ['APPDATA']}\\runED\\update"
	OCULUS_ASW = f"{os.environ["APPDATA"]}\\runED\\scripts\\oculusASWoff.txt"
	ED_OPTIONS_BACKUP = f"{os.environ['APPDATA']}\\runED\\ed-options-backup"
#//