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

  searchButton.addEventListener("click", () => {
    let company_name = getCompanyName();

    bodyEle.style.display = "none";

    fetch(root_link + get_summary + "?company=" + company_name)
      .then((res) => {
        if (!res.ok) {
          throw new Error("network response was not ok");
        }

        return res.json();
      })
      .then((data) => {
        const summaryText = data.data.split("\n").join("<br /><br />");
        summary.innerHTML = summaryText;
      })
      .catch((err) => {
        summary.innerHTML = `There was an error with the fetch operation ${err}`;
      });
  });

  function staticCompanies(element, company) {
    element.addEventListener("click", () => {
      bodyEle.style.display = "none";
      fetch(root_link + get_summary + "?company=" + company)
        .then((res) => {
          if (!res.ok) {
            throw new Error("network response was not ok");
          }

          return res.json();
        })
        .then((data) => {
          // add title to the summary
          const title = document.createElement("h1");
          title.innerHTML = company;
          summary.appendChild(title);
          // add summary to the summary

          const summaryText = data.data.split("\n").join("<br /><br />");
          summary.innerHTML = summaryText;
        })
        .catch((err) => {
          summary.innerHTML = `There was an error with the fetch operation ${err}`;
        });
    });
  }

  staticCompanies(googleBtn, "google");
  staticCompanies(facebookBtn, "facebook");
  staticCompanies(twitterBtn, "twitter");
  staticCompanies(microsoftBtn, "microsoft");

  userButton.addEventListener("click", () => {
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
        const summaryText = data.data.split("\n").join("<br /><br />");

        summary.innerHTML = summaryText;
      })
      .catch((err) => {
        summary.innerHTML = `There was an error with the fetch operation ${err}`;
      });
  });
});
