let foo = {
  _ = "_";
}; in
let my_data = {
  items = [({other = 1;}) foo];
  mapping = {value = foo;};
}; in my_data
