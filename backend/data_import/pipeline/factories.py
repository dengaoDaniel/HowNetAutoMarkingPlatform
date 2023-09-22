from .catalog import (
    CSV,
    JSON,
    JSONL,
   
    CoNLL,
    Excel,
    FastText,
    Format,

    TextFile,
    TextLine,
)
from .parsers import (
    CoNLLParser,
    CSVParser,
    ExcelParser,
    FastTextParser,
    JSONLParser,
    JSONParser,
    LineParser,
    PlainParser,
    TextFileParser,
)


def create_parser(file_format: Format, **kwargs):
    mapping = {
        TextFile.name: TextFileParser,
        TextLine.name: LineParser,
        CSV.name: CSVParser,
        JSONL.name: JSONLParser,
        JSON.name: JSONParser,
        FastText.name: FastTextParser,
        Excel.name: ExcelParser,
        CoNLL.name: CoNLLParser,
      
       
    }
    return mapping[file_format.name](**kwargs)
