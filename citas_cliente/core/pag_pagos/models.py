"""
Pagos Pagos, modelos
"""
from collections import OrderedDict
from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class PagPago(Base, UniversalMixin):
    """PagPago"""

    ESTADOS = OrderedDict(
        [
            ("SOLICITADO", "Solicitado"),  # Cuando se crea el pago en espera de que el banco lo procese
            ("CANCELADO", "Cancelado"),  # Cuando pasa mucho tiempo y no hay respuesta del banco, se cancela
            ("PAGADO", "Pagado"),  # Cuando el banco procesa el pago con exito
            ("FALLIDO", "Fallido"),  # Cuando el banco reporta que falla el pago
            ("ENTREGADO", "Entregado"),  # Cuando el usuario entrega el trámite o servicio
        ]
    )

    # Nombre de la tabla
    __tablename__ = "pag_pagos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="pag_pagos")
    cit_cliente_id = Column(Integer, ForeignKey("cit_clientes.id"), index=True, nullable=False)
    cit_cliente = relationship("CitCliente", back_populates="pag_pagos")
    pag_tramite_servicio_id = Column(Integer, ForeignKey("pag_tramites_servicios.id"), index=True, nullable=False)
    pag_tramite_servicio = relationship("PagTramiteServicio", back_populates="pag_pagos")

    # Columnas
    caducidad = Column(Date, nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    descripcion = Column(String(256), nullable=False, default="")
    email = Column(String(256), nullable=False, default="")  # Email opcional si el cliente desea que se le envie el comprobante a otra dirección
    estado = Column(Enum(*ESTADOS, name="estados", native_enum=False), nullable=False)
    folio = Column(String(256), nullable=False, default="")
    resultado_tiempo = Column(DateTime, nullable=True)
    resultado_xml = Column(Text, nullable=True)
    total = Column(Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=False)
    ya_se_envio_comprobante = Column(Boolean, nullable=False, default=False)

    @property
    def autoridad_clave(self):
        """Autoridad clave"""
        return self.autoridad.clave

    @property
    def autoridad_descripcion(self):
        """Autoridad descripción"""
        return self.autoridad.descripcion

    @property
    def autoridad_descripcion_corta(self):
        """Autoridad descripción corta"""
        return self.autoridad.descripcion_corta

    @property
    def cit_cliente_nombre(self):
        """Nombre del cliente"""
        return self.cit_cliente.nombre

    @property
    def distrito_nombre(self):
        """Nombre del distrito"""
        return self.autoridad.distrito.nombre

    @property
    def pag_tramite_servicio_clave(self):
        """Clave"""
        return self.pag_tramite_servicio.clave

    @property
    def pag_tramite_servicio_descripcion(self):
        """Descripción"""
        return self.pag_tramite_servicio.descripcion

    def __repr__(self):
        """Representación"""
        return f"<PagPago {self.descripcion}>"
