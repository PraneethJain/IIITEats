const items = document.querySelectorAll(".item");
const form = document.querySelector("form");

const travelCost = form.querySelector(".travel-cost");
const foodCost = form.querySelector(".food-cost");
const totalCost = form.querySelector(".total-cost");

const travelCostHidden = form.querySelector(".travel-cost-hidden");
const foodCostHidden = form.querySelector(".food-cost-hidden");
const totalCostHidden = form.querySelector(".total-cost-hidden");

const getFoodCost = () => {
  let res = 0;
  items.forEach((item) => {
    res +=
      item.querySelector("select").value *
      item.querySelector(".right").dataset.price;
  });

  return res;
};

const updateTotalCost = () => {
  const travelCostInt = 40;
  const foodCostInt = getFoodCost();
  const totalCostInt = travelCostInt + foodCostInt;

  travelCost.textContent = `${travelCostInt}`;
  foodCost.textContent = `${foodCostInt}`;
  totalCost.textContent = `${totalCostInt}`;

  travelCostHidden.value = `${travelCostInt}`;
  foodCostHidden.value = `${foodCostInt}`;
  totalCostHidden.value = `${totalCostInt}`;
};

items.forEach((item) => {
  item.querySelector("select").addEventListener("change", () => {
    updateTotalCost();
  });
});

console.log("test");
document.querySelector(".background").style.backgroundImage =
  "url(../static/images/bg_red.svg)";
