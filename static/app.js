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

function logpos() {
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

function scan() {
	if (!geo) {
		console.log('bad init :(')
		return
	}
	geo.getCurrentPosition(pos => {
		$.ajax({
			type: 'POST',
			url: 'scan',
			data: {
				lat: pos.coords.latitude,
				lon: pos.coords.longitude,
				acc: pos.coords.accuracy
			},
			success: (res) => {
				if (res.error === undefined) {
					output.append($('<p></p>').text(
						res.things.map(t => 'there is a ' + t.name + ' ' + t.dist + ' meters away.')
					))
				} else {
					debug.log('error: ' + res.error)
				}
			}
		})
	})
}
