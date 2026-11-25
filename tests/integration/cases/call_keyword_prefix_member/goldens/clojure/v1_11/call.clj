(create-ns 'Playlist)
(intern 'Playlist 'newValue (fn [& _args] nil))
(Playlist/newValue :x 1)
