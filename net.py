import SocketServer
import socket
import logging
from logging.handlers import RotatingFileHandler

addr = ('', 20443)


def logset():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='myserver.log',
                        filemode='w')
    logrotating()


def logrotating():  # log huigun
    Rthandler = RotatingFileHandler('myserver.log', maxBytes=10 * 1024 * 1024, backupCount=5)
    Rthandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    Rthandler.setFormatter(formatter)
    logging.getLogger('').addHandler(Rthandler)


class MyTCPHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        try:
            name_len = ord(self.rfile.read(1))
            name = self.rfile.read(name_len)
            logging.info("From IP:" + self.client_address[0])
        except Exception as err:
            logging.error(err)
        logging.info('Get request' + name)
        fd = open("Downloads/" + name, 'wb')
        cont = self.rfile.read(4096)
        while cont:
            fd.write(cont)
            cont = self.rfile.read(4096)
        fd.close()
        logging.info('Out:' + name)
        print "Saved", name


if __name__ == "__main__":
    print "Server start in ip:", socket.gethostbyname(socket.gethostname())
    logset()
    try:
        server = SocketServer.TCPServer(addr, MyTCPHandler)
        server.serve_forever()
    except Exception as err:
        logging.error(err)
# server.shutdown()

