use DateTime;
sub process {}
sub emit {}
emit(process(1), DateTime->new(year => 2024, month => 1, day => 15));
