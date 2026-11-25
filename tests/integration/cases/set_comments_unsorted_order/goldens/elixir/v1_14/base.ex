defmodule Check do
  def x do
    my_data = MapSet.new([
        # before apple
        "apple",
        "banana",  # banana inline
        # trailing
    ])
    _ = my_data
  end
end
