document.getElementById("priceField").addEventListener("input", totalerPrice);
document.getElementById("taxField").addEventListener("change", totalerTax);
document.forms['tambah-pembukuan']['tax'].value = 0;

function totalerPrice() {
    var price = document.forms['tambah-pembukuan']['price'].value;
    document.forms['tambah-pembukuan']['subtotal'].value = price;
}

function totalerTax() {
    var price = document.forms['tambah-pembukuan']['price'].value;
    var tax = document.forms['tambah-pembukuan']['tax'].value;
    var intPrice = parseInt(price);
    var intTax = parseInt(tax);
    var total = intPrice + intTax;
    document.forms['tambah-pembukuan']['subtotal'].value = total;
}