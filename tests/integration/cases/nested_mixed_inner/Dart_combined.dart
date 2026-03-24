void main() {
  {
    final my_data = [
        [1, "a"],
        [2, "b"],
    ];
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = [
        [1, "a"],
        [2, "b"],
    ];
    my_data.hashCode;
  }
}
