
if (true) {
    def my_data = '''
first line
  indented

last line
'''
    assert my_data == "\nfirst line\n  indented\n\nlast line\n"
}
