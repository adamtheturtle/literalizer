defmodule ThrottlerType_ do
  def check(_user_id, _ts), do: nil
end
defmodule Check do
  def emit(_arg), do: nil
  def x do
    throttler = ThrottlerType_
    emit(throttler.check("user_1", 1000.0))
    emit(throttler.check("user_2", 2000.5))
  end
end
