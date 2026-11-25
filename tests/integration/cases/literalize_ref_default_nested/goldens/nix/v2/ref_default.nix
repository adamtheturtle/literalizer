let item_var = {
  _ = "_";
}; in
let my_data = {
  items = [item_var ({fallback = "value";})];
}; in my_data
