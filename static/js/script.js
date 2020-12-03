$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.collapsible').collapsible();    
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

$(document).ready(function() {
	var max_fields      = 10; //maximum input boxes allowed
	var wrapper   		= $(".input_fields_wrap"); //Fields wrapper
	var add_button      = $(".add_field_button"); //Add button ID
	
	var x = 1; //initlal text box count
	$(add_button).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<div><input type="text" name="mytext[]"/><a href="#" class="remove_field">Remove</a></div>'); //add input box
		}
	});
	
	$(wrapper).on("click",".remove_field", function(e){ //user click on remove text
		e.preventDefault(); $(this).parent('div').remove(); x--;
	})
});