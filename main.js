

var trunc = function(input, length) {
    if (input.length > 20) {
        return input.slice(0,length - 3)+'...'    
    };
    return input;
};

var uniqueOf = function(arr, keys) {
    var set = [];
    for (var i = 0; i < arr.length; i++) {
        var filtered = set;
        for (var k = 0; k < keys.length; k++) {
            var key = keys[k];
            filtered = filtered.filter(function(x){return x[key]==arr[i][key]});
        };
        if (filtered.length == 0) {
            set.push(arr[i]);
        };
    };
    return set;
};

var makeTable = function(arr, config) {
    var tds = [];
    for (var i = 0; i < arr.length; i++) {
        var contents = [];
        for (var k = 0; k < config.keys.length; k++) {
            var content = arr[i][config.keys[k]];
            if (config.button_event[k]) {
                content = '(this.parentNode.parentNode, &quot;' + content + '&quot;)">';
                content = '<button onclick="' + config.button_event[k] + content;
                content += config.button_text[k] + '</button>';
            };
            if (config.max_length[k]) {
                content = trunc(content, config.max_length[k]);
            };
            if (config.fixed_dec[k]) {
                content = parseFloat(content).toFixed(config.fixed_dec[k]);
            }
            contents.push(content);
        };
        tds.push('<td>' + contents.join('</td><td>') + '</td>');
    }

    var thead = '<thead><tr><th class="downarrow">' + config.heads.join('</th><th>') + '</th></tr></thead>';
    var tbody = '<tbody><tr>' + tds.join('</tr><tr>') + '</tr></tbody>';
    var table = '<table>' + thead + tbody + '</table>';
    return table;
}

var getArtists = function() {
    var results = document.getElementById("artists");
    results.innerHTML = "<div class='loading'></div>";
    var ajaxUrl = "https://dl.dropboxusercontent.com/u/29149143/coachella/lineup.txt";
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status==200) {
            var artists = JSON.parse(xhr.responseText);
            artists = artists.sort(function(a,b) { return b.popularity - a.popularity; });
            var config = {
                "heads": ['Pop', 'Artist', ''],
                "keys": ['popularity', 'name', 'href'],
                "max_length": [null, 20, null],
                "fixed_dec": [1, null, null],
                "button_event": [null, null, 'getTracks'],
                "button_text": [null, null, 'Tracks']
            };
            var table = makeTable(artists, config);
            results.innerHTML = table;
        };
    };
    xhr.open('GET', ajaxUrl, true);
    xhr.send();
};

var toggleSelectedRow = function(tr) {
    var table = tr.parentNode;
    var trs = table.getElementsByTagName("tr");
    for (var i = 0; i < trs.length; i++) {
        var cur_tr = trs[i];
        if (cur_tr != tr) {
            cur_tr.className = "";
        } else {
            cur_tr.className = "selected";
        };
    }
}

var getTracks = function(tr, uri) {
    toggleSelectedRow(tr);
    var results = document.getElementById("tracks");
    results.innerHTML = "<div class='loading'></div>"
    var ajaxUrl = "https://dl.dropboxusercontent.com/u/29149143/coachella/coachella.txt";
    //var lookupBase = "http://ws.spotify.com/lookup/1/.json?";
    //var ajaxUrl = lookupBase + 'uri=' + uri + '&extras=trackdetail';
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status==200) {
            var data = JSON.parse(xhr.responseText);
            var pieces = uri.split(":");
            var tracks = data[pieces[pieces.length-1]];
            //var tracks = data['album']['tracks'];
            var config = {
                "heads": ['Pop', 'Track Name', '', ''],
                "keys": ['popularity', 'name', 'href', 'href'],
                "max_length": [null, 20, null, null],
                "fixed_dec": [1, null, null, null],
                "button_event": [null, null, 'addTrack', 'playTrack'],
                "button_text": [null, null, 'Add&nbsp;Track', 'Play']
            }   
            var table = makeTable(tracks, config);
            results.innerHTML = table;
        };
    };
    xhr.open('GET', ajaxUrl, true);
    xhr.send();
};

var addPlayIndicator = function() {
    var playlist = document.getElementById("playlist");
    var iframe = document.querySelector("iframe");
    playlist.className = "refreshed";
    iframe.addEventListener('click', function() {
        console.log("clicked");
        iframe.className = "";
    });
};

var playTrack = function(tr, uri) {
    toggleSelectedRow(tr);
    document.getElementById("playlist").className = "loading";
    var iframe = document.querySelector("iframe");
    iframe.src = "https://embed.spotify.com/?uri=" + uri;
    document.getElementById("playlist").className = "";
};

var addTrack = function(tr, uri) {
    var uri_num = uri.split(":")[2];
    var tracksetBase = "https://embed.spotify.com/?uri=spotify:trackset:Coachellified:"
    var iframe = document.querySelector("iframe");
    var pieces = iframe.src.split("?")[1].split("=")[1].split(":");
    var uris = pieces[pieces.length - 1].split(",");
    uris.push(uri_num);
    console.log(tracksetBase + uris.join(","));
    iframe.src = tracksetBase + uris.join(",");
}

getArtists();