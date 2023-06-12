const elements = document.querySelectorAll('.value');
for (const td of elements) {
    // console.log(typeof(parseFloat(td.innerText)));
    if (parseFloat(td.innerText) > 0){
        td.classList.add("change-up");
    }else if (parseFloat(td.innerText) == 0){
        td.classList.add("change-none");
    }else {
        td.classList.add("change-down");
    }
}

var dataTable1 = new DataTable("#example", {
	searchable: true,
	fixedHeight: false,
	sortable: true,
	exportable: {
        // options go here
        type: "sql",
        tableName: "sql_users",
        selection: [1,2,3,4,5]
    }
});

var dataTable2 = new DataTable("#example2", {
	searchable: true,
	fixedHeight: false,
	sortable: true,
	exportable: {
        // options go here
        type: "sql",
        tableName: "sql_users",
        selection: [1,2,3,4,5]
    }
});

var dataTable3 = new DataTable("#example3", {
	searchable: true,
	fixedHeight: false,
	sortable: true
});



