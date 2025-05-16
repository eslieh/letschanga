import { useState } from "react";
import "../styles/Auth.css";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
// Font Awesome icon simulation
// (In a real app, you'd include the Font Awesome library properly)
const Icon = ({ icon, className }) => {
  return <i className={`fa ${icon} ${className || ""}`}></i>;
};

export default function AuthFlow() {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState(4);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [about, setAbout] = useState("");
  const [imagePreview, setImagePreview] = useState(null);
  const [verificationCode, setVerificationCode] = useState("");
  const [image, setImage] = useState(null);
  const [isPosting, setIsPosting] = useState();
  // console.log(isPosting)
  // For demo purposes - normally would be handled by backend
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };
  const handlePostMail = (e) => {
    if (e) e.preventDefault();
    if (isPosting) return;
    setIsPosting(true);
    if (currentStep < 3) {
      // setIsPosting(true);
      const payload = {
        email: email,
        name: name,
        password: password,
      };
      console.log(payload);
      fetch("http://127.0.0.1:5000/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Server response:", data);
          if (data.user_id) {
            // setIsPosting(false);
            toast.success("email sent to " + email);
            setCurrentStep(currentStep + 1);
          } else {
            setIsPosting(false);
            toast.error(data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
      setIsPosting(false);
      // setCurrentStep(currentStep + 1);
    } else {
      // Final submission
      console.log("Account created successfully!");
      // Here you would normally send data to your backend
    }
  };
  const handleLogin = (e) => {
    if (e) e.preventDefault();
    if (isPosting) return;
    setIsPosting(true);
    // setIsPosting(true);
    const payload = {
      email: email,
      password: password,
    };
    console.log(payload);
    fetch("http://127.0.0.1:5000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Server response:", data);
        if (data.user) {
          // setIsPosting(false);
          toast.success("welcome "+ data.user.name);
          navigate('/app')
        } else {
          setIsPosting(false);
          toast.error(data.message);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    setIsPosting(false);
    
  };
  const handleVerifyMail = (e) => {
    if (e) e.preventDefault();
    if (isPosting) return;
    if (currentStep < 3) {
      setIsPosting(true);
      const payload2 = {
        email: email,
        otp: verificationCode,
      };
      fetch("http://127.0.0.1:5000/auth/verify-otp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload2),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Server response:", data);
          if (data.user.id) {
            setCurrentStep(currentStep + 1);
            toast.success("email verified successfull");
          } else {
            toast.error(data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
      setIsPosting(false);
      // setCurrentStep(currentStep + 1);
    } else {
      // Final submission
      console.log("Account created successfully!");
      // Here you would normally send data to your backend
    }
  };
  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    if (isPosting) return;
    setIsPosting(true);
    console.log(imagePreview);
    if (currentStep <= 3) {
      const formData = new FormData();
      formData.append("image", image);

      try {
        const response = await fetch("http://127.0.0.1:5000/api/media/upload", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`Server responded with status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Upload response:", data);

        if (data.url) {
          toast.success("Image uploaded to: " + data.url);

          const payload3 = {
            image_url: data.url,
            tagline: "nulldata",
            bio: about,
          };
          const accessToken = localStorage.getItem("token");
          const profileRes = await fetch(
            "http://127.0.0.1:5000/api/user/profile",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${accessToken}`,
              },
              body: JSON.stringify(payload3),
            }
          );

          if (!profileRes.ok) {
            throw new Error(
              `Profile update failed with status ${profileRes.status}`
            );
          }

          const profileData = await profileRes.json();
          toast.success("Profile created successfully");
          navigate('/app')
          console.log("Profile update response:", profileData);
        } else {
          toast.error("Upload succeeded but no URL in response");
          console.log("No URL in response", data);
        }
      } catch (error) {
        console.error("Image upload or profile update failed:", error);
        toast.error("Something went wrong: " + error.message);
      } finally {
        setIsPosting(false);
      }
      // setCurrentStep(currentStep + 1);
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
            <div className={`step ${currentStep >= 1 ? "active" : ""}`}>1</div>
            <div className="step-line"></div>
            <div className={`step ${currentStep >= 2 ? "active" : ""}`}>2</div>
            <div className="step-line"></div>
            <div className={`step ${currentStep >= 3 ? "active" : ""}`}>3</div>
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
              <p className="password-hint">
                Must be at least 8 characters with a number and special
                character
              </p>
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

            <button
              onClick={handlePostMail}
              className={`btn-primary ${
                isPosting ? "cursor-wait opacity-50 pointer-events-none" : ""
              }`}
              disabled={isPosting}
            >
              Continue{" "}
              {isPosting ? (
                <>
                  Sending... <span className="loader ml-2"></span>
                </>
              ) : (
                <>
                  <Icon icon="fa-arrow-right" />
                </>
              )}
            </button>

            <div className="auth-footer">
              <p>
                Already have an account?{" "}
                <a href="#login" onClick={() => setCurrentStep(4)}>
                  Log In
                </a>
              </p>
            </div>
          </div>
        )}

        {currentStep === 2 && (
          <div className="auth-form">
            <div className="verification-graphics">
              <Icon
                icon="fa-envelope-open-text"
                className="verification-icon"
              />
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

            <button
              onClick={handleVerifyMail}
              className={`btn-primary ${
                isPosting ? "cursor-wait opacity-50 pointer-events-none" : ""
              }`}
              disabled={isPosting}
            >
              Verify Email
              {isPosting ? (
                <>
                  Sending... <span className="loader ml-2"></span>
                </>
              ) : (
                <>
                  <Icon icon="fa-check-circle" />
                </>
              )}
            </button>

            <div className="auth-footer">
              <p>
                Didn't receive a code? <a href="#resend">Resend Code</a>
              </p>
              <button type="button" className="btn-back" onClick={goBack}>
                <Icon icon="fa-arrow-left" /> Back
              </button>
            </div>
          </div>
        )}

        {currentStep === 3 && (
          <div className="auth-form">
            <h2>Complete Your Profile</h2>
            <p className="profile-subtitle">
              Help others know who they're donating to
            </p>

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
                style={{ display: "none" }}
                required
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
                required
              ></textarea>
              <p className="character-count">{about.length}/200</p>
            </div>

            <button
              onClick={handleSubmit}
              className={`btn-primary ${
                isPosting ? "cursor-wait opacity-50 pointer-events-none" : ""
              }`}
              disabled={isPosting}
            >
              Complete Signup
              {isPosting ? (
                <>
                  Sending... <span className="loader ml-2"></span>
                </>
              ) : (
                <>
                  <Icon icon="fa-check" />
                </>
              )}
            </button>

            <div className="auth-footer">
              <button type="button" className="btn-back" onClick={goBack}>
                <Icon icon="fa-arrow-left" /> Back
              </button>
            </div>
          </div>
        )}
        {currentStep === 4 && (
          <div className="auth-form">
            <div className="verification-graphics">
              <Icon
                icon="fa-envelope-open-text"
                className="verification-icon"
              />
            </div>
            <h2>Login</h2>

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
            </div>

            <button
              onClick={handleLogin}
              className={`btn-primary ${
                isPosting ? "cursor-wait opacity-50 pointer-events-none" : ""
              }`}
              disabled={isPosting}
            >
              Login
              {isPosting ? (
                <>
                  Sending... <span className="loader ml-2"></span>
                </>
              ) : (
                <>
                  <Icon icon="fa-check-circle" />
                </>
              )}
            </button>

            <div className="auth-footer">
              <div className="auth-footer">
                <p>
                  Dont have an account?{" "}
                  <a href="#login" onClick={() => setCurrentStep(1)}>
                    Signup
                  </a>
                </p>
              </div>
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
