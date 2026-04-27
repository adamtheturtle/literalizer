procedure Check is
    my_data : A_Val := AMap'(
        AEntry ("description", AStr ("# not a comment" & Character'Val(10))),
        AEntry ("name", AStr ("foo"))
    );
begin
    null;
end Check;
