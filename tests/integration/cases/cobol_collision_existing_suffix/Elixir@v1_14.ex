defmodule Check do
  def x do
    my_data = %{
        "a-b" => 1,
        "a-b-2" => 2,
        "a b" => 3,
    }
    _ = my_data
  end
end
