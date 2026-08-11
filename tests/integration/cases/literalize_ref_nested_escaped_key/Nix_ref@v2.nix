let foo = {
  _ = "_";
}; in
let my_data = {
  mapping = {value = foo;};
  items = [({other = 1;}) foo];
}; in my_data
