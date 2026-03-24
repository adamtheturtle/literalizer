void main() {
  {
    final my_data = <String, double>{
        "a": 1,
        "b": 2.5,
        "c": 3,
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String, double>{
        "a": 1,
        "b": 2.5,
        "c": 3,
    };
    my_data.hashCode;
  }
}
