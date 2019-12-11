let dropdownTrolley = document.querySelector('#dropdown-trolley');
dropdownTrolley.addEventListener('click', function(event) {
  event.stopPropagation();
  dropdownTrolley.classList.toggle('is-active');
});

function refreshTrolley() {
    const trolleyList = document.querySelector("#trolley-list");

    trolleyList.innerHTML = "";
    fetch("/api/me/trolley")
    .then((data) => data.json())
    .then((decoded_data) => {
        let trolley = decoded_data.trolley;
        let product_total = 0;
        let price_total = 0;
        for (let key in trolley) {
            product_total++;
            price_total += trolley[key].price * trolley[key].quantity;
            trolleyList.innerHTML += `<a href="#" class="dropdown-item">${trolley[key].name} — ${trolley[key].quantity} — Rp. ${trolley[key].price * trolley[key].quantity}</a>`;
        }
        if (product_total > 0) {
            trolleyList.innerHTML += `<hr class="dropdown-divider"><p class="dropdown-item">Total — ${price_total}</p><hr class="dropdown-divider"><a href="/checkout" id="trolley-checkout" class="dropdown-item">Checkout</a>`;

            let trolleyCheckout = document.querySelector('#trolley-checkout');
            trolleyCheckout.addEventListener('click', function(event) {
              event.preventDefault();
              if (typeof user_email === "undefined") {
                if (confirm("Please login to your account")) {
                    window.location = "/signin"
                }
              } else {
                window.location = "/checkout"
              }
            });
        } else {
            trolleyList.innerHTML = `<p class="dropdown-item">You haven''t add any product</p>`;
        }
    });
}