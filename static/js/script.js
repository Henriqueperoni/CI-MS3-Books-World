$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
});

function startModalBooks() {
    const modal = document.querySelector(".container-modal")
    modal.classList.add("show-modal");

    modal.addEventListener("click", (e) => {
        if(e.target.id == "modal-review" || e.target.className == "close-modal") {
            modal.classList.remove("show-modal")
        }
    })
}

document.addEventListener('DOMContentLoaded', function () {
const addBook = document.getElementById("add-book")
addBook.addEventListener("click", () => {
    startModalBooks()
})
})

const editBook = document.getElementById("edit-book")
editBook.addEventListener("click", () => {
    startModalBooks()
})

function deleteModal() {
    const modal = document.querySelector(".container-modal-delete")
    modal.classList.add("show-modal-delete");

    modal.addEventListener("click", (e) => {
        if(e.target.id == "modal-delete" || e.target.className == "close-modal-delete" || e.target.id == "cancel-delete") {
            modal.classList.remove("show-modal-delete")
        }
    })
}


const deleteBook = document.getElementById("delete-book")
deleteBook.addEventListener("click", () => {
    deleteModal()
})