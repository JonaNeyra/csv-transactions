from dataclasses import dataclass
from datetime import datetime


@dataclass
class CsvRow:
    id: int
    date: datetime
    transaction: float
