const output = $('.output')
var geo;

const dirmap = {
	'N' : 'north',
	'NE': 'northeast',
	'NW': 'northwest',
	'S' : 'south',
	'SE': 'southeast',
	'SW': 'southwest',
	'E' : 'east',
	'W' : 'west',
}

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
			acc: pos.coords.accuracy,
			csrf_token: csrf_token,
		},
		success: (res) => {
			if (res.error === undefined) {
				output.append(
					res.things.map(t => $('<p></p>').text(
						t.dist < 10 ?
							'There is a ' + t.name + ' here.' 
							: 'You sense a ' + t.name 
								+ ' ' + t.dist + ' meters to the '
								+ dirmap[t.dir] + "."
					))
				)
			} else {
				console.log('error: ' + JSON.stringify(res.error))
			}
		}
	})
}

function scan() {
	if (!geo) {
		console.log('bad init :(')
		return
	}
	posop(scanwith)
}

function debugscan() {
	scanwith ({
		coords: {
			latitude: 0.0,
			longitude: 0.0,
			accuracy: 10,
		}
	})
}

function dig() {
	if (!geo) {
		console.log('bad init :(')
		return
	}
	posop((pos) => {
		$.ajax({
			type: 'POST',
			url: 'scan',
			data: {
				lat: pos.coords.latitude,
				lon: pos.coords.longitude,
				acc: pos.coords.accuracy,
				csrf_token: csrf_token,
			},
			success: (res) => {
				if (res.error === undefined) {
					output.append(
						(res.found > 0) ?
							"Your shovel strikes a chest, in it you find " + res.found
								+ " gold pieces!" 
							: "You dig but find nothing but dirt."
					)
				} else {
					console.log('error: ' + JSON.stringify(res.error))
				}
			},
		})
	})
}
