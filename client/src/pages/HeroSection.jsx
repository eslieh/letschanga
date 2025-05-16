import React from "react";
import "../styles/HeroSection.css";
import { useNavigate } from "react-router-dom";

const benefits = {
  individuals: {
    title: "For Individuals (Donors)",
    subtitle: "Give with confidence. Watch your impact.",
    benefits: [
      "Transparent Giving – See exactly where your money goes.",
      "Support Any Cause – Fund medical bills, tuition, community projects, and more.",
      "Donate Anonymously or Publicly – Choose how visible you want to be.",
      "Simple & Secure Payment – Easily donate via M-Pesa or card.",
      "Instant Receipts – Automatically logged donations and confirmations.",
    ],
    image_url : "https://i.pinimg.com/736x/20/5e/f5/205ef5e27daa2642ff80d059fc4df267.jpg",
  },
  fundraisers: {
    title: "For Fundraisers (Cause Owners)",
    subtitle: "Raise funds. Build trust. Reach your goal faster.",
    benefits: [
      "Quick Campaign Setup – Launch a fundraiser in minutes.",
      "Real-time Progress – Track donations as they happen.",
      "Built-in Ledger & Wallet – Withdraw funds, manage balances transparently.",
      "Live Donor Feed – Build momentum and social proof through public support.",
      "Community Trust Tools – Verified campaigns, status updates, and authenticity badges.",
      "Shareable Campaign Links – Instantly share across social media.",
    ],
    image_url : "https://i.pinimg.com/736x/28/dc/13/28dc13bd9853ebcea1c007a6651e74a2.jpg",
  },
  content_creators: {
    title: "For Content Creators & Livestreamers",
    subtitle: "Monetize your audience. Empower your fans to support you.",
    benefits: [
      "Live Donations on Screen – Like Twitch, but for real-world causes.",
      "Real-time Alerts – Show donor messages and names live during streams.",
      "Custom Widgets – Embed donation feeds or QR codes into your content.",
      "Track Support Growth – Visual dashboards for streams and campaign performance.",
      "Flexible Campaigns – Fund creative projects, charity collabs, or subscriber goals.",
    ],
    image_url : "https://i.pinimg.com/736x/81/d1/9f/81d19f1881a220f46abbb41a1cb2d708.jpg",
  },
};

export default function HeroSection(){
    const navigate = useNavigate()  
  return (
    <div className="hero-page">
      <section className="hero">
        <section className="header">
          <div className="icon-branding">
            <div className="zero">$</div>
            <span className="brand-name">
              letschanga<span className="cjc">.com</span>
            </span>
          </div>
          <div className="login-placce">
            <button className="login_btn" onClick={() => navigate('/auth')}>Login</button>
          </div>
        </section>
        <section className="name-places">
          <div className="name-places">
            <span className="taxt-phrse1">
              Empowering <div className="grey-blurt">Change</div>
            </span>
            <span className="text-phrase2">
              <div className="grey-blurt">With one </div>Click.{" "}
              <button className="click-donate">
                <i class="fa-solid fa-arrow-pointer"></i>
              </button>
            </span>
          </div>
          <div className="diagram-place">
            <div className="example-diagram">
              <div className="dolla">$</div>
            </div>
          </div>
        </section>
        <section className="whatwedo">
          <h2 className="fo_individuals">{benefits.individuals.title}</h2>
          <h3 className="subtitle">{benefits.individuals.subtitle}</h3>
          <div className="dividers">
            <div className="impacts-jkd">
              <ul className="bentsk">
                {benefits.individuals.benefits.map((benefit, index) => (
                  <li key={index}>{benefit}</li>
                ))}
              </ul>
            </div>
            <div className="image-place-hs">
                <img src={benefits.individuals.image_url} alt="" />
            </div>
          </div>
        </section>
        <section className="whatwedo" id="fund">
          <h2 className="fo_individuals">{benefits.fundraisers.title}</h2>
          <h3 className="subtitle">{benefits.fundraisers.subtitle}</h3>
          <div className="dividers">
            <div className="impacts-jkd">
              <ul className="bentsk">
                {benefits.fundraisers.benefits.map((benefit, index) => (
                  <li key={index}>{benefit}</li>
                ))}
              </ul>
            </div>
            <div className="image-place-hs">
                <img src={benefits.fundraisers.image_url} alt="" />
            </div>
          </div>
        </section>
        <section className="whatwedo" id="cre">
          <h2 className="fo_individuals">{benefits.content_creators.title}</h2>
          <h3 className="subtitle">{benefits.content_creators.subtitle}</h3>
          <div className="dividers">
            <div className="impacts-jkd">
              <ul className="bentsk">
                {benefits.content_creators.benefits.map((benefit, index) => (
                  <li key={index}>{benefit}</li>
                ))}
              </ul>
            </div>
            <div className="image-place-hs">
                <img src={benefits.content_creators.image_url} alt="" />
            </div>
          </div>
        </section>
      </section>
    </div>
  );
};

