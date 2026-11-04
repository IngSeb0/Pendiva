"""Import and explain simple sales and expense exports."""
from __future__ import annotations

import csv
from datetime import datetime
from io import StringIO


class FinanceError(ValueError):
    pass


def parse_records(content: str) -> list[dict]:
    if not isinstance(content, str) or len(content.encode("utf-8")) > 2_000_000:
        raise FinanceError("El archivo financiero supera el límite de 2 MB.")
    reader = csv.DictReader(StringIO(content))
    if not reader.fieldnames:
        raise FinanceError("El archivo debe ser CSV exportado desde Excel.")
    aliases = {"date": "fecha", "type": "tipo", "amount": "monto", "category": "categoria"}
    fields = {aliases.get(field.strip().lower(), field.strip().lower()) for field in reader.fieldnames if field}
    required = {"fecha", "tipo", "monto"}
    if not required <= fields:
        raise FinanceError("El CSV debe tener columnas fecha, tipo y monto.")
    records = []
    for row_number, raw in enumerate(reader, 2):
        normalized = {aliases.get(str(key).strip().lower(), str(key).strip().lower()): (value or "").strip()
                      for key, value in raw.items() if key}
        kind = normalized.get("tipo", "").lower()
        kind = {"sale": "venta", "expense": "gasto"}.get(kind, kind)
        if kind not in {"venta", "gasto"}:
            raise FinanceError(f"Fila {row_number}: tipo debe ser venta o gasto.")
        try:
            date = datetime.strptime(normalized["fecha"], "%Y-%m-%d").date().isoformat()
            amount = float(normalized["monto"].replace(",", ""))
        except (ValueError, KeyError):
            raise FinanceError(f"Fila {row_number}: fecha YYYY-MM-DD y monto numérico requeridos.") from None
        if amount < 0:
            raise FinanceError(f"Fila {row_number}: el monto no puede ser negativo.")
        records.append({"date": date, "kind": kind, "amount": amount,
                        "category": normalized.get("categoria", "")[:120]})
    if not records:
        raise FinanceError("El CSV no contiene registros.")
    return records
