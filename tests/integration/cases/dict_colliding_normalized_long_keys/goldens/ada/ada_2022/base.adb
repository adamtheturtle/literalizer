with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := AMap'[
        AEntry ("a_b", AInt (1)),
        AEntry ("a-b", AInt (2)),
        AEntry ("averyveryverylongkeynamethatgoesonandonandon", AInt (3)),
        AEntry ("averyveryverylongkeynamethatgoesonandmore", AInt (4))
    ];
begin
    null;
end Main;
