$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
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
if(editBook){
     editBook.addEventListener("click", () => {
         startModalBooks()
     })
}

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
if(deleteBook) {
deleteBook.addEventListener("click", () => {
    deleteModal()
})
}



// Function to dynamically add input fields
//https://www.sanwebe.com/2013/03/addremove-input-fields-dynamically-with-jquery
$(document).ready(function() {
	var max_fields      = 10; //maximum input boxes allowed
	var wrapper   		= $(".input_fields_wrap"); //Fields wrapper
    var add_button      = $(".add-field-button"); //Add button ID
	
	var x = 1; //initlal text box count
    $(add_button).click(function(e){ //on add input button click
        console.log('clicked')
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			$(wrapper).append('<div><label for="img_url">Insert image URL</label><input id="img_url" name="img_url" type="text" class="validate" minlength="5" maxlength="100" required/><a href="#" class="remove_field btn-small red darken-2">Remove</a></div>'); //add input box
		}
	});
	
	$(wrapper).on("click",".remove_field", function(e){ //user click on remove text
		e.preventDefault(); $(this).parent('div').remove(); x--;
	})
});