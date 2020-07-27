#! /usr/bin/env python
"""
Important note: for this script to work, the following conditions should be met:
* There must be ftp server data, via environment variables (FTP_SERVER, FTP_USERNAME and FTP_PASSWORD) or via arguments to the script call (in the prior order). Connection to this server is done via default ftp port via TLS.
* this code assumes it's going to connect to an FTP via TLS.
* If the version to upload is alpha, there's not need of an extra variable. Otherwise, CI_COMMIT_TAG should point to a version as vx.x, where v is a literal and x are numbers, example may be v0.18, v0.25, v0.3. This variable should be set in the environment.
* Inside the ftp server, the following directory structure will be expected: manuelcortez.net/static/files/music_dl. The script will create the <version> folder or alpha if needed.
* The script will upload all .exe, .zip and .json files located in the root directory from where it was called. The json files are uploaded to manuelcortez.net/static/files/music_dl/update and other files are going to manuelcortez.net/static/files/music_dl/<version>.
"""
import sys
import os
import glob
import ftplib

transferred=0

class MyFTP_TLS(ftplib.FTP_TLS):
	"""Explicit FTPS, with shared TLS session"""
	def ntransfercmd(self, cmd, rest=None):
		conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
		if self._prot_p:
			conn = self.context.wrap_socket(conn,
											server_hostname=self.host,
											session=self.sock.session)  # this is the fix
		return conn, size

def convert_bytes(n):
	K, M, G, T, P = 1 << 10, 1 << 20, 1 << 30, 1 << 40, 1 << 50
	if   n >= P:
		return '%.2fPb' % (float(n) / T)
	elif   n >= T:
		return '%.2fTb' % (float(n) / T)
	elif n >= G:
		return '%.2fGb' % (float(n) / G)
	elif n >= M:
		return '%.2fMb' % (float(n) / M)
	elif n >= K:
		return '%.2fKb' % (float(n) / K)
	else:
		return '%d' % n

def callback(progress):
	global transferred
	transferred = transferred+len(progress)
	print("Uploaded {}".format(convert_bytes(transferred),))

ftp_server = os.environ.get("FTP_SERVER") or sys.argv[1]
ftp_username = os.environ.get("FTP_USERNAME") or sys.argv[2]
ftp_password = os.environ.get("FTP_PASSWORD") or sys.argv[3]
version = os.environ.get("CI_COMMIT_TAG") or "latest"
version = version.replace("v", "")

print("Uploading files to the Socializer server...")
connection = MyFTP_TLS(ftp_server)
print("Connected to FTP server {}".format(ftp_server,))
connection.login(user=ftp_username, passwd=ftp_password)
connection.prot_p()
print("Logged in successfully")
connection.cwd("manuelcortez.net/static/files/music_dl")
if version not in connection.nlst():
	print("Creating version directory {} because does not exists...".format(version,))
	connection.mkd(version)

if "update" not in connection.nlst():
	print("Creating update info directory because does not exists...")
	connection.mkd("update")
connection.cwd(version)
print("Moved into version directory")
files = glob.glob("*.zip")+glob.glob("*.exe")+glob.glob("*.json")
print("These files will be uploaded into the version folder: {}".format(files,))
for file in files:
	transferred = 0
	print("Uploading {}".format(file,))
	with open(file, "rb") as f:
		if file.endswith("json"):
			connection.storbinary('STOR ../update/%s' % file, f, callback=callback, blocksize=1024*1024) 
		else:
			connection.storbinary('STOR %s' % file, f, callback=callback, blocksize=1024*1024) 
print("Upload completed. exiting...")
connection.quit()