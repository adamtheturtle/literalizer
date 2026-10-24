defmodule Check do
  def x do
    custom_data = "head\nfinal my_data = 123;\nfinal fakeRoot = 1;\nfinal fixtureRoot = 1;\ntail"
    _ = custom_data
  end
end
