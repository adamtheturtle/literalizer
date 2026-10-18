with A_Stub; use A_Stub;
procedure Main is
    one : A_Val := AInt (1);
    two : A_Val := AStr ("s");
    my_data : A_Val := AList'[
        one,
        two
    ];
begin
    null;
end Main;
