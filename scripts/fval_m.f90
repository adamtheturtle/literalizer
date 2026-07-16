! Real fval_m module backing the Fortran JSON round-trip check
! (issue #2652). Replaces the lint-only stubs the literalizer emits as
! its ``static_preamble``/``static_body_preamble`` for Fortran in
! ``src/literalizer/languages/fortran.py``: those stub procedures have
! empty bodies because the per-language lint job only checks that the
! generated source compiles. This module instead actually stores each
! value passed to the constructors so that ``to_json`` can serialize
! the tree back to JSON for the round-trip comparison in
! ``run_fortran_roundtrip.py``.
!
! The constructor signatures (``fnull``/``fbool``/``fint``/``freal``/
! ``fstr``/``flist``/``fmap``/``fset``/``fentry``) and the ``int64`` /
! ``real64`` kind choices match the lint-stub preamble verbatim, so
! literalized source compiles unchanged against either copy of the
! module. ``fset`` and ``fnull`` are present for signature parity even
! though the null-free shared input never exercises them.
!
! ``to_json`` is a hand-rolled serializer because Fortran ships no
! standard JSON library and the json-fortran package is not in any
! commonly-installed apt/brew bundle; per the issue, this is the
! "language has no standard option" carve-out from the
! prefer-a-library rule that other ``run_<lang>_roundtrip.py`` helpers
! follow. The float path uses ``es24.17e3``, which always emits 17
! significant decimal digits and therefore round-trips every IEEE 754
! ``binary64`` value through ``json.loads`` (the equality check in
! ``roundtrip_common.verify`` compares parsed Python floats, so the
! produced text only needs to reparse to the same float).
module fval_m
  use, intrinsic :: iso_fortran_env, only: int64, real64
  implicit none
  private
  public :: fval_t
  public :: fnull, fbool, fint, freal, fstr, flist, fmap, fset, fentry
  public :: to_json
  ! Re-export the kind constants so that the literalized program (which
  ! does only ``use fval_m``) can write ``42_int64`` / ``3.14_real64``
  ! literals. This matches the lint-stub preamble, which has no
  ! ``private`` and so leaks the kinds the same way.
  public :: int64, real64

  integer, parameter :: tag_null  = 0
  integer, parameter :: tag_bool  = 1
  integer, parameter :: tag_int   = 2
  integer, parameter :: tag_real  = 3
  integer, parameter :: tag_str   = 4
  integer, parameter :: tag_list  = 5
  integer, parameter :: tag_map   = 6
  integer, parameter :: tag_set   = 7
  integer, parameter :: tag_entry = 8

  ! ``items`` is a pointer (not allocatable) because gfortran's automatic
  ! deallocation of a derived type with a recursive ``allocatable ::
  ! items(:)`` component double-frees temporaries produced by a
  ! ``[fval_t :: ...]`` array constructor whose elements themselves carry
  ! allocated components — observed as a SIGTRAP at program exit even
  ! though every intermediate copy looked structurally fine. A pointer
  ! sidesteps the compiler-generated finalizer entirely; the leaked
  ! memory is reclaimed when the round-trip subprocess exits.
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

  recursive function to_json(v) result(s)
    type(fval_t), intent(in) :: v
    character(len=:), allocatable :: s
    character(len=64) :: buf
    integer :: i
    select case (v%tag)
    case (tag_null)
      s = "null"
    case (tag_bool)
      if (v%bv) then
        s = "true"
      else
        s = "false"
      end if
    case (tag_int)
      write(buf, '(i0)') v%iv
      s = trim(buf)
    case (tag_real)
      s = format_real(v%rv)
    case (tag_str)
      s = json_string(v%sv)
    case (tag_list)
      s = "["
      do i = 1, size(v%items)
        if (i > 1) s = s // ","
        s = s // to_json(v%items(i))
      end do
      s = s // "]"
    case (tag_map)
      s = "{"
      do i = 1, size(v%items)
        if (i > 1) s = s // ","
        ! Break the assignment into separate statements: with all four
        ! parts in a single ``s = s // ... // ... // ...`` expression
        ! gfortran 15 silently dropped the closing quote of the last
        ! map entry's key and the following ``":"`` separator, which
        ! looked like a reallocation-during-evaluation bug.
        s = s // json_string(v%items(i)%sv)
        s = s // ":"
        s = s // to_json(v%items(i)%items(1))
      end do
      s = s // "}"
    case default
      s = "null"
    end select
  end function to_json

  function format_real(x) result(s)
    real(kind=real64), intent(in) :: x
    character(len=:), allocatable :: s
    character(len=40) :: buf
    ! ``es26.17e3`` reserves a sign, a leading digit, the decimal point,
    ! 17 fractional digits, the exponent letter, an exponent sign, and 3
    ! exponent digits — 24 characters minimum; the extra two characters
    ! of slack keep gfortran from filling the field with asterisks on
    ! borderline values like ``-0.0``. 17 significant digits round-trip
    ! every IEEE 754 binary64 value through Python's ``json.loads``.
    write(buf, '(es26.17e3)') x
    s = trim(adjustl(buf))
  end function format_real

  function json_string(t) result(s)
    character(len=*), intent(in) :: t
    character(len=:), allocatable :: s
    integer :: i, c
    character(len=6) :: hex
    s = '"'
    do i = 1, len(t)
      c = iachar(t(i:i))
      select case (c)
      case (34)
        s = s // '\"'
      case (92)
        s = s // '\\'
      case (8)
        s = s // '\b'
      case (9)
        s = s // '\t'
      case (10)
        s = s // '\n'
      case (12)
        s = s // '\f'
      case (13)
        s = s // '\r'
      case default
        if (c < 32) then
          write(hex, '("\u",z4.4)') c
          s = s // trim(hex)
        else
          s = s // t(i:i)
        end if
      end select
    end do
    s = s // '"'
  end function json_string

end module fval_m
