# Sistema Logístico FASABI - Módulo de Inventarios (PUCE TEC)
## Documentación Técnica y Manual de Usuario

---

## 1. Documentación Técnica

El **Sistema Logístico FASABI** es una plataforma web desarrollada en Python con el framework Django para la gestión integral de activos fijos, insumos, inventario físico por bodegas, flujos de compras y auditoría de transacciones logísticas.

### 1.1 Arquitectura y Tecnologías
- **Backend:** Python 3.12, Django 6.0.
- **Base de Datos:** PostgreSQL en producción, SQLite 3 como base de datos de respaldo y desarrollo rápido.
- **Frontend:** HTML5, CSS3, Bootstrap 5.3, Bootstrap Icons y FontAwesome 6 para íconos interactivos.
- **Generación de Reportes:** ReportLab para la exportación directa y en tiempo real de reportes de stock y de activos a formato PDF.

### 1.2 Modelos de Datos Clave
1. **Usuario (`Usuario`):** Extiende el modelo base de Django agregando el `rol` de usuario (Administrador, Técnico, Conserje, Laboratorio) y el teléfono de contacto.
2. **Carrera (`Carrera`) & Centro de Costo (`CentroCosto`):** Relacionan de manera lógica las áreas administrativas, carreras académicas y centros de costo responsables del gasto e inventario.
3. **Bodega (`Bodega`):** Almacenes físicos de inventario parametrizados por tipo (Vigentes, Uso Diario, Caducados, Limpieza).
4. **Insumo (`Insumo`):** Catálogo maestro de suministros (pipetas, reactivos, materiales) clasificados por `CategoriaInsumo` y con indicador de perecedero (`es_perecedero`).
5. **Stock por Bodega (`StockInsumo`):** Relación de muchos a muchos que mapea la cantidad actual de un insumo, su cantidad mínima de alerta, número de lote y fecha de caducidad en una bodega específica.
6. **Movimiento de Insumo (`MovimientoInsumo`):** Historial transaccional inmutable para registrar ingresos (entradas) o egresos (salidas) de suministros en una bodega.
7. **Solicitud de Insumos (`Solicitud`):** Flujo de requisición de suministros por parte de una `Persona` ligada a una `Carrera` y `CentroCosto`. Mantiene estados en tiempo real (Pendiente, Aprobada, Rechazada, Comprada, Recibida).
8. **Detalle de Solicitud (`DetalleSolicitud`):** Tabla relacional intermedia que detalla qué insumos y qué cantidad han sido solicitados.
9. **Compra (`Compra`):** Registro de transacciones financieras de adquisición de insumos, asociada opcionalmente a una solicitud de insumos de origen.

### 1.3 Automatizaciones e Integridad Referencial
- **Ajustes de Stock Automáticos:** Al guardar un `MovimientoInsumo`, se dispara automáticamente una actualización sobre la tabla `StockInsumo` correspondiente, sumando o restando el saldo según el tipo de movimiento (`INGRESO`/`EGRESO`).
- **Validación de Stock Mínimo en Salidas:** El formulario `MovimientoInsumoForm` valida a nivel de negocio que una bodega disponga de suficiente stock antes de permitir registrar un egreso, evitando saldos negativos de inventario.
- **Recepción de Mercadería Automatizada:** Al marcar una compra como "Recibida" (`compra_recibir`), el sistema recorre de forma automática todos los artículos de la solicitud de origen y registra movimientos de ingreso en la bodega destino seleccionada, actualizando las existencias en un solo clic.

### 1.4 Instrucciones de Ejecución Local y Pruebas
1. **Activar base de datos SQLite (Desarrollo):**
   Definir la variable de entorno `USE_SQLITE=1` para usar la base de datos local rápida:
   ```bash
   export USE_SQLITE=1
   ```
2. **Ejecutar migraciones de base de datos:**
   ```bash
   python manage.py migrate
   ```
3. **Ejecutar el conjunto de pruebas unitarias e integrales:**
   ```bash
   python manage.py test
   ```

---

## 2. Manual de Usuario

El Sistema FASABI unifica toda la experiencia de usuario bajo una interfaz web moderna, limpia y de navegación fluida.

### 2.1 Módulo de Insumos y Categorías
- **Visualización:** Acceda a **Insumos -> Ver Insumos** para ver la lista completa de insumos, su código, categoría, unidad de medida, estado de vigencia y si es perecedero.
- **Registro de Insumos:** Haga clic en **Nuevo Insumo** en la esquina superior derecha, llene el formulario (Código, Nombre, Categoría, Unidad de Medida, etc.) y guarde.
- **Categorías de Insumos:** Acceda a **Insumos -> Categorías de Insumos** para ver y crear clasificaciones (ej. Reactivos, Vidriería, Equipos de Seguridad).

### 2.2 Gestión de Existencias (Stock por Bodega)
- **Visualización:** Acceda a **Insumos -> Gestión de Stock** para ver la cantidad actual de insumos en cada bodega física, las alertas de stock bajo y las fechas de caducidad.
- **Filtrado:** Use el selector superior "Filtrar por Bodega" para analizar en tiempo real las existencias de un almacén particular.
- **Alertas de Stock Bajo:** Los insumos con existencias por debajo de su stock mínimo se resaltarán automáticamente con una tarjeta roja en la columna "Estado de Stock".
- **Exportación PDF:** Haga clic en **Exportar a PDF** en el módulo de stock para descargar un documento PDF formateado con el inventario completo, donde los ítems con stock crítico aparecen coloreados para facilitar las decisiones de compra rápida.

### 2.3 Registro de Movimientos (Entradas y Salidas)
- **Historial:** Acceda a **Insumos -> Movimientos de Insumos** para auditar el registro cronológico de entradas y salidas del almacén, detallando quién registró el movimiento y bajo qué observación.
- **Registrar Movimiento:** Haga clic en **Registrar Movimiento (Entrada/Salida)**. Seleccione el insumo, la bodega, el tipo de movimiento (`Ingreso` o `Egreso`) y la cantidad.
  - *Nota:* Si intenta registrar un egreso que exceda las existencias actuales de esa bodega, el sistema bloqueará la operación y le indicará un mensaje de error detallado.

### 2.4 Requisición de Insumos (Flujo Completo de Compras)
1. **Creación de Solicitud:** Un usuario autorizado accede a **Insumos -> Solicitudes de Insumos** y hace clic en **Nueva Solicitud**. Selecciona la carrera, centro de costo, la persona solicitante y añade hasta 3 filas de insumos con las cantidades deseadas.
2. **Revisión y Aprobación:** La solicitud se guarda con estado `Pendiente`. Un administrador accede a la solicitud desde la lista y tiene botones directos para **Aprobar Solicitud** (pasa a `Aprobada`) o **Rechazar Solicitud** (pasa a `Rechazada`).
3. **Registro de Compra:** Para las solicitudes aprobadas, aparece el botón **Registrar Compra**. Al hacer clic, se abre el formulario de registro financiero prellenado con la solicitud de origen. Al guardar, el estado de la solicitud cambia automáticamente a `Comprada`.
4. **Recepción e Ingreso de Mercadería:** Cuando los insumos llegan físicamente a la facultad, el bodeguero abre la compra, selecciona la bodega física donde se depositarán y hace clic en **Registrar Ingreso a Bodega**. El sistema cambia los estados a `Recibida` e ingresa automáticamente las existencias al inventario.

### 2.5 Centro de Alertas y Notificaciones (Dashboard)
Al acceder a **Alertas** desde la barra de navegación, visualizará un panel analítico dividido en:
- **Mantenimientos Próximos:** Lista los mantenimientos correctivos o preventivos agendados para los próximos 7 días.
- **Insumos con Stock Bajo:** Lista en tiempo real todos los suministros en estado de escasez.
- **Control de Caducidad:** Tabla de insumos perecederos con fechas de caducidad dentro de los próximos 30 días, destacando lotes de riesgo.
- **Historial de Solicitudes:** Feed con el estado en tiempo real de las últimas 5 requisiciones registradas (Pendiente, Aprobada, Rechazada, Comprada, Recibida).
