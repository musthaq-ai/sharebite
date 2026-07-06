document.addEventListener("DOMContentLoaded", function () {

    const container = document.getElementById("foodItemsContainer");
    const addBtn = document.getElementById("addFoodItem");

    if (!container || !addBtn) return;

    addBtn.addEventListener("click", addFoodItem);

    function addFoodItem() {

        const firstCard = container.querySelector(".food-item");

        const clone = firstCard.cloneNode(true);

        // ---------- Clear Values ----------

        clone.querySelectorAll("input").forEach(input => {

            if (input.type === "text") {

                input.value = "";

            }

        });

        clone.querySelectorAll("textarea").forEach(textarea => {

            textarea.value = "";

        });

        clone.querySelectorAll("select").forEach(select => {

            select.selectedIndex = 0;

        });

        // ---------- Number ----------

        const total = container.querySelectorAll(".food-item").length + 1;

        clone.querySelector(".item-number").textContent = total;

        // ---------- Remove Button ----------

        let removeBtn = clone.querySelector(".removeFoodItem");

        if (!removeBtn) {

            removeBtn = document.createElement("button");

            removeBtn.type = "button";

            removeBtn.className =
                "btn btn-outline-danger btn-sm removeFoodItem";

            removeBtn.innerHTML =
                '<i class="bi bi-trash"></i> Remove';

            clone.querySelector(".d-flex").appendChild(removeBtn);

        }

        removeBtn.onclick = function () {

            clone.remove();

            updateNumbers();

        };

        container.appendChild(clone);

    }

    function updateNumbers() {

        const cards = container.querySelectorAll(".food-item");

        cards.forEach((card, index) => {

            card.querySelector(".item-number").textContent = index + 1;

        });

    }

});