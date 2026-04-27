procedure Check is
    my_data : A_Val := AList'(
        AList'(AInt (1), AInt (2)),
        AList'(1 .. 0 => ANull),
        AList'(AStr ("a"), AStr ("b"))
    );
begin
    null;
end Check;
