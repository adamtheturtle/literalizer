pub type GVal {
  GStr(String)
  GDict(List(#(String, GVal)))
}

pub fn main() {
  let my_data = GDict([
    #("cr", GStr("a\rb")),
    #("crlf", GStr("a\r\nb")),
    #("lf", GStr("a\nb")),
  ])
  let _ = my_data
}
