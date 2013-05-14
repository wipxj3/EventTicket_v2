__author__ = 'DEXTER'
import hashlib
import base64
import os
import sqlite3
import time
import qrcode
import places


class QRencode():
    def getTime(self):
        t = time.localtime()
        return str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + '_' + str(t.tm_hour) + '_' + str(
            t.tm_min) + '_' + str(t.tm_sec)

    def getData(self, iCinema, iDay, iTime, iMovie, iLoc):
        lst_d = [iCinema, iDay, iTime, iMovie, iLoc]
        self.salt = str(os.urandom(128))

        self.info = self.getEventInfo(lst_d)

        digest = hashlib.sha512(self.salt + self.info).hexdigest()
        self.data = base64.b64encode(digest)
        return [self.info, self.data[30:84]]

    def getEventInfo(self, lst):
        return places.cinema[int(lst[0])] + '_' \
               + places.day[int(lst[1])] + '_' \
               + places.time_stamp[int(lst[2])] + '_' \
               + places.movie[int(lst[3])] + '_' \
               + places.locul[int(lst[4])]

    def generate(self, data):
        qr = qrcode.QRCode(
            version=6,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=4,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        im = qr.make_image()
        timestamp = self.getTime()
        imageIndex = timestamp + '_' + data[0:7] + '_qr'
        imagePath = './mysite/static/img/'
        im.save(imagePath + imageIndex + '.png')
        return imageIndex

    def saveToDB(self, qrImage, info, qrHash, shortHash):
        conn = sqlite3.connect('./dev.db')
        c = conn.cursor()
        # Insert a row of data
        c.execute("INSERT INTO QRs VALUES (?, ?, ?, ?, ?)", (None, qrImage, info, qrHash, shortHash))
        # Save (commit) the changes
        conn.commit()
        # We can also close the cursor if we are done with it
        c.close()
        return 'added to DB!'

    def verifyHash(self, recvHash):
        con = sqlite3.connect('./dev.db')
        with con:
            cur = con.cursor()
            result = cur.execute("SELECT COUNT(*) FROM QRs WHERE qrHash=?", (recvHash,))
            rows = result.next()[0]
            #print 'FOUND',rows
            #Consolidate Duplicate Conditional Fragments
            if rows == 1:
                response = 'VALID'
                #return response
            else:
                response = 'INVALID'
                #return response
            return response

# def handler(clientSocket, remoteAddress):
#     while True:
#         qr = QRencode()
#         try:
#             serverRecieved = clientSocket.recv(1024)
#             print '>>> Command from client:', serverRecieved[:8],remoteAddress
#         except Exception:
#             continue
#         if serverRecieved[:9] == 'VALIDATE ':
#             rvHash = serverRecieved[9:]
#             #print rvHash
#             check = qr.verifyHash(rvHash)
#             print '   <','*'*50+rvHash[47:],'>', check
#             clientSocket.send(check)
#         elif serverRecieved[:9] == 'generate ':
#             request = serverRecieved[9:18].split(',')
#             info, qrHash = qr.getData(int(request[0]),int(request[1]),int(request[2]),int(request[3]),int(request[4]))
#             qrImage = qr.generate(qrHash)
#             qr.saveToDB(str(qrImage), str(info), str(qrHash))
#             #print info, qrHash, qrImage
#             qrStorage = './mysite/static/qrs/'
#             f = open(qrStorage + qrImage + '.png', "rb")
#             qrToSend = f.read()
#             qrFile = clientSocket.send(qrToSend)
#             print '>>> passed:',qrImage,qrFile,'bytes'
#             f.close()
#         elif serverRecieved == ' ':
#             print 'poke!'
#         #Decompose Conditional
#         #elif serverRecieved == "close" or serverRecieved == "Close":
#         elif isConnectionClosed(serverRecieved):
#             clientSocket.send("bye-bye")
#             clientSocket.close()
#             break
# #        elif serverRecieved == "Hastalavista" or serverRecieved == "hastalavista":
# #            global kill
# #            kill = 1
# #            clientSocket.send("down")
# #            clientSocket.close()
# #            break
#         else:
#             clientSocket.send("> Can you elaborate on that?")

# def isConnectionClosed(self,serverRecieved):
#     return serverRecieved == "close" or serverRecieved == "Close" or serverRecieved == "CLOSE"
# #if __name__ == "__main__":
# #    kill = 0
# #    val = 1
# #    while val == 1:
# #        try:
# #            clientSocket, remoteAddress = serverSocket.accept()
# #        except Exception:
# #            if kill == 1:
# #                print "< SERVER SHUTDOWN >"
# #                val = 0
# #                serverSocket.close()
# #                break
# #            else:
# #                continue
# #        #print "> accepted with address ", remoteAddress
# #        thread.start_new_thread(handler,(clientSocket, remoteAddress))
