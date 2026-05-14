defmodule ThrottlerType_ do
  def check(), do: nil
end
defmodule Check do
  def x do
    throttler = ThrottlerType_
    throttler.check()
    throttler.check()
  end
end
