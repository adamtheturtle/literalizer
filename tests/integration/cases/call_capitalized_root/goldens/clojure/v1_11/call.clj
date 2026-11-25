(create-ns 'Playlist)
(intern 'Playlist 'new (fn [& _args] nil))
(Playlist/new :x 1)
(Playlist/new :x 2)
