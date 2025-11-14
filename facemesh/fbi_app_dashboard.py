"""
FBI Facial Recognition Application with Dashboard
Shows complete profile information when person is identified
"""

import cv2
import numpy as np
import time
from fbi_system import FBIFacialRecognitionSystem
from fbi_dashboard import FBIDashboard

class FBIApplicationDashboard:
    """FBI application with comprehensive dashboard display."""
    
    def __init__(self):
        """Initialize FBI application with dashboard."""
        print("Initializing FBI Facial Recognition System with Dashboard...")
        self.system = FBIFacialRecognitionSystem()
        self.dashboard = FBIDashboard()
        self.show_dashboard = False
        self.current_profile = None
        self.current_match = None
        self.last_match_time = 0
        self.dashboard_lock_time = 0
        self.fullscreen = False
        self.window_name = 'FBI Facial Recognition - Dashboard'
        
    def run(self):
        """Run the FBI application."""
        print("=" * 70)
        print("FBI FACIAL RECOGNITION SYSTEM - DASHBOARD MODE")
        print("=" * 70)
        print("\nInitializing camera...")
        
        self.system.initialize_camera()
        
        print("\nControls:")
        print("  Q - Quit")
        print("  D - Toggle Dashboard")
        print("  F - Toggle Fullscreen")
        print("  S - Show statistics")
        print("  R - Generate report")
        print("\nStarting identification...\n")

        # Create window
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
        try:
            while True:
                ret, frame = self.system.cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Calculate FPS
                fps = self.system.calculate_fps()
                
                # Identify face
                match_data, landmarks = self.system.identify_face(frame)
                
                # Auto-show dashboard when match found
                if match_data and match_data.get('is_match'):
                    current_time = time.time()
                    # Only update if it's a new match or 2 seconds have passed
                    if (self.current_match is None or 
                        self.current_match.get('person_id') != match_data.get('person_id') or
                        current_time - self.last_match_time > 2.0):
                        
                        person_id = match_data.get('person_id')
                        profile = self.dashboard.get_profile(person_id)
                        
                        if profile:
                            self.current_profile = profile
                            self.current_match = match_data
                            self.show_dashboard = True
                            self.dashboard_lock_time = current_time
                            self.last_match_time = current_time
                            print(f"\n✓ MATCH FOUND: {profile.get('full_name')} - Confidence: {match_data.get('confidence', 0)*100:.1f}%")
                            print("  Dashboard displayed automatically")
                
                # Create display
                if self.show_dashboard and self.current_profile and self.current_match:
                    # Show dashboard
                    display = self.dashboard.draw_dashboard(frame, self.current_profile, self.current_match)
                else:
                    # Show live view
                    display = self._draw_live_view(frame, match_data, landmarks, fps)
                
                # Show display
                cv2.imshow(self.window_name, display)

                # Handle keys
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('f'):
                    # Toggle fullscreen
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        print("Fullscreen: ON")
                    else:
                        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                        print("Fullscreen: OFF")
                elif key == ord('d'):
                    # Toggle dashboard
                    if self.current_profile and self.current_match:
                        self.show_dashboard = not self.show_dashboard
                        print(f"Dashboard: {'ON' if self.show_dashboard else 'OFF'}")
                elif key == ord('s'):
                    self._show_statistics()
                elif key == ord('r'):
                    self._generate_report()
                
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.system.close()
            cv2.destroyAllWindows()
            print("✓ System closed")
    
    def _draw_live_view(self, frame: np.ndarray, match_data, landmarks, fps: float) -> np.ndarray:
        """Draw live camera view with match overlay."""
        display = frame.copy()
        
        # Draw FBI header
        display = self.system.ui.draw_fbi_header(display, "FBI FACIAL RECOGNITION SYSTEM")
        
        # Draw face box if detected
        if landmarks is not None:
            landmarks_array = np.array(landmarks)
            x_min = int(np.min(landmarks_array[:, 0]))
            y_min = int(np.min(landmarks_array[:, 1]))
            x_max = int(np.max(landmarks_array[:, 0]))
            y_max = int(np.max(landmarks_array[:, 1]))
            
            color = self.system.ui.colors['green'] if match_data and match_data.get('is_match') else self.system.ui.colors['yellow']
            cv2.rectangle(display, (x_min, y_min), (x_max, y_max), color, 3)
        
        # Draw match info if available
        if match_data:
            if match_data.get('is_match'):
                status = f"MATCH: {match_data.get('name', 'Unknown')}"
                display = self.system.ui.draw_match_info_panel(display, match_data, position=(20, 100))
                display = self.system.ui.draw_confidence_meter(display, match_data.get('confidence', 0), 
                                                              position=(display.shape[1] - 350, 100), 
                                                              label="MATCH CONFIDENCE")
            else:
                status = "NO MATCH"
        else:
            status = "SCANNING FOR FACES"
        
        # Draw status
        display = self.system.ui.draw_status_indicator(display, status, position=(20, 80))
        
        # Draw FPS
        fps_text = f"FPS: {fps:.1f}" if fps is not None else "FPS: --"
        cv2.putText(display, fps_text, (display.shape[1] - 150, display.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.system.ui.colors['white'], 2)
        
        # Instructions
        cv2.putText(display, "Press D for Dashboard | F for Fullscreen | Q to Quit | S for Stats",
                   (20, display.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.system.ui.colors['yellow'], 2)
        
        return display
    
    def _show_statistics(self):
        """Show database statistics."""
        stats = self.system.get_database_stats()
        print("\n" + "=" * 50)
        print("DATABASE STATISTICS")
        print("=" * 50)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print("=" * 50 + "\n")
    
    def _generate_report(self):
        """Generate match report."""
        print("\n" + "=" * 50)
        print("GENERATING MATCH REPORT...")
        print("=" * 50)
        import os
        from datetime import datetime
        report_path = os.path.join("fbi_logs", f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        self.system.logger.generate_report(report_path)
        print(f"✓ Report saved to: {report_path}")
        print("=" * 50 + "\n")


def main():
    """Main entry point."""
    app = FBIApplicationDashboard()
    app.run()


if __name__ == "__main__":
    main()

