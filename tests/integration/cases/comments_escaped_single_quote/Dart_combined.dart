void _declaration() {
  final my_data = <String, String>{
      "key": "it's here",  // a comment
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <String, String>{
      "key": "it's here",  // a comment
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
