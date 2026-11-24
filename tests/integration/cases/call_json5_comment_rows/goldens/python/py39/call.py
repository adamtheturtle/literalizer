def f(*_args: object, **_kwargs: object) -> object: ...
# calls heading
# before call one
# first argument
f(a=1, b=2)  # after call one
# second argument
f(a=3, b=4)
# after all calls
