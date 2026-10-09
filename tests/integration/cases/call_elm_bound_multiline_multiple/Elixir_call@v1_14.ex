defmodule Check do
  def f(_value), do: nil
  def x do
    ref_data = [
        1,
        2,
    ]
    f([
        ref_data,
    ])
    f([
        ref_data,
    ])
  end
end
