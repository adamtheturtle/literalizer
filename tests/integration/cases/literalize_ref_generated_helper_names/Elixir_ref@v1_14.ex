defmodule Check do
  def x do
    std = %{
        "a" => 1,
    }
    arena = %{
        "a" => 1,
    }
    allocator = %{
        "a" => 1,
    }
    my_data = [
        std,
        arena,
        allocator,
    ]
    _ = my_data
  end
end
