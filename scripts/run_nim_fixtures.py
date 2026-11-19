"""Compile and execute Nim fixtures with all pinned warnings fatal."""

import concurrent.futures
import os
import shutil
import tempfile
from pathlib import Path

import click

from scripts.bounded_command import run_bounded_command
from tests.integration.list_fixtures import fixture_paths

# Refresh from `nim check --warnings:list` when upgrading the compiler.
_WARNING_FLAGS = (
    "--warningAsError:AboveMaxSizeSet:on",
    "--warningAsError:AmbiguousLink:on",
    "--warningAsError:AnyEnumConv:on",
    "--warningAsError:BareExcept:on",
    "--warningAsError:BrokenLink:on",
    "--warningAsError:CStringConv:on",
    "--warningAsError:CannotOpen:on",
    "--warningAsError:CannotOpenFile:on",
    "--warningAsError:CaseTransition:on",
    "--warningAsError:CastSizes:on",
    "--warningAsError:CommentXIgnored:on",
    "--warningAsError:ConfigDeprecated:on",
    "--warningAsError:CycleCreated:on",
    "--warningAsError:Deprecated:on",
    "--warningAsError:Destructor:on",
    "--warningAsError:DotLikeOps:on",
    "--warningAsError:EachIdentIsTuple:on",
    "--warningAsError:Effect:on",
    "--warningAsError:EnumConv:on",
    "--warningAsError:FieldXNotSupported:on",
    "--warningAsError:FileChanged:on",
    "--warningAsError:GcMem:on",
    "--warningAsError:GcUnsafe:on",
    "--warningAsError:GcUnsafe2:on",
    "--warningAsError:GlobalVarConstructorTemporary:on",
    "--warningAsError:HoleEnumConv:on",
    "--warningAsError:IgnoredSymbolInjection:on",
    "--warningAsError:ImplicitDefaultValue:on",
    "--warningAsError:ImplicitRangeConversion:on",
    "--warningAsError:ImplicitTemplateRedefinition:on",
    "--warningAsError:IndexCheck:on",
    "--warningAsError:InheritFromException:on",
    "--warningAsError:LanguageXNotSupported:on",
    "--warningAsError:LockLevel:on",
    "--warningAsError:LongLiterals:on",
    "--warningAsError:ObservableStores:on",
    "--warningAsError:OctalEscape:on",
    "--warningAsError:ProveField:on",
    "--warningAsError:ProveIndex:on",
    "--warningAsError:ProveInit:on",
    "--warningAsError:PtrToCstringConv:on",
    "--warningAsError:RedefinitionOfLabel:on",
    "--warningAsError:ResultShadowed:on",
    "--warningAsError:ResultUsed:on",
    "--warningAsError:SmallLshouldNotBeUsed:on",
    "--warningAsError:Spacing:on",
    "--warningAsError:StdPrefix:on",
    "--warningAsError:StmtListLambda:on",
    "--warningAsError:StrictNotNil:on",
    "--warningAsError:TypelessParam:on",
    "--warningAsError:Uninit:on",
    "--warningAsError:UnknownMagic:on",
    "--warningAsError:UnknownNotes:on",
    "--warningAsError:UnknownSubstitutionX:on",
    "--warningAsError:UnnamedBreak:on",
    "--warningAsError:UnreachableCode:on",
    "--warningAsError:UnreachableElse:on",
    "--warningAsError:UnsafeCode:on",
    "--warningAsError:UnsafeDefault:on",
    "--warningAsError:UnsafeSetLen:on",
    "--warningAsError:UnusedImport:on",
    "--warningAsError:UnusedImportdoc:on",
    "--warningAsError:UseBase:on",
    "--warningAsError:User:on",
    "--warningAsError:WriteToForeignHeap:on",
    "--warningAsError:XIsNeverRead:on",
    "--warningAsError:XmightNotBeenInit:on",
    "--warningAsError:warnRstStyle:on",
)


def _check(*, fixture: Path, compiler: str) -> None:
    """Stage a valid module name and use a private compiler cache."""
    with tempfile.TemporaryDirectory(suffix="-literalizer-nim") as temporary:
        source = Path(temporary) / "check.nim"
        _ = shutil.copyfile(src=fixture, dst=source)
        run_bounded_command(
            args=[
                compiler,
                "c",
                "-r",
                "--hints:off",
                *_WARNING_FLAGS,
                f"--nimcache:{temporary}",
                source,
            ],
            fixture=f"Nim V2 compile/execution: {fixture}",
            timeout_seconds=60.0,
            cwd=None,
        )


@click.command()
def main() -> None:
    """Compile and execute the full Nim V2 fixture population."""
    compiler = shutil.which(cmd="nim")
    if compiler is None:
        raise click.ClickException(message="The nim executable is required.")
    fixtures = fixture_paths(extension=".nim")
    if len(fixtures) == 0:
        raise click.ClickException(message="No Nim fixtures.")
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        checks = [
            executor.submit(_check, fixture=fixture, compiler=compiler)
            for fixture in fixtures
        ]
        for check in checks:
            check.result()


if __name__ == "__main__":
    main()
