pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("del", GStr("ab")),
    #("nel", GStr("a  b")),
    #("c1", GStr("ab")),
  ])
  let _ = my_data
}
