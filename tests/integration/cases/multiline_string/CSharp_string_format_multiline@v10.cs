using System;
var my_data = (
    @"first line
  indented

last line",
    @"
leading newline",
    @"trailing newline
",
    @"
leading and trailing
",
    @"quotes: """""" ''' ` and backslash: \",
    @"interpolation: ${value} #{value} #@value #$value $value",
    "trailing spaces  \nnext",
    @"C++ delimiter collision: )LITERALIZER""
value",
    @"Rust delimiter collision: ""#
value",
    "Ruby fallback interpolation  \n#{expression} #@instance #$global",
    "NUL followed by a digit: \07",
    "carriage\rreturn"
);
