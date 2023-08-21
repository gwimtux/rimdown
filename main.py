import subprocess
import os
import shutil
import xml.etree.ElementTree as ET

class RimDown:
    def __init__(self):
        self.setup()
        self.gameID = 294100
        self.steamcmd_path = os.path.expanduser('~/.config/rimdown/steam/steamcmd.sh')

    def setup(self):
        try:
            self.mod_dir = open(os.path.expanduser('~/.config/rimdown/settings.cfg'), 'r').read()
        except FileNotFoundError:
            steam_dir = os.path.expanduser('~/.config/rimdown/steam')
            config_dir = os.path.expanduser('~/.config/rimdown')

            # download steamcmd if not installed
            if not os.path.isdir(config_dir) and not os.path.isdir(steam_dir):
                os.mkdir(config_dir)
                os.mkdir(steam_dir)
                os.chdir(steam_dir)
                print('Downloading steamcmd...')
                subprocess.call('curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -', shell=True)
                os.system('clear')
                
            self.mod_dir = input('Enter the path to RimWorld mods folder: ')
            #check if path is valid
            if not os.path.isdir(self.mod_dir):
                print('Invalid path!')
                self.setup()
            with open(os.path.expanduser('~/.config/rimdown/settings.cfg'), 'w') as f:
                f.write(self.mod_dir)

    def get_mods(self):
        global workshopID
        mod = input('Enter the link to the mod: ')
        workshopID = mod.split('?id=')[1][:10]

    def download_mods(self):
        subprocess.call([self.steamcmd_path, '+force_install_dir', self.mod_dir, '+login', 'anonymous', '+workshop_download_item', str(self.gameID), str(workshopID), '+quit'])

    def extract_mods(self):
        tree = ET.parse(f'{self.mod_dir}/steamapps/workshop/content/{self.gameID}/{workshopID}/About/About.xml')
        root = tree.getroot()
        modName = root.find('name').text
        shutil.move(f'{self.mod_dir}/steamapps/workshop/content/{self.gameID}/{workshopID}', f'{self.mod_dir}/{modName}')
        shutil.rmtree(f'{self.mod_dir}/steamapps')
        os.system('clear')
        print('Done!')

def main():
    rimdown = RimDown()
    rimdown.get_mods()
    rimdown.download_mods()
    rimdown.extract_mods()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting...')
        exit()