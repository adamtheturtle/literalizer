
do {
    let my_data = #"""

first line
  indented

last line

"""#
    precondition(my_data == "\nfirst line\n  indented\n\nlast line\n")
}
