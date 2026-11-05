Rendering function calls
========================

If your documentation or test suite needs to show function calls with literal arguments across multiple languages, :func:`literalizer.literalize_call` generates those calls from a single YAML, JSON, JSONC, JSON5, or TOML source.

Each row of a top-level list becomes a separate function call, with arguments formatted according to the target language's calling convention.

Example
-------

Suppose you want to generate calls to ``throttler.check`` with two parameters (``user_id`` and ``ts``) and wrap each call in ``print()``:

.. code-block:: python

   """Generate per-language function call examples."""

   import textwrap

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Python

   yaml_source = """\
   ---
   - - user_1
     - 1000.0
   - - user_2
     - 2000.5
   """

   result = literalize_call(
       source=yaml_source,
       input_format=InputFormat.YAML,
       language=Python(
           date_format=Python.date_formats.PYTHON,
           datetime_format=Python.datetime_formats.PYTHON,
           bytes_format=Python.bytes_formats.HEX,
           sequence_format=Python.sequence_formats.TUPLE,
           set_format=Python.set_formats.SET,
           variable_type_hints=Python.variable_type_hints_formats.NEVER,
       ),
       target_function="throttler.check",
       parameter_names=["user_id", "ts"],
       call_transform=lambda ctx: f"print({ctx.call})",
   )

   assert result.code == textwrap.dedent(
       text="""\
       print(throttler.check(user_id="user_1", ts=1000.0))
       print(throttler.check(user_id="user_2", ts=2000.5))""",
   )

Selecting a nested input root
-----------------------------

Some formats require a mapping at the document root.
For example, a TOML document cannot itself be an array of call rows.
Use ``input_root_key`` to select such an array without parsing the document yourself:

.. code-block:: python

   """Render call rows stored below a TOML key."""

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Python

   result = literalize_call(
       source="calls = [[1], [2]]",
       input_format=InputFormat.TOML,
       input_root_key="calls",
       language=Python(),
       target_function="process",
       parameter_names=["value"],
   )

   assert result.code == "process(value=1)\nprocess(value=2)"

The parsed root must be a mapping and the key must exist.
Violations raise :class:`~literalizer.exceptions.InputRootNotMappingError` and :class:`~literalizer.exceptions.InputRootKeyNotFoundError`, respectively.

Calling conventions
-------------------

Each language has a calling convention that determines how arguments are formatted.
There are three styles:

**Keyword** (e.g. Python, Swift, Ruby): arguments are passed as ``name=value`` pairs.

.. code-block:: python

   """Illustrate the keyword-call style."""


   class Throttler:
       """Stub throttler for the example."""

       def check(self, *, user_id: str, ts: float) -> str:
           """Return a confirmation string."""
           return f"{type(self).__name__} checked {user_id} at {ts}"


   throttler = Throttler()
   print(throttler.check(user_id="user_1", ts=1000.0))

**Object** (e.g. JavaScript, TypeScript): arguments are wrapped in an object literal.

.. code-block:: javascript

   print(throttler.check({ user_id: "user_1", ts: 1000.0 }));

**Positional** (e.g. Rust, Java, C++): arguments are passed by position only, so parameter names are not included in the output.

.. code-block:: rust

   print(throttler.check("user_1", 1000.0));

You do not need to choose a style, because it is determined automatically by the language you pass to :func:`~literalizer.literalize_call`.

Constructor targets
-------------------

To bind the result of a zero-argument constructor call, ask the language for its constructor target and pass that to :func:`~literalizer.literalize_call` as ``target_function``:

.. code-block:: python

   """Bind a zero-argument constructor call."""

   from literalizer import InputFormat, NewVariable, literalize_call
   from literalizer.languages import Rust

   language = Rust()
   result = literalize_call(
       source="[[]]",
       input_format=InputFormat.JSON,
       language=language,
       target_function=language.format_constructor_target("Playlist"),
       parameter_names=[],
       variable_form=NewVariable(
           name="p",
           modifiers=frozenset({Rust.modifiers.MUT}),
       ),
   )

   assert result.code == "let mut p = Playlist::new();"

The default constructor target is ``ClassName``.
Languages with different common constructor syntax override it; for example Java and JavaScript return ``new ClassName``, Go returns ``NewClassName``, Ruby returns ``ClassName.new``, and Rust returns ``ClassName::new``.

For languages whose default call style wraps arguments in an object, use the positional call-style option when rendering a no-argument constructor so the call is emitted as ``new Playlist()`` rather than ``new Playlist({})``.

Caller-owned callee requirements
--------------------------------

Literalizer renders the target name and arguments; the caller supplies the external function or constructor declaration.
That declaration must accept the generated argument types and calling convention.
Literalizer does not inspect the callee or infer its return type from its arguments.
The stubs emitted by ``wrap_in_file=True`` provide example scaffolding; they do not validate an external callee's contract.

When ``variable_form`` binds a call result, the callee must return a value compatible with the declaration or existing variable.
For example, a C++ ``auto`` declaration or Rust ``let`` binding lets the compiler infer the actual return type, while an assignment must fit the existing variable's type and mutability.
A ``call_transform`` can impose further requirements: a wrapper that formats, compares, or consumes a value must accept the callee's actual result.

A declaration that requires a compile-time constant also requires the call expression to satisfy the target language's constant-expression rules.
Immutability alone does not necessarily impose that requirement: JavaScript ``const`` and Rust's ordinary ``let`` can bind runtime call results.
In Dart, ``Dart.declaration_styles.CONST`` requires a constant expression.
This constant-constructor call is valid:

.. code-block:: python

   """Generate a Dart constant-constructor binding."""

   from literalizer import InputFormat, NewVariable, literalize_call
   from literalizer.languages import Dart

   result = literalize_call(
       source="[[42]]",
       input_format=InputFormat.JSON,
       language=Dart(declaration_style=Dart.declaration_styles.CONST),
       target_function="Widget",
       parameter_names=["count"],
       variable_form=NewVariable(
           name="result",
           modifiers=frozenset(),
       ),
   )

   assert result.code == "const result = Widget(count: 42);"

The caller can supply the following declaration and use that generated binding:

.. code-block:: dart

   class Widget {
     final int count;
     const Widget({required this.count});
   }

   const result = Widget(count: 42);

   void main() {
     print(result.count);
   }

The initializer is already a constant context, so ``Widget(...)`` does not need an additional ``const`` keyword.
Replacing the constructor with an ordinary function, such as ``String make_widget({required int count}) => "count=$count";``, makes ``const result = make_widget(count: 42);`` invalid: ordinary function invocations are not Dart constant expressions.
Choose a runtime binding for that function, or supply a constant constructor when a constant binding is needed.
Literalizer preserves the requested declaration policy because the external callee is unknown.

Variable references as arguments
--------------------------------

An argument can be a **reference to a named variable** instead of an inline literal value.
Use a ``{"$ref": "name"}`` marker at the argument position and pass ``ref_key="$ref"``; :func:`~literalizer.literalize_call` then emits the identifier verbatim at that slot.
Other arguments are still rendered as literals as usual, so refs and literals can be mixed freely.

For example, passing the JSON source ``[[{"$ref": "my_var"}, 42]]`` to :func:`~literalizer.literalize_call` with ``parameter_names=["data", "count"]``, ``language=Python()``, and ``ref_key="$ref"`` yields ``process(data=my_var, count=42)``.

This composes with :class:`~literalizer.NewVariable`: declare the data once with :func:`~literalizer.literalize` and then refer to it from a call rendered by :func:`~literalizer.literalize_call`, without repeating the literal value at the call site.

When the referenced value contains types that affect generated declarations or imports, pass those source values via ``ref_values``.
The referenced value participates in preamble inference without inserting that value into the call:

.. code-block:: python

   """Render a call whose ref contributes to preamble inference."""

   from literalizer import InputFormat, NewVariable, literalize, literalize_call
   from literalizer.languages import Haskell

   language = Haskell()
   declaration = literalize(
       source="[1, 2, 3]",
       input_format=InputFormat.JSON,
       language=language,
       variable_form=NewVariable(name="myList", modifiers=frozenset()),
   )
   call = literalize_call(
       source='[[{"$ref": "myList"}, 42]]',
       input_format=InputFormat.JSON,
       language=language,
       target_function="process",
       parameter_names=["data", "count"],
       ref_key="$ref",
       ref_values={"myList": declaration.source_data},
   )
   assert call.declaration_code == "process myList (42)"

If a ref name is omitted from ``ref_values``, its marker is ignored for preamble inference as before.
``ref_values`` keys are the names from the input data before any ``ref_case`` conversion.

Preserving external bindings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calls preserve external bindings unless the caller explicitly permits consumption through ``consumable_refs``.
The preserving expression depends on the language and the binding representation.
Rust copies known ``Copy`` values directly and clones owned containers so later calls can still use them.
For an unknown external reference, Rust conservatively emits ``name.clone()``; removing that clone without knowing the binding type can introduce a move error.

Supply ``ref_values`` when composing separately generated declarations and calls:

.. code-block:: python

   """Preserve a reusable map without cloning Copy scalar bindings."""

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Rust

   result = literalize_call(
       source='[[{"$ref": "comments"}, {"$ref": "keyword"}, {"$ref": "depth"}]]',
       input_format=InputFormat.JSON,
       language=Rust(),
       target_function="search",
       parameter_names=["comments", "keyword", "depth"],
       ref_key="$ref",
       ref_values={"comments": {"a": "hello"}, "keyword": "tech", "depth": 2},
   )
   assert result.code == "search(comments.clone(), keyword, depth);"

The values must describe compatible external declarations rendered with the same representation options.
For example, a Rust string rendered as a JSON value has different ownership behavior from a native ``&str`` binding.
``ref_values`` supplies inference hints; it neither emits declarations nor grants consumption permission.
Use ``bound_refs`` when Literalizer should own the declaration and its representation as well.
An explicit hint for a bound reference may guide inference, while copying still follows the actual binding representation.

``consumable_refs`` permits a consuming expression only for references used exactly once in the call input.
Repeated references continue to preserve their bindings.
Leave a name out of that set whenever the surrounding program needs it later.

By default the identifier's spelling is unchanged, independently of any copy or clone expression around it.
Pass ``ref_case`` to :func:`~literalizer.literalize_call` to convert the name to the target language's idiomatic case.

Case conversion
~~~~~~~~~~~~~~~

The ``ref_case`` parameter accepts a :class:`~literalizer.IdentifierCase` value (``SNAKE``, ``CAMEL``, ``PASCAL``, ``UPPER_SNAKE``, or ``KEBAB``).
Each :class:`Language` exposes two related but independent attributes:

* :attr:`~literalizer.Language.supported_ref_cases` -- the cases that produce a syntactically legal identifier in the target language.
  Passing a case outside this set raises :class:`~literalizer.exceptions.UnsupportedIdentifierCaseError`.
  Most C-family languages set this to :data:`~literalizer.NON_KEBAB_REF_CASES`, since ``my-var`` is not a legal identifier; Lisp-family languages and other kebab-friendly grammars use :data:`~literalizer.ALL_REF_CASES`.
* :attr:`~literalizer.Language.identifier_cases` -- the cases that are *idiomatic* for the language, ordered by stylistic preference (the first element is the default).
  This list is documentation of style only; it is not used to reject explicit ``ref_case`` choices.
  A language may prefer only ``SNAKE`` while still syntactically supporting ``CAMEL``, ``PASCAL``, and ``UPPER_SNAKE``.

The same YAML source can drive idiomatic identifiers across multiple languages.
For example, the JSON source ``[[{"$ref": "user_obj"}, 42]]`` with ``parameter_names=["data", "count"]`` produces:

With ``ref_key="$ref"`` passed:

* ``ref_case=IdentifierCase.SNAKE`` with ``language=Python()`` → ``process(data=user_obj, count=42)``.
* ``ref_case=IdentifierCase.CAMEL`` with ``language=JavaScript()`` → ``process({ data: userObj, count: 42 });``.
* ``ref_case=IdentifierCase.PASCAL`` with ``language=Go()`` → ``process(UserObj, 42)``.

Composing declarations and calls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pairing a :func:`~literalizer.literalize` call (which declares a variable) with a :func:`~literalizer.literalize_call` call (which references that variable via ``{"$ref": "name"}``) is the natural way to render a complete, self-contained source file: declaration first, call second.

Each call independently computes its own :attr:`~literalizer.LiteralizeResult.preamble` and :attr:`~literalizer.LiteralizeResult.body_preamble` from the data it sees.
When the two halves see overlapping data (for example, both contain integers in a language where integers require a wrapper type declaration), concatenating their outputs as-is produces duplicates.
Strict compilers reject the result (Haskell rejects duplicate ``data`` declarations; D rejects duplicate ``import`` lines) and a linter flags it (``ruff`` and ``pylint`` warn about repeated ``from typing import Any`` lines).

Pass the ref values through the ``bound_refs`` argument of :func:`~literalizer.literalize_call` (with ``wrap_in_file=True``) and it renders the whole file for you: each ref is declared ahead of the calls, a no-op stub for the target function is injected, and one reconciled preamble is placed in front.
This is the call-side counterpart of :func:`~literalizer.literalize`'s own ``bound_refs`` argument; the returned :attr:`~literalizer.LiteralizeResult.code` is the finished file:

.. code-block:: python

   """Render a call that declares its refs into one Haskell file."""

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Haskell

   composed = literalize_call(
       source='[[{"$ref": "my_list"}, 42]]',
       input_format=InputFormat.JSON,
       language=Haskell(),
       target_function="process",
       parameter_names=["value", "count"],
       ref_key="$ref",
       wrap_in_file=True,
       bound_refs={"my_list": [1, 2, 3]},
   )

   assert composed.code.count("data Val = HInt Integer | HList [Val]") == 1

``bound_refs`` entries double as ``ref_values``, so a name need not be repeated in both mappings, and they are emitted in iteration order ahead of their first use.

When you already have separate :class:`~literalizer.LiteralizeResult` objects, or need to add custom target or transform scaffolding, pass the declaration results and call result to :func:`~literalizer.literalize_call_with_declarations`.
It exposes the same preamble reconciliation and file assembly used by ``bound_refs``.
Prefer ``bound_refs`` for the ordinary case where Literalizer can declare every reference itself.

Snake case is the recommended authoring convention for ``$ref`` names: ``pyhumps`` converts ``snake_case`` to every other case without loss.
Inputs in other conventions are normalized to ``snake_case`` first, so ``userObj`` or ``UserObj`` also convert correctly, but at the cost of losing any preserved acronyms: ``HTTPRequest`` normalizes to ``http_request`` and converts back to Pascal case as ``HttpRequest``.

References inside plain data structures
----------------------------------------

``{"$ref": "name"}`` markers also work inside data passed to :func:`~literalizer.literalize` -- not just inside call arguments.
This is useful when you want to emit a data structure where some values are references to variables declared elsewhere rather than inline literals.

By default, ref identifiers are emitted verbatim.
Pass ``ref_case`` to :func:`~literalizer.literalize` when the identifier should be converted before rendering.

For example, suppose you have a configuration dict where ``timeout`` and ``host`` are already declared as named constants and you want to reference them rather than repeat the values:

.. code-block:: python

   """Emit a config dict with variable references as values."""

   from literalizer import IdentifierCase, InputFormat, literalize
   from literalizer.languages import Python

   config_json = (
       '{"timeout": {"$ref": "timeout_secs"}, "host": {"$ref": "default_host"}}'
   )

   result = literalize(
       source=config_json,
       input_format=InputFormat.JSON,
       language=Python(),
       ref_key="$ref",
       ref_case=IdentifierCase.SNAKE,
   )
   assert result.bare_code == (
       '{\n    "timeout": timeout_secs,\n    "host": default_host,\n}'
   )

The same ``ref_case`` rules apply as for :func:`~literalizer.literalize_call`: the identifier is case-converted to the requested convention and any language-specific sigil is applied (e.g. ``$timeout_secs`` in PHP).
Refs can appear at any depth -- nested inside dicts, inside lists, or as the top-level value -- and can be mixed freely with ordinary literals in the same structure.

Pairing each call with a value
------------------------------

``call_transform`` receives a :class:`~literalizer.CallContext`, not just the call string.
Alongside ``ctx.call`` (the rendered call expression) it carries the call's zero-based ``ctx.index``, its input ``ctx.row``, and -- when ``zip_source`` is supplied -- ``ctx.zipped``: the matching top-level element of a second, equal-length companion source, parsed with the same parser as ``source`` and rendered as a language-native literal.
This lets you print an expected value beside each call's actual return value:

.. code-block:: python

   """Pair each generated call with a value from a parallel sequence."""

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Python

   books_yaml = """\
   ---
   - [Dune, 1965]
   - [Solaris, 1961]
   """

   in_print_yaml = """\
   ---
   - true
   - false
   """

   result = literalize_call(
       source=books_yaml,
       input_format=InputFormat.YAML,
       language=Python(),
       target_function="catalog.lookup",
       parameter_names=["title", "year"],
       zip_source=in_print_yaml,
       zip_input_format=InputFormat.YAML,
       call_transform=lambda ctx: (
           f'print("in_print?", {ctx.zipped}, "->", {ctx.call})'
       ),
   )

   assert result.code == (
       'print("in_print?", True, "->", '
       'catalog.lookup(title="Dune", year=1965))\n'
       'print("in_print?", False, "->", '
       'catalog.lookup(title="Solaris", year=1961))'
   )

``zip_source`` is parsed with the same parser as ``source``; when ``per_element`` is ``True`` it must parse to a list whose top-level elements pair one-for-one with the generated calls.
It requires ``zip_input_format`` and a ``call_transform``.
``call_transform`` is only supported for languages whose call form is an expression that can be wrapped (positional, keyword, or object call style); prefix-, postfix-, and command-style languages reject it with :class:`~literalizer.exceptions.UnsupportedCallShapeError`.

Annotating each call with a trailing comment
--------------------------------------------

A ``call_transform`` only sees the *call expression*, before the language's statement terminator is applied, so it cannot append a trailing line comment: in C-family languages the terminator would land *inside* the comment (``catalog.lookup("Dune", 1965)  // first edition;``) and the statement would no longer compile.
``comment_source`` solves this by handing the core a sequence of comments -- one per generated call, paired positionally -- which it emits **after** the statement terminator using the target language's comment syntax:

.. code-block:: python

   """Attach a per-row trailing comment to each generated call."""

   from literalizer import InputFormat, literalize_call
   from literalizer.languages import Java

   books_yaml = """\
   ---
   - [Dune, 1965]
   - [Solaris, 1961]
   """

   result = literalize_call(
       source=books_yaml,
       input_format=InputFormat.YAML,
       language=Java(),
       target_function="catalog.lookup",
       parameter_names=["title", "year"],
       comment_source=["first edition", "translated from Polish"],
   )

   assert result.code == (
       'catalog.lookup("Dune", 1965);  // first edition\n'
       'catalog.lookup("Solaris", 1961);  // translated from Polish'
   )

``comment_source`` is a plain sequence, not a parsed source, so it needs neither a ``call_transform`` nor an input format.
Its length must equal the number of generated calls (one per top-level element when ``per_element`` is ``True``, otherwise one) or :class:`~literalizer.exceptions.CommentSourceLengthMismatchError` is raised; an empty entry emits no comment, and an entry containing a newline raises :class:`~literalizer.exceptions.CommentSourceMultilineError`.
Languages with no line comment fall back to that language's block-comment form (``catalog.lookup("Dune", 1965)  (* first edition *)`` in OCaml), which is valid on a single line.

A trailing comment is only safe where each generated call is a self-contained line.
Languages that assemble the call sequence into a single clause, list or expression -- so a separator, terminator or closer would follow the call on the same line and the line comment would swallow it (Erlang's clause-terminating ``.``, a Jsonnet list ``,``, a Roc ``dbg ( ... )`` wrapper) -- reject a non-empty ``comment_source`` with :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
The supported set is exactly the languages whose :attr:`~literalizer.Language.supports_standalone_comments_in_wrapped_calls` is ``True``.

Typed native invocations
------------------------

``literalize_call`` retains its existing string-target calling conventions.
Use :func:`~literalizer.literalize_native_call` when a call needs a native receiver, selector, constructor, or explicit scalar/object signature.
The first backend declaring ``supports_native_invocations`` is Objective-C.
Unsupported backends raise :class:`~literalizer.exceptions.NativeCallError` rather than approximating the requested syntax.

A native expression uses :class:`~literalizer.FunctionTarget`, :class:`~literalizer.MessageTarget`, or :class:`~literalizer.ConstructorTarget`.
For message receivers, use a typed :class:`~literalizer.NativeReference`, a :class:`~literalizer.NativeClass`, a literal, or a nested invocation.
Selectors include all colons: ``accept:timestamp:`` has exactly two arguments, while ``reset`` has none.
The receiver name is emitted unchanged; no synthetic global or function-pointer struct is introduced.

.. code-block:: python

   """Render a typed native notification method call."""

   from literalizer import (
       MessageTarget,
       NativeInvocation,
       NativeLiteral,
       NativeReference,
       ObjectType,
       ScalarType,
       literalize_native_call,
   )
   from literalizer.languages import ObjectiveC

   invocation = NativeInvocation(
       target=MessageTarget(
           receiver=NativeReference(
               name="throttler", type=ObjectType(name="NotificationThrottler")
           ),
           selector="shouldSendNotification:notificationTimestamp:",
           parameter_types=(ObjectType(name="NSString"), ScalarType.FLOAT),
           return_type=ScalarType.BOOL,
       ),
       arguments=(NativeLiteral(value="user_1"), NativeLiteral(value=100.0)),
   )
   result = literalize_native_call(language=ObjectiveC(), invocation=invocation)
   print(result.code)

The expression is rendered as:

.. code-block:: objective-c

   [throttler shouldSendNotification:@"user_1" notificationTimestamp:100.0];

The timestamp is a scalar ``double`` because the signature requests ``ScalarType.FLOAT``.
An object parameter such as ``ObjectType(name="NSNumber")`` instead boxes the literal.
The other scalar roles are ``BOOL``, ``INTEGER``, ``UNSIGNED``, and ``VOID``; Objective-C spells these as ``BOOL``, ``NSInteger``, ``NSUInteger``, and ``void``.
``ObjectType`` can describe generic collections, for example ``ObjectType(name="NSArray", arguments=(ObjectType(name="NSString"),))``.
Literal element types are checked against the requested generic arguments.
Null data is ``NSNull``, not a nil object reference.

A ``ConstructorTarget(class_name="NotificationThrottler")`` produces ``[[NotificationThrottler alloc] init]``.
Use its ``selector`` and ``parameter_types`` for an initializer with arguments.
``NewVariable`` emits a declaration using the declared result type; ``ExistingVariable`` emits one assignment and invokes the target once.
Binding a void result or supplying unrelated declaration modifiers is rejected.
A ``NativeInvocation`` can be an argument of another invocation, allowing typed result checks without source-string interpolation.

The caller supplies the actual class/function declarations and places the returned executable fragment in the appropriate function scope.
Preamble and executable-placement metadata support composition with :func:`~literalizer.literalize_call_with_declarations`; external declarations remain caller-owned.

Declarative invocation recipes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`~literalizer.literalize_native_calls` applies a recipe to source rows parsed by the same input parsers as the existing rendering APIs.
The recipe is a mapping, independent of the data being rendered.
For example:

.. code-block:: json

   {
     "function": "checkTestCase",
     "parameter-types": ["bool", "NSArray"],
     "return-type": "void",
     "arguments": [
       {
         "receiver": {"reference": "throttler", "type": "NotificationThrottler"},
         "selector": "shouldSendNotification:notificationTimestamp:",
         "parameter-types": ["NSString", "float"],
         "return-type": "bool",
         "arguments": [{"input": 0}, {"input": 1}]
       },
       {"zipped": true}
     ]
   }

``input`` selects an argument by its zero-based index in the current source row.
``zipped`` selects the matching companion value supplied through ``zip_source`` and ``zip_input_format``.
``literal`` embeds a data value, and ``reference`` with ``type`` names an existing value.
A receiver of ``{"class": "Counter"}`` sends a class message; ``{"constructor": "Counter"}`` allocates and initializes an instance.
Object type names are strings, while scalar roles use ``bool``, ``integer``, ``unsigned``, ``float``, or ``void``.
Generic types use ``{"object": "NSArray", "arguments": ["NSString"]}``.

Unknown fields, invalid selectors, out-of-range input indexes, incompatible types, and mismatched companion lengths raise located native-call errors.
Native recipes select data values; source comments are not interpolated into expressions.
Keep explanatory prose in the surrounding document or in explicit expected-result data.

Printing call results
---------------------

Use ``literalize_call(..., print_result=True)`` to print each result through its language's native printing operation.
Required imports are returned in ``result.preamble`` and participate in normal preamble composition.
For example, C++14 emits ``std::cout << calculate(1) << std::endl;`` with ``#include <iostream>`` in the preamble; Go emits ``fmt.Println(calculate(1))`` with ``import "fmt"``.
These dependencies are omitted for empty call sequences to avoid unused imports in languages such as Go.

Supported languages are Python, Java, C++, C#, Go, JavaScript, TypeScript, Kotlin, Ruby, Scala, and Rust.
Each operation writes a newline and uses native formatting; Rust uses debug formatting.
Because argument data provides no return-type information, callers must supply a function whose result supports native printing (such as C++ stream insertion), with custom transforms providing any extra serialization behavior.
Boolean, numeric, and collection representations can differ between languages.

Printing cannot be combined with ``call_transform``, ``variable_form``, or ``zip_source``.
Keep a custom transform for application-specific formatting; its dependencies remain the caller's responsibility.
Printing works with ``wrap_in_file`` and with separately composed declarations.
