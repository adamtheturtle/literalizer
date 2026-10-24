module Main

type Val =
    | FStr of string
let my_data: Val = FStr "\nroot first line\n  indented\n\nroot last line\n"
