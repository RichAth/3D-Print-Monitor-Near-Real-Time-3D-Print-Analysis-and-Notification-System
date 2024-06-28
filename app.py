import cv2
import time
import yagmail
from datetime import datetime
import json
from openai import OpenAI
import base64

# Gmail settings
gmail_user = 'your_email@gmail.com'
gmail_password = 'your_password'
recipient_email = 'recipient_email@gmail.com'

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Adjust '0' if you have multiple webcams

def take_photo():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        return None
    filename = f'photos/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.jpg'
    cv2.imwrite(filename, frame)
    return filename

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_print(filename):
    
    client = OpenAI(api_key='your_openai_api_key')

    prompt ="""
        Please evaluate the attached image of a 3D print in progress. Determine if the print is successful or failing based on the following criteria:

        1. Fires: Check for any signs of fire, smoke, unusual heating, or electrical malfunctions.
        2. Spaghetti Stringing: Look for plastic strings or misplaced filaments resembling spaghetti.
        3. Bed Adhesion: Ensure the object remains firmly attached to the print bed, without warping, curling, or lifting of the object's edges.

        Or if the print has completed. 
        
        Explination of requirements:
        - Fires:
        Causes: Fires can occur due to overheating of the printer components, electrical malfunctions, or issues with the power supply. It's crucial to have a printer that is well-maintained, with electronics and wiring that meet safety standards.
        Prevention: Using a printer with thermal runaway protection, keeping the printer in a clean, ventilated space, and regular maintenance checks are essential steps to prevent fires.
        
        - Spaghetti Stringing:
        Description: This issue occurs when the printer extrudes plastic but it doesn’t stick to the desired part of the build, instead creating strings of plastic that resemble spaghetti. This can happen if the print detaches from the bed, or if there’s an issue with the print path.
        Causes: Poor adhesion, incorrect temperature settings for the filament, or issues with the print speed can lead to this problem.
        Solutions: Ensuring proper bed leveling, adjusting the nozzle temperature, print speed, and ensuring the filament is dry can help mitigate this issue.
        
        - Bed Adhesion:
        Description: Bed adhesion is critical to ensure the initial layers of the print stick to the print bed properly. Poor adhesion can cause the print to move during printing, leading to failure.
        Causes: Inadequate bed cleaning, incorrect bed temperature, or the use of a wrong bed surface material.
        Solutions: Cleaning the bed thoroughly before printing, using adhesives like glue sticks or hairspray, adjusting the bed temperature, and using a suitable print bed surface can improve adhesion.
                Return your assessment as a JSON object with the following structure:

        - Completed Print:
        Description: The print head will be raised and homed in its horizontal axis and the print bed will be in the most forward position presenting the completed part.
        Causes: The printer has completed executing the print program.

        Example Assessment:
        Based on the visual clues in the provided image and the descriptions of common printing issues:
        Fires: There is no visible sign of smoke, unusual heating, or any electrical malfunctions in the image. The printer components appear to be operating normally without any signs of distress that could lead to a fire. Therefore, it is likely that there is no fire hazard occurring at the moment the image was taken.
        Spaghetti Stringing: The object on the print bed shows a smooth, clean layering without any visible strands or misplaced filaments that resemble spaghetti stringing. This suggests that the filament is adhering properly to the layers below and the printer is following the correct path.
        Bed Adhesion: The object being printed appears to be stable and adhering well to the print bed. There is no visible warping, curling, or lifting of the object's edges, which are common signs of adhesion problems.
        From these observations, there's a reasonable level of confidence that the 3D print is proceeding successfully without the specific failures of fires, spaghetti stringing, or adhesion issues. Of course, a comprehensive evaluation would require more than a snapshot, involving ongoing observation and possibly a closer look at the printer's settings and the material condition. But from what can be seen in the image, the print seems to be on the right track.
        
        Example Response:        
        {
        "status": "success", "failure", or "complete"
        "confidence": "high", "medium", or "low",
        "issues": ["list of detected issues, if any"]
        }
        """
    response = client.chat.completions.create(
        model= "gpt-4o",
        response_format={ "type": "json_object" },
        messages= [
            {
                "role": "user", 
                "content":[
                    {"type": "text", "text": f"{prompt}"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(filename)}"#,
                            #"detail": "medium"
                        }
                    }
                ]
            }
        ],
        max_tokens= 4000
    )
        
    return json.loads(response.choices[0].message.content)

def send_email(subject, body):
    yag = yagmail.SMTP(gmail_user, gmail_password)
    yag.send(
        to=recipient_email,
        subject=subject,
        contents=body,
    )

def main():
    while True:
        photo_path = take_photo()
        if photo_path:
            analysis = analyze_print(photo_path)
            try:
                analysis_result = analysis
                if analysis_result['status'] == 'failure':
                    subject = f"3D Print Failure Alert: {analysis_result['confidence']} Confidence"
                    body = f"Issues detected: {', '.join(analysis_result['issues'])}"
                    send_email(subject, body)
                if analysis_result['status'] == 'complete':
                    subject = f"3D Print Completed: {analysis_result['confidence']} Confidence"
                    body = f"Issues detected: {', '.join(analysis_result['issues'])}"
                    send_email(subject, body)                    
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing analysis result: {e}")
        time.sleep(300)  # Wait for 5 minutes

if __name__ == '__main__':
    main()
