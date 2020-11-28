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

const addBook = document.getElementById("add-book")
addBook.addEventListener("click", () => {
    startModalBooks()
})



// function starModalReview() {
//     const book1 = document.querySelectorAll(".book")
//     const modal1 = document.getElementById("modal-bokk")

//     book1.addEventListener("click", () => {
//         modal1.style.display = "none"
//     })
// }
// starModalReview()

// for (i = 0; i < navClose.length; i++) {
//     navClose[i].addEventListener("click", () => {
//       nav.classList.toggle("nav-active");
//     });
//   }




