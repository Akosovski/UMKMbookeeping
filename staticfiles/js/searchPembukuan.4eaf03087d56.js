const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector("#pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

let rupiahIDR_loop = Intl.NumberFormat("id-ID", {
  style: "currency",
  currency: "IDR",
});

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
        paginationContainer.style.display = "block";
        tbody.innerHTML = "";
        fetch("/cari-pembukuan", {
          body: JSON.stringify({ searchText: searchValue }),
          method: "POST",
        })
          .then((res) => res.json())
          .then((data) => {
            console.log("data", data);
            appTable.style.display = "none";
            tableOutput.style.display = "block";
    
            console.log("data.length", data.length);
    
            if (data.length === 0) {
              noResults.style.display = "block";
              tableOutput.style.display = "none";
            } else {
              noResults.style.display = "none";
              data.forEach((item) => {
                var price_loop = rupiahIDR_loop.format(item.price);
                var tax_loop = rupiahIDR_loop.format(item.tax);
                var subtotal_loop = rupiahIDR_loop.format(item.subtotal);
                tbody.innerHTML += `
                    <tr class="align-middle">
                        <td>${item.date}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td target="_blank">${price_loop}</td>
                        <td target="_blank">${tax_loop}</td>
                        <td target="_blank">${subtotal_loop}</td>
                    </tr>`;
              });
            }
          });
      } else {
        tableOutput.style.display = "none";
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
      }
})