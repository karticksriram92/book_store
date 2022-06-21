function get_username() {
	const u_id = $('#accountDropdownMenu').data('id');
	const data = { 'u_id' : u_id }
	if($('.username').length) {
		fetch('/get_u_id', {
			method: 'POST',
			headers: {
				'Content-Type':'application/json',
				},
			body: JSON.stringify(data),
		})
		.then(response => response.json())
		.then(result => { document.querySelector('.username').innerHTML=result['username']; });
	}
};

function getRecentViews() {
	var page_url = window.location.href;
	const urlArray = page_url.split("/");
	const u_id = $('#accountDropdownMenu').data('id');
	if(u_id) {
		if(urlArray[3] === "books") {
			setRecentView(u_id, urlArray[4]);
		}
	}
};

function setRecentView(u_id, book_id) {
	const data = { 'u_id' : u_id, 'book_id' : book_id }
	fetch('/addRecent', {
		method: 'POST',
		headers: {
			'Content-Type' : 'application/json',
		},
		body: JSON.stringify(data),
	});
};

document.addEventListener("DOMContentLoaded", get_username);
document.addEventListener("DOMContentLoaded", getRecentViews);
