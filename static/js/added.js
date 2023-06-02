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

        let mkt_cap = document.querySelector('#mkt-cap');
        mkt_cap.innerText = "Yes";

        let cap_values = document.querySelectorAll('.mkt-cap-values');
        let total_cap = 0
        for (const element of cap_values) {
            console.log(element.innerText);
            console.log(typeof parseFloat(element.innerText));
            total_cap += parseFloat(element.innerText)
            console.log(total_cap);
        }
        console.log(total_cap);
        mkt_cap.innerText = total_cap;