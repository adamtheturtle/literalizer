void main() {
  {
    final my_data = {
        // before apple
        "apple",
        "banana",  // banana inline
        // trailing
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        // before apple
        "apple",
        "banana",  // banana inline
        // trailing
    };
    my_data.hashCode;
  }
}
