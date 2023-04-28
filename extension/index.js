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

  function showLoadingAnimation() {
    document.getElementById("loading").style.display = "block";
  }

  function hideLoadingAnimation() {
    document.getElementById("loading").style.display = "none";
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
