defmodule Check do
  def x do
    shared = [
        1,
        2,
    ]
    my_data = [
        %{"left" => shared, "right" => shared},
    ]
    _ = my_data
  end
end
