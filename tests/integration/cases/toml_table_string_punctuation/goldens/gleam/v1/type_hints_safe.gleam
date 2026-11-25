pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("comma_hash", GStr("a,#b")),
    #("comma_space_hash", GStr("trail, # comment")),
    #("escaped_quote", GStr("quote \" and , #")),
    #("next_line", GStr("x  y")),
    #("line_separator", GStr("x   y")),
    #("paragraph_separator", GStr("x   y")),
  ])
  let _ = my_data
}
