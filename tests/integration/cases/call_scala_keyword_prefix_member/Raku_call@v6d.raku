class PlaylistType { method newValue(*@a, *%kw) {} }
my $Playlist = PlaylistType.bless;
$Playlist.newValue(1);
