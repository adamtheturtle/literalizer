module Main

type Val =
    | FStr of string
    | FList of Val list
let process (_value: obj) : obj = null
process(FStr "Dune")  // first edition
process(FStr "Solaris")
process(FStr "Neuromancer")  // cyberpunk
