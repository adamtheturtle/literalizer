defmodule Check do
  def x do
    my_data = %{
        "outer" => %{"a" => 1, "b" => "x", "c" => nil},
    }
    _ = my_data
  end
end
