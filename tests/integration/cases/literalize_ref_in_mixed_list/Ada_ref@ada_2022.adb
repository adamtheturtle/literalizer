with A_Stub; use A_Stub;
procedure Main is
    ref_x : A_Val := AInt (3);
    my_data : A_Val := AList'[
        ref_x,
        AInt (1),
        AInt (2)
    ];
begin
    null;
end Main;
