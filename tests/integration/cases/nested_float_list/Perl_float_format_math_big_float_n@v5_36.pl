use Math::BigFloat;
{
    package LiteralizerFloat;
    our @ISA = ('Math::BigFloat');
    sub new { my ($c, $s) = @_; bless { _s => $s }, $c }
    sub bstr { $_[0]->{_s} }
}
my $my_data = [
    [LiteralizerFloat->new("1.5"), LiteralizerFloat->new("2.5")],
    [LiteralizerFloat->new("3.5"), LiteralizerFloat->new("4.5")],
];
