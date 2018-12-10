import subprocess
import time

import gs

class MinecraftServer(gs.GameServer):
    def __init__(self, id, wdir):
        gs.GameServer.__init__(self, id, wdir)
        self.jar = 'minecraft_server.jar'
        self.jvmargs = []
        self.rcon = []
        self.mb_ram = 4096
        self.shutdown_time = 10
        self.stop_timeout = 10

    def shutdown(self, msg):
        if len(self.rcon) > 0:
            # RCON available - do it nicely
            # Give players a countdown
            msg = msg if len(msg) > 0 else 'Server maintenance shutdown'
            countdown = self.shutdown_time
            while countdown > 0:
                subprocess.Popen(self.rcon + [
                    'title @a title {"text":"'
                        + str(countdown) + '"}'
                ])
                subprocess.Popen(self.rcon + [
                    'title @a subtitle {"color":"red","text":"'
                        + str(msg) + '"}'
                ])
                time.sleep(1)
                countdown -= 1

            # Stop server
            subprocess.Popen(self.rcon + ['stop'])

            # wait for process to be gone
            t = self.stop_timeout
            while t > 0 and self.is_running():
                time.sleep(1)
                t -= 1

            # if it's still not gone, kill it
            if self.is_running():
                self.kill()
                print(self.id + ': had to kill server process because stop ' + 'timed out')
        else:
            # RCON not available, do it the hard way...
            self.kill()

    def cmdline(self):
        return ['java'] + self.jvmargs + ['-Xmx' + str(self.mb_ram) + 'M'] + ['-jar',self.jar,'nogui']
