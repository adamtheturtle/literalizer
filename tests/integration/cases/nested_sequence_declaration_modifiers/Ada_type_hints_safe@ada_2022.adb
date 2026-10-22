with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AList'[
        AList'[],
        AList'[AInt (1)],
        AList'[AInt (1), AInt (2)],
        AList'[AInt (1), AStr ("x"), ABool (True), ANull],
        AList'[AInt (1), AInt (2), AInt (3), AInt (4), AInt (5), AInt (6), AInt (7), AInt (8)]
    ];
begin
    null;
end Main;
