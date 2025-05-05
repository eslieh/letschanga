import { useState } from 'react';
import "../styles/Auth.css"
// Font Awesome icon simulation 
// (In a real app, you'd include the Font Awesome library properly)
const Icon = ({ icon, className }) => {
  return <i className={`fa ${icon} ${className || ''}`}></i>;
};

export default function AuthFlow() {
  const [currentStep, setCurrentStep] = useState(1);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [about, setAbout] = useState('');
  const [imagePreview, setImagePreview] = useState(null);
  const [verificationCode, setVerificationCode] = useState('');
  
  // For demo purposes - normally would be handled by backend
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };
  
  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    } else {
      // Final submission
      console.log("Account created successfully!");
      // Here you would normally send data to your backend
    }
  };

  const goBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <div className="step-indicators">
            <div className={`step ${currentStep >= 1 ? 'active' : ''}`}>1</div>
            <div className="step-line"></div>
            <div className={`step ${currentStep >= 2 ? 'active' : ''}`}>2</div>
            <div className="step-line"></div>
            <div className={`step ${currentStep >= 3 ? 'active' : ''}`}>3</div>
          </div>
          <p className="step-description">
            {currentStep === 1 && "Create your account"}
            {currentStep === 2 && "Verify your email"}
            {currentStep === 3 && "Complete your profile"}
          </p>
        </div>

        {currentStep === 1 && (
          <div className="auth-form">
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <div className="input-icon-wrapper">
                <Icon icon="fa-envelope" className="input-icon" />
                <input
                  type="email"
                  id="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>
            
            <div className="form-group">
              <label htmlFor="name">Full Name</label>
              <div className="input-icon-wrapper">
                <Icon icon="fa-user" className="input-icon" />
                <input
                  type="text"
                  id="name"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
            </div>
            
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="input-icon-wrapper">
                <Icon icon="fa-lock" className="input-icon" />
                <input
                  type="password"
                  id="password"
                  placeholder="Create a password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <p className="password-hint">Must be at least 8 characters with a number and special character</p>
            </div>
            
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <div className="input-icon-wrapper">
                <Icon icon="fa-lock" className="input-icon" />
                <input
                  type="password"
                  id="confirmPassword"
                  placeholder="Confirm your password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
            </div>
            
            <button onClick={handleSubmit} className="btn-primary">
              Continue <Icon icon="fa-arrow-right" />
            </button>
            
            <div className="auth-footer">
              <p>Already have an account? <a href="#login">Log In</a></p>
            </div>
          </div>
        )}

        {currentStep === 2 && (
          <div className="auth-form">
            <div className="verification-graphics">
              <Icon icon="fa-envelope-open-text" className="verification-icon" />
            </div>
            <h2>Check your inbox</h2>
            <p className="verification-text">
              We've sent a verification code to <strong>{email}</strong>
            </p>
            
            <div className="form-group">
              <label htmlFor="verificationCode">Verification Code</label>
              <div className="verification-code-input">
                <input
                  type="text"
                  id="verificationCode"
                  placeholder="Enter 6-digit code"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value)}
                  required
                  maxLength="6"
                />
              </div>
            </div>
            
            <button onClick={handleSubmit} className="btn-primary">
              Verify Email <Icon icon="fa-check-circle" />
            </button>
            
            <div className="auth-footer">
              <p>Didn't receive a code? <a href="#resend">Resend Code</a></p>
              <button type="button" className="btn-back" onClick={goBack}>
                <Icon icon="fa-arrow-left" /> Back
              </button>
            </div>
          </div>
        )}

        {currentStep === 3 && (
          <div className="auth-form">
            <h2>Complete Your Profile</h2>
            <p className="profile-subtitle">Help others know who they're donating to</p>
            
            <div className="profile-image-upload">
              <div className="image-preview">
                {imagePreview ? (
                  <img src={imagePreview} alt="Profile preview" />
                ) : (
                  <div className="image-placeholder">
                    <Icon icon="fa-user" />
                  </div>
                )}
              </div>
              <label htmlFor="profile-image" className="upload-btn">
                <Icon icon="fa-camera" /> Upload Photo
              </label>
              <input
                type="file"
                id="profile-image"
                accept="image/*"
                onChange={handleImageUpload}
                style={{ display: 'none' }}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="about">About You</label>
              <textarea
                id="about"
                placeholder="Tell us about yourself or your cause"
                value={about}
                onChange={(e) => setAbout(e.target.value)}
                rows="4"
              ></textarea>
              <p className="character-count">{about.length}/200</p>
            </div>
            
            <button onClick={handleSubmit} className="btn-primary">
              Complete Signup <Icon icon="fa-check" />
            </button>
            
            <div className="auth-footer">
              <button type="button" className="btn-back" onClick={goBack}>
                <Icon icon="fa-arrow-left" /> Back
              </button>
            </div>
          </div>
        )}
      </div>
      
      <div className="app-info">
        <div className="info-content">
        <div className="icon-branding">
            <div className="zero">$</div>
            <span className="brand-name">
            letschanga<span className="cjc">.com</span>
            </span>
          </div>
        </div>
      </div>
      
      
    </div>
  );
}