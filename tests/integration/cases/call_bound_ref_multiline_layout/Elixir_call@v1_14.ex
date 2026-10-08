defmodule Check do
  def f(_value), do: nil
  def x do
    x = [
        [
            1,
            2,
        ],
        [
            3,
            4,
        ],
    ]
    f([
        [
            x,
        ],
    ])
  end
end
