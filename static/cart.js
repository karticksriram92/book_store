//Stripe
var stripe = Stripe(checkout_public_key);

const button = document.querySelector('.make-payment');
//~ button.addEventListener('click',  );

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

//~ function get_id() {
	//~ const data = { 'u_id' : 'u_id' }
	//~ fetch('/get_sid', {
			//~ method: 'POST',
			//~ headers: {
				//~ 'Content-Type':'application/json',
				//~ },
			//~ body: JSON.stringify(data),
		//~ })
		//~ .then(response => response.json())
		//~ .then(result => setEvent(result['session_id']));
//~ };
//end

function handleCheckBox(e) {
	if(e.currentTarget.value === "yes") {
		console.log("setting false")
		e.currentTarget.value="no";
		e.currentTarget.style.opacity = 0.5;
	}
	else {
		console.log("setting true")
		e.currentTarget.value="yes";
		e.currentTarget.style.opacity = 1;
	}
	addCart(e, 'update');
}

function addCart(e, call_status) {
	var current = e.currentTarget;
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
	var status = call_status;
	const book_id = current.id;
	var num = current.querySelector('.pbook_input').value;
	if(ebook_selected === "yes" && num === "0" ) {
		num = 1;
	}
	if(ebook_selected === "no" && paperback_selected === "no") {
		status = "delete";
	}
	const data = { 'source': 'cart', 'book_id' : book_id, 'ebook': ebook_selected, 'paperback': paperback_selected, 'no' : num, 'status' :  status };
	console.log(data);
	var result;
	getProper(data).then(r => { changeValues(r); });
}

async function getProper(data) {
	const r = await fetch('/manage_cart', {
		method: 'POST',
		headers: {
			'Content-Type':'application/json',
			},
		body: JSON.stringify(data),
	})
	.then(response => { if(response.ok) { 
		result = response.json();
		return result;
	}});
	return r;
}

function changeValues(udata) {
	udata = JSON.parse(udata);
	console.log(udata);
	var product = document.getElementById(udata['book_id'])
	//~ console.log(product)
	if(udata['status'] === 'delete') {
		console.log("hello");
		product.style.display="none";
		udata['session_id'] = '';
		document.querySelector('.make-payment').disabled = true;
	}
	
	if(udata['status'] === 'update') {
		console.log("still going");
	if(udata['ebook'] === 0) {
		product.querySelector('.ebook_input').value = "";
		product.querySelector('.ebook_price').innerHTML = "&#8377;0.0";
	}
	else {
		product.querySelector('.ebook_input').value = "1";
		product.querySelector('.ebook_price').innerHTML = "&#8377;"+udata['ebook_total'];
	}
	if(udata['paperback'] === 0) {
		product.querySelector('.pbook_total').innerHTML = "&#8377;0.0";
	}
	else {
		product.querySelector('.pbook_total').innerHTML = "&#8377;"+udata['pbook_total'];
	}
}
	document.querySelector('.book-sum').innerHTML = udata['book_sum'];
	document.querySelector('.shipping').innerHTML = udata['shipping'];
	document.querySelector('.total-sum').innerHTML = udata['total_sum'];
	
	//setting session id
	setEvent(udata['session_id']);	
}

function getElems(tag, check_class) {
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
	if(check_class === "delete") {
		for (var i=0; i<select_elems.length; ++i) {
			select_elems[i].addEventListener('click', function(e) { addCart(e,'delete'); });
		}
	return;
	}
	
	for (var i=0; i<select_elems.length; ++i) {
		select_elems[i].addEventListener('click', handleCheckBox);
	}
}

//~ document.addEventListener("DOMContentLoaded", get_id);
document.addEventListener("DOMContentLoaded", function() {
	getElems("button", "ebook_select");
	getElems("button", "pbook_select");
	getElems("input", "pbook_input");
	getElems("button", "delete");
});
