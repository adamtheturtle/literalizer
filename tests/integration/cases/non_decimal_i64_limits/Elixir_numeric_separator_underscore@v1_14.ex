defmodule Check do
  def x do
    my_data = [
        -9_223_372_036_854_775_808,
        -1,
        9_223_372_036_854_775_807,
    ]
    _ = my_data
  end
end
