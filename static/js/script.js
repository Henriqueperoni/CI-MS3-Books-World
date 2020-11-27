$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
});

function startModal() {
    const modal = document.querySelector(".container-modal")
    modal.classList.add("show-modal");

    modal.addEventListener("click", (e) => {
        if(e.target.id == "modal-review" || e.target.className == "close-modal") {
            modal.classList.remove("show-modal")
        }
    })
}

const addBook = document.getElementById("add-book")
addBook.addEventListener("click", () => {
    startModal()
})
console.log(addBook)



