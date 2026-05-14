defmodule Check do
  def x do
    my_data = %{
        "host" => "localhost",
        "port" => nil,  # not configured yet
        "debug" => true,
    }
    _ = my_data
  end
end
