defmodule Check do
  def x do
    my_data = %{
        "half" => ~N[1979-05-27 07:32:00.500000],
        "milli" => ~N[1979-05-27 07:32:00.100000],
        "max_milli" => ~N[1979-05-27 07:32:00.999000],
        "whole" => ~N[1979-05-27 07:32:00],
    }
    _ = my_data
  end
end
