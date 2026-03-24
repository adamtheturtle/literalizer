void main() {
  {
    final my_data = [
        1,
        "hello",
        true,
        null,
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = [
        1,
        "hello",
        true,
        null,
    ];
    my_data.hashCode;
  }
}
