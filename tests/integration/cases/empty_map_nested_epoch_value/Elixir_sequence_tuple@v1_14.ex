defmodule Check do
  def x do
    my_data = {
        %{"nested" => %{"times" => {"1900-01-01T00:00:00+00:00"}}},
        %{},
    }
    _ = my_data
  end
end
