let my_var = {
  _ = "_";
}; in
let item_var = {
  _ = "_";
}; in
let my_data = {
  key = my_var;
  items = [item_var ({fallback = "value";})];
}; in my_data
