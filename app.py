import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Training data with specified mental health conditions
training_data = {
    "mental_health": {
        "definition": "Mental health refers to cognitive, emotional, and social well-being.",
        "conditions": {
            "depression": {
                "definition": "Depression is characterized by persistent sadness and loss of interest.",
                "types": ["Major Depressive Disorder", "Persistent Depressive Disorder"],
                "symptoms": [
                    "Feelings of hopelessness",
                    "Loss of energy",
                    "Difficulty concentrating",
                    "Changes in appetite or weight",
                    "Thoughts of self-harm"
                ],
                "management": [
                    "Therapy sessions",
                    "Antidepressant medications",
                    "Regular physical activity"
                ],
                "image": "https://example.com/depression.jpg"
            },
            "anxiety": {
                "definition": "Anxiety involves excessive worry or fear that interferes with daily activities.",
                "types": ["Generalized Anxiety Disorder", "Panic Disorder"],
                "symptoms": [
                    "Restlessness",
                    "Rapid heart rate",
                    "Sweating",
                    "Difficulty concentrating"
                ],
                "management": [
                    "Relaxation techniques",
                    "Cognitive-behavioral therapy",
                    "Medications like SSRIs"
                ],
                "image": "https://example.com/anxiety.jpg"
            },
            "schizophrenia": {
                "definition": ("Schizophrenia is a severe mental disorder that affects how a person thinks, feels, and behaves."),
                "types": ["Paranoid Schizophrenia", "Disorganized Schizophrenia", "Catatonic Schizophrenia"],
                "symptoms": [
                    "Hallucinations",
                    "Delusions",
                    "Disorganized thinking",
                    "Negative symptoms (e.g., lack of motivation)"
                ],
                "management": [
                    "Antipsychotic medications",
                    "Psychotherapy",
                    # Add an image URL if available
                ],
            },
            # Bipolar disorder condition
            "bipolar": {
                "definition": ("Bipolar disorder is characterized by extreme mood swings, including emotional highs "
                               "(mania) and lows (depression)."),
                "types": ["Bipolar I Disorder", "Bipolar II Disorder", "Cyclothymic Disorder"],
                "symptoms": {
                    "mania": ["Increased energy", "Euphoric mood", "Impulsive behavior"],
                    "depression": ["Feelings of sadness", "Low energy", "Difficulty concentrating"]
                },
                "management": [
                    "Mood stabilizers like lithium",
                    "Psychotherapy",
                    # Add an image URL if available
                ],
            },
            # Insomnia condition
            "insomnia": {
                "definition": ("Insomnia is a sleep disorder that is characterized by difficulty falling asleep or staying asleep."),
                "types": ["Acute Insomnia",  "Chronic Insomnia"],
               "symptoms": [
                   "Difficulty falling asleep",
                   "Waking up frequently during the night",
                   "Waking up too early and not being able to go back to sleep"
               ],
               "management": [
                   "Sleep hygiene practices",
                   "Cognitive Behavioral Therapy for Insomnia (CBT-I)",
                   "Medications (as prescribed)"
               ],
               # Add an image URL if available
           }
        }
    },
    # Specialists list
    'professionals': {
        'list': [
            {'name': 'Dr. Jane Doe', 'specialty': 'Psychiatrist', 'location': 'Nairobi', 'contact': '123-456-7890'},
            {'name': 'Dr. John Smith', 'specialty': 'Psychologist', 'location': 'Mombasa', 'contact': '987-654-3210'},
            {'name': 'Dr. Alice Jones', 'specialty': 'Therapist', 'location': 'Kisumu', 'contact': '0712345678'}
        ]
    },
    # Facilities list
    'facilities': {
        'list': [
            {'name': 'Nairobi Mental Health Center', 'services': ['Counseling', 'Therapy'], 'location': 'Nairobi'},
            {'name': 'Mombasa Wellness Clinic', 'services': ['Psychiatric Services', 'Support Groups'], 'location': 'Mombasa'},
            {'name': 'Kisumu Counseling Center', 'services': ['Individual Therapy', 'Group Therapy'], 'location': 'Kisumu'}
        ]
    }
}

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Chatbot route
@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form.get("message").lower()
    response = ("I'm sorry, I couldn't find relevant information.")

    # Detect and respond to definitions
    if ("mental health" in user_message):
        response = f"<h1>Mental Health</h1><p>{training_data['mental_health']['definition']}</p>"

    # Respond to specific conditions using keyword detection
    for condition, details in training_data["mental_health"]["conditions"].items():
        if re.search(r"\b" + re.escape(condition) + r"\b", user_message):
            response = (
                f"<h1>{condition.capitalize()}</h1>"
                f"<p><strong>Definition:</strong> {details['definition']}</p>"
                f"<h2>Symptoms:</h2><ul>" +
                "".join(f"<li>{symptom}</li>" for symptom in details.get("symptoms", [])) +
                "</ul><h2>Types:</h2><ul>" +
                "".join(f"<li>{type_}</li>" for type_ in details.get("types", [])) +
                "</ul><h2>Management:</h2><ol>" +
                "".join(f"<li>{step}</li>" for step in details.get("management", [])) +
                f"</ol><img src='{details.get('image', '#')}' alt='{condition} image'>"
            )
            break

    # Filter professionals based on location and specialization
    if ("professional" in user_message or ("specialist" in user_message)):
        location = None
        specialization = None

        # Detect location keywords
        for word in user_message.split():
            if word in ["nairobi", "mombasa", "kisumu"]:  # Add more locations as needed
                 location = word
                 break

        # Detect specialization keywords
        for word in user_message.split():
            if word in ["psychiatrist", "psychologist", "therapist"]:  # Add more specialties as needed
                 specialization = word
                 break

        # Filter professionals
        professionals = [
            prof for prof in training_data["professionals"]["list"]
            if (location is None or prof["location"].lower() == location.lower()) and
               (specialization is None or prof["specialty"].lower() == specialization.lower())
        ]

        if professionals:
            response = "<h1>Available Professionals:</h1>" + "".join(
                 [f"<p>{prof['name']} ({prof['specialty']}) - {prof['contact']} in {prof['location']}</p>" for prof in professionals]
             )
        else:
             response = "<p>No professionals found matching your criteria.</p>"

    # Filter facilities based on location and services
    if ("facility" in user_message or ("center" in user_message)):
         location = None
         service = None

         # Detect location keywords
         for word in user_message.split():
             if word in ["nairobi", 'mombasa', 'kisumu']:  # Add more locations as needed
                  location = word
                  break

         # Detect service keywords
         for word in user_message.split():
             if word in ["counseling", 'therapy', 'psychiatric services']:  # Add more services as needed
                  service = word
                  break

         # Filter facilities
         facilities = [
             facility for facility in training_data["facilities"]["list"]
             if (location is None or facility["location"].lower() == location.lower()) and
               (service is None or service in facility["services"])
         ]

         if facilities:
             response = "<h1>Available Facilities:</h1>" + "".join(
                 [f"<p>{facility['name']} - {', '.join(facility['services'])} in {facility['location']}</p>" for facility in facilities]
             )
         else:
             response = "<p>No facilities found matching your criteria.</p>"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)



