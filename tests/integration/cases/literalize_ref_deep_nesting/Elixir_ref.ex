defmodule Check do
  def x do
    deep = %{
        "_" => "_",
    }
    my_data = %{
        "a" => %{"b" => %{"c" => deep}},
    }
    _ = my_data
  end
end
