import gradio as gr
import os
from PIL import Image
import numpy as np

def upload_images(images, student_name):
    """Uploads multiple images to a student-specific folder."""
    try:
        if not student_name:
            return "Student Name is required!"

        # Clean and format the student name for folder creation
        student_name = student_name.strip().replace(" ", "_")
        save_dir = f"images/{student_name}"
        os.makedirs(save_dir, exist_ok=True)

        # Process and save each image
        for idx, image in enumerate(images):
            # Generate filename using student name and index
            unique_filename = f"{student_name}_{idx+1}.jpg"
            save_path = os.path.join(save_dir, unique_filename)

            # If image is a tuple (Gallery might return (array, path) or (array,))
            if isinstance(image, tuple):
                print(f"Tuple contents for image {idx+1}: {image}")
                image_data = image[0]
                if isinstance(image_data, np.ndarray):
                    pil_img = Image.fromarray(image_data)
                elif isinstance(image_data, str):
                    pil_img = Image.open(image_data)
                else:
                    return f"Error: Unexpected tuple content for image {idx+1} - Type: {type(image_data)}"
            # If image is a numpy array directly
            elif isinstance(image, np.ndarray):
                pil_img = Image.fromarray(image)
            # If image is a file path directly
            elif isinstance(image, str):
                pil_img = Image.open(image)
            else:
                return f"Error: Unexpected image format for image {idx+1} - Type: {type(image)}"

            # Convert to RGB if needed (JPG requires RGB)
            if pil_img.mode != 'RGB':
                pil_img = pil_img.convert('RGB')

            # Save as JPG
            pil_img.save(save_path, format='JPEG', quality=95)

        return f"{len(images)} Images uploaded successfully for {student_name}!"

    except Exception as e:
        return f"Error uploading images: {e}"

# Create the Gradio interface
iface = gr.Interface(
    fn=upload_images,
    inputs=[
        gr.Gallery(label="Upload Multiple Images", columns=2, height="auto"),  # Input for multiple image uploads
        gr.Textbox(label="Student Name", placeholder="Enter Full Name of Student"),  # Input for student name
    ],
    outputs=gr.Textbox(label="Status"),  # Output message
    title="Student Face Registration",
    description="Upload multiple face images of a student. Images will be saved as JPG files in a folder named after the student under abhay ka system",
)

# Launch the interface
iface.launch(share=True)