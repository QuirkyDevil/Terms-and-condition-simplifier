const root_link = "http://localhost:8000"; //change this link to api
const get_summary = "/get_summary";

let button = document.createElement("button");
// Create the loading animation element

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
  img.height = "70";
  img.width = "70";

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

  tryAgainButton.addEventListener("click", () => {});

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

  div.appendChild(errorDiv);
};

button.innerHTML = "T&CS";

button.style.position = "fixed";
button.style.top = "50%";
button.style.right = "0%";
button.style.transform = "translate(-50%,   0%)";
button.style.background = "#00acee";
button.style.color = "white";
button.style.fontSize = "16px";
button.style.fontWeight = "bold";
button.style.fontFamily = "sans-serif";
button.style.padding = "10px 20px";
button.style.width = "70px";
button.style.borderRadius = "10px";
button.style.border = "none";
button.style.boxShadow = "0px 2px 5px rgba(0, 0, 0, 0.25)";
button.style.transition = "0.3s";
button.style.cursor = "pointer";
button.style.height = "70px";
button.style.display = "flex";
button.style.justifyContent = "center";
button.style.alignItems = "center";

let body = document.querySelector("body");
body.appendChild(button);
let titleDiv = document.createElement("div");
titleDiv.style.height = "10vh";
titleDiv.style.backgroundColor = "#00acee";
titleDiv.style.display = "flex";
titleDiv.style.justifyContent = "center";
titleDiv.style.alignItems = "center";

let title = document.createElement("h4");
title.style.textAlign = "center";
title.innerHTML = "Terms and conditions simplifier";
title.style.color = "white";
title.style.fontWeight = "bold";
title.style.fontSize = "14";
titleDiv.appendChild(title);

const div = document.createElement("div");
div.style.fontFamily = "sans-serif";
div.style.width = "300px";
div.style.height = "550px";

div.style.display = "none";

div.style.position = "absolute";
div.style.top = "50%";
div.style.right = "2%";
div.style.transform = "translate(2%,-50%)";
div.style.boxShadow = "0px 2px 5px rgba(0, 0, 0, 0.25)";
div.style.borderRadius = "10px";

button.addEventListener("click", () => {
  let url = window.location.href;
  let company = url.split("/")[2];

  company = company.replace(/^www\./, "").replace(/\.com$/, "");

  button.style.display = "none"; // Hide the button

  div.style.display = "block";
  div.append(titleDiv);

  body.append(div);

  fetch(` ${root_link + get_summary}?company=${company}`)
    .then((res) => {
      if (!res.ok) {
        throw new Error("network response was not ok");
      }

      return res.json();
    })
    .then((data) => {
      let dataParam = data.data.summary;
      const summaryText = dataParam.split("\n").join("<br /><br />");
      div.innerHTML = summaryText;
    })
    .catch((err) =>
      // (summary.innerHTML = `There was an error with the fetch operation ${err}`)
      errorDesign()
    );
});

button.addEventListener("mouseover", () => {
  button.style.backgroundColor = "#FFC200";
});

button.addEventListener("mouseout", () => {
  button.style.backgroundColor = "#FF3A3A";
});
