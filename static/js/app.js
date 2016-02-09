$(function(){
	// Set function for deleting contact
	$(".contact-delete").click(deleteContact);
});

/*
	Gets contact id for deletion and passes it to delete route for contact model
*/
function deleteContact() {
	var contact_id = $(this).attr("id");
	$.ajax({
		url: "/contacts",
		method: "delete",
		data: {
			"contact_id" : contact_id
		}
	}).done(function (result) {
		// Reload the table on the contacts page after a contact is deleted
		reloadContactTable();
	});
}

/*
	Reloads the content of the contact table after a contact is deleted
*/
function reloadContactTable() {
	var tableBody = $("#contacts-table-body")
	$.get({
		url:"/contacts"
	}).done(function (result){
		// result will be a set of contacts
		tableBody.empty();
		var contact;
		var i;
		for (i in result) {
			contact = result[i];
			var row = generateContactTableRow(contact);
			tableBody.append(row);
		}
	});
}

/*
	Helper function that generates the html required for a row in the contacts table
*/
function generateContactTableRow(contact) {
	var row = $("<tr />");
	$("<td />").html(contact.first_name).attr("scope", "row").appendTo(row);
	$("<td />").html(contact.last_name).appendTo(row);
	$("<td />").html(contact.email).appendTo(row);
	$("<td />").html(contact.phone_number).appendTo(row);
	var editRow = $("<td />").appendTo(row);
	$("<a />").html("Edit").attr("href", "/contacts.html?id=" + String(contact.id)).appendTo(editRow);
	var deleteRow = $("<td />").appendTo(row);
	$("<a />").html("Delete").attr("href", "#").attr("class", "contact-delete").attr("id", contact.id).appendTo(deleteRow).click(deleteContact);
	return row;
}
/*
	Function to decide between patch and post routes for create and edit contact
*/
function submitContact() {
	var contactForm = $("#contactForm");
	// The method type is passed when the template is being rendered, so we can find and access it
	var method = contactForm.attr("method");
	$.ajax({
		url: "/contacts",
		method: method,
		// send the form data
		data: contactForm.serialize()
	}).done(function (result) {
		console.log(result)
		// Check to see if successful
		if (result.created || result.updated) {
			window.location.assign("/contacts.html");
		}
		// else produce error page
	});
	return false;
}