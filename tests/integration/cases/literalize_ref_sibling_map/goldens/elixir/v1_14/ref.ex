defmodule Check do
  def x do
    sibling_map = %{
        "k" => 2,
    }
    my_data = [
        %{"k" => 1},
        sibling_map,
    ]
    _ = my_data
  end
end
