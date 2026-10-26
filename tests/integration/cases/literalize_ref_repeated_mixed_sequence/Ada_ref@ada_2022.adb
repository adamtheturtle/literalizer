with A_Stub; use A_Stub;
procedure Main is
    shared : A_Val := AList'[
        AInt (1),
        AStr ("x")
    ];
    my_data : A_Val := AList'[
        shared,
        shared
    ];
begin
    null;
end Main;
