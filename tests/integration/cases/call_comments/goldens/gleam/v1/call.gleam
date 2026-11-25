pub type GVal {
  GStr(String)
  GList(List(GVal))
}
pub fn process(_value: a) -> Nil { Nil }

pub fn main() {
  // Test cases
  let _ = process(GStr("hello"))  // single word
  let _ = process(GStr("hello world"))  // two words
  // trailing comment
}
