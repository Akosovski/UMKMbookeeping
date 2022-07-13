const searchFieldProduk = document.querySelector("#searchField-produk");
const tableOutputProduk = document.querySelector(".table-output-produk");
const appTableProduk = document.querySelector(".app-table-produk");
const paginationContainerProduk = document.querySelector("#pagination-container-produk");
tableOutputProduk.style.display = "none";
const noResultsProduk = document.querySelector(".no-results-produk");
const tbodyProduk = document.querySelector(".table-body-produk");


let rupiahIDR_produk = Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
});

searchFieldProduk.addEventListener('keyup',(e)=>{
    const searchValueProduk = e.target.value;

    if (searchValueProduk.trim().length > 0) {
        paginationContainerProduk.style.display = "block";
        tbodyProduk.innerHTML = "";
        fetch("/produk/cari-produk", {
          body: JSON.stringify({ searchText: searchValueProduk }),
          method: "POST",
        })
          .then((res) => res.json())
          .then((data) => {
            console.log("data", data);
            appTableProduk.style.display = "none";
            tableOutputProduk.style.display = "block";
    
            console.log("data.length", data.length);
    
            if (data.length === 0) {
              noResultsProduk.style.display = "block";
              tableOutputProduk.style.display = "none";
            } else {
              noResultsProduk.style.display = "none";
              data.forEach((item) => {
                var buyprice_loop = rupiahIDR_produk.format(item.buyprice);
                var sellprice_loop = rupiahIDR_produk.format(item.sellprice);
                tbodyProduk.innerHTML += `
                    <tr class="align-middle">
                        <td>${item.name}</td>
                        <td target="_blank">${buyprice_loop}</td>
                        <td target="_blank">${sellprice_loop}</td>
                        <td>${item.description}</td>
                        <td>${item.stock}</td>
                        <td>${item.dateadded}</td>
                        <td>${item.dateupdated}</td>
                        <td>${item.vendor}</td>
                    </tr>`;
              });
            }
          });
      } else {
        tableOutputProduk.style.display = "none";
        appTableProduk.style.display = "block";
        paginationContainerProduk.style.display = "block";
      }
})