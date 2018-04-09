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

function posop(callback) {
	if (!geo) {
		console.log('bad init :(')
		return
	}
	geo.getCurrentPosition(
		callback,
		() => {output.append($('<p></p>').text('you don\'t know where you are'))},
		{enableHighAccuracy: true, maximumAge: 0}
	)
}

function logpos() {
	console.log('scanning')
	if (!geo) {
		console.log('bad init :(')
		return
	}
	posop(pos => {
		output.append($('<p></p>').text(
			[
				"lat: " + pos.coords.latitude,
				"lon: " + pos.coords.longitude,
				"acc: " + pos.coords.accuracy
			].join("\n")
		))
	})
}

function scanwith(pos) {
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
				console.log('error: ' + res.error)
			}
		}
	})
}

function scan() {
	if (!geo) {
		console.log('bad init :(')
		return
	}
	posop(scanwith(pos))
}

function debugscan() {
	scanwith ({
		coords: {
			latitude: 0.0,
			longitude: 0.0,
			accuracy: 10
		}
	})
}
