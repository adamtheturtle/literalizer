procedure Check is
    my_data : A_Val := AList'(
        AMap'(AEntry ("key", AStr ("hello   world")), AEntry ("value", AInt (1)))
    );
begin
    null;
end Check;
