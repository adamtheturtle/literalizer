defmodule Check do
  def x do
    my_data = MapSet.new([
        1,
        1_099_511_627_776,
    ])
    _ = my_data
  end
end
