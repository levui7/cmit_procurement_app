import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from parser.wb_parse import run_wb_parser

print("Тестируем WB парсер...")
result = run_wb_parser("Arduino Nano")
print(f"Результат: {result}")