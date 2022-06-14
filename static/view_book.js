function toggleForm() {
	document.body.classList.toggle("activeForm");
};

//~ function toggleBookOption() {
	//~ document.querySelector('.book-mode-paperback').addEventListener('click', () => { e.
//~ }

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
	//~ toggleBookOption();
	testValue();
	setTimeout(checkAlert,5000);
	});
