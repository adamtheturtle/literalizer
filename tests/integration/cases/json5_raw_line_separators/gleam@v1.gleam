pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("double", GStr("a   b")),
    #("single", GStr("c   d")),
    #("both", GStr("e   f   g")),
    #("continued", GStr("hi")),
    #("escaped backslash", GStr("j\\   k")),
  ])
  let _ = my_data
}
