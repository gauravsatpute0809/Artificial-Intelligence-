import React, { useState, useEffect, useRef } from 'react';

const ChatPanel = ({ selectedDoctor, setSelectedDoctor }) => {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm your Engineering Hospital Chatbot. Type 'Hi' to start booking an appointment.", sender: "bot" }
  ]);
  const [inputText, setInputText] = useState("");
  const [step, setStep] = useState("start");
  const [patientData, setPatientData] = useState({ name: "", age: "", mobile: "", doctor_id: null, doctor_name: "", slot: "" });
  const [options, setOptions] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    if (selectedDoctor && (step === "doctor" || step === "department")) {
      handleDoctorSelection(selectedDoctor);
    }
  }, [selectedDoctor]);

  const addMessage = (text, sender) => {
    setMessages((prev) => [...prev, { text, sender, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }]);
  };

  const processResponse = async (userInput, currentStep) => {
    setIsTyping(true);
    try {
      const res = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput, step: currentStep })
      });
      const data = await res.json();
      
      setTimeout(() => {
        setIsTyping(false);
        addMessage(data.response, "bot");
        setStep(data.next_step);

        if (data.options) {
          setOptions(data.options);
        } else if (data.next_step === "department" || data.next_step === "symptom_confirm") {
          setOptions(data.data);
        } else {
          setOptions([]);
        }

        // Store patient data as we go
        if (currentStep === "name") setPatientData(p => ({ ...p, name: userInput }));
        if (currentStep === "age") setPatientData(p => ({ ...p, age: userInput }));
        if (currentStep === "mobile") setPatientData(p => ({ ...p, mobile: userInput }));

        // Handle auto transition if department is confirmed
        if (data.next_step === "auto_dept") {
          fetchDoctors(data.dept);
        }

      }, 800);
    } catch (err) {
      console.error(err);
      setIsTyping(false);
      addMessage("Sorry, I'm having trouble connecting to the server.", "bot");
    }
  };

  const handleSend = (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    addMessage(inputText, "user");
    const input = inputText;
    setInputText("");
    processResponse(input, step);
  };

  const handleOptionClick = (option) => {
    addMessage(option, "user");
    if (step === "department") {
      fetchDoctors(option);
    } else {
      processResponse(option, step);
    }
  };

  const fetchDoctors = async (dept) => {
    setIsTyping(true);
    const res = await fetch(`http://localhost:5000/get_doctors?department=${dept}`);
    const data = await res.json();
    setIsTyping(false);
    addMessage(`Great Choice! Here are the specialists in ${dept}. Please select one:`, "bot");
    // FIX: Store doctor objects (id AND name) to ensure handleDoctorSelection works
    setOptions(data);
    setStep("doctor");
  };

  const handleDoctorSelection = async (doctor) => {
    addMessage(`Selected Doctor: ${doctor.name}`, "user");
    setPatientData(p => ({ ...p, doctor_id: doctor.id, doctor_name: doctor.name }));
    setIsTyping(true);
    const res = await fetch(`http://localhost:5000/check_availability?doctor_id=${doctor.id}`);
    const slots = await res.json();
    setIsTyping(false);
    
    if (slots.length > 0) {
      addMessage(`Dr. ${doctor.name} is available. Please select a time slot:`, "bot");
      setOptions(slots);
      setStep("slot");
    } else {
      addMessage(`Sorry, Dr. ${doctor.name} has no available slots today. Please choose another doctor from the tree.`, "bot");
      setStep("doctor");
    }
  };

  const handleSlotSelection = async (slot) => {
    addMessage(slot, "user");
    setPatientData(p => ({ ...p, slot: slot }));
    confirmBooking(slot);
  };

  const confirmBooking = async (slot) => {
    setIsTyping(true);
    const finalData = { ...patientData, slot: slot };
    const res = await fetch('http://localhost:5000/book_appointment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(finalData)
    });
    const data = await res.json();
    setIsTyping(false);
    
    if (data.status === "success") {
      addMessage(`${data.message}\n\n📝 Booking Summary:\n- Patient: ${finalData.name}\n- Doctor: ${finalData.doctor_name}\n- Time: ${slot}\n- Date: Today\n\nThank you for choosing Engineering Hospital!`, "bot");
      setStep("finished");
    } else {
      addMessage(data.message, "bot");
    }
    setOptions([]);
  };

  const resetChat = () => {
    setMessages([{ text: "Hello! I'm your Engineering Hospital Chatbot. Type 'Hi' to start booking an appointment.", sender: "bot" }]);
    setStep("start");
    setOptions([]);
    setPatientData({ name: "", age: "", mobile: "", doctor_id: null, doctor_name: "", slot: "" });
    setSelectedDoctor(null);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="bot-avatar">🤖</div>
        <div className="bot-info">
          <h3>Assistant</h3>
          <span className="status">Online</span>
        </div>
        <button onClick={resetChat} className="reset-btn" title="Reset Chat">🔄</button>
      </div>

      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`message-wrapper ${m.sender}`}>
             <div className="message-bubble">
               <div className="message-content">{m.text}</div>
               {m.time && <div className="message-time">{m.time}</div>}
             </div>
          </div>
        ))}
        {isTyping && (
          <div className="message-wrapper bot">
            <div className="message-bubble typing-bubble">
              <span className="dot"></span><span className="dot"></span><span className="dot"></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-footer">
        {(options && options.length > 0) && (
          <div className="options-container">
            {options.map((opt, i) => (
              <button 
                key={i} 
                onClick={() => {
                  if (step === "slot") return handleSlotSelection(opt);
                  if (step === "doctor") return handleDoctorSelection(opt);
                  return handleOptionClick(opt);
                }}
                className="option-btn"
              >
                {opt.name || opt}
              </button>
            ))}
          </div>
        )}
        <form onSubmit={handleSend} className="input-form">
          <input 
            type="text" 
            placeholder={step === "finished" ? "Booking complete" : "Type your message..."} 
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={step === "finished" || (options && options.length > 0)}
          />
          <button type="submit" className="send-btn" disabled={step === "finished" || (options && options.length > 0)}>
            ➤
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPanel;
