const Playlist: any = new Proxy({}, {get: function g() { return new Proxy(function(){}, {get: g}); }});
Playlist.new({ x: 1 });
Playlist.new({ x: 2 });
export {};
