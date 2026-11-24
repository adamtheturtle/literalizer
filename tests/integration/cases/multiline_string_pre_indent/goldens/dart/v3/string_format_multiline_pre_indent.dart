
void main() {
    final my_data = '''\nfirst line
  indented

last line
''';
    if (my_data != "\nfirst line\n  indented\n\nlast line\n") { throw StateError("changed multiline string"); }
}
