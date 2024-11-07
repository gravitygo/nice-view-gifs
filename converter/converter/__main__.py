import os
import sys
from process import process_gif
from lvgf import create_edits

VIEW_WIDTH = 68
VIEW_HEIGHT = 140

def validate_gif_file(file_path):
    if not os.path.isfile(file_path):
        print("Error: File not found. Please enter a valid file path.")
        return False
    if not file_path.lower().endswith(".gif"):
        print("Error: File is not a GIF. Please enter a valid GIF file.")
        return False
    return True

def prompt_for_gif_file():
    while True:
        gif_file = input("Enter the path to the GIF file: ").strip()
        if validate_gif_file(gif_file):
            return gif_file

def prompt_for_output_directory():
    while True:
        output_directory = input("Enter the output directory to put the processed gif and git patch: ").strip()
        if os.path.isdir(output_directory):
            return output_directory
        else:
            print("Error: Invalid directory. Please enter a valid directory path.")

def prompt_for_threshold():
    while True:
        try:
            threshold = int(input("Enter the threshold, lower reduces brightness (0-255): ").strip())
            if 0 <= threshold <= 255:
                return threshold
            else:
                print("Error: Threshold must be between 0 and 255.")
        except ValueError:
            print("Error: Please enter a valid integer.")

def main():
    gif_file = prompt_for_gif_file()
    output_directory = prompt_for_output_directory()
    output_file = os.path.join(output_directory, os.path.basename(gif_file))
    speed = 100

    while True:
        threshold = prompt_for_threshold()

        print(f"Processing {gif_file}...")
        speed = process_gif(gif_file, output_file, VIEW_WIDTH, VIEW_HEIGHT, threshold, 1)

        # Prompt user to check output and decide if they want to redo
        print(f"GIF has been saved to {output_file}")
        redo = input("Would you like to redo processing with a different threshold? (y/n): ").strip().lower()
        if redo != 'y':
            break
    
    create_edits(output_file, speed)


if __name__ == "__main__":
    main()
