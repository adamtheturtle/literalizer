defmodule Check do
  def consume(_items, _mapping), do: nil
  def x do
    foo = 42
    consume([
        %{
            "other" => 1,
        },
        foo,
    ], %{
        "left" => foo,
        "other" => 1,
    })
  end
end
