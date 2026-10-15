defmodule Check do
  def f(_a, _b), do: nil
  def x do
    # calls heading
    # before call one
    # first argument
    f(1, 2)  # after call one
    # second argument
    f(3, 4)
    # after all calls
  end
end
