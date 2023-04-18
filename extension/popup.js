console.log("function started");
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

var body = document.querySelector("body");
body.appendChild(button);

button.addEventListener("click", function () {
  chrome.runtime.openOptionsPage();
});

button.addEventListener("mouseover", function () {
  button.style.backgroundColor = "#FFC200";
});

button.addEventListener("mouseout", function () {
  button.style.backgroundColor = "#FF3A3A";
});

img.onerror = function (event) {
  console.log(event.type); // "error"
  console.log(event.target.src); // image source URL that failed to load
  console.log(event.target.error); // error object that caused the error
};
