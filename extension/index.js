document.addEventListener("DOMContentLoaded", () => {
  // your JavaScript code here
  const bodyEle = document.getElementById("body");

  const summary = document.getElementById("summary");
  const userButton = document.getElementById("user_button");
  const searchButton = document.getElementById("search_btn");
  const textarea = document.getElementById("terms_input");
  //static websites

  const googleBtn = document.getElementById("google");
  const facebookBtn = document.getElementById("facebook");
  const twitterBtn = document.getElementById("twitter");
  const microsoftBtn = document.getElementById("microsoft");

  const root_link = "http://localhost:8000"; //change this link to api
  const get_summary = "/get_summary";
  const user_summary = "/user_summary";

  function getCompanyName() {
    let company_input = document.getElementById("myInput");
    let company_name = company_input.value;

    return company_name;
  }

  let terms_jokes = [
    "I'm a Nigerian prince now thanks to the terms and conditions.",
    "Relationships and terms and conditions have one thing in common: we don't read them, but still say 'I agree'.",
    "Saying 'I have read and agree to the terms and conditions' is the internet's biggest lie, next to 'I have read the book'.",
    "Terms and conditions: the best way to ensure no one reads your legal documents.",
    "I rarely read terms and conditions, but when I do, they're incomprehensible.",
    "Reading terms and conditions is like drinking orange juice after brushing your teeth: unpleasant and unnecessary.",
    "Terms and conditions are like puzzles: you don't know the full picture until you put the pieces together.",
    "By reading terms and conditions, you're  saving a lawyer's job somewhere.",
    "Remember when we read books instead of terms and conditions?",
    "In a world where no one reads terms and conditions, be the exception, and still don't read them.",
    "Terms and conditions are like Jenga: one wrong move and the whole thing falls apart.",
    "The twists and turns in terms and conditions are better than a soap opera.",
    "I agree to the terms and conditions only because I can't live without cat videos.",
    "By clicking 'I agree', you agree to sell your soul to the internet for eternity. Have a nice day!",
    "I always read terms and conditions, but I still don't understand them.",
  ];

  let loadJoke = () => {
    let index = Math.floor(Math.random() * terms_jokes.length);

    return terms_jokes[index];
  };

  function showLoadingAnimation() {
    document.getElementById("loading").style.display = "block";
    document.getElementById("jokes").style.display = "block";

    document.getElementById("jokes").innerHTML = loadJoke();
  }

  function hideLoadingAnimation() {
    document.getElementById("loading").style.display = "none";
    document.getElementById("jokes").style.display = "none";
  }

  let errorProperties = {
    errorMessage: "Please double-check the company name and try again",
    errorImage: "./logos/file_error.png",
    errorJokeImage:
      "https://media.tenor.com/6PjP_7dSl4QAAAAC/akshay-kumar-dizziness.gif",

    errorJokeMessage:
      "Oops! Did you search for Laxmi Chit Fund or do we have high traffic? Please try again :)",
  };

  let errorDesign = (message) => {
    let errorDiv = document.createElement("div");
    document.body.style.overflow = "hidden";

    let img = document.createElement("img");
    img.src = errorProperties.errorImage;
    img.height = "90";
    img.width = "90";

    let title = document.createElement("p");
    title.innerText = "Error!";
    title.style.textAlign = "center";
    title.style.fontWeight = "bold";
    title.style.marginTop = "50px";

    var text = document.createElement("p");
    text.innerText = message;
    text.style.textAlign = "center";
    text.style.color = "#888888";

    let errorText = document.createElement("div");

    errorText.appendChild(title);
    errorText.appendChild(text);

    let tryAgainButton = document.createElement("button");
    tryAgainButton.style.margin = "20px";
    tryAgainButton.textContent = "Try again?";
    tryAgainButton.style.width = "60%";
    tryAgainButton.style.backgroundColor = "#00acee";
    tryAgainButton.style.borderRadius = "30px";
    tryAgainButton.style.color = "white";
    tryAgainButton.style.fontWeight = "bold";
    tryAgainButton.style.border = "none";
    tryAgainButton.style.height = "40px";
    tryAgainButton.style.cursor = "pointer";

    tryAgainButton.addEventListener("click", () => {
      let company_name = getCompanyName();
      summary.style.display = "none";
      showLoadingAnimation();
      fetchData(get_summary, "?company=", company_name);
    });

    errorDiv.appendChild(img);
    errorDiv.appendChild(errorText);
    errorDiv.appendChild(tryAgainButton);

    errorDiv.style.display = "flex";
    errorDiv.style.alignItems = "center";
    errorDiv.style.justifyContent = "center";
    errorDiv.style.flexDirection = "column";

    errorDiv.style.position = "absolute";

    // errorDiv.style.top = "50%";
    // errorDiv.style.left = "50%";
    // errorDiv.style.transform = "translate(-50%, -50%)";
    errorDiv.style.height = "70%"; // Set height to 70%
    errorDiv.style.width = "70%";

    summary.appendChild(errorDiv);
    summary.style.height = "80vh";


    summary.style.display = "flex";
    summary.style.alignItems = "center";
    summary.style.justifyContent = "center";
    summary.style.overflow = "hidden";
  };

  let fetchData = (endPoint, parameter, company) => {
    fetch(root_link + endPoint + parameter + company)
     .then((res) => {
        hideLoadingAnimation();
        if (!res.ok) {
          throw new Error("network response was not ok");
          errorDesign("There was an internet connectivity issue");
        }

        return res.json();
      })
      .then((data) => {
        let status = data.data.status;
        let dataParam = data.data.summary;
        const summaryText = dataParam.split("\n").join("<br /><br />");
        summary.innerHTML = summaryText;
      })
      .catch((err) => {
        hideLoadingAnimation();
        errorDesign(errorProperties.errorMessage);
      });
  };

  hideLoadingAnimation();

  searchButton.addEventListener("click", function () {
    let company_name = getCompanyName();

    bodyEle.style.display = "none";

    showLoadingAnimation();
    fetchData(get_summary, "?company=", company_name);
  });

  function staticCompanies(element, company) {
    element.addEventListener("click", () => {
      bodyEle.style.display = "none";


      showLoadingAnimation();
      fetchData(get_summary, "?company=", company);

    });
  }

  userButton.addEventListener("click", () => {
    const text = textarea.value;

    bodyEle.style.display = "none";

    showLoadingAnimation();
    fetchData(user_summary, "?text=", text);

  });

  staticCompanies(googleBtn, "google");
  staticCompanies(facebookBtn, "facebook");
  staticCompanies(twitterBtn, "twitter");
  staticCompanies(microsoftBtn, "microsoft");
});
