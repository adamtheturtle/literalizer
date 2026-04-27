procedure Check is
    my_data : A_Val := AMap'(
        AEntry ("name", AStr ("Alice")),
        AEntry ("scores", AMap'(AEntry ("1", AStr ("first")), AEntry ("2", AStr ("second"))))
    );
begin
    null;
end Check;
