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

## Objetivos y Beneficios del Proyecto
### Objetivos
- **Proteger Datos Sensibles:** Implementar medidas para proteger los datos personales y financieros.
- **Cumplimiento Regulatorio:** Asegurar que las prácticas cumplen con regulaciones locales e internacionales de privacidad y protección de datos.
- **Demostrar Buenas Prácticas:** Mostrar ejemplos de prácticas efectivas de seguridad de datos que se pueden aplicar en el sector bancario.

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

### Protección de Datos Conforme a Normativas

Para garantizar la protección adecuada de los datos la implementación de seguridad se adhiere a:

- **Normativas Internacionales como el GDPR:** Implementación de principios de minimización de datos, consentimiento del usuario y derecho al olvido.
- **Ley Peruana de Protección de Datos y Otras Normativas Locales:** Adecuación a las leyes locales en cada jurisdicción donde opera el banco, asegurando la implementación de medidas de seguridad necesarias como auditorías regulares y evaluaciones de impacto sobre la protección de datos.

### Planes de Contingencia y Recuperación

Entendiendo que ningún sistema es infalible, el banco deberia establecer robustos mecanismos de contingencia y recuperación:

- **Backups Automatizados y Encriptados:** No ha sido directamente implementado pero sería bueno contar con backups de todos los datos críticos de forma diaria a múltiples ubicaciones seguras y encriptadas si es que la entidad dispone de otras sucursales para poder tener bajo control ese backup y el traslado de informacion que sea tambien seguro. (Data en tránsito)

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
```
La función encrypt toma los datos en texto plano y los encripta usando una clave (key). La salida incluye tanto el vector de inicialización como el texto encriptado, separados por ":".

#### Hashing de Contraseñas

```python
from hashlib import sha256

def hash_data(data):
    return sha256(data.encode()).hexdigest()
```
El hashing se utiliza para asegurar la integridad de los datos, mientras que las funciones de registro permiten un seguimiento detallado de todas las operaciones de seguridad para auditorías.

Proporciona una forma segura de almacenar contraseñas y otros datos sensibles, utilizando SHA-256 para generar un resumen que no puede revertirse, protegiendo contra el acceso no autorizado.

#### Autenticación de Dos Factores (2FA)
Se simula el envío de un código de autenticación de dos factores al correo electrónico del usuario. Este código de seis dígitos se genera aleatoriamente y se muestra en la consola (en un sistema real, se enviaría por correo o SMS).

```python
import random

def send_2fa_code(email):
    code = str(random.randint(100000, 999999))  # Código de 6 dígitos
    print(f"Código 2FA enviado a {email}: {code}")
    return code

```

#### Registro de Accesos (Logging)

```python
def log_access(operation, data_type):
    logging.info(f"Operation: {operation}, Data Type: {data_type}")

```
Facilita el monitoreo y la auditoría de las acciones de seguridad, permitiendo una rápida detección y respuesta ante actividades sospechosas o maliciosas.

## Funcionalidades Interfaz de Usuario

La interfaz gráfica, construida con Tkinter, permite a los usuarios interactuar con la aplicación de manera segura y sencilla.

### Consentimiento y Políticas de Privacidad

Al iniciar la aplicación, se muestra un mensaje de consentimiento que informa a los usuarios sobre el uso de sus datos y les permite aceptar los términos antes de continuar.

```python
def show_consent_message(self):
    consent_label = tk.Label(self.consent_frame, text="Consentimiento de Recolección de Datos", font=("Arial", 16, "bold"), fg="white", bg="#003366")
    # Detalle de términos y política de privacidad

```

Además, se incluye una opción de "Política de Privacidad" dentro de la aplicación que proporciona información clara y concisa sobre cómo se manejan los datos. La política se encuentra en la pantalla principal, accesible mediante el botón de ayuda (?). Si la política de privacidad se actualiza, el usuario es notificado.

```python
def check_policy_update(self):
    current_policy_version = "1.1"
    # Verifica si hay actualizaciones en la política
```

### Autenticación de Usuario y Requisitos de Contraseña

La aplicación permite a los usuarios crear una cuenta y asegurarla mediante una contraseña que debe cumplir ciertos requisitos de seguridad. Al crear una contraseña, se muestra a los usuarios los requisitos para ayudarles a establecer una contraseña segura.

```python
def show_password_requirements(self):
    requirements = """
    Requisitos para la contraseña:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula
    - Al menos un carácter especial (!@#$%^&*)
    - Al menos un número
    """
    self.info_label.config(text=requirements)

```

### Control de Acceso a Datos

En la pantalla principal, el usuario puede ver y restringir el uso de sus datos. También puede descargar sus datos en un archivo CSV utilizando el botón "Descargar Mis Datos".

```python
def download_user_data(self, transaction_id):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Guardar archivo como")
    if file_path:
        user_data.to_csv(file_path, index=False)

```

### Restricción de datos

La aplicación permite a los usuarios restringir hasta dos tipos de datos para restringir su uso en la aplicación, lo que cumple con el principio de minimización de datos. Esto se gestiona a través de una ventana emergente que muestra opciones como Correo, Teléfono, Estado Civil y Ubicación.

```python
def restrict_data_usage(self):
    # lógica para seleccionar datos para restringir su uso
```

### Eliminación de cuenta

La opción de "Eliminar Mi Cuenta" permite a los usuarios borrar su cuenta y toda la información asociada de la base de datos. Esto cumple con el derecho al olvido, un aspecto esencial en regulaciones como el GDPR.

```python
def delete_account(self):
    self.df = self.df[self.df['ID'] != self.user_data['ID']]
    self.df.to_csv('archivos/combined_dataset.csv', index=False)

```

## Estrategias de Uso Seguro de los Datos

### Medidas, políticas y Procedimientos
- **Encriptación AES-256 y Hashing SHA-256:** La encriptación y el hashing son fundamentales para proteger la información almacenada y evitar accesos no autorizados. Se utilizan técnicas de encriptación AES-256 en modo CBC para los datos sensibles y hashing SHA-256 para las contraseñas.
- **Cumplimiento de Políticas de Privacidad:** La aplicación asegura que la política de privacidad es fácilmente accesible, clara y fácil de entender, y notifica a los usuarios sobre cualquier cambio en la misma. Esto ayuda a construir confianza y asegura que la aplicación cumple con las normativas de transparencia.

### Integración de Privacidad desde diseño
El proyecto adopta el enfoque de Privacidad por Diseño desde la fase inicial, lo que significa que todas las decisiones de diseño y funcionalidad consideraron la privacidad del usuario.

1. **Minimización de Datos:** Solo se recopilan los datos estrictamente necesarios para el funcionamiento de la aplicación.
2. **Acceso Controlado:** Implementación de restricciones de acceso que permiten a los usuarios definir qué datos pueden ser accedidos o usados por la aplicación.
3. **Protocolos de Revisión Periódica:**: No esta implementado pero se sugiere hacer revisiones periódicas de la política de privacidad y procedimientos de seguridad para manterer actualizados los protocolos de seguridad.

## Plan de Respuesta ante Incidentes de Seguridad

- **Equipo de Respuesta a Incidentes:** Creación de un equipo de respuesta a incidentes que esté preparado para actuar de manera rápida y efectiva en caso de una fuga o pérdida de datos.
- **Protocolos de Respuesta:** Establecimiento de protocolos claros que incluyan la identificación del incidente, contención de la fuga, evaluación del impacto, comunicación con los afectados y remedios para evitar futuras incidencias.
- **Simulacros de Seguridad:** Realización de simulacros de seguridad para asegurar que el equipo está preparado y que los protocolos de respuesta son efectivos.

## Recomendaciones de Protección de Datos Futura

- **Implementar Encriptación Homomórfica:** Investigar y adoptar tecnologías avanzadas de protección de datos como la encriptación homomórfica, que permite realizar cálculos sobre datos cifrados sin necesidad de descifrarlos, ofreciendo una capa adicional de protección.

- **Inteligencia Artificial en Seguridad:** Explorar el uso de soluciones de inteligencia artificial para mejorar la detección de amenazas y respuestas automáticas a incidentes de seguridad.

- **Blockchain para Integridad de Datos:** Evaluar la implementación de tecnología blockchain para mejorar la integridad y trazabilidad de los datos sensibles, lo cual puede ser especialmente útil en ambientes donde la manipulación de datos es un riesgo crítico.

### Conclusión

Este proyecto subraya la importancia de una gestión adecuada y ética de la seguridad de los datos en el sector financiero, destacando los principales logros y compromisos del proyecto:

- **Tecnología Avanzada:** Implementación de encriptación AES-256 y uso de TLS 1.3 para asegurar la protección de los datos tanto en reposo como en tránsito.
- **Cumplimiento Regulatorio:** Adherencia a normativas internacionales y locales, asegurando que todas las operaciones cumplen con estándares como el GDPR y la Ley Peruana de Protección de Datos.
- **Reducción de Riesgos:** Implementación de medidas que disminuyen el riesgo de brechas de seguridad, incluyendo autenticación de dos factores y políticas de privacidad claras.
- **Confianza del Cliente:** Mejora de la percepción de seguridad entre los clientes, lo que refuerza la confianza y la relación a largo plazo con el banco.
- **Educación y Concientización:** Programas continuos de formación y concientización para el personal, fomentando una cultura de seguridad de datos sólida y consciente.
- **Preparación para el Futuro:** Investigación y adopción proactiva de nuevas tecnologías como la encriptación homomórfica y soluciones de inteligencia artificial, preparando al banco para enfrentar desafíos futuros en seguridad de datos.