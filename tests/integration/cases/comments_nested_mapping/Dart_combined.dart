void main() {
  {
    final my_data = {
        "a": <String, int>{"x": 1},
        "b": 2,
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        "a": <String, int>{"x": 1},
        "b": 2,
    };
    my_data.hashCode;
  }
}
