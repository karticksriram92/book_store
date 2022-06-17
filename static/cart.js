//Stripe
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
//end

function handleCheckBox(e) {
	//~ e.currentTarget.preventDefault;
	console.log(e.currentTarget);
	if(e.currentTarget.value === "selected") {
		console.log("setting false")
		e.currentTarget.value="not-selected";
		e.currentTarget.style.opacity = 0.5;
	}
	else {
		console.log("setting true")
		e.currentTarget.value="selected";
		e.currentTarget.style.opacity = 1;
	}
	//~ addCart('
}

function addCart(e, call_status) {
	var current = e.currentTarget;
	console.log(current);
	while(true) {
		if(current.classList.contains('cart-product')) {
			break;
		}
		else {
			current = current.parentNode;
		}
	}
	const ebook_selected = current.querySelector('.ebook_select').value;
	const paperback_selected = current.querySelector('.pbook_select').value;
	const status = call_status;
	const book_id = current.id;
	const num = current.querySelector('.pbook_input').value;
	const data = { 'source': 'cart', 'book_id' : book_id, 'ebook': ebook_selected, 'paperback': paperback_selected, 'no' : num, 'status' :  status };
	//~ const url = window.location.href+'/cart';
	console.log(book_id)
	fetch('/manage_cart', {
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
			},
		body: JSON.stringify(data),
	})
	.then(response => { if(response.status == 200) { 
		changeValues();
		console.log(response.status); 
		console.log(response.json()); 
	}});
}

function getEbookCheckbox(tag, check_class) {
	select_elems = [];
	var input_elems = document.getElementsByTagName(tag);
	
	for (var i=0; i<input_elems.length; ++i) {
		if(input_elems[i].classList.contains(check_class)) {
			select_elems.push(input_elems[i]);
		}
	}
	
	if(tag === "input") {
		for (var i=0; i<select_elems.length; ++i) {
			select_elems[i].addEventListener('change', function(e) { addCart(e,'update'); });
	}
	return;
	}
	
	for (var i=0; i<select_elems.length; ++i) {
		select_elems[i].addEventListener('click', handleCheckBox);
	}
}

document.addEventListener("DOMContentLoaded", get_id);
document.addEventListener("DOMContentLoaded", function() {
	getEbookCheckbox("button", "ebook_select");
	getEbookCheckbox("button", "pbook_select");
	getEbookCheckbox("input", "pbook_input");
});
