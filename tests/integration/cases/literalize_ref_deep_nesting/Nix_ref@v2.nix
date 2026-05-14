let deep = {
  _ = "_";
}; in
let my_data = {
  a = {b = {c = deep;};};
}; in my_data
