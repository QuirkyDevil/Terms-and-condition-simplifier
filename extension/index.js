document.addEventListener("DOMContentLoaded", function () {
  // your JavaScript code here
  const bodyEle = document.getElementById("body");
  console.log(bodyEle);

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

    console.log(company_name);

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

  hideLoadingAnimation();

  searchButton.addEventListener("click", function () {
    let company_name = getCompanyName();

    bodyEle.style.display = "none";

    showLoadingAnimation();

    fetch(root_link + get_summary + "?company=" + company_name)
      .then((res) => {
        hideLoadingAnimation();
        if (!res.ok) {
          throw new Error("network response was not ok");
        }

        return res.json();
      })
      .then((data) => {
        console.log(data.data);
        const summaryText = data.data.split("\n").join("<br /><br />");
        summary.innerHTML = summaryText;
      })
      .catch((err) =>
        console.log("There was an error with the fetch operation")
      );
  });

  function staticCompanies(element, company) {
    element.addEventListener("click", function () {
      bodyEle.style.display = "none";
      fetch(root_link + get_summary + "?company=" + company)
        .then((res) => {
          if (!res.ok) {
            throw new Error("network response was not ok");
          }

          return res.json();
        })
        .then((data) => {
          console.log(data.data);
          // add title to the summary
          const title = document.createElement("h1");
          title.innerHTML = company;
          summary.appendChild(title);
          // add summary to the summary

          const summaryText = data.data.split("\n").join("<br /><br />");
          summary.innerHTML = summaryText;
        })
        .catch((err) =>
          console.log("There was an error with the fetch operation")
        );
    });
  }

  staticCompanies(googleBtn, "google");
  staticCompanies(facebookBtn, "facebook");
  staticCompanies(twitterBtn, "twitter");
  staticCompanies(microsoftBtn, "microsoft");

  userButton.addEventListener("click", function () {
    const text = textarea.value;

    bodyEle.style.display = "none";

    fetch(root_link + user_summary + "?text=" + text)
      .then((res) => {
        if (!res.ok) {
          throw new Error("network response was not ok");
        }

        return res.json();
      })
      .then((data) => {
        console.log(data.data);
        const summaryText = data.data.split("\n").join("<br /><br />");
        console.log(data.data);

        summary.innerHTML = summaryText;
      })
      .catch((err) =>
        console.log("There was an error with the fetch operation")
      );
  });
});
