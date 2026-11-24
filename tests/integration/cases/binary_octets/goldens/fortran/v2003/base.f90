module fval_m
  implicit none
  integer, parameter :: int64 = selected_int_kind(18)
  integer, parameter :: real64 = selected_real_kind(15, 307)
  integer, parameter :: tag_null = 0
  integer, parameter :: tag_bool = 1
  integer, parameter :: tag_int = 2
  integer, parameter :: tag_real = 3
  integer, parameter :: tag_str = 4
  integer, parameter :: tag_list = 5
  integer, parameter :: tag_map = 6
  integer, parameter :: tag_set = 7
  integer, parameter :: tag_entry = 8
  type :: fval_t
    integer :: tag = tag_null
    logical :: bv = .false.
    integer(kind=int64) :: iv = 0_int64
    real(kind=real64) :: rv = 0.0_real64
    character(len=:), pointer :: sv => null()
    type(fval_t), pointer :: items(:) => null()
  end type fval_t
contains
  function fnull() result(v)
    type(fval_t) :: v
    v%tag = tag_null
  end function fnull
  function fbool(b) result(v)
    logical, intent(in) :: b
    type(fval_t) :: v
    v%tag = tag_bool
    v%bv = b
  end function fbool
  function fint(n) result(v)
    integer(kind=int64), intent(in) :: n
    type(fval_t) :: v
    v%tag = tag_int
    v%iv = n
  end function fint
  function freal(x) result(v)
    real(kind=real64), intent(in) :: x
    type(fval_t) :: v
    v%tag = tag_real
    v%rv = x
  end function freal
  function fstr(s) result(v)
    character(len=*), intent(in) :: s
    type(fval_t) :: v
    v%tag = tag_str
    allocate(character(len=len(s)) :: v%sv)
    v%sv = s
  end function fstr
  function flist(a) result(v)
    type(fval_t), intent(in) :: a(:)
    type(fval_t) :: v
    v%tag = tag_list
    allocate(v%items(size(a)))
    v%items = a
  end function flist
  function fmap(a) result(v)
    type(fval_t), intent(in) :: a(:)
    type(fval_t) :: v
    v%tag = tag_map
    allocate(v%items(size(a)))
    v%items = a
  end function fmap
  function fset(a) result(v)
    type(fval_t), intent(in) :: a(:)
    type(fval_t) :: v
    v%tag = tag_set
    allocate(v%items(size(a)))
    v%items = a
  end function fset
  function fentry(k, u) result(v)
    character(len=*), intent(in) :: k
    type(fval_t), intent(in) :: u
    type(fval_t) :: v
    v%tag = tag_entry
    allocate(character(len=len(k)) :: v%sv)
    v%sv = k
    allocate(v%items(1))
    v%items(1) = u
  end function fentry
end module fval_m
program main
    use fval_m
    implicit none
    type(fval_t) :: my_data
    my_data = flist([fval_t :: &
        fstr(''), &
        fstr('000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323' // &
    & '33435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f60616263646566' // &
    & '6768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999' // &
    & 'a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccd' // &
    & 'cecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'), &
        fstr('fffefdfcfbfaf9f8f7f6f5f4f3f2f1f0efeeedecebeae9e8e7e6e5e4e3e2e1e0dfdedddcdbdad9d8d7d6d5d4d3d2d1d0cfcecdc' // &
    & 'ccbcac9c8c7c6c5c4c3c2c1c0bfbebdbcbbbab9b8b7b6b5b4b3b2b1b0afaeadacabaaa9a8a7a6a5a4a3a2a1a09f9e9d9c9b9a99' // &
    & '9897969594939291908f8e8d8c8b8a898887868584838281807f7e7d7c7b7a797877767574737271706f6e6d6c6b6a696867666' // &
    & '564636261605f5e5d5c5b5a595857565554535251504f4e4d4c4b4a494847464544434241403f3e3d3c3b3a3938373635343332' // &
    & '31302f2e2d2c2b2a292827262524232221201f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100') &
    ])
end program main
