defmodule Check do
  def x do
    my_data = [
        %{"missing" => -1, "present" => 1},
        %{"missing" => 2, "present" => 3},
    ]
    _ = my_data
  end
end
