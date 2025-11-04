import cv2
import pyautogui
import numpy as np
import time
import os
from datetime import datetime


class VideoRecorder:
    """Grabadora de video para evidencias de pruebas"""
    
    def __init__(self, output_dir="videos", fps=12.0):
        self.output_dir = output_dir
        self.fps = fps
        self.recording = False
        self.video_writer = None
        self.start_time = None
        self.video_filename = None
        
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
    
    def start_recording(self, test_name):
        """Iniciar grabación de video"""
        try:
            # Configurar resolución
            screen_size = pyautogui.size()
            
            # Definir codec y crear VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.video_filename = f"{self.output_dir}/{test_name}_{timestamp}.avi"
            
            self.video_writer = cv2.VideoWriter(
                self.video_filename, 
                fourcc, 
                self.fps, 
                screen_size
            )
            
            self.recording = True
            self.start_time = time.time()
            
            print(f"🎥 Grabación de video iniciada: {self.video_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Error iniciando grabación de video: {e}")
            return False
    
    def capture_frame(self):
        """Capturar un frame de la pantalla"""
        try:
            if not self.recording or not self.video_writer:
                return False
            
            # Capturar screenshot
            screenshot = pyautogui.screenshot()
            
            # Convertir a array numpy y luego a BGR para OpenCV
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Escribir frame
            self.video_writer.write(frame)
            return True
            
        except Exception as e:
            print(f"⚠️ Error capturando frame: {e}")
            return False
    
    def stop_recording(self):
        """Detener grabación de video"""
        try:
            if self.recording and self.video_writer:
                self.recording = False
                self.video_writer.release()
                
                end_time = time.time()
                duration = end_time - self.start_time
                
                print(f"⏹️ Grabación de video detenida: {self.video_filename}")
                print(f"   Duración: {duration:.2f} segundos")
                
                return self.video_filename
            return None
            
        except Exception as e:
            print(f"❌ Error deteniendo grabación: {e}")
            return None
    
    def record_test(self, test_function, test_name):
        """Decorador para grabar video durante la ejecución de un test"""
        def wrapper(*args, **kwargs):
            self.start_recording(test_name)
            try:
                result = test_function(*args, **kwargs)
                return result
            finally:
                self.stop_recording()
        return wrapper