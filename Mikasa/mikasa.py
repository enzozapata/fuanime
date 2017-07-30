# -*- coding: utf-8 -*-
import socket, time, os, io, urllib2, struct
from urlparse import urlparse
from subprocess import call
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.1.10', 8090))
serversocket.listen(2) # become a server socket, maximum 5 connections
def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)
def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data
while True:
    connection, address = serversocket.accept()
    buf = recv_msg(connection)
    if len(buf) > 0:
		parsed_uri = urlparse(buf)
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
		if domain == "http://www.crunchyroll.com/":
			print time.asctime()+" Iniciando descarga para posterior envio: "+buf
			ytdl_dir="C:\\Users\\Enzo Zapata\\Documents\\youtube-dl\\"
			#os.chdir(ytdl_dir) #Ingresa al directorio de Youtube-DL
			call(["youtube-dl","--skip-download","--write-sub","--sub-lang","esLA","--cookie","cookie.txt","-o","subs.ass",buf])
			with io.open("subs.esLA.ass", "r+", encoding="utf_8_sig") as assnobom:
				send_msg(connection, assnobom.read().encode("utf-8"))
			print time.asctime()+" Finalizado: "+buf
		elif domain == "http://feedproxy.google.com/":
			req = urllib2.Request(buf)
			res = urllib2.urlopen(req)
			finalurl = res.geturl()
			
			print time.asctime()+" Iniciando descarga para posterior envio: "+finalurl
			ytdl_dir="C:\\Users\\Enzo Zapata\\Documents\\youtube-dl\\"
			#os.chdir(ytdl_dir) #Ingresa al directorio de Youtube-DL
			call(["youtube-dl","--skip-download","--write-sub","--sub-lang","esLA","--cookie","cookie.txt","-o","subs.ass",finalurl])
			with io.open("subs.esLA.ass", "r+", encoding="utf_8_sig") as assnobom:
				send_msg(connection, assnobom.read().encode("utf-8"))
			print time.asctime()+" Finalizado: "+finalurl
		else:
			msj="Mikasa "+time.asctime()+buf+"  says: Error, no entiendo lo que me enviaste. ¿Sabes lo que estas haciendo?."
			print msj
			connection.send(msj)
