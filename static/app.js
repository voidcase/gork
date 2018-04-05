const output = $('.output')
var geo;

function initGeo() {
	if (geo) {
		return true;
	} else if (navigator.geolocation) {
		geo = navigator.geolocation
		return true;
	} else {
		$('body').text("You can't know where you are.")
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
		},
		() => {output.append($('<p></p>').text('you don\'t know where you are'))},
		, {enableHighAccuracy: true}
	)
}

function scan() {
	if (!geo) {
		console.log('bad init :(')
		return
	}
	geo.getCurrentPosition(
		pos => {
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
						output.append(
							res.things.map(t => $('<p></p>').text(
								t.dist < 10 ? 'There is a ' + t.name + ' here.' : 'You sense a ' + t.name + ' ' + t.dist + ' meters away.'
							))
						)
					} else {
						debug.log('error: ' + res.error)
					}
				}
			})
		},
		() => {output.append($('<p></p>').text('you don\'t know where you are'))},
		{enableHighAccuracy: true, timeout: 8000}
	)
}
