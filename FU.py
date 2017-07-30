# -*- coding: utf-8 -*-
import os,sys,random,io,codecs,socket, struct
from subprocess import call,Popen, CREATE_NEW_CONSOLE, check_output #Para ejecutar comandos externos (Youtube-DL y demas)
import json
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
#Bueno, el proceso que va a realizar este script se separa en 3 partes, descargar, encodear y subir, tambien hay una funcion aviscript que es parte del proceso encodear
def descargar(crunchyroll_link,nombre,crunchyroll_episodenumber):
	ytdl_dir=r"C:/Users/Enzo Zapata/Desktop/Descargas/youtube-dl/" #Directorio de Youtube-DL
	random_path = random.randint(100000, 999999) #Numero aleatorio para crear carpeta
	global temp_path
	temp_path = ytdl_dir+"temps/"+nombre+"-"+str(crunchyroll_episodenumber)+"-"+str(random_path) #Carpeta aleatoria a crear
	#temp_path = descargar.temp_path
	os.makedirs(temp_path, 0755) #Crear la carpeta
	assert os.path.isdir(ytdl_dir) #Checkea que el directorio de youtube-dl sea valido
	os.chdir(ytdl_dir) #Ingresa al directorio de Youtube-DL
	#call(["youtube-dl.exe","--skip-download","--write-sub","--sub-lang","esLA","--cookie","cccookie.txt","-o",temp_path+"/subs.ass",crunchyroll_link]) 
	#Descargamos el .ass en espanol LA
	mikasa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	with io.open("iptxt.txt", "r+", encoding="utf-8") as iptxt:
		ipmikasa=iptxt.read()
	mikasa.connect((ipmikasa, 8090))
	send_msg(mikasa, crunchyroll_link)
	subtitulos = recv_msg(mikasa)
	#with io.open(temp_path+"/subs.esLA.ass", "r+", encoding="utf-8") as assnobom:
	#	unicodeSub=assnobom.read()
	#os.remove(temp_path+"/subs.esLA.ass")
	with io.open(temp_path+"/subs.esLA.ass", "w", encoding="utf_8_sig") as assbom:
		assbom.write(u'\ufeff')
		assbom.write(subtitulos.decode("utf-8"))
	call(["youtube-dl.exe","--verbose","-f","best","--cookie","cccookie.txt","-o",temp_path+"/video.%(ext)s",crunchyroll_link]) 
#Descargado el video y obtenido el subtitulo, seguimos definiendo la funcion aviscript que genera un script de avisynth dependiendo el formato del video y la calidad que se busca obtener, ligera 480p o hd 720p
	global formato
	if os.path.isfile(temp_path+"/video.flv"):
		formato="flv"
	elif os.path.isfile(temp_path+"/video.mp4"):
		formato="mp4"
def aviscript(formato, version):
	#temp_path=descargar.temp_path
	os.chdir(temp_path)
	f = open('aviscript.avs','w')
	if formato == "flv":
		f.write('LoadPlugin("C:\Users\Enzo Zapata\Desktop\Descargas\MIPONY Downloads\staxrip1.4\Apps\Plugins\\both\\ffms2\\ffms2.dll")\n')
		f.write('LoadPlugin("C:\Users\Enzo Zapata\Desktop\Descargas\MIPONY Downloads\staxrip1.4\Apps\Plugins\\avs\VSFilterMod\VSFilterMod64.dll")\n')
		f.write('FFVideoSource("'+temp_path+'/video.flv", cachefile = "'+temp_path+'/video.ffindex")\n')
	elif formato == "mp4":
		f.write('LoadPlugin("C:\Users\Enzo Zapata\Desktop\Descargas\MIPONY Downloads\staxrip1.4\Apps\Plugins\\avs\L-SMASH-Works\LSMASHSource.dll")\n')
		f.write('LoadPlugin("C:\Users\Enzo Zapata\Desktop\Descargas\MIPONY Downloads\staxrip1.4\Apps\Plugins\\avs\VSFilterMod\VSFilterMod64.dll")\n')
		f.write('LSMASHVideoSource("'+temp_path+'/video.mp4", format = "YUV420P8")\n')
	f.write('TextSubMod("E:\Enzo Zapata\Descargas\MIPONY Downloads\AnimeMF.ass")\n')
	f.write('TextSubMod("'+temp_path+'/subs.esLA.ass")\n')
	if version == "480p":
		f.write('BicubicResize(848, 480, 0, 0.5)')
	elif version == "720p":
		f.write('BicubicResize(1280, 720, 0, 0.5)')
	f.close()
def encodear(version, nombre, crunchyroll_episodenumber, uploader):
	if formato=="flv":
		#Generamos el .ffindex para despues usarlo en el script de avisynth
		os.chdir("C:\Users\Enzo Zapata\Desktop\Descargas\MIPONY Downloads\staxrip1.4\Apps\Plugins\\both\\ffms2")
		call(["ffmsindex.exe",temp_path+"/video.flv",temp_path+"/video.ffindex"])
		#Extraemos el audio del .flv a video.aac
		os.chdir("C:\Users\Enzo Zapata\Desktop\Descargas\youtube-dl\\flvextract")
		call(["FLVExtractCL.exe","-a","-d",temp_path,"-o",temp_path+"/video.flv"])
		#Generamos el script de avisynth
		aviscript(formato,version)
	elif formato=="mp4":
		#Extraemos el audio del .mp4 a audio.m4a
		os.chdir("C:\Users\Enzo Zapata\Desktop\Descargas\MIPONY Downloads\staxrip1.4\Apps\MP4Box")
		call(["mp4box.exe","-single","2","-out",temp_path+"/audio.m4a",temp_path+"/video.mp4"]) 
		#Gemera,ps eñ scro´t de avisynth
		aviscript(formato,version)
	#Entramos al directorio del x264
	os.chdir("C:\Users\Enzo Zapata\Desktop\Descargas\MIPONY Downloads\staxrip1.4\Apps\\x264")
	#Primera pasada
	if version == "480p":
		bitrate="612"
	elif version == "720p":
		bitrate = "1224"
	call(["x264.exe","--tune","animation","--pass","1","--bitrate",bitrate,"--stats",temp_path+"/x264stats.stats","--output","NUL",temp_path+"/aviscript.avs"])
	#Segunda pasada y ultima
	call(["x264.exe","--tune","animation","--pass","2","--bitrate",bitrate,"--stats",temp_path+"/x264stats.stats","--output",temp_path+"/video_new_vl.h264",temp_path+"/aviscript.avs"])
	#Una vez finalizado el encodeo, entramos al directorio del MP4Box para unir el audio y video en un .mp4 final
	os.chdir("C:\Users\Enzo Zapata\Desktop\Descargas\MIPONY Downloads\staxrip1.4\Apps\MP4Box")
	if formato == "flv":
		audio="video.aac"
	elif formato == "mp4":
		audio="audio.m4a"
	call(["mp4box.exe","-add",temp_path+"/video_new_vl.h264#video","-add",temp_path+"/"+audio+"#audio:lang=eng:name=","-new",temp_path+"/"+nombre+"-"+str(crunchyroll_episodenumber)+"-"+version+"-[AnimeMF.org]-"+uploader+".mp4"])
def subir(usermega, passwordmega, version, carpeta_mega,nombre,crunchyroll_episodenumber, uploader):
	site="AnimeMF.org"
	if version == "480p":
		carpeta_mega=carpeta_mega+"-VL"
	elif version == "720p":
		carpeta_mega=carpeta_mega+"-HD"
	nombre_cap=nombre+"-"+str(crunchyroll_episodenumber)+"-"+version+"-["+site+"]-"+uploader+".mp4"
	megaput_cmd = ['C:\Users\Enzo Zapata\Desktop\Descargas\youtube-dl\megatools\megaput.exe',"--path","/Root/"+carpeta_mega+"/"+nombre_cap,"-u",usermega,"-p",passwordmega,"--no-ask-password",temp_path+"/"+nombre_cap]
	Popen(megaput_cmd, creationflags=CREATE_NEW_CONSOLE)

def general(uploader,usermega, passwordmega, carpeta_mega, nombre, link_cap, crunchyroll_episodenumber,hd,sd):
	descargar(link_cap, nombre, crunchyroll_episodenumber)
	#os.chdir("C:/Users/Enzo Zapata/Desktop/Descargas/youtube-dl/")
	#call(["ffprobe.exe","-v","quiet","-print_format","json","-show_format","-show_streams", temp_path+"/video."+formato])
	#a = check_output("ffprobe.exe -v quiet -print_format json -show_format -show_streams \""+temp_path+"/video."+formato+"\"", shell=True)
	#videojson = json.loads(a)

	#print videojson["streams"][0]["bit_rate"]
	if hd==1:
		encodear("720p", nombre, crunchyroll_episodenumber, uploader)
		subir(usermega, passwordmega,"720p",carpeta_mega, nombre, crunchyroll_episodenumber, uploader)
	if sd==1:
		encodear("480p", nombre, crunchyroll_episodenumber, uploader)
		subir(usermega, passwordmega,"480p",carpeta_mega, nombre, crunchyroll_episodenumber, uploader)
	
