struct ThrottlerType; check; end
throttler = ThrottlerType((args...; kwargs...) -> nothing)
throttler.check()
throttler.check()
