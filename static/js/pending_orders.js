const acceptButtons = document.querySelectorAll(".accept button");

acceptButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    const name = prompt("Enter your name: ");
    const number = prompt("Enter your phone number: ");
    const timestamp = btn.dataset.time;
    const code = Math.floor(Math.random() * 90000) + 10000;

    alert(`Your code is: ${code}`);
    fetch("/api/acceptOrder", {
      method: "POST",
      body: JSON.stringify({
        name,
        number,
        code,
        timestamp,
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    })
      .then((response) => response.json())
      .then((x) => {
        if (x.status == 200) window.location = "/orders/accepted";
      });
  });
});
