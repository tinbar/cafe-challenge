$(function(){
	// Start
	$(".contact-delete").click(deleteContact);
});

function deleteContact() {
	var contact_id = $(this).attr("id");
	$.ajax({
		url: "/contacts",
		method: "delete",
		data: {
			"contact_id" : contact_id
		}
	}).done(function (result) {
		reloadContactTable();
	});
}

function reloadContactTable() {
	var tableBody = $("#contacts-table-body")
	$.get({
		url:"/contacts"
	}).done(function (result){
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

function submitContact() {
	var contactForm = $("#contactForm");
	var method = contactForm.attr("method");
	$.ajax({
		url: "/contacts",
		method: method,
		data: contactForm.serialize()
	}).done(function (result) {
		console.log(result)
		if (result.created || result.updated) {
			window.location.assign("/contacts.html");
		}
		// else produce error page
	});
	return false;
}