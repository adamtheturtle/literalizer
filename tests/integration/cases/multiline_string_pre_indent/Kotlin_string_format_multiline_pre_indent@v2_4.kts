
run {
    val my_data = """
first line
  indented

last line
"""
    check(my_data == "\nfirst line\n  indented\n\nlast line\n")
}
