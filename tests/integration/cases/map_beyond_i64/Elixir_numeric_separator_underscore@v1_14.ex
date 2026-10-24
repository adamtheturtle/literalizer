defmodule Check do
  def x do
    my_data = %{
        "a" => 9_223_372_036_854_775_807,
        "b" => 9_223_372_036_854_775_808,
    }
    _ = my_data
  end
end
