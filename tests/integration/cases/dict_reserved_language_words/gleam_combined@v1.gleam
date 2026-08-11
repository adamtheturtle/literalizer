pub type GVal {
  GInt(Int)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("assert", GInt(1)),
    #("else", GInt(1)),
    #("error", GInt(1)),
    #("false", GInt(1)),
    #("for", GInt(1)),
    #("function", GInt(1)),
    #("if", GInt(1)),
    #("import", GInt(1)),
    #("importbin", GInt(1)),
    #("importstr", GInt(1)),
    #("in", GInt(1)),
    #("local", GInt(1)),
    #("null", GInt(1)),
    #("self", GInt(1)),
    #("super", GInt(1)),
    #("tailstrict", GInt(1)),
    #("then", GInt(1)),
    #("true", GInt(1)),
    #("ordinary", GInt(1)),
  ])
  let my_data = GDict([
    #("assert", GInt(1)),
    #("else", GInt(1)),
    #("error", GInt(1)),
    #("false", GInt(1)),
    #("for", GInt(1)),
    #("function", GInt(1)),
    #("if", GInt(1)),
    #("import", GInt(1)),
    #("importbin", GInt(1)),
    #("importstr", GInt(1)),
    #("in", GInt(1)),
    #("local", GInt(1)),
    #("null", GInt(1)),
    #("self", GInt(1)),
    #("super", GInt(1)),
    #("tailstrict", GInt(1)),
    #("then", GInt(1)),
    #("true", GInt(1)),
    #("ordinary", GInt(1)),
  ])
  let _ = my_data
}
