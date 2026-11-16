Val := [
    RInt(I128),
]

my_data : Val
my_data = # scalar heading
# second heading line
RInt(42.I128)  # scalar inline
# inline continuation
# scalar trailing

main! = |_args| {
    _ = my_data
    Ok({})
}
