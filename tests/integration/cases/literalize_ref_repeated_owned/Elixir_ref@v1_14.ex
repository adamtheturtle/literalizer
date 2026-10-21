defmodule Check do
  def x do
    shared = [
        1,
        2,
    ]
    my_data = [
        shared,
        shared,
    ]
    _ = my_data
  end
end
