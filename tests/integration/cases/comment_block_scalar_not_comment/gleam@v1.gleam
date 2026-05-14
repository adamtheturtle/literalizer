pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("description", GStr("# not a comment\n")),
    #("name", GStr("foo")),
  ])
  let _ = my_data
}
