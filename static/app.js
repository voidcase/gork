const output = $('.output')
var geo;

function initGeo() {
	if (geo) {
		return true;
	} else if (navigator.geolocation) {
		geo = navigator.geolocation
		return true;
	} else {
		$('body').text("You don't know where you are.")
		return false;
	}
}

function scan() {
	console.log('scanning')
	if (!geo) {
		console.log('bad init :(')
		return
	}
	geo.getCurrentPosition((pos) => {
		output.append($('<p></p>').text(
			[
				"lat: " + pos.coords.latitude,
				"lon: " + pos.coords.longitude,
				"acc: " + pos.coords.accuracy
			].join("\n")
		))
	})
}
