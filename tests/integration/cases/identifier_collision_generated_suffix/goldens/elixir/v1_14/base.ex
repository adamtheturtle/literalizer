defmodule Check do
  def x do
    my_data = %{
        "a-b" => 1,
        "a b" => 2,
        "a-b-2" => 3,
    }
    _ = my_data
  end
end
