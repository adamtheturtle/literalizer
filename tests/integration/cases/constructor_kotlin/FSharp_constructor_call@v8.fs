class Playlist { val value = 42 }

type Val =
    | FList of Val list
let p = Playlist()
check(p.value == 42)
