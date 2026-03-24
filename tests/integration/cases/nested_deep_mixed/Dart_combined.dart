void main() {
  {
    final my_data = [
        [<int>[1, 2], <String>["a", "b"]],
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = [
        [<int>[1, 2], <String>["a", "b"]],
    ];
    my_data.hashCode;
  }
}
