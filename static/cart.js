function update() {
	var select = document.getElementById('no');
	var value = select.options[select.selectedIndex].value;
};

//edit
var stripe = Stripe(checkout_public_key);

const button = document.querySelector('.make-payment');

function user_payment() {
	console.log(checkout_session_id);
	stripe.redirectToCheckout({
		sessionId: checkout_session_id
	}).then(function (result) {
	});
}

function setEvent(cs_id) {
	console.log("setting event");
	button.removeEventListener('click', user_payment);
	
	checkout_session_id = cs_id;
	
	button.addEventListener('click', user_payment );

}
//end

function get_id() {
	const data = { 'u_id' : 'u_id' }
	fetch('/get_sid', {
			method: 'POST',
			headers: {
				'Content-Type':'application/json',
				},
			body: JSON.stringify(data),
		})
		.then(response => response.json())
		.then(result => setEvent(result['session_id']));
};

document.addEventListener("DOMContentLoaded", get_id);


