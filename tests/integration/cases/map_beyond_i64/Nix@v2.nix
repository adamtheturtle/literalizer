let my_data = {
  a = 9223372036854775807;
  b = (builtins.fromJSON "9223372036854775808");
}; in my_data
