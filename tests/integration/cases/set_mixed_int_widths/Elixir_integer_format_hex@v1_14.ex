defmodule Check do
  def x do
    my_data = MapSet.new([
        0x1,
        0x10000000000,
    ])
    _ = my_data
  end
end
