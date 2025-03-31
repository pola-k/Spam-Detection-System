import { useState, useEffect } from "react"
import "./App.css"

function App() {

  const [email, setEmail] = useState("")
  const [notification, setNotification] = useState("")
  const [notificationColor, setNotificationColor] = useState("");

  function handleNotification(data)
  {
    if (data.prediction === "Spam") 
    {
      setNotification("This Email is Classified as Spam.")
      setNotificationColor("red");
    } 
    else 
    {
      setNotification("This Email is Classified as Not Spam.")
      setNotificationColor("#1db954");
    }
    setTimeout(() => {
      setNotification("")
      setNotificationColor("");
    }
    , 5000)
  }

  useEffect(() => {
    const notificationElement = document.getElementById("notification");
    if (notification) 
    {
      notificationElement.classList.add("show");
      setTimeout(() => {
        notificationElement.classList.remove("show");
      }, 5000);
    }
  }, [notification]);

  function handleEmail(e) 
  {
    setEmail(e.target.value)
  }

  function resetEmail()
  {
    setEmail("")
  }

  function handleSubmit() 
  {
    if (email === "")
    {
      setNotification("Please enter an email text.");
      setNotificationColor("red");
      return;
    }
    fetch("http://127.0.0.1:5000/predict", 
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_text: email }),
    })
    .then(response => response.json())
    .then(data => handleNotification(data))
    .catch(error => console.error("Error:", error));
}

  return (
      <>
        <div className="container">
          {notification ? <h1 id="notification" style={{ backgroundColor: notificationColor }}>{notification}</h1> : null}
          <h1>Spam Detection System</h1>
          <p>Our spam detection system uses advanced machine learning techniques to accurately classify emails as spam or legitimate messages. 
            It processes the email content by extracting key features such as the presence of suspicious links, spelling mistakes, and common spam
             keywords. The system applies TF-IDF vectorization to convert text into numerical representations and scales additional features
              for better accuracy. Using a Random Forest Classifier, the model analyzes patterns and assigns a classification based on learned
               data. With a precision-focused approach, our system ensures that spam emails are detected effectively while minimizing false
                positives, providing a reliable way to filter out unwanted messages.</p>
          <div className="input-container">
            <textarea name="email-msg" id="email-textarea" placeholder="Enter Email Text Here..." onChange={handleEmail} value={email}></textarea>
            <div className="btn-container">
              <button className="submit-btn" onClick={handleSubmit}>Submit</button>
              <button className="reset-btn" onClick={resetEmail}>Reset</button>
            </div>
          </div>
        </div>
      </>
  )
}

export default App
