const counters = document.querySelectorAll('.counter');
const speed = 100; // The lower the slower
const grants = document.querySelector('.grants');
const indivGrant = document.querySelectorAll('.individual-grant');

// counters.forEach(counter => {
// 	const updateCount = () => {
// 		const target = +counter.getAttribute('data-target');
// 		const count = +counter.innerText;

// 		// Lower inc to slow and higher to slow
// 		const inc = target / speed;

// 		if (count < target) {
// 			counter.innerText = count + inc;
// 			// Call function every ms
// 			setTimeout(updateCount, 1);
// 		} else {
// 			counter.innerText = target;
// 		}
// 	};

// 	grants.addEventListener('scroll', function(){
// 		indivGrant.forEach(function(grant){
// 			if (grant.getBoundingClientRect().top < window.innerHeight) {
// 				updateCount();
// 			}
// 		});
// 	});
// });

// grants.addEventListener('scroll', function(){
// 	indivGrant.forEach((grant, index) => {
// 		const counter = counters[index];
// 		const target = +counter.getAttribute('data-target');
// 		const inc = target / speed;
// 		let count = 0;
	
// 		const updateCount = () => {
// 		if (count < target) {
// 			count += inc;
// 			counter.innerText = Math.ceil(count);
// 			requestAnimationFrame(updateCount); // Use requestAnimationFrame for smoother animation
// 		} else {
// 			counter.innerText = target;
// 		}
// 		};
	
// 		if (grant.getBoundingClientRect().top < window.innerHeight) {
// 			updateCount();
// 		}
// 	});
// });

const isVisible = function (elem) {
    let bounding = elem.getBoundingClientRect();
    return (
        bounding.top >= 0 &&
        bounding.left >= 0 &&
        bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
};

let done = false;

grants.addEventListener('scroll', function(e) {

	indivGrant.forEach((grant, index) => {
		const visible = isVisible( grant );
		const counter = counters[index];
		const target = +counter.getAttribute('data-target');
		const inc = target / speed;
		let count = 0;

		const updateCount = () => {
			if (count < target) {
					count += inc;
					counter.innerText = Math.ceil(count);
					requestAnimationFrame(updateCount); // Use requestAnimationFrame for smoother animation
				} else {
					counter.innerText = target;
					done = true;
				}
			};

		if( visible && !done ){
			updateCount();
		} else {
			counter.innerText = target;
		}
	});
});