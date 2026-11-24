defmodule Check do
  def x do
    my_data = %{
        "a" => %{"k" => ~U[2040-01-01 00:00:00+00:00]},
        "b" => %{"k" => 1},
    }
    _ = my_data
  end
end
