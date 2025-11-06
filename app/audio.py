import pyttsx3
import threading
import logging
from typing import Optional
from app.config import Config

logger = logging.getLogger(__name__)

class AudioManager:
    """Text-to-speech manager for audio announcements"""
    
    def __init__(self, config: Config):
        self.config = config
        self.engine = None
        self.is_speaking = False
        self.speech_thread = None
        self._initialize_engine()
        
    def _initialize_engine(self):
        """Initialize the text-to-speech engine"""
        try:
            logger.info("Initializing text-to-speech engine")
            self.engine = pyttsx3.init()
            
            # Configure voice properties
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)  # Use default voice
                
            self.engine.setProperty('rate', 200)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume level
            
            logger.info("Text-to-speech engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize text-to-speech engine: {e}")
            raise
            
    def speak_async(self, text: str) -> None:
        """
        Speak text asynchronously to avoid blocking
        
        Args:
            text: Text to be spoken
        """
        if self.engine is None:
            logger.error("Text-to-speech engine not initialized")
            return
            
        if self.is_speaking:
            logger.debug("Already speaking, skipping: %s", text)
            return
            
        def _speak():
            try:
                self.is_speaking = True
                logger.debug("Speaking: %s", text)
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logger.error(f"Failed to speak: {e}")
            finally:
                self.is_speaking = False
                
        # Run in a separate thread to avoid blocking
        try:
            if self.speech_thread and self.speech_thread.is_alive():
                # If there's an active thread, wait for it to finish or skip
                logger.debug("Speech thread is active, skipping new speech request")
                return
                
            self.speech_thread = threading.Thread(target=_speak, daemon=True)
            self.speech_thread.start()
        except RuntimeError as e:
            if "threads can only be started once" in str(e):
                # Create a new thread instance
                self.speech_thread = threading.Thread(target=_speak, daemon=True)
                self.speech_thread.start()
            else:
                logger.error(f"Failed to start speech thread: {e}")
        
    def announce_object_direction(self, label: str, direction: str, distance: str) -> None:
        """
        Announce object with direction and distance
        
        Args:
            label: Object label
            direction: Direction of the object
            distance: Distance descriptor
        """
        announcement = f"{label} detected at {direction}, {distance}"
        self.speak_async(announcement)
        
    def announce_navigation(self, instruction: str) -> None:
        """
        Announce navigation instruction
        
        Args:
            instruction: Navigation instruction
        """
        self.speak_async(instruction)