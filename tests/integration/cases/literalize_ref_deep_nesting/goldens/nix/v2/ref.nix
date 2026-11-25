let deep = [
  ([
    "one"
    "two"
  ])
  ([
    "three"
    "four"
  ])
]; in
let my_data = {
  a = {
    b = {
      c = deep;
    };
  };
}; in my_data
