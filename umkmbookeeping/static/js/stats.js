let rupiahIDR = Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
});

const tableList = document.querySelectorAll("td[target]");
for (let i = 0; i < tableList.length; i++) {
    var price = tableList[i].innerHTML;
    tableList[i].innerHTML = rupiahIDR.format(price);
}

const totalList = document.querySelectorAll("h5[target]");
for (let j = 0; j < totalList.length; j++) {
    var totals = totalList[j].innerHTML;
    totalList[j].innerHTML = rupiahIDR.format(totals);
}

const renderChart=(data,labels)=>{
    const bordercolor = [];
    const backgroundcolor = [];
    for (i = 0; i<labels.length; i++){
        if (labels[i]=="Pengeluaran"){
            backgroundcolor.push('rgba(255, 0, 0, 0.2)');
            bordercolor.push('rgba(255, 99, 132, 1)');
        }
        if (labels[i]=="Pemasukan"){
            backgroundcolor.push('rgba(0,128,0,0.2)');
            bordercolor.push('rgba(0,128,0,1)');
        }
        if (labels[i]=="Lain-lain"){
            backgroundcolor.push('rgba(54, 162, 235, 0.2)');
            bordercolor.push('rgba(54, 162, 235, 1)');
        }
    }
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Pembukuan 6 Bulan Terakhir",
                data: data,
                backgroundColor: backgroundcolor,
                borderColor: bordercolor,
                borderWidth: 1
            }]
        }
    });

};

const getChartData=()=>{
    console.log("fetching chart");
    fetch("/pembukuan-chart")
    .then(res=>res.json())
    .then(results=>{
        console.log('results', results);
        const category_data = results.pembukuan_category_data;
        const [labels, data] = [
            Object.keys(category_data),
            Object.values(category_data),
        ];
        renderChart(data, labels);
    });
}
document.onload=getChartData();