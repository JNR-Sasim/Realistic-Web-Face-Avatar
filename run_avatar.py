#!/usr/bin/env python3
"""
Face Avatar Launcher
Choose between different avatar versions
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Print the application banner"""
    print("=" * 50)
    print("🎭 FACE AVATAR SYSTEM")
    print("=" * 50)
    print()

def print_menu():
    """Print the main menu"""
    print("Choose an avatar version:")
    print("1. Basic Face Avatar (Python + OpenCV)")
    print("2. Fixed Face Avatar (Better camera handling)")
    print("3. Advanced Face Avatar (Enhanced features)")
    print("4. Realistic Face Avatar (3D Mesh - Python)")
    print("5. Web Face Avatar (Browser-based)")
    print("6. Realistic Web Avatar (3D Mesh - Browser)")
    print("7. Test Camera")
    print("8. Test System Setup")
    print("9. Exit")
    print()

def run_basic_avatar():
    """Run the basic face avatar"""
    print("Starting Basic Face Avatar...")
    print("Press 'q' to quit the application")
    print()
    
    try:
        subprocess.run([sys.executable, "face_avatar.py"], check=True)
    except KeyboardInterrupt:
        print("\nAvatar stopped by user")
    except Exception as e:
        print(f"Error running basic avatar: {e}")

def run_fixed_avatar():
    """Run the fixed face avatar"""
    print("Starting Fixed Face Avatar (Better camera handling)...")
    print("Press 'q' to quit the application")
    print()
    
    try:
        subprocess.run([sys.executable, "face_avatar_fixed.py"], check=True)
    except KeyboardInterrupt:
        print("\nAvatar stopped by user")
    except Exception as e:
        print(f"Error running fixed avatar: {e}")

def run_advanced_avatar():
    """Run the advanced face avatar"""
    print("Starting Advanced Face Avatar...")
    print("Press 'q' to quit the application")
    print()
    
    try:
        subprocess.run([sys.executable, "advanced_avatar.py"], check=True)
    except KeyboardInterrupt:
        print("\nAvatar stopped by user")
    except Exception as e:
        print(f"Error running advanced avatar: {e}")

def run_realistic_avatar():
    """Run the realistic face avatar"""
    print("Starting Realistic Face Avatar (3D Mesh)...")
    print("Features: MediaPipe 3D face mesh, realistic rendering")
    print("Press 'q' to quit the application")
    print()
    
    try:
        subprocess.run([sys.executable, "realistic_face_avatar.py"], check=True)
    except KeyboardInterrupt:
        print("\nAvatar stopped by user")
    except Exception as e:
        print(f"Error running realistic avatar: {e}")

def run_web_avatar():
    """Open the web-based avatar in browser"""
    print("Opening Web Face Avatar in browser...")
    print("Make sure to allow camera access when prompted")
    print()
    
    web_file = Path("web_avatar.html")
    if web_file.exists():
        webbrowser.open(f"file://{web_file.absolute()}")
        print("Web avatar opened in your default browser")
        print("Close the browser tab to stop the avatar")
    else:
        print("Error: web_avatar.html not found")

def run_realistic_web_avatar():
    """Open the realistic web-based avatar in browser"""
    print("Opening Realistic Web Face Avatar in browser...")
    print("Features: MediaPipe 3D face mesh, realistic rendering, depth mapping")
    print("Make sure to allow camera access when prompted")
    print()
    
    web_file = Path("realistic_web_avatar.html")
    if web_file.exists():
        webbrowser.open(f"file://{web_file.absolute()}")
        print("Realistic web avatar opened in your default browser")
        print("Close the browser tab to stop the avatar")
    else:
        print("Error: realistic_web_avatar.html not found")
        print("Creating realistic web avatar...")
        create_realistic_web_avatar()

def create_realistic_web_avatar():
    """Create the realistic web avatar file"""
    try:
        print("Realistic web avatar creation not implemented yet.")
        print("Use the basic web avatar for now.")
    except Exception as e:
        print(f"Error creating realistic web avatar: {e}")

def test_camera():
    """Run the camera test"""
    print("Running camera test...")
    print()
    
    try:
        subprocess.run([sys.executable, "camera_test.py"], check=True)
    except Exception as e:
        print(f"Error running camera test: {e}")

def test_setup():
    """Run the system test"""
    print("Running system test...")
    print()
    
    try:
        subprocess.run([sys.executable, "test_setup.py"], check=True)
    except Exception as e:
        print(f"Error running test: {e}")

def main():
    """Main launcher function"""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-9): ").strip()
            
            if choice == "1":
                run_basic_avatar()
            elif choice == "2":
                run_fixed_avatar()
            elif choice == "3":
                run_advanced_avatar()
            elif choice == "4":
                run_realistic_avatar()
            elif choice == "5":
                run_web_avatar()
            elif choice == "6":
                run_realistic_web_avatar()
            elif choice == "7":
                test_camera()
            elif choice == "8":
                test_setup()
            elif choice == "9":
                print("Goodbye! 👋")
                break
            else:
                print("Invalid choice. Please enter 1-9.")
            
            print()
            input("Press Enter to continue...")
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()

if __name__ == "__main__":
    main() 