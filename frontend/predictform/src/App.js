import React, { useState } from 'react';
import './App.css';

function App() {

    const initialState = { ParentalEducation: '', StudyTimeWeekly:'', Absences:'',
      ParentalSupport:0, Tutoring:0, Extracurricular:0, Sports:0,
      Music:0, Volunteering:0 };
    const [formData, setFormData] = useState(initialState);
    const [prediction, setPrediction] = useState(null);
    
    const handleChange = (e) => {
      const name = e.currentTarget.name;
      const value = e.currentTarget.value;
      setFormData((prevState) => ({
        ...prevState,  /* copy previous state */
        [name]: value /* update specific key/value */
      }));
    }
    
    const predict = async (formData) => {
      try {
        const response = await fetch('/predict', {
          method: 'POST',
          headers: { 
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ formData }),
        });
        const data = await response.json();
        setPrediction(data.response);
      } catch (error) {
        console.error('Error:', error);
      }
    };

  const handleSubmit = (e) => {
    e.preventDefault();
    predict(formData);
    setFormData(initialState);
  };

  return (
    <div className="App" style={{ backgroundImage:"url('/background.jpg')", /* Path to image */
      backgroundSize: "cover", /* Cover the entire container */
      height: '100vh', /* Make the container full viewport height */
      width: '100vw', /* Make the container full viewport width */
    }}>
      
      <div className="container">
    <header className='headers'>Student GPA Predictor</header>
    <form onSubmit={handleSubmit}>
      <div className="inputs">
        <label for="ParentalEducation">Parental Education:</label>
        <select name="ParentalEducation" required onChange={handleChange} defaultValue={formData.ParentalEducation}>
            <option value="0">No High School</option>
            <option value="1">High School</option>
            <option value="2">Some College</option>
            <option value="3">Bachelor's Degree</option>
            <option value="4">Graduate Degree</option>
        </select>
      </div>
        <div className="inputs">
        <label for="StudyTimeWeekly">Study Time Weekly (hrs):</label>
        <input type="number" name="StudyTimeWeekly" required onChange={handleChange} value={formData.StudyTimeWeekly} />
        </div>
        <div className="inputs">
        <label for="Absences">Number of Absences:</label>
        <input type="number" name="Absences" required onChange={handleChange} value={formData.Absences}/>
        </div>
        <div className="inputs">
        <label for="ParentalSupport">Parental Support Level:</label>
        <select name="ParentalSupport" required onChange={handleChange} defaultValue={formData.ParentalSupport}>
            <option value="1">Low</option>
            <option value="2">Moderate</option>
            <option value="3">High</option>
        </select>
        </div>
        <div className="inputs">
        <label for="Tutoring">Tutoring:</label>
        <select name="Tutoring" required onChange={handleChange} defaultValue={formData.Tutoring}>
            <option value="1">Yes</option>
            <option value="0">No</option>
        </select>
        </div>
        <div className="inputs">
        <label for="Extracurricular">Extracurricular Activities:</label>
        <select name="Extracurricular" required onChange={handleChange} defaultValue={formData.Extracurricular}>
            <option value="1">Yes</option>
            <option value="0">No</option>
        </select>
        </div>
        <div className="inputs">
        <label for="Sports">Sports Participation:</label>
        <select name="Sports" required onChange={handleChange} defaultValue={formData.Sports}>
            <option value="1">Yes</option>
            <option value="0">No</option>
        </select>
        </div>
        <div className="inputs">
        <label for="Music">Music Participation:</label>
        <select name="Music" required onChange={handleChange} defaultValue={formData.Music}>
            <option value="1">Yes</option>
            <option value="0">No</option>
        </select>
        </div>
        <div className="inputs">
        <label for="Volunteering">Volunteering:</label>
        <select name="Volunteering" required onChange={handleChange} defaultValue={formData.Volunteering}>
            <option value="1">Yes</option>
            <option value="0">No</option>
        </select>
        </div>
        <button type="submit" className="btn">Predict GPA</button>
    </form>
        <p className="result"> Predicted GPA: <strong>{ prediction }</strong></p>
        
</div>
      
    </div>
  );
}

export default App;
