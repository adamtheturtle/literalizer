void _declaration() {
  final my_data = <List<List<int>>>[
      <List<int>>[<int>[1, 2], <int>[3, 4]],
      <List<int>>[<int>[5]],
  ];
  my_data.hashCode;
}
void _assignment() {
  dynamic my_data;
  my_data = <List<List<int>>>[
      <List<int>>[<int>[1, 2], <int>[3, 4]],
      <List<int>>[<int>[5]],
  ];
  my_data.hashCode;
}
void main() {
  _declaration();
  _assignment();
}
