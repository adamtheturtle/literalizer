with A_Stub; use A_Stub;
procedure Main is
    ref_data : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
    my_data : A_Val := AList'[
        AInt (0)
    ];
begin
    (void)my_data;
    my_data := ref_data;
    (void)my_data;
end Main;
