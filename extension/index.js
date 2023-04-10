document.addEventListener("DOMContentLoaded", function () {
  // your JavaScript code here
  const bodyEle = document.getElementById("body");
  console.log(bodyEle);

  const summary = document.getElementById("summary");

  const searchButton = document.getElementById("search_btn");

  //static websites
  const google = document.getElementById("google");
  const facebook = document.getElementById("facebook");
  const twitter = document.getElementById("twitter");
  const microsoft = document.getElementById("microsoft");

  const root_link = "http://localhost:8000"; //change this link to api
  const get_summary = "/get_summary";

  function getCompanyName() {
    let company_input = document.getElementById("myInput");
    let company_name = company_input.value;

    console.log(company_name);

    return company_name;
  }

  searchButton.addEventListener("click", function () {
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
        console.log(data.summary);
        const summaryText = data.summary.split('\n').join('<br /><br />');
        summary.innerHTML = summaryText;
      })
      .catch((err) =>
        console.log("There was an error with the fetch operation")
      );

    console.log("Hello");
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
          console.log(data.summary)
          // add title to the summary
          const title = document.createElement('h1');
          title.innerHTML = company;
          summary.appendChild(title);
          // add summary to the summary
          
          
          const summaryText = data.summary.split('\n').join('<br /><br />');
          summary.innerHTML = summaryText;
        })
        .catch((err) =>
          console.log("There was an error with the fetch operation")
        );
    });
  }

  staticCompanies(google, "google");
  staticCompanies(facebook, "facebook");
  staticCompanies(twitter, "twitter");
  staticCompanies(microsoft, "microsoft");
});
