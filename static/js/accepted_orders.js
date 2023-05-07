const deliverButtons = document.querySelectorAll(".deliver button");

deliverButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    const timestamp = btn.dataset.time;
    const code = prompt("Enter your code: ");
    fetch("/api/deliverOrder", {
      method: "POST",
      body: JSON.stringify({
        timestamp,
        code,
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    })
      .then((response) => response.json())
      .then((x) => {
        if (x.status == 401) {
          alert("Wrong code!");
        } else if (x.status == 200) {
          window.location.reload();
        }
      });
  });
});
