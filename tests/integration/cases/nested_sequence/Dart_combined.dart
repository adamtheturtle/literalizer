void main() {
  {
    final my_data = [
        true,
        "hi",
        <int>[1, 2],
        null,
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = [
        true,
        "hi",
        <int>[1, 2],
        null,
    ];
    my_data.hashCode;
  }
}
