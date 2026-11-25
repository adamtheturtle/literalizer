with A_Stub; use A_Stub;
procedure Main is
    integer_value : A_Val := AFloat (1.0);
    my_data : A_Val := AList'[
        integer_value,
        AFloat (1.5)
    ];
begin
    null;
end Main;
