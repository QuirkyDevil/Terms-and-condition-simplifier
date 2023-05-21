const root_link = "http://localhost:8000"; // change this link to the API
const get_summary = "/get_summary";

let button = document.createElement("button");
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
div.style.overflow = "auto";
div.style.padding = "15px";

button.addEventListener("click", () => {
  let url = window.location.href;
  let company = url.split("/")[2];
  company = company.replace(/^www\./, "").replace(/\.com$/, "");

  button.style.display = "none"; // Hide the button

  div.style.display = "block";
  div.appendChild(titleDiv);
  document.body.appendChild(div);

  fetch(`${root_link}${get_summary}?company=${company}`)
    .then((res) => {
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      return res.json();
    })
    .then((data) => {
      let dataParam = data.data.summary;
      const summaryText = dataParam.split("\n").join("<br /><br />");

      let lineBreak = document.createElement("br");
      div.appendChild(lineBreak);

      let helloWorld = document.createElement("p");
      helloWorld.innerHTML = `<strong><h4>${company} terms and conditions: </strong></h4>`;
      div.appendChild(helloWorld);

      let lineBreak2 = document.createElement("br");
      div.appendChild(lineBreak2);

      let summary = document.createElement("p");
      summary.innerHTML = summaryText;
      div.appendChild(summary);
    })
    .catch((err) => {
      console.error("Error:", err);
      // Handle error
    });
});

document.body.appendChild(button);
