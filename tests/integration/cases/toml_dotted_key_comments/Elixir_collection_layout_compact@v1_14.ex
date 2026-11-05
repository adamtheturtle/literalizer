defmodule Check do
  def x do
    my_data = %{
        # first dotted key
        # second dotted key
        "a" => %{"b" => 1, "c" => 2},
    }
    _ = my_data
  end
end
