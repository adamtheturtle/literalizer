defmodule Check do
  def x do
    my_data = [
        -0x8000000000000000,
        -0x1,
        0x7fffffffffffffff,
    ]
    _ = my_data
  end
end
