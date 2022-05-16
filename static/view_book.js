function toggleForm() {
	document.body.classList.toggle("activeForm");
}

function getStars() {
	const ratingStars = [...document.getElementsByClassName("fa-star")];
	const ratingResult = document.querySelector(".rating-result");
	console.log(ratingResult);
	printRatingResult(ratingResult);
	executeRating(ratingStars, ratingResult);
}

function executeRating(stars, result) {
	const starClassActive = "rating__star fas fa-star";
	const starClassInactive = "rating__star far fa-star";
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

function printRatingResult(result, num = 0) {
   result.textContent = `${num}/5`;
}

document.addEventListener("DOMContentLoaded", () => { getStars() });
