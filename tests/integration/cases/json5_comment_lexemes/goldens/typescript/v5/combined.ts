let my_data: Record<string, string> = {
  // heading
  "a": "single ' // data",
  "b": "linecontinuation",
  "c": "\\",  // actual comment
  "d": "\u2028\u2029",  // final comment
};
my_data = {
  // heading
  "a": "single ' // data",
  "b": "linecontinuation",
  "c": "\\",  // actual comment
  "d": "\u2028\u2029",  // final comment
};
export {};
