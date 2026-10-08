const my_data: Record<string, string> = {
  "double": "a\u2028b",
  "single": "c\u2029d",
  "both": "e\u2028f\u2029g",
  "continued": "hi",
  "escaped backslash": "j\\\u2028k",
};
export {};
