"""
FBI-Style Facial Recognition Application
Professional interface with real-time matching and database management
"""

import cv2
import numpy as np
import time
from fbi_system import FBIFacialRecognitionSystem


class FBIApplication:
    """
    Main FBI-style facial recognition application.
    Professional interface with real-time matching.
    """
    
    def __init__(self):
        """Initialize FBI application."""
        self.system = FBIFacialRecognitionSystem()
        self.mode = "IDENTIFY"  # IDENTIFY, MANAGE
        self.status = "SCANNING"
        self.current_match = None
        
    def run_identification_mode(self):
        """Run real-time identification mode."""
        print("=" * 70)
        print("FBI FACIAL RECOGNITION SYSTEM - IDENTIFICATION MODE")
        print("=" * 70)
        print("\nInitializing camera...")
        
        try:
            self.system.initialize_camera()
            
            print("\nControls:")
            print("  Q - Quit")
            print("  S - Show statistics")
            print("  R - Generate report")
            print("\nStarting identification...\n")
            
            while True:
                ret, frame = self.system.cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Calculate FPS
                self.system.calculate_fps()
                
                # Identify face
                match_data, landmarks = self.system.identify_face(frame)
                
                # Create display frame
                display = frame.copy()
                
                # Draw FBI header
                display = self.system.ui.draw_fbi_header(display)
                
                # Determine status
                if match_data and match_data['is_match']:
                    self.status = "MATCH FOUND"
                    self.current_match = match_data
                elif landmarks is not None:
                    self.status = "NO MATCH"
                    self.current_match = None
                else:
                    self.status = "SCANNING"
                    self.current_match = None
                
                # Draw status indicator
                display = self.system.ui.draw_status_indicator(
                    display, self.status, position=(20, 80)
                )
                
                # Draw match info if found
                if self.current_match:
                    display = self.system.ui.draw_match_info_panel(
                        display, self.current_match, position=(20, 150)
                    )
                    
                    # Draw confidence meter
                    display = self.system.ui.draw_confidence_meter(
                        display, 
                        self.current_match['confidence'],
                        position=(400, 150)
                    )
                
                # Draw database stats
                stats = self.system.get_database_stats()
                stats_text = [
                    f"FPS: {self.system.fps}",
                    f"Persons in DB: {stats['total_persons']}",
                    f"Total Images: {stats['total_images']}"
                ]
                
                y_pos = 80
                for text in stats_text:
                    cv2.putText(display, text, (display.shape[1] - 250, y_pos),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                               self.system.ui.colors['white'], 1, cv2.LINE_AA)
                    y_pos += 25
                
                # Draw timeline of recent matches
                if self.system.recent_matches:
                    display = self.system.ui.draw_timeline(
                        display, 
                        self.system.recent_matches,
                        position=(20, display.shape[0] - 120),
                        width=display.shape[1] - 40
                    )
                
                # Update animation
                self.system.ui.update_animation()
                
                # Show display
                cv2.imshow('FBI Facial Recognition System', display)
                
                # Handle keys
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('s') or key == ord('S'):
                    self.show_statistics()
                elif key == ord('r') or key == ord('R'):
                    self.generate_report()
                    
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.system.close()
    
    def show_statistics(self):
        """Show system statistics."""
        print("\n" + "=" * 70)
        print("SYSTEM STATISTICS")
        print("=" * 70)
        
        db_stats = self.system.get_database_stats()
        for key, value in db_stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        log_stats = self.system.logger.get_statistics()
        print("\nMatch Statistics:")
        for key, value in log_stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        print("=" * 70 + "\n")
    
    def generate_report(self):
        """Generate and save report."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = f"fbi_report_{timestamp}.txt"
        
        self.system.export_report(report_file)
        print(f"\n✓ Report generated: {report_file}\n")


def main():
    """Main entry point."""
    app = FBIApplication()
    app.run_identification_mode()


if __name__ == "__main__":
    main()

