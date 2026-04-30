defmodule Check do
  def x do
    my_data = %{
        "a" => %{"b" => %{"c" => %{"$ref" => "deep"}}},
    }
    _ = my_data
  end
end
