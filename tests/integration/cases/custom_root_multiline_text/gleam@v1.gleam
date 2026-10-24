pub type GVal {
  GStr(String)
}

pub fn main() {
  let custom_data = GStr("head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail")
  let _ = custom_data
}
