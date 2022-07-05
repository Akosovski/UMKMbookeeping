const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector("#pagination-container");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

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
                tbody.innerHTML += `
                    <tr class="align-middle">
                        <td>${item.date}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>Rp. ${item.price}0</td>
                        <td>Rp. ${item.tax}0</td>
                        <td>Rp. ${item.subtotal}0</td>
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