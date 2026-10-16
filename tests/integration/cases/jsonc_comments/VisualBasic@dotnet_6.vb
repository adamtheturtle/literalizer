Imports System.Collections.Generic
Module Check
    ' A JSONC input case with both comment forms.
    ' detail
    ' continued
    ' trailing line comment
    Dim my_data = New Dictionary(Of String, Object) From {
        {"url", "https://example.org/a/*b*/"},
        {"count", 2}
    }
End Module
