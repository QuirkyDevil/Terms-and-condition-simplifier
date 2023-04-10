setTimeout(function () {
  console.log("function started");
  var button = document.createElement("button");
  button.innerHTML = "Click me!";

  button.style.position = "fixed";
  button.style.top = "50%";
  button.style.left = "50%";
  button.style.transform = "translate(-50%, -50%)";
  button.style.backgroundColor = "blue";
  button.style.color = "white";

  var body = document.querySelector("body");
  body.appendChild(button);

  button.addEventListener("click", function () {
    alert("Button clicked!");

    console.log("Hiihsdisid");
  });
}, 3000);
