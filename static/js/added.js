const elements = document.querySelectorAll('.value');
for (const td of elements) {
    // console.log(typeof(parseFloat(td.innerText)));
    if (parseFloat(td.innerText) >= 0){
        td.classList.add("change-none");
    } else {
        td.classList.add("change-down");
    }
}