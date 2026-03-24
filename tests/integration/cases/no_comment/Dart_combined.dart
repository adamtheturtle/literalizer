void _declaration() {
  final my_data = <String, String>{
      "message": "no comment here",
  };
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <String, String>{
      "message": "no comment here",
  };
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
