pub type GVal {
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("outer", GList([GList([GStr("nested first line\n  indented\n\nnested last line\n")])])),
  ])
  let _ = my_data
}
