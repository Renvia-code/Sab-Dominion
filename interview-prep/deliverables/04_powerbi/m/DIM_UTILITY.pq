// Query DIM_UTILITY (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "dim_utility.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"UTILITY_ID", "STATE", "UTILITY_KEY", "UTILITY_NAME", "ENTITY_TYPE", "PEER_GROUP"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"UTILITY_ID", type number}, {"STATE", type text}, {"UTILITY_KEY", type text}, {"UTILITY_NAME", type text}, {"ENTITY_TYPE", type text}, {"PEER_GROUP", type text}}, "en-US")
in
    Typed
