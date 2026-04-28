with A_Stub; use A_Stub;
procedure Main is
    my_data : A_Val := ASet'[
        ABool (True),
        AInt (42),
        AStr ("apple")
    ];
begin
    my_data := ASet'[
        ABool (True),
        AInt (42),
        AStr ("apple")
    ];
end Main;
