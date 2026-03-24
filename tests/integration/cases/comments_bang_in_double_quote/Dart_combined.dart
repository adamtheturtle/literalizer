void main() {
  {
    final my_data = <String, String>{
        "key": "\"bang!\"",  // real
    };
    my_data.hashCode;
  }
  {
    dynamic my_data;
    my_data = <String, String>{
        "key": "\"bang!\"",  // real
    };
    my_data.hashCode;
  }
}
