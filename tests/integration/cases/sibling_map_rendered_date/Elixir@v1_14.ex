defmodule Check do
  def x do
    my_data = %{
        "a" => %{"k" => ~D[2020-01-01]},
        "b" => %{"k" => "string"},
    }
    _ = my_data
  end
end
