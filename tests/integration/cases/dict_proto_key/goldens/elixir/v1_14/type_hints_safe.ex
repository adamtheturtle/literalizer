defmodule Check do
  def x do
    my_data = %{
        "__proto__" => %{"x" => 1},
        "n" => %{"__proto__" => 3},
        "y" => 2,
    }
    _ = my_data
  end
end
