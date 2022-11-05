# coding: utf-8
import RPi.GPIO as GPIO
import time
import sys
import readchar
import threading
import os
import subprocess
import pygame.mixer


#角度からデューティ比を求める関数
def servo_angle(Servo, angle):
    duty = 2.5 + (12.0 - 2.5) * (angle + 90) / 180   #角度からデューティ比を求める
    Servo.ChangeDutyCycle(duty)                      #デューティ比を変更
    time.sleep(0.3)

def keeper():
    Servo_pin = 19
    GPIO.setup(Servo_pin, GPIO.OUT)

    Servo = GPIO.PWM(Servo_pin, 50)     #GPIO.PWM(ポート番号, 周波数[Hz])
    Servo.start(0)                      #Servo.start(デューティ比[0-100%])
    back_angle=0
    servo_angle(Servo, 0)

    while True:

      servo_angle(Servo, 70)
      time.sleep(1)
      servo_angle(Servo, 0)
      time.sleep(1)
      servo_angle(Servo,-70)
      time.sleep(1)
      servo_angle(Servo, 0)
      time.sleep(1)

def kicker():

    Servo_pin = 18
    GPIO.setup(Servo_pin, GPIO.OUT)
    
    # switch LEFT
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # switch RIGHT
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    #PWMの設定
    #サーボモータSG90の周波数は50[Hz]
    Servo = GPIO.PWM(Servo_pin, 50)     #GPIO.PWM(ポート番号, 周波数[Hz])
    Servo.start(0)                      #Servo.start(デューティ比[0-100%])
    
    back_angle=0
    servo_angle(Servo, -10)

    # BGM
    BGM_MUSIC='./music/bgm.wav'
    pygame.mixer.init(44100, -16, 2, 2048)
    bgm = pygame.mixer.Sound(BGM_MUSIC)
    bgm.set_volume(0.1)
    bgm.play(-1)

    # VOICE
    BGM_MUSIC='./music/stadium_voice.wav'
    voice = pygame.mixer.Sound(BGM_MUSIC)
    voice.set_volume(0.2)
    voice.play(-1)

    while True:
    
       sw_status_l = GPIO.input(16)
       sw_status_r = GPIO.input(25)
    
       if sw_status_l == 0:
         print('LEFT Switch!\n')
         back_angle-=10
         if back_angle < -90:
           back_angle=-90
         servo_angle(Servo, back_angle)
    
       if sw_status_r == 0:
         print('RIGHT Switch!\n')
         servo_angle(Servo, 90)
         pygame.mixer.music.load("./music/kick_sound.mp3")
         pygame.mixer.music.play(1)

         time.sleep(2)
         back_angle=0
         servo_angle(Servo, -10)

def main():

    GPIO.setmode(GPIO.BCM)

    thread1 = threading.Thread(target=kicker)
    thread2 = threading.Thread(target=keeper)
    thread1.setDaemon(True)
    thread2.setDaemon(True)
    thread1.start()
    thread2.start()

    try:
         while True:
            kb = readchar.readchar()
            sys.stdout.write(kb)
            if kb == 'q':
              GPIO.cleanup()
              sys.exit()
    
    except KeyboardInterrupt:
         GPIO.cleanup()
         sys.exit()

if __name__ == "__main__":
    main()

