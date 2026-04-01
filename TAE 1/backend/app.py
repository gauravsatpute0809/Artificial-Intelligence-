from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from chatbot_logic import ChatbotLogic
import os
import sqlite3

app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
CORS(app) # Allow cross-origin requests

chatbot = ChatbotLogic()
DB_PATH = os.path.join(os.path.dirname(__file__), "hospital.db")

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")


@app.route('/get_departments', methods=['GET'])
def departments():
    return jsonify(chatbot.get_departments())

@app.route('/get_doctors', methods=['GET'])
def doctors_list():
    dept = request.args.get('department')
    if dept:
        return jsonify(chatbot.get_doctors_by_department(dept))
    # otherwise return all structured for the tree
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, department FROM Doctors")
    all_docs = {}
    for row in cursor.fetchall():
        if row[2] not in all_docs:
            all_docs[row[2]] = []
        all_docs[row[2]].append({"id": row[0], "name": row[1]})
    conn.close()
    return jsonify(all_docs)

@app.route('/check_availability', methods=['GET'])
def check():
    doc_id = request.args.get('doctor_id')
    return jsonify(chatbot.get_availability(doc_id))

@app.route('/book_appointment', methods=['POST'])
def book():
    data = request.json
    ok = chatbot.book_appointment(data, data['doctor_id'], data['slot'])
    if ok:
        return jsonify({"status": "success", "message": "Booking Confirmed!"})
    return jsonify({"status": "error", "message": "Failed to book. Slot might be taken."}), 400

@app.route('/chat', methods=['POST'])
def chat_entry():
    user_input = request.json.get('message', '').lower()
    step = request.json.get('step', 'start')
    
    if step == 'start':
        greeting = chatbot.get_greeting(user_input)
        if greeting:
            return jsonify({"response": greeting, "next_step": "name"})
        return jsonify({"response": "I didn't quite get that. Could you say Hello to start?", "next_step": "start"})
    
    if step == 'name':
        if chatbot.validate_name(user_input.strip()):
            return jsonify({"response": f"Nice to meet you {user_input.title()}! How old are you?", "next_step": "age"})
        return jsonify({"response": "Please enter a valid name.", "next_step": "name"})
    
    if step == 'age':
        if chatbot.validate_age(user_input):
            return jsonify({"response": "Great! Please provide your 10-digit mobile number.", "next_step": "mobile"})
        return jsonify({"response": "Please enter a valid age (1-120).", "next_step": "age"})
    
    if step == 'mobile':
        if chatbot.validate_mobile(user_input):
            return jsonify({
                "response": "Perfect! Now, would you like to **Book Directly** or use the **Symptom Checker**?", 
                "next_step": "mode", 
                "options": ["Book Directly", "Symptom Checker"]
            })
        return jsonify({"response": "Invalid number. Please enter a 10-digit mobile number.", "next_step": "mobile"})

    if step == 'mode':
        if "symptom" in user_input.lower():
            return jsonify({"response": "Tell me about your symptoms (e.g., 'I have chest pain').", "next_step": "symptoms"})
        else:
            return jsonify({"response": "No problem. Which department would you like to visit?", "next_step": "department", "data": chatbot.get_departments()})

    if step == 'symptoms':
        dept = chatbot.suggest_department(user_input)
        if dept:
            return jsonify({
                "response": f"Based on your symptoms, it looks like you should visit **{dept}**. Confirm or Choose Manual?", 
                "next_step": "symptom_confirm", 
                "data": [dept, "Manual Choice"]
            })
        return jsonify({"response": "I'm not sure which department. Please choose specialized one:", "next_step": "department", "data": chatbot.get_departments()})

    if step == 'symptom_confirm':
        if "manual" in user_input.lower():
            return jsonify({"response": "Please select a department:", "next_step": "department", "data": chatbot.get_departments()})
        return jsonify({"response": f"Selecting doctors for {user_input}...", "next_step": "auto_dept", "dept": user_input})

    return jsonify({"response": "Error processing chat.", "next_step": "start"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
