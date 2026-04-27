procedure Check is
    my_data : A_Val := AMap'(
        AEntry ("outer", AMap'(AEntry ("a", AInt (1)), AEntry ("b", AStr ("x")), AEntry ("c", ANull)))
    );
begin
    null;
end Check;
