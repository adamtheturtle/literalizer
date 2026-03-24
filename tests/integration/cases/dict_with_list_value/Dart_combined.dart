void main() {
  {
    final my_data = {
        "name": "Alice",
        "scores": <int>[10, 20, 30],
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        "name": "Alice",
        "scores": <int>[10, 20, 30],
    };
    my_data.hashCode;
  }
}
