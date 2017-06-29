import RPi.GPIO as GPIO
import time
from threading import Thread



#TRIG = 23
#ECHO = 24

class Sonar(Thread):

    def __init__(self, TRIG, ECHO, dist_min_obst_cm):
        Thread.__init__(self)

        #variaveis para a pinagem do sensor sonar (echo e trigger)
        self.TRIG = TRIG
        self.ECHO = ECHO

        #distancia minima em centimetros para considerar que foi detectado obstaculo
        self.dist_min_obst_cm = dist_min_obst_cm

        """CONFIGURANDO OS PINOS"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG,GPIO.OUT)
        GPIO.setup(self.ECHO,GPIO.IN)
        GPIO.output(self.TRIG, False)

        """INICIANDO VARIAVEL OBSTACULO"""
        self.obstaculo = False

    def run(self):
        # envio de trem de pulso
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        while GPIO.input(self.ECHO)==0:
            self.pulse_start = time.time()

        while GPIO.input(self.ECHO)==1:
            self.pulse_end = time.time()
            self.pulse_duration = self.pulse_end - self.pulse_start
            self.distance = self.pulse_duration * 17150 # considerou-se a velocidade do som como 343m/s
                                                        # logo, passando para centimetros: 34300 = (distance/(time/2))
                                                        # 17150 = distance/time
                                                        # distance = time * 17150

            self.distance = round(self.distance, 2)

        if self.distance < self.dist_min_obst_cm:
            self.obstaculo = True

        else:
            self.obstaculo = False


#limpando as portas do GPIO antes de iniciar
GPIO.cleanup()

sensor_frente = Sonar(23,24,15)

while True:
    sensor_frente.run()
    print "Distancia " + str(sensor_frente.distance) + "cm"

    print "obstaculo frente =" + str(sensor_frente.obstaculo)

    time.sleep(0.1)