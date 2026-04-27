procedure Check is
    my_data : A_Val := AMap'(
        AEntry ("lint", AList'(AInt (2), AList'(1 .. 0 => ANull))),
        AEntry ("test", AList'(AInt (5), AList'(AStr ("compile"))))
    );
begin
    null;
end Check;
