with A_Stub; use A_Stub;
procedure Main is
    item : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
    my_data : A_Val := AList'[
        AInt (1),
        AInt (2)
    ];
begin
    (void)my_data;
    my_data := item;
    (void)my_data;
end Main;
