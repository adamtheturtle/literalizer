var Playlist = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
Playlist.new({ x: 1 });
