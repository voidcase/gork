const output = $('.output')
const geoOptions = {enableHighAccuracy: true, maximumAge: 0}
var geo
var latestPos
var watchId

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

function watchErr() {
	output.append($('<p></p>').style({color:'#f00'}).text('geo error!'))
}

function updatePos(pos) {
	latestPos = pos;
}

function logpos(pos) {
	output.append($('<p></p>').text(
		[
			"lat: " + pos.coords.latitude,
			"lon: " + pos.coords.longitude,
			"acc: " + pos.coords.accuracy
		].join("\n")
	))
}

function initGeo() {
	if (geo) {
		return true
	} else if (navigator.geolocation) {
		geo = navigator.geolocation
		watchId = geo.watchPosition(updatePos, watchErr, geoOptions)
		return true
	} else {
		$('body').text("You can't know where you are.")
		return false
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
		geoOptions
	)
}

function logposbtn() {
	console.log('scanning')
	if (!geo) {
		console.log('bad init :(')
		return
	}
	logpos(latestPos)
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
				output.empty().append(
					res.things.map(t => $('<p></p>').text(
						t.dist < pos.coords.accuracy ?
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
	scanwith(latestPos)
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
	var pos = latestPos
	$.ajax({
		type: 'POST',
		url: 'dig',
		data: {
			lat: pos.coords.latitude,
			lon: pos.coords.longitude,
			acc: pos.coords.accuracy,
			csrf_token: csrf_token,
		},
		success: (res) => {
			if (res.error === undefined) {
				output.append(('<p></p>').text(
					(res.found > 0) ?
						"Your shovel strikes a chest, in it you find " + res.found
							+ " gold pieces!" 
						: "You dig but find nothing but dirt."
					)
				)
			} else {
				console.log('error: ' + JSON.stringify(res.error))
			}
		},
	})
}
