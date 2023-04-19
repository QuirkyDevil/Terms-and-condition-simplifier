const root_link = "http://localhost:8000"; //change this link to api
const get_summary = "/get_summary";
const user_summary = "/user_summary";

let body = document.querySelector("body");
var button = document.createElement("button");

// var img = document.createElement("img");

// img.src = "chrome-extension://lobbenadnepajcechbdkgnlbgiofcddh/logo.png";

// img.style.height = "200px";

// img.style.width = "200px";

button.innerHTML = "T&CS";

button.style.position = "fixed";
button.style.top = "50%";
button.style.right = "0%";
button.style.transform = "translate(-50%,   0%)";
button.style.background = "linear-gradient(to right, #FFC200, #FF3A3A)";
button.style.color = "white";
button.style.fontSize = "16px";
button.style.fontFamily = "'Helvetica Neue',Helvetica,Arial,sans-serif";
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

body.appendChild(button);

button.addEventListener("click", () => {
  let url = window.location.href;

  let company = url.split("/")[2];

  company = company.replace(/^www\./, "").replace(/\.com$/, "");

  fetch(`${root_link + get_summary}?company=${company}`)
    .then((res) => {
      if (!res.ok) {
        throw new Error("network response was not ok");
      }

      return res.json();
    })
    .then((data) => {
      const summaryText = data.summary.split("\n").join("<br /><br />");
      summary.innerHTML = summaryText;
    })
    .catch(
      (err) =>
        (summary.innerHTML = `There was an error with the fetch operation ${err}`)
    );
});

button.addEventListener("mouseover", () => {
  button.style.backgroundColor = "#FFC200";
});

button.addEventListener("mouseout", () => {
  button.style.backgroundColor = "#FF3A3A";
});

// img.onerror = function (event) {
//   console.log(event.type); // "error"
//   console.log(event.target.src); // image source URL that failed to load
//   console.log(event.target.error); // error object that caused the error
// };
