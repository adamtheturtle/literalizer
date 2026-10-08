class PlaylistType { method new(*@a, *%kw) {} }
my $Playlist = PlaylistType.bless;
$Playlist.new(1);
