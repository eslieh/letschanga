import React from 'react';
import '../styles/FundraiserPage.css';

const FundraiserPage = () => {
  return (
    <div className="fundraiser-container">
      <div className="fundraiser-header">
        <h1>Legal Support for C. Beachler</h1>
        <p className="location"><i className="fas fa-map-marker-alt"></i> Columbus, OH</p>
      </div>

      <div className="fundraiser-main">
        <div className="fundraiser-image">
          <img src="https://www.gofundme.com/mvc.php?route=images.share.preview&url=https://gfmapi.s3.amazonaws.com/campaign/88450483_1715613021469576_r.jpeg" alt="Fundraiser" />
        </div>

        <div className="fundraiser-info">
          <h2>$4,837 raised of $10,000 goal</h2>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: '48%' }}></div>
          </div>
          <p className="donors"><i className="fas fa-user-friends"></i> 97 donations</p>
          <button className="btn-donate"><i className="fas fa-heart"></i> Donate now</button>
          <button className="btn-share"><i className="fas fa-share-alt"></i> Share</button>
        </div>
      </div>

      <div className="fundraiser-story">
        <h3>Story</h3>
        <p>
          C. Beachler is raising funds to cover legal expenses related to an ongoing case.
          Your support helps ensure justice and fairness.
        </p>
        <p>
          Every donation, no matter the size, brings them one step closer to their goal.
          If you can't donate, sharing this campaign helps a lot!
        </p>
      </div>
    </div>
  );
};

export default FundraiserPage;
