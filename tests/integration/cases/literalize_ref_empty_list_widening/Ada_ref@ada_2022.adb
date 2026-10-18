with A_Stub; use A_Stub;
procedure Main is
    empty_values : A_Val := AList'[];
    integer_values : A_Val := AList'[
        AInt (1)
    ];
    my_data : A_Val := AList'[
        empty_values,
        integer_values
    ];
begin
    null;
end Main;
