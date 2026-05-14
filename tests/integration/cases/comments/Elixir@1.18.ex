defmodule Check do
  def x do
    my_data = %{
        # Server configuration
        "host" => "localhost",  # default host
        "port" => 8080,
        # Enable debug mode
        "debug" => true,
    }
    _ = my_data
  end
end
