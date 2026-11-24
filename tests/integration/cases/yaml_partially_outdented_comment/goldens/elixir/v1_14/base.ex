defmodule Check do
  def x do
    my_data = %{
        "a" => %{
            "b" => [1],
            # Outdented from the sequence, so the inner mapping claims this.
            "c" => 2,
        },
        # Outdented from the inner mapping too, so the root claims this.
        "d" => 3,
    }
    _ = my_data
  end
end
