import os
import signal
import subprocess

# Server error class
class GameServerError(Exception):
    pass

# Base class for game servers
class GameServer:
    def __init__(self, id, wdir):
        self.id = id
        self.wdir = wdir
        self.pid = -1

    # get server command line
    def cmdline(self):
        raise GameServerError('cmdline not implemented')

    # shutdown
    def shutdown(self):
        raise GameServerError('shutdown not implemented')

    # tests if the server is currently running
    def is_running(self):
        try:
            os.kill(self.pid, 0)
        except OSError:
            return False
        else:
            return True

    def check_running(self):
        if self.pid >= 0:
            if self.is_running():
                return True
            else:
                print(self.id + ': seems to have crashed')
                self.pid = -1
                return False
        else:
            return False

    # start server and set PID
    def start(self):
        if self.check_running():
            raise GameServerError('server already running with PID '
                + str(self.pid))

        p = subprocess.Popen(self.cmdline(),
            cwd=self.wdir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)

        self.pid = p.pid

    # gracefully shutdown server
    def stop(self, msg):
        if self.check_running():
            self.shutdown(msg)
            self.pid = -1
        else:
            raise GameServerError('server not running')

    # forcefully kill server process
    def kill(self):
        if self.check_running():
            os.kill(self.pid, signal.SIGTERM)
            self.pid = -1
        else:
            raise GameServerError('server not running')

    # get server status
    def status(self):
        if self.check_running():
            print(self.id + ': running with PID ' + str(self.pid))
        else:
            print(self.id + ': not running')

    # restart server if it's not running even though it should be
    def keepalive(self):
        if self.pid >= 0 and not self.is_running():
            self.start()
            print(self.id + ': restarted crashed (?) server with PID ' + str(self.pid))

    # handle other command
    def handle(self, command):
        cmd = command[0]
        msg = command[1] if len(command) > 1 else ''

        if cmd == 'start':
            self.start()
            print(self.id + ': started with PID ' + str(self.pid))
        elif cmd == 'stop':
            self.stop(msg)
            print(self.id + ': stopped')
        elif cmd == 'kill':
            self.kill()
            print(self.id + ': killed')
        elif cmd == 'status':
            self.status()
        elif cmd == 'keepalive':
            self.keepalive()
        elif cmd == 'restart':
            self.stop(msg)
            self.start()
            print(self.id + ': restarted with PID ' + str(self.pid))
        else:
            raise GameServerError('command \'' + cmd + '\' not supported!')

# Server registry
servers = []
