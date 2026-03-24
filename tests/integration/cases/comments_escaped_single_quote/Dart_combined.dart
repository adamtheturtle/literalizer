void main() {
  {
    final my_data = <String, String>{
        "key": "it's here",  // a comment
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String, String>{
        "key": "it's here",  // a comment
    };
    my_data.hashCode;
  }
}
