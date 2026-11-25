Imports System.Collections.Generic
Module Check
    ' About the first dotted key.
    ' About the second dotted key.
    ' About the plain key.
    ' Before the first entry.
    ' Before the second entry.
    ' Inside the table.
    Dim my_data = New Dictionary(Of String, Object) From {
        {"dotted", New Dictionary(Of String, Object) From {{"first", 1}, {"second", 2}}},
        {"plain", 3},
        {"entries", New Object() {New Dictionary(Of String, Object) From {{"name", "one"}}, New Dictionary(Of String, Object) From {{"name", "two"}}}},
        {"table", New Dictionary(Of String, Object) From {{"inner", 4}}}
    }
End Module
