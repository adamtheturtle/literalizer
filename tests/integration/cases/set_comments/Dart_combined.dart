void _declaration() {
  final my_data = {
      "apple",  // inline comment
      // before banana
      "banana",
      // trailing
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      "apple",  // inline comment
      // before banana
      "banana",
      // trailing
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
