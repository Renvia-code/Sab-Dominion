// Query DOM_LOAD_PROFILE (Import)
let
    Source = Csv.Document(File.Contents(DataFolder & "dom_load_profile.csv"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),
    Selected = Table.SelectColumns(UpperNames, {"HOUR_NO", "AVG_MW_2019", "AVG_MW_2025", "GROWTH_PCT"}),
    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),
    Typed = Table.TransformColumnTypes(Blanks, {{"HOUR_NO", type number}, {"AVG_MW_2019", type number}, {"AVG_MW_2025", type number}, {"GROWTH_PCT", type number}}, "en-US")
in
    Typed
