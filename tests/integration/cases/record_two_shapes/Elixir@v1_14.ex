defmodule Check do
  def x do
    my_data = %{
        "metrics" => %{"count" => 100, "rate" => 50},
        "flags" => %{"retries" => 3, "timeout" => 30},
    }
    _ = my_data
  end
end
