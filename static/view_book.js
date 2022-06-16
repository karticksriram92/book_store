function toggleOption(e) {
	console.log("i got called");
	if(document.getElementById(e).value == "yes") {
		console.log("setting false");
		document.getElementById(e).value = "no";
	}
	else {
		document.getElementById(e).value = "yes";
	}
};

function changeBook(e) {
	if(e.children[0].classList.contains('active')) {
		e.children[0].classList.remove('active','border-success');
		e.children[0].classList.add('border-primary');
		e.children[1].classList.add('border-primary'); 
		e.children[1].classList.remove('border-success','text-success');
	}
	else {
		e.children[0].classList.add('active','border-success');
		e.children[0].classList.remove('border-primary');
		e.children[1].classList.remove('border-primary'); 
		e.children[1].classList.add('border-success','text-success');
	}
}

function toggleBookOption() {
	paperback = document.getElementsByClassName('paperback')[0];
	paperback.addEventListener('click', function(e) { 
		if(ebook.children[0].classList.contains('active')) { changeBook(this); toggleOption('paperback'); }});
	ebook = document.getElementsByClassName('ebook')[0];
	ebook.addEventListener('click', function(e) { 
		if(paperback.children[0].classList.contains('active')) { changeBook(this); toggleOption('ebook'); }});
}

function addCart() {
	const ebook_selected = document.getElementById('ebook').value;
	const paperback_selected = document.getElementById('paperback').value;
	const status = document.querySelector('.add-cart-button').id;
	const book_id = document.querySelector('.book-image').getAttribute('data-id')
	const data = { 'source': 'view', 'book_id' : book_id, 'ebook': ebook_selected, 'paperback': paperback_selected, 'no' : 1, 'status' :  status };
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
		changeStatus();
		console.log(response.status); 
	}});
}

function changeStatus() {
	add_cart_button = document.querySelector('.add-cart-button')
	if(add_cart_button.id === "added") {
		add_cart_button.setAttribute('id','not-added');
		add_cart_button.innerText = 'Add to Cart';
	}
	else {
		add_cart_button.setAttribute('id','added');
		add_cart_button.innerText = 'Remove from Cart';
	}
}

function handleCart() {
	document.querySelector('.add-cart-button').addEventListener('click', addCart);
}

//review
function toggleForm() {
	document.body.classList.toggle("activeForm");
};

function checkAlert() {
	if($(".alert-comment").length) {
	$(".alert-comment").slideUp(3000,0);
}
};

function prevent(e) {
	e.preventDefault()
}

function testValue() {
	if(document.getElementById('rstar').value === '0.0' || document.getElementById('rstar').value === '0') {
		review_button.classList.add('disabled');
		review_button.classList.remove('active');
		review_button.addEventListener('click', prevent);
	}
	else {
		if(document.readyState === "complete") {
		review_button.classList.remove('disabled');
		review_button.classList.add('active');
		review_button.removeEventListener('click', prevent);
		}
	}
};

//stars-rating
function getStars() {
	const ratingStars = [...document.getElementsByClassName("rating_star")];
	const ratingResult = document.querySelector(".rating-result");
	executeRating(ratingStars, ratingResult);
}

function executeRating(stars, result) {
	const starClassActive = "rating_star fas fa-star";
	const starClassInactive = "rating_star far fa-star";
	const starsLength = stars.length;
	let i;
	stars.map((star) => {
		star.onclick = () => {
			i = stars.indexOf(star);
			if (star.className.indexOf(starClassInactive) !== -1) {
				printRatingResult(result, i+1);
				for(i; i >= 0; --i) stars[i].className=starClassActive;
			}
			else {
				printRatingResult(result, i);
				for(i; i < starsLength; ++i) stars[i].className = starClassInactive;
			}
		};
	});
}

function printRatingResult(result, num = 0.0) {
	result.textContent = `${num}/5`;
	document.getElementById('rstar').value=num;
	testValue();
}

document.addEventListener("DOMContentLoaded", () => { 
	getStars();
	review_button = document.querySelector('.comment-submit')
	testValue();
	setTimeout(checkAlert,5000);
	//end
	toggleBookOption();
	handleCart();
	});
