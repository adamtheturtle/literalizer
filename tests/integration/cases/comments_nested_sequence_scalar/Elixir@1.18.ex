defmodule Check do
  def x do
    my_data = [
        ["ADD", "alice", "hello"],
        ["DEL", "bob", "5"],  # removes "world"
    ]
    _ = my_data
  end
end
