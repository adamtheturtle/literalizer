defmodule Check do
  def x do
    my_data = MapSet.new([
        "apple",  # inline comment
        # before banana
        "banana",
        # trailing
    ])
    _ = my_data
  end
end
