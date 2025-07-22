"""
Sistema de Reportes de Vehículos — Principios SOLID
Genera PDF real con ReportLab cuando se ejecuta.

Requiere: pip install reportlab
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ───────── 1.  Vehículos ──────────────────────────────────────
class Vehicle(ABC):
    def __init__(self, brand: str, model: str) -> None:
        self.brand = brand
        self.model = model

    @abstractmethod
    def specs(self) -> Dict[str, str | int | float]:
        ...

class Car(Vehicle):
    def __init__(self, brand, model, seats, fuel_eff):
        super().__init__(brand, model)
        self.seats = seats
        self.fuel_eff = fuel_eff

    def specs(self):
        return {"Tipo": "Auto", "Marca": self.brand, "Modelo": self.model,
                "Asientos": self.seats, "Rendimiento (km/l)": self.fuel_eff}

class Truck(Vehicle):
    def __init__(self, brand, model, max_load_tons):
        super().__init__(brand, model)
        self.max_load_tons = max_load_tons

    def specs(self):
        return {"Tipo": "Camión", "Marca": self.brand, "Modelo": self.model,
                "Carga máx. (t)": self.max_load_tons}

class Motorbike(Vehicle):
    def __init__(self, brand, model, cc):
        super().__init__(brand, model)
        self.cc = cc

    def specs(self):
        return {"Tipo": "Moto", "Marca": self.brand, "Modelo": self.model,
                "Cilindrada (cc)": self.cc}

# ───────── 2.  Interfaz de reporte ────────────────────────────
class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, specs: Dict[str, str | int | float]) -> None: ...

# ───────── 3.  Implementaciones de reporte ────────────────────
class ConsoleReport(ReportGenerator):
    def generate(self, specs):
        print("=== REPORTE – CONSOLA ===")
        for k, v in specs.items():
            print(f"{k:25}: {v}")
        print()

class TextFileReport(ReportGenerator):
    def __init__(self, path="reporte_auto.txt"): self.path = path
    def generate(self, specs):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("=== REPORTE – TEXTO ===\n")
            for k, v in specs.items():
                f.write(f"{k:25}: {v}\n")
        print(f"[TXT] Guardado en {self.path}\n")

class RealPDFReport(ReportGenerator):
    """Genera un PDF real usando ReportLab."""
    def __init__(self, path="reporte_vehiculo.pdf"):
        self.path = path

    def generate(self, specs):
        c = canvas.Canvas(self.path, pagesize=A4)
        width, height = A4
        y = height - 40
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "REPORTE DE VEHÍCULO")
        y -= 30
        c.setFont("Helvetica", 12)
        for k, v in specs.items():
            c.drawString(60, y, f"{k}: {v}")
            y -= 20
        c.save()
        print(f"[PDF] Generado: {self.path}\n")

# ───────── 4.  Servicio (inyección de dependencias) ───────────
class ReportService:
    def __init__(self, generator: ReportGenerator):
        self.gen = generator
    def create_report(self, vehicle: Vehicle):
        self.gen.generate(vehicle.specs())

# ───────── 5.  Demo rápida ────────────────────────────────────
def main():
    fleet = [
        Car("Toyota", "Corolla", 5, 16.5),
        Truck("Volvo", "FH16", 25),
        Motorbike("Honda", "CBR500R", 471),
    ]

    # Tres formatos obligatorios
    ReportService(ConsoleReport()).create_report(fleet[0])
    ReportService(TextFileReport()).create_report(fleet[1])
    ReportService(RealPDFReport()).create_report(fleet[2])

if __name__ == "__main__":
    main()
