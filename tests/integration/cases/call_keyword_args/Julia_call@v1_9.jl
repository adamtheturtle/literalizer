struct ThrottlerType; check; end
throttler = ThrottlerType((args...; kwargs...) -> nothing)
emit(args...; kwargs...) = nothing
emit(throttler.check(user_id="user_1", ts=1000.0))
emit(throttler.check(user_id="user_2", ts=2000.5))
