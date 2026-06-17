pub type GVal {
  GInt(Int)
  GList(List(GVal))
}
pub fn put(_key: a, _value: b) -> Nil { Nil }
pub fn get(_key: a) -> Nil { Nil }

pub fn main() {
  put(GInt(1), GInt(10))
  get(GInt(1))
}
