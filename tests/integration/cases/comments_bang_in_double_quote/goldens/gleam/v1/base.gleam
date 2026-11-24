pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("key", GStr("\"bang!\"")),  // real
  ])
  let _ = my_data
}
