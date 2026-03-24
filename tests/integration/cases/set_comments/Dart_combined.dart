void main() {
  {
    final my_data = {
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = {
        "apple",  // inline comment
        // before banana
        "banana",
        // trailing
    };
    my_data.hashCode;
  }
}
