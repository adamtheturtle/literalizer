pub type GVal {
  GInt(Int)
  GStr(String)
  GList(List(GVal))
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("test", #(GInt(5), #(GStr("compile")))),
    #("package", #(GInt(7), #(GStr("link"), GStr("test")))),
  ])
  let _ = my_data
}
