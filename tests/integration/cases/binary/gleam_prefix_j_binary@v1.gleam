pub type GVal {
  JStr(String)
  JList(List(GVal))
}

pub fn main() {
  let my_data = JList([
    JStr("48656c6c6f"),
  ])
  let _ = my_data
}
