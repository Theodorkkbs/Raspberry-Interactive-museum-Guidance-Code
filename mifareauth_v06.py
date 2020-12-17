
#libraries
import time
import logging
import ctypes
import string
import nfc
import os
import sys
from subprocess import Popen
import wiringpi
import RPi.GPIO as GPIO
GPIO.setmode (GPIO.BOARD)

#setting up the awesome EXPANDER------------------------
pin_base = 100
i2c_addr = 0x20
pins = [100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115]
wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(pin_base,i2c_addr)
for pin in pins:
	wiringpi.pinMode(pin,1)
	wiringpi.digitalWrite(pin,0) #turn off all leds for a clean begining
	
#setting up EXPANDER DONE!-------------------------------

#the import for the button
btn = 11
#nfc variable
allnfcs = 0
#movies destination
outromagician_vid=("/home/pi/project_files/videos/outromagician.mp4")
journalist_vid=("/home/pi/project_files/videos/journalist.mp4")
director_vid=("/home/pi/project_files/videos/director.mp4")
sailor_vid=("/home/pi/project_files/videos/sailor.mp4")
italian_vid=("/home/pi/project_files/videos/Italian.mp4")
ziller_vid=("/home/pi/project_files/videos/Ziller.mp4")
typographer_vid=("/home/pi/project_files/videos/Typographer.mp4")
intromagician=("/home/pi/project_files/videos/intromagician.mp4")
er1=("/home/pi/project_files/videos/Patris.mp4")
ap1=("/home/pi/project_files/videos/Patris_2.mp4")
er2=("/home/pi/project_files/videos/Orfeas.mp4")
ap2=("/home/pi/project_files/videos/Orpheus_2.mp4")
er3=("/home/pi/project_files/videos/Harbor.mp4")
ap3=("/home/pi/project_files/videos/Harbor_2.mp4")
er4=("/home/pi/project_files/videos/Italy.mp4")
ap4=("/home/pi/project_files/videos/Italy_2.mp4")
er5=("/home/pi/project_files/videos/Typo.mp4")
ap5=("/home/pi/project_files/videos/Typo_2.mp4")
er6=("/home/pi/project_files/videos/Drawings.mp4")
ap6=("/home/pi/project_files/videos/Drawings_2.mp4")
er7=("/home/pi/project_files/videos/mpaoulo.mp4")
ap7=("/home/pi/project_files/videos/mpaoulo_2.mp4")


#game phase variable
stage = 0



def hex_dump(string):
    #Dumps data as hexstrings
    return ' '.join(["%0.2X" % ord(x) for x in string])
    
# Photocell Setup
def rc_time (x):
    count = 0
    
    #Output on the pin for
    GPIO.setup (x, GPIO.OUT)
    GPIO.output (x, GPIO.LOW)
    time.sleep(1) #AN GINEI sleep(0) DEN PROLAVAINEI KAN NA PAREI DIGMA

    #Change the pin back to input
    GPIO.setup(x, GPIO.IN)

    #Count until the pin goes high
    while (GPIO.input(x) == GPIO.LOW):
        count += 1

    return count


          #function for when the letter is placed in the chest
def isLetterAtPin(desired_pin, led_pin):
    global stage
    letter_inplace = False
    while not letter_inplace:
        print "b2 ", rc_time(desired_pin)
        if (rc_time(desired_pin) > 2500):
            letter_inplace = True
            wiringpi.digitalWrite(led_pin,0)            
            stage += 1
            return True




# NFC device setup
class NFCReader(object):
    MC_AUTH_A = 0x60
    MC_AUTH_B = 0x61
    MC_READ = 0x30
    MC_WRITE = 0xA0
    card_timeout = 10

    def __init__(self, logger):
        self.__context = None
        self.__device = None
        self.log = logger

        self._card_present = False
        self._card_last_seen = None
        self._card_uid = None
        self._clean_card()

        mods = [(nfc.NMT_ISO14443A, nfc.NBR_106)]

        self.__modulations = (nfc.nfc_modulation * len(mods))()
        for i in range(len(mods)):
            self.__modulations[i].nmt = mods[i][0]
            self.__modulations[i].nbr = mods[i][1]

    def run(self):
        # Starts the looping thread
        self.__context = ctypes.pointer(nfc.nfc_context())
        nfc.nfc_init(ctypes.byref(self.__context))
        loop = True
        try:
            self._clean_card()
            conn_strings = (nfc.nfc_connstring * 10)()
            devices_found = nfc.nfc_list_devices(self.__context, conn_strings, 10)
            if devices_found >= 1:
                self.__device = nfc.nfc_open(self.__context, conn_strings[0])
                try:
                    _ = nfc.nfc_initiator_init(self.__device)
                    while True: #IMPORTANT: LOOPS ITSELF INSTANTLY AND FOREVER

                        if stage == 0:
                            self._poll_loop() #IMPORTANT: LOOPS ITSELF EVERY 1 SEC
                            

                        elif stage == 1:
                            print "Proceeding to Stage One. Waiting for Flashlight..."
                            #edw mpainei synexeia kai tha looparei mexri to stage na allaxei xana.

                            while stage==1:
                                print "a ", rc_time(7) #ekthema (flashlight)
                                #print "b ", rc_time(29) #letter
                                if (rc_time(7) < 70):
                                        #LED_EXTENDER: turn on first led to indicatre position for letter P.
                                        wiringpi.digitalWrite(100,1)

                                        print "LIT COMPLETE", "You got a P! Led is on for the first letter! Put it there!"
                                        if isLetterAtPin(29,100):
                                                print "You placed the first letter, P!"
                                                print "P _ _ _ _ _ _ _ _ _"
                                                print " "
                                                print "Stage 2 entered", " Waiting for the NFC..."
                                              
                                                os.system('killall omxplayer.bin')
                                                omxc=Popen(['omxplayer', '-o','hdmi', ap1])
                                                player=True
                                                time.sleep(17)
                                                os.system('killall omxplayer.bin')
                                                omxc=Popen(['omxplayer', '-o','hdmi', journalist_vid])
                                                player=True
                                                time.sleep(12)
                                                os.system('killall omxplayer.bin')
                                                omxc=Popen(['omxplayer', '-o','hdmi', er2])
                                                player=True
                                                

                            #GPIO.cleanup() #TO XALAEI OPOTE DE TO VAZOUME

                        elif stage == 2:
                            self._poll_loop()

                        elif stage == 3:
                            self._poll_loop()

                        elif stage == 4:
                            print "4"
                            
                            GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_UP)
                           
                            
                            while True:
                                print "ok"
                              
                                input_state = GPIO.input(11)
                                print input_state
                                time.sleep(0.5)
                                if input_state == False :
                            
                                    print "pressed"
                                    #turn on LEDs for I's
                                    #LED_EXTENDER: turn on first led to indicatre position for letter P.
                                    wiringpi.digitalWrite(103,1)
                                    wiringpi.digitalWrite(105,1)
                                    
                                    time.sleep(0.5)

                                    if isLetterAtPin(35, 103) and isLetterAtPin(22,105):
                                        global stage
                                        print "You found two I's! Congratulations!"
                                        print "P O L I _ I _ _ O _"
                                        os.system('killall omxplayer.bin')
                                        omxc=Popen(['omxplayer', '-o','hdmi', ap4])
                                        player=True
                                        time.sleep(17)
                                        os.system('killall omxplayer.bin')
                                        omxc=Popen(['omxplayer', '-o','hdmi', italian_vid])
                                        player=True
                                        time.sleep(17)
                                        os.system('killall omxplayer.bin')
                                        omxc=Popen(['omxplayer', '-o','hdmi', er5])
                                        player=True
                                        
                                        print " "
                                        print "Stage 5 entered", "Waiting for the NFC..."
                                        stage-=1
                                        
                                        break                   

                        elif stage == 5:
                            self._poll_loop()

                        elif stage == 6:
                            self._poll_loop()

                        elif stage == 7:
                            self._poll_loop()


                finally:
                    nfc.nfc_close(self.__device)
            else:
                self.log("NFC Waiting for device.")
                time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            loop = False
        except IOError, e:
            self.log("Exception: " + str(e))
            loop = True  # not str(e).startswith("NFC Error whilst polling")
        # except Exception, e:
        # loop = True
        #    print "[!]", str(e)
        finally:
            nfc.nfc_exit(self.__context)
            self.log("NFC Clean shutdown called")
        return loop

    @staticmethod
    def _sanitize(bytesin):
        """Returns guaranteed ascii text from the input bytes"""
        return "".join([x if 0x7f > ord(x) > 0x1f else '.' for x in bytesin])

    @staticmethod
    def _hashsanitize(bytesin):
        """Returns guaranteed hexadecimal digits from the input bytes"""
        return "".join([x if x.lower() in 'abcdef0123456789' else '' for x in bytesin])

    def _poll_loop(self):
        """Starts a loop that constantly polls for cards"""
        nt = nfc.nfc_target()
        res = nfc.nfc_initiator_poll_target(self.__device, self.__modulations, len(self.__modulations), 10, 2,
                                            ctypes.byref(nt))
        # print "RES", res
        if res < 0:
            raise IOError("NFC Error whilst polling")
        elif res >= 1:
            uid = None
            if nt.nti.nai.szUidLen == 4:
                uid = "".join([chr(nt.nti.nai.abtUid[i]) for i in range(4)])
            if uid:
                if not ((self._card_uid and self._card_present and uid == self._card_uid) and \
                                    time.mktime(time.gmtime()) <= self._card_last_seen + self.card_timeout):
                    self._setup_device()
                   

                    if stage == 0:
                        self.read_card(uid)
                        #if stage is zero then look for the master
                        #if master checked in, proceed to stage 1
                        
                        
                        if uid.encode("hex") == 'fd1cfe16':
                            global stage
                            stage += 1
                            print "Hello Master. Stage Zero Completed."
                            print "_ _ _ _ _ _ _ _ _ _"
                            os.system('killall omxplayer.bin')
                            omxc=Popen(['omxplayer', '-o', 'hdmi', intromagician])
                            player=True
                            time.sleep(28)

                           
                            
                            os.system('killall omxplayer.bin')
                            omxc=Popen(['omxplayer', '-o','hdmi', er1])
                            player=True
                        

                            GPIO.setup(15,GPIO.OUT)#setting up the servo motor (pin =15 )
                            m=GPIO.PWM(15,50)#pin=15 frequency=50 heartz
                            m.start(12.5)#starting at 180 degrees position ,basicly its unlocked
                            op=2
                              #axristi metavliti gia na forcarw to susthma na mpei ston servomixanismo
                            if (op==2):          
                                    m.ChangeDutyCycle(2.5)#duty cycle = length/period opote gia na stripsei sti thesi 0 diladi na kleidwsei thelei na einai st dc 2.5 
                                    time.sleep(4)# o servomixanismos pernei pulses ana 20ms opote dc=0.5/20 * 100 =2.5 , g auto ka ievala kateutheian to 2.5
                                    m.stop
                        else:
                            print "still no master found..."

                    elif stage == 2:
                        self.read_card(uid)
                        #galazio
                        if uid.encode("hex") == '525dc935':
                            print "Good job buddy! Now get the O's and place them in the LED areas..."
                            #turn on LEDs for O's
                            #LED_EXTENDER: turn on first led to indicatre position for letter P.
                            wiringpi.digitalWrite(101,1)
                            wiringpi.digitalWrite(108,1)                            
                            if isLetterAtPin(31,101) and isLetterAtPin(38,108):
                                print "You found two O's! Congratulations!"
                                print "P O _ _ _ _ _ _ O _"
                                print " "
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', ap2])
                                player=True
                                time.sleep(17)
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', director_vid])
                                player=True
                                time.sleep(16)
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', er3])
                                player=True
                                
                                print "Stage 3 entered", "Waiting for the NFC..."
                                global stage
                                stage-=1
                        else:
                            print "still no O's found..."

                    elif stage == 3:
                        self.read_card(uid)
                        #prasino
                        if uid.encode("hex") == '3982c935':
                            print "Awesome! Now get the L's and place them where the LEDs are..."
                            #turn on LEDs for L's
                            #LED_EXTENDER: turn on first led to indicatre position for letter P.
                            wiringpi.digitalWrite(102,1)
                            
                            if isLetterAtPin(33,102):
                                print "You found the L! Congratulations!"
                                print "P O L _ _ _ _ _ O _"
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', ap3])
                                player=True
                                time.sleep(17)
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', sailor_vid])
                                player=True
                                time.sleep(17)
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', er4])
                                player=True
                                
                                print " "
                                print "Stage 4 entered", "Waiting for the button...!"
                        else:
                            print "still no L found..."


                    elif stage == 5:
                        self.read_card(uid)
                        #kitrino
                        if uid.encode("hex") == '9d4eec23':
                            print "Awesome! Now get the T's and place them where the LEDs are..."
                            #turn on LEDs for T's
                            #LED_EXTENDER: turn on first led to indicatre position for letter P.
                            wiringpi.digitalWrite(104,1)
                            
                            if isLetterAtPin(37, 104):
                                print "You found the T! Congratulations!"
                                print "P O L I T I _ _ O _"
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', ap5])
                                player=True
                                time.sleep(17)
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', typographer_vid])
                                player=True
                                time.sleep(11)
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', er6])
                                player=True
                                
                                print " "
                                print "Stage 6 entered", "Waiting for the nfc 4...!"
                        else:
                            print "still no T found..."

                    elif stage == 6:
                        self.read_card(uid)
                        #kokkino
                        if uid.encode("hex") == '0d9dc935':
                            print "Awesome! Now get the S's and place them where the LEDs are..."
                            #turn on LEDs for S's
                            #LED_EXTENDER: turn on first led to indicatre position for letter P.
                            wiringpi.digitalWrite(106,1)
                            wiringpi.digitalWrite(109,1)
                            if isLetterAtPin(32,106) and isLetterAtPin(40,109):
                                print "You found the S! Congratulations!"
                                print "P O L I T I S _ O S"
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', ap6])
                                player=True
                                time.sleep(22)
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', ziller_vid])
                                player=True
                                time.sleep(9)
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', er7])
                                player=True
                                
                                print " "
                                print "Stage 7 entered", "Waiting for the team work...!"
                                global stage
                                stage-=1
                        else:
                            print "still no S found..."

                    elif stage == 7:
                        
                        global allnfcs
                        
                        if ((allnfcs == 0 ) and (uid.encode("hex") == '525dc935')):
                            allnfcs +=1
                            print "card1"
                        elif ((allnfcs == 1 ) and (uid.encode("hex") == '3982c935')):
                            allnfcs +=1
                            print "card2"
                        elif ((allnfcs == 2) and (uid.encode("hex") == '9d4eec23')):
                            allnfcs +=1
                            print "card3"
                        elif ((allnfcs == 3) and (uid.encode("hex") == '0d9dc935')):
                            allnfcs +=1
                            print "card4"
                            print "Now you can place the letter M on the LEDs."
                            #turn on leds
                            #LED_EXTENDER: turn on first led to indicatre position for letter P.
                            wiringpi.digitalWrite(107,1)
                            
                            if isLetterAtPin(36,107):
                                print "You found the M! Congratulations!"
                                print "P O L I T I S M O S"
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', ap7])
                                player=True
                                time.sleep(17)
                                os.system('killall omxplayer.bin')
                                omxc=Popen(['omxplayer', '-o','hdmi', outromagician_vid])
                                player=True

                                print " "
                                print "OPEN"

                                GPIO.setup(15,GPIO.OUT)
                                p=GPIO.PWM(15,50)
                                p.start(2.5)
                                op=1

                                if (op==1):
                                        
                                        p.ChangeDutyCycle(12.5)
                                        time.sleep(4)
                                        p.stop
                              
                                                
                        else:
                            print "Wrong card buddy! Wait for your turn!"
                        
                        
                        
    
            self._card_uid = uid
            self._card_present = True
            self._card_last_seen = time.mktime(time.gmtime())

        else:
            self._card_present = False
            self._clean_card()

    def _clean_card(self):
        self._card_uid = None

    def select_card(self):
        """Selects a card after a failed authentication attempt (aborted communications)

           Returns the UID of the card selected
        """
        nt = nfc.nfc_target()
        _ = nfc.nfc_initiator_select_passive_target(self.__device, self.__modulations[0], None, 0, ctypes.byref(nt))
        uid = "".join([chr(nt.nti.nai.abtUid[i]) for i in range(nt.nti.nai.szUidLen)])
        return uid

    def _setup_device(self):
        """Sets all the NFC device settings for reading from Mifare cards"""
        if nfc.nfc_device_set_property_bool(self.__device, nfc.NP_ACTIVATE_CRYPTO1, True) < 0:
            raise Exception("Error setting Crypto1 enabled")
        if nfc.nfc_device_set_property_bool(self.__device, nfc.NP_INFINITE_SELECT, False) < 0:
            raise Exception("Error setting Single Select option")
        if nfc.nfc_device_set_property_bool(self.__device, nfc.NP_AUTO_ISO14443_4, False) < 0:
            raise Exception("Error setting No Auto ISO14443-A jiggery pokery")
        if nfc.nfc_device_set_property_bool(self.__device, nfc.NP_HANDLE_PARITY, True) < 0:
            raise Exception("Error setting Easy Framing property")

    def _read_block(self, block):
        """Reads a block from a Mifare Card after authentication

           Returns the data read or raises an exception
        """
        if nfc.nfc_device_set_property_bool(self.__device, nfc.NP_EASY_FRAMING, True) < 0:
            raise Exception("Error setting Easy Framing property")
        abttx = (ctypes.c_uint8 * 2)()
        abttx[0] = self.MC_READ
        abttx[1] = block
        abtrx = (ctypes.c_uint8 * 250)()
        res = nfc.nfc_initiator_transceive_bytes(self.__device, ctypes.pointer(abttx), len(abttx),
                                                 ctypes.pointer(abtrx), len(abtrx), 0)
        if res < 0:
            raise IOError("Error reading data")
        return "".join([chr(abtrx[i]) for i in range(res)])

    def __write_block(self, block, data):
        """Writes a block of data to a Mifare Card after authentication

           Raises an exception on error
        """
        if nfc.nfc_device_set_property_bool(self.__device, nfc.NP_EASY_FRAMING, True) < 0:
            raise Exception("Error setting Easy Framing property")
        if len(data) > 16:
            raise ValueError("Data value to be written cannot be more than 16 characters.")
        abttx = (ctypes.c_uint8 * 18)()
        abttx[0] = self.MC_WRITE
        abttx[1] = block
        abtrx = (ctypes.c_uint8 * 250)()
        for i in range(16):
            abttx[i + 2] = ord((data + "\x00" * (16 - len(data)))[i])
        return nfc.nfc_initiator_transceive_bytes(self.__device, ctypes.pointer(abttx), len(abttx),
                                                  ctypes.pointer(abtrx), len(abtrx), 0)

    def _authenticate(self, block, uid, key = "\xff\xff\xff\xff\xff\xff", use_b_key = False):
        """Authenticates to a particular block using a specified key"""
        if nfc.nfc_device_set_property_bool(self.__device, nfc.NP_EASY_FRAMING, True) < 0:
            raise Exception("Error setting Easy Framing property")
        abttx = (ctypes.c_uint8 * 12)()
        abttx[0] = self.MC_AUTH_A if not use_b_key else self.MC_AUTH_B
        abttx[1] = block
        for i in range(6):
            abttx[i + 2] = ord(key[i])
        for i in range(4):
            abttx[i + 8] = ord(uid[i])
        abtrx = (ctypes.c_uint8 * 250)()
        return nfc.nfc_initiator_transceive_bytes(self.__device, ctypes.pointer(abttx), len(abttx),
                                                  ctypes.pointer(abtrx), len(abtrx), 0)

    def auth_and_read(self, block, uid, key = "\xff\xff\xff\xff\xff\xff"):
        """Authenticates and then reads a block

           Returns '' if the authentication failed
        """
        # Reselect the card so that we can reauthenticate
        self.select_card()
        res = self._authenticate(block, uid, key)
        if res >= 0:
            return self._read_block(block)
        return ''

    def auth_and_write(self, block, uid, data, key = "\xff\xff\xff\xff\xff\xff"):
        """Authenticates and then writes a block

        """
        res = self._authenticate(block, uid, key)
        if res >= 0:
            return self.__write_block(block, data)
        self.select_card()
        return ""

    def read_card(self, uid):
        """Takes a uid, reads the card and return data for use in writing the card"""
        key = "\xff\xff\xff\xff\xff\xff"
        print "Reading card", uid.encode("hex")
        self._card_uid = self.select_card()
        self._authenticate(0x00, uid, key)
        block = 0
        for block in range(64):
            data = self.auth_and_read(block, uid, key)
            #print block, data.encode("hex"), "".join([ x if x in string.printable else "." for x in data])

    def write_card(self, uid, data):
        """Accepts data of the recently read card with UID uid, and writes any changes necessary to it"""
        raise NotImplementedError

if __name__ == '__main__':
    logger = logging.getLogger("cardhandler").info
    while NFCReader(logger).run():
        pass
