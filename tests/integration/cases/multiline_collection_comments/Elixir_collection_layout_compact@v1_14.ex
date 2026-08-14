defmodule Check do
  def x do
    my_data = %{
        "a" => [1, 2, 3],  # inline a
        "b" => 2,  # inline b
    }
    _ = my_data
  end
end
