with A_Stub; use A_Stub;
procedure Main is
    procedure Send (Value : A_Val) is begin null; end Send;
    existing : A_Val := AInt (42);
begin
    Send(value => existing);
end Main;
