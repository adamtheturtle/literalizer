defmodule Check do
  def x do
    my_data = %{
        "host" => "it's here",  # a comment
        "port" => 80,  # another
    }
    _ = my_data
  end
end
