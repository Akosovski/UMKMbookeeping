let rupiahIDR = Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
});

const nodeList = document.querySelectorAll("td[target]");
for (let i = 0; i < nodeList.length; i++) {
    var price = nodeList[i].innerHTML;
    nodeList[i].innerHTML = rupiahIDR.format(price);
}

const renderChart=(data,labels)=>{
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Pembukuan 6 Bulan Terakhir",
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        }
    });

};

const getChartData=()=>{
    console.log("fetching");
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



