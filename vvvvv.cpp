import cv2
import face_recognition

def compare_faces_and_display():
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Create a text file to store the results
    result_file = open("face_comparison_results.txt", "w")
    
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab a frame from the camera.")
            break

        # Find face locations in the frame
        face_locations = face_recognition.face_locations(frame)

        for (top, right, bottom, left) in face_locations:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Extract facial embeddings for the detected face
            face_embedding = face_recognition.face_encodings(frame, [(top, right, bottom, left)])[0]

            # Compare the face embedding with a known reference embedding
            # For demonstration purposes, we assume a known reference embedding "known_embedding"
            known_embedding = face_recognition.face_encodings(known_image)[0]
            face_distance = face_recognition.face_distance([known_embedding], face_embedding)[0]

            # Display the similarity score inside the rectangular area
            cv2.putText(frame, f"Similarity: {1 - face_distance:.2f}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Write the result to the text file
            result_file.write(f"Face Position: (left={left}, top={top}, right={right}, bottom={bottom}), Similarity: {1 - face_distance:.2f}\n")

        # Display the frame with the face detection results
        cv2.imshow("Face Comparison", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera, close the window, and close the result file
    cap.release()
    cv2.destroyAllWindows()
    result_file.close()

if __name__ == "__main__":
    # Load the known reference image
    known_image = face_recognition.load_image_file("path/to/known_reference_image.jpg")

    compare_faces_and_display()
