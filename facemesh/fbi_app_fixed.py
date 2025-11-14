"""
FBI Facial Recognition Application - FIXED VERSION
Clean, bug-free implementation with dashboard
"""

import cv2
import numpy as np
import time
import os
from datetime import datetime
from fbi_system import FBIFacialRecognitionSystem
from fbi_dashboard import FBIDashboard


class FBIApp:
    """Bug-free FBI application."""
    
    def __init__(self):
        """Initialize."""
        print("Initializing FBI System...")
        self.system = FBIFacialRecognitionSystem()
        self.dashboard = FBIDashboard()
        self.window_name = 'FBI Facial Recognition System'
        self.fullscreen = False
        self.show_dashboard = False
        self.current_profile = None
        self.current_match = None
        
    def run(self):
        """Run the application."""
        print("=" * 70)
        print("FBI FACIAL RECOGNITION SYSTEM")
        print("=" * 70)
        print("\nControls:")
        print("  F - Toggle Fullscreen")
        print("  D - Toggle Dashboard")
        print("  Q - Quit")
        print("  S - Statistics")
        print("  R - Report")
        print("\nInitializing camera...")
        
        try:
            self.system.initialize_camera()
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            print("✓ Ready!\n")
            
            while True:
                # Read frame
                ret, frame = self.system.cap.read()
                if not ret:
                    print("Failed to read frame")
                    break
                
                # Identify face
                try:
                    match_data, landmarks = self.system.identify_face(frame)
                except Exception as e:
                    print(f"Identification error: {e}")
                    match_data, landmarks = None, None
                
                # Update current match
                if match_data and match_data.get('is_match'):
                    person_id = match_data.get('person_id')
                    profile = self.dashboard.get_profile(person_id)
                    
                    if profile:
                        self.current_profile = profile
                        self.current_match = match_data
                        self.show_dashboard = True
                        print(f"✓ MATCH: {profile.get('full_name')} - {match_data.get('confidence', 0)*100:.1f}%")
                
                # Create display
                try:
                    if self.show_dashboard and self.current_profile and self.current_match:
                        display = self.dashboard.draw_dashboard(frame, self.current_profile, self.current_match)
                    else:
                        display = self._draw_live_view(frame, match_data, landmarks)
                except Exception as e:
                    print(f"Display error: {e}")
                    display = frame.copy()
                    cv2.putText(display, f"Error: {str(e)}", (50, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Show
                cv2.imshow(self.window_name, display)
                
                # Handle keys
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("\nQuitting...")
                    break
                    
                elif key == ord('f'):
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        print("Fullscreen: ON")
                    else:
                        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                        print("Fullscreen: OFF")
                        
                elif key == ord('d'):
                    if self.current_profile and self.current_match:
                        self.show_dashboard = not self.show_dashboard
                        print(f"Dashboard: {'ON' if self.show_dashboard else 'OFF'}")
                    else:
                        print("No match to show dashboard for")
                        
                elif key == ord('s'):
                    self._show_stats()
                    
                elif key == ord('r'):
                    self._save_report()
                    
        except KeyboardInterrupt:
            print("\nInterrupted")
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.system.close()
            cv2.destroyAllWindows()
            print("✓ Closed")
    
    def _draw_live_view(self, frame, match_data, landmarks):
        """Draw live camera view."""
        display = frame.copy()
        h, w = display.shape[:2]
        
        # Header
        display = self.system.ui.draw_fbi_header(display, "FBI FACIAL RECOGNITION SYSTEM")
        
        # Draw face box
        if landmarks is not None:
            try:
                landmarks_array = np.array(landmarks)
                x_min = int(np.min(landmarks_array[:, 0]))
                y_min = int(np.min(landmarks_array[:, 1]))
                x_max = int(np.max(landmarks_array[:, 0]))
                y_max = int(np.max(landmarks_array[:, 1]))
                
                color = self.system.ui.colors['green'] if (match_data and match_data.get('is_match')) else self.system.ui.colors['yellow']
                cv2.rectangle(display, (x_min, y_min), (x_max, y_max), color, 3)
            except:
                pass
        
        # Status
        if match_data and match_data.get('is_match'):
            status = f"MATCH: {match_data.get('name', 'Unknown')}"
        elif landmarks is not None:
            status = "FACE DETECTED - NO MATCH"
        else:
            status = "SCANNING"
        
        display = self.system.ui.draw_status_indicator(display, status, (20, 80))
        
        # Instructions
        cv2.putText(display, "F=Fullscreen | D=Dashboard | Q=Quit", 
                   (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                   self.system.ui.colors['yellow'], 2)
        
        return display
    
    def _show_stats(self):
        """Show statistics."""
        stats = self.system.get_database_stats()
        print("\n" + "=" * 50)
        print("STATISTICS")
        print("=" * 50)
        for k, v in stats.items():
            print(f"  {k}: {v}")
        print("=" * 50 + "\n")
    
    def _save_report(self):
        """Save report."""
        try:
            os.makedirs("fbi_logs", exist_ok=True)
            report_path = os.path.join("fbi_logs", f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            self.system.logger.generate_report(report_path)
            print(f"\n✓ Report saved: {report_path}\n")
        except Exception as e:
            print(f"\n✗ Report error: {e}\n")


if __name__ == "__main__":
    app = FBIApp()
    app.run()

