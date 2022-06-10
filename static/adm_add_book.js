window.addEventListener('load', function() {
	const name = document.getElementById('name');
	name.addEventListener('blur', function() {checkLength();});
	const author = document.getElementById('author');
	author.addEventListener('blur', function() {checkLength();});
	const publisher = document.getElementById('publisher');
	publisher.addEventListener('blur', function() {checkLength();});
	const description = document.getElementById('description');
	description.addEventListener('blur', function() {checkLength(min=300,max=3000);});
});

function checkLength(min=5, max=100) {
	const val = event.target.value;
	if (!(val>min && val<max)) {
		
	}
}
