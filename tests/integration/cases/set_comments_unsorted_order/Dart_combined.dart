void _declaration() {
  final my_data = {
      // before apple
      "apple",
      "banana",  // banana inline
      // trailing
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = {
      // before apple
      "apple",
      "banana",  // banana inline
      // trailing
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
