use Math::BigFloat;
{
    package LiteralizerFloat;
    our @ISA = ('Math::BigFloat');
    sub new { my ($c, $s) = @_; bless { _s => $s }, $c }
    sub bstr { $_[0]->{_s} }
}
my $my_data = [
    LiteralizerFloat->new("0.0"),
    LiteralizerFloat->new("1.0"),
    LiteralizerFloat->new("1500.0"),
    LiteralizerFloat->new("0.001"),
];
