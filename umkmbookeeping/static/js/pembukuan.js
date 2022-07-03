var price = 0;
var tax = 0;
var total = 0;

document.getElementById("priceField").addEventListener("input", totalerPrice);
document.getElementById("taxField").addEventListener("change", totalerTax);

function totalerPrice() {
    price = document.forms['tambah-pembukuan']['price'].value;
    document.forms['tambah-pembukuan']['total'].value = price;
}

function totalerTax() {
    price = document.forms['tambah-pembukuan']['price'].value;
    tax = document.forms['tambah-pembukuan']['tax'].value;
    var intPrice = parseInt(price);
    var intTax = parseInt(tax);
    total = intPrice + intTax;
    document.forms['tambah-pembukuan']['total'].value = total;
}