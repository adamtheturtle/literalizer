defmodule Check do
  def x do
    my_data = %{
        "b" => nil,
        "a" => %{"y" => [1.0], "x" => false},
    }
    _ = my_data
  end
end
