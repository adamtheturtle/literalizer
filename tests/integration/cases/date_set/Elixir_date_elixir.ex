defmodule Check do
  def x do
    my_data = MapSet.new([
        ~D[2024-01-15],
        ~D[2024-06-01],
    ])
    _ = my_data
  end
end
