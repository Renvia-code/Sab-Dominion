// Query Tests (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "test_results.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"TEST", "TEST_NO", "SQL_FILE", "DESCRIPTION", "EXPECTED", "ROWS_RETURNED", "OBSERVED_VALUE", "STATUS"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"TEST", type text}, {"TEST_NO", Int64.Type}, {"SQL_FILE", type text}, {"DESCRIPTION", type text}, {"EXPECTED", type text}, {"ROWS_RETURNED", Int64.Type}, {"OBSERVED_VALUE", type text}, {"STATUS", type text}}, "en-US")
in
    Typed
