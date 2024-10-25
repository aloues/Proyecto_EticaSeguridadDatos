# Proyecto de Ética y Seguridad de Datos

**Autor:** Aleksander Fabrizio Paico Reyna

## Contexto

En un entorno financiero global cada vez más interconectado, la protección de datos personales y financieros es primordial para mantener la integridad y la confianza en el sistema financiero. Este proyecto se centra en implementar y demostrar prácticas robustas de seguridad de datos para proteger la información personal y transaccional de los clientes de un banco internacional.

## Introducción

Este proyecto combina un dataset de información personal con registros de transacciones bancarias para crear un entorno de prueba realista donde se pueden aplicar y evaluar estrategias de seguridad de datos avanzadas. El objetivo es demostrar la efectividad de estas estrategias en la protección contra accesos no autorizados, brechas de datos y otros riesgos de seguridad.

## Descripción del Dataset

El dataset utilizado en este proyecto incluye datos críticos como:
- Nombre
- Apellido
- Correo electrónico
- Teléfono
- Estado Civil
- TransactionID
- CustomerID
- Fecha de Nacimiento
- Género
- Ubicación del Cliente
- Saldo de la Cuenta
- Fecha y Hora de la Transacción
- Monto de la Transacción (en INR)

Estos datos se utilizan para implementar y demostrar técnicas de protección de datos, tales como encriptación, hashing y gestión de accesos.

## Beneficios del Proyecto

Este proyecto ofrece múltiples beneficios:
- **Cumplimiento Regulatorio:** Asegura el cumplimiento con leyes de protección de datos nacionales e internacionales, como la Ley Peruana de Protección de Datos y el GDPR.
- **Protección contra Brechas de Datos:** Implementa tecnologías avanzadas y mejores prácticas para reducir significativamente el riesgo de brechas de datos.
- **Confianza del Cliente:** Mejora la percepción del cliente sobre la seguridad de sus datos, fortaleciendo la relación cliente-banco.

## Requerimientos y Estrategias del Proyecto

### Generación de Valor al Caso de Negocio

El proyecto utiliza KPIs y OKRs para cuantificar el valor generado a través de la implementación de prácticas de seguridad de datos:
- **Índice de Incidentes de Seguridad:** Este KPI mide la frecuencia de incidentes de seguridad antes y después de la implementación del proyecto.
- **Reducción de Brechas de Datos:** Este OKR tiene como objetivo reducir las brechas de datos de ahora en adelante sea un 10 o 20% más seguro.
- **Mejora en la Satisfacción del Cliente en Seguridad de Datos:** A través de encuestas, se busca aumentar la satisfacción y seguridad mental del cliente respecto a la seguridad de sus datos en un 30%.

### Protección de Datos Conforme a Estándares Internacionales y Locales

Para garantizar la protección adecuada de los datos, el banco se adhiere a:

- **Normativas Internacionales como el GDPR:** Implementación de principios de minimización de datos, consentimiento del usuario y derecho al olvido.
- **Ley Peruana de Protección de Datos y Otras Normativas Locales:** Adecuación a las leyes locales en cada jurisdicción donde opera el banco, asegurando la implementación de medidas de seguridad necesarias como auditorías regulares y evaluaciones de impacto sobre la protección de datos.

### Planes de Contingencia y Recuperación

Entendiendo que ningún sistema es infalible, el banco deberia establecer robustos mecanismos de contingencia y recuperación:

- **Backups Automatizados y Encriptados:** Realización de backups de todos los datos críticos de forma diaria a múltiples ubicaciones seguras y encriptadas si es que la entidad dispone de otras sucursales para poder tener bajo control ese backup y el traslado de informacion que sea tambien seguro. (Data en tránsito=)

- **Plan de Recuperación Ante Desastres:** Un plan detallado que considero que deberia enfocarse en procedimientos de recuperación rápida para asegurar la continuidad del negocio en caso de desastres naturales o ataques cibernéticos y procedimientos que ya esten con protocolos para efectuar inmediatamente ante el desastre.

### Implementación de la Seguridad de Datos

#### Estructura General

data_security_operations.py:

- Contendrá las funciones de encriptación y desencriptación.
- Funciones para registrar accesos (auditoría).
- Incluirá las operaciones de seguridad solicitadas para manejar los datos sensibles de tu dataset.

app.py:

- Usará Tkinter para cargar el archivo CSV y mostrar los datos.
- Permitirá aplicar las funciones de encriptación/desencriptación sobre el campo Correo y registrar las operaciones.

#### Encriptación y Desencriptación

```python
def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ":" + ct

def decrypt(encrypted_data, key):
    iv, ct = encrypted_data.split(':')
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()
```
Estas funciones utilizan AES-256 CBC para encriptar y desencriptar datos sensibles como correos electrónicos y detalles de transacciones. El uso de un vector de inicialización (IV) y el cifrado de bloque aseguran que cada instancia de datos cifrados sea única.

#### Hashing de Contraseñas

```python
def hash_data(data):
    return sha256(data.encode()).hexdigest()

def log_access(operation, data_type):
    logging.info(f"Operation: {operation}, Data Type: {data_type}")
```

El hashing se utiliza para asegurar la integridad de los datos, mientras que las funciones de registro permiten un seguimiento detallado de todas las operaciones de seguridad para auditorías.

Proporciona una forma segura de almacenar contraseñas y otros datos sensibles, utilizando SHA-256 para generar un resumen que no puede revertirse, protegiendo contra el acceso no autorizado.

#### Registro de Accesos (Logging)

```python
def log_access(operation, data_type):
    logging.info(f"Operation: {operation}, Data Type: {data_type}")

```
Facilita el monitoreo y la auditoría de las acciones de seguridad, permitiendo una rápida detección y respuesta ante actividades sospechosas o maliciosas.

## Estrategias de Uso Seguro de los Datos

### Políticas y Procedimientos
- **Política de Gestión de Datos:** Todos los empleados deben seguir una política estricta que define cómo se deben manejar y proteger los datos sensibles. Esto incluye el cifrado de datos sensibles, el acceso controlado y la retención segura de la información.
- **Procedimientos de Auditoría:** Implementación de procedimientos regulares de auditoría para revisar y asegurar la integridad y seguridad de los datos.

### Concientización y Formación del Equipo
- **Programas de Concientización:** Desarrollar y mantener un programa de concientización sobre seguridad que eduque a todos los empleados sobre los riesgos de seguridad de datos y las mejores prácticas para mitigar estos riesgos.
- **Capacitaciones Regulares:** Sesiones de formación obligatorias para el personal sobre las políticas de seguridad, cómo manejar incidentes de seguridad y la importancia de proteger la información del cliente.

## Plan de Respuesta ante Incidentes de Seguridad

- **Equipo de Respuesta a Incidentes:** Creación de un equipo de respuesta a incidentes que esté preparado para actuar de manera rápida y efectiva en caso de una fuga o pérdida de datos.
- **Protocolos de Respuesta:** Establecimiento de protocolos claros que incluyan la identificación del incidente, contención de la fuga, evaluación del impacto, comunicación con los afectados y remedios para evitar futuras incidencias.
- **Simulacros de Seguridad:** Realización de simulacros de seguridad para asegurar que el equipo está preparado y que los protocolos de respuesta son efectivos.

## Recomendaciones de Protección de Datos Futura

- **Adopción de Tecnología Avanzada:** Investigar y adoptar tecnologías avanzadas de protección de datos como la encriptación homomórfica, que permite realizar cálculos sobre datos cifrados sin necesidad de descifrarlos, ofreciendo una capa adicional de protección.

- **Inteligencia Artificial en Seguridad:** Explorar el uso de soluciones de inteligencia artificial para mejorar la detección de amenazas y respuestas automáticas a incidentes de seguridad.

- **Blockchain para Integridad de Datos:** Evaluar la implementación de tecnología blockchain para mejorar la integridad y trazabilidad de los datos sensibles, lo cual puede ser especialmente útil en ambientes donde la manipulación de datos es un riesgo crítico.

Estas estrategias y recomendaciones están diseñadas para asegurar que la organización no solo cumpla con las regulaciones actuales de protección de datos, sino que también esté preparada para enfrentar los desafíos futuros en lo que se refiere a la seguridad y ética en el uso, almacenamiento y tratamiento de los datos.

### Conclusión

Este proyecto subraya la importancia de una gestión rigurosa y ética de la seguridad de los datos en el sector financiero. A continuación se destacan los principales logros y compromisos del proyecto:

- **Tecnología Avanzada:** Implementación de encriptación AES-256 y uso de TLS 1.3 para asegurar la protección de los datos tanto en reposo como en tránsito.
- **Cumplimiento Regulatorio:** Adherencia a normativas internacionales y locales, asegurando que todas las operaciones cumplen con estándares como el GDPR y la Ley Peruana de Protección de Datos.
- **Reducción de Riesgos:** Disminución significativa en la frecuencia y gravedad de las brechas de datos, gracias a las tecnologías de seguridad avanzadas y las prácticas de gestión de riesgos.
- **Confianza del Cliente:** Mejora de la percepción de seguridad entre los clientes, lo que refuerza la confianza y la relación a largo plazo con el banco.
- **Educación y Concientización:** Programas continuos de formación y concientización para el personal, fomentando una cultura de seguridad de datos sólida y consciente.
- **Preparación para el Futuro:** Investigación y adopción proactiva de nuevas tecnologías como la encriptación homomórfica y soluciones de inteligencia artificial, preparando al banco para enfrentar desafíos futuros en seguridad de datos.