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

document.addEventListener("DOMContentLoaded", get_username);
