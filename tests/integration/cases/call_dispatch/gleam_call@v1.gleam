pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn store_item(_key: a, _value: b) -> Nil { Nil }
pub fn read_item(_key: a) -> Nil { Nil }

pub fn main() {
  store_item(GInt(1), GInt(10))
  read_item(GInt(1))
}
