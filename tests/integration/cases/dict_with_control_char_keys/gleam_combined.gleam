pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("key\nwith\nnewlines", GStr("value1")),
    #("key\twith\ttabs", GStr("value2")),
    #("", GStr("value3")),
  ])
  let my_data = GDict([
    #("key\nwith\nnewlines", GStr("value1")),
    #("key\twith\ttabs", GStr("value2")),
    #("", GStr("value3")),
  ])
  let _ = my_data
}
