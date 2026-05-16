module Main

type Val =
    | FStr of string
    | FList of Val list
let process (_value: obj) : obj = null
process("Dune")  // first edition
process("Solaris")
process("Neuromancer")  // cyberpunk
