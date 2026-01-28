import cv2
import numpy as np
import os

def main():
    # Define paths
    input_path = "product.jpg"
    output_dir = "output/"
    
    # Check if input image exists
    if not os.path.exists(input_path):
        print(f"Error: Input image '{input_path}' not found.")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Load the image
    image = cv2.imread(input_path)
    if image is None:
        print(f"Error: Could not load image from '{input_path}'.")
        return
    
    # Get image dimensions for area calculations
    height, width = image.shape[:2]
    total_image_area = height * width
    
    # Step 2: Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_dir + "gray.jpg", gray)
    
    # Step 3: Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite(output_dir + "blurred.jpg", blurred)
    
    # Step 4: Object Segmentation - Isolate main object from background
    # Use adaptive thresholding to separate object from background
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours to identify connected components
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the largest contour (main object)
    if contours:
        main_object_contour = max(contours, key=cv2.contourArea)
        
        # Create binary mask for the main object
        object_mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.fillPoly(object_mask, [main_object_contour], 255)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        object_mask = cv2.morphologyEx(object_mask, cv2.MORPH_CLOSE, kernel)
        object_mask = cv2.morphologyEx(object_mask, cv2.MORPH_OPEN, kernel)
        
        # Apply mask to the blurred image to suppress background
        masked_blurred = cv2.bitwise_and(blurred, blurred, mask=object_mask)
    else:
        # Fallback to original blurred image if no contours found
        masked_blurred = blurred
        object_mask = np.ones(gray.shape, dtype=np.uint8) * 255
    
    # Step 5: Canny Edge Detection (object only)
    edges = cv2.Canny(masked_blurred, 50, 150)
    cv2.imwrite(output_dir + "edges.jpg", edges)
    
    # Step 6: Morphological Processing
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    morphology = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(output_dir + "morphology.jpg", morphology)
    
    # Step 7: Binary thresholding
    _, binary = cv2.threshold(morphology, 127, 255, cv2.THRESH_BINARY)
    
    # Step 8: Detect contours (damage only - background already suppressed)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter small contours (noise removal)
    min_contour_area = 50  # Adjust based on image size
    valid_contours = []
    total_damage_area = 0
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_contour_area:
            valid_contours.append(contour)
            total_damage_area += area
    
    # Step 9: Create output image with black & red theme
    # Darken the original image
    darkened = cv2.convertScaleAbs(image, alpha=0.6, beta=0)
    
    # Draw damage highlights in red (only on object)
    for contour in valid_contours:
        # Draw bounding box in red
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(darkened, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Optional: Fill contour with semi-transparent red overlay
        overlay = darkened.copy()
        cv2.drawContours(overlay, [contour], -1, (0, 0, 255), -1)
        darkened = cv2.addWeighted(darkened, 0.7, overlay, 0.3, 0)
    
    # Save final result
    cv2.imwrite(output_dir + "damage_detected.jpg", darkened)
    
    # Calculate damage percentage
    damage_percentage = (total_damage_area / total_image_area) * 100
    
    # Rule-based quality decision
    damage_detected = len(valid_contours) > 0
    quality_status = "REJECT" if damage_percentage > 5 else "ACCEPTABLE"
    
    # Print terminal quality report
    print("----------------------------------")
    print("Product Material: Rigid Metal / Hard Plastic")
    print(f"Damage Detected: {'YES' if damage_detected else 'NO'}")
    print(f"Damage Area (%): {damage_percentage:.2f}")
    print(f"Quality Status: {quality_status}")
    print("Decision Basis: Edge discontinuity and damage area threshold")
    print("----------------------------------")

if __name__ == "__main__":
    main()
