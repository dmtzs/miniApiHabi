<p align="center">
  <!-- <img width="300" src="" alt="Cover image"> -->
  <h1 align="center" style="margin: 0 auto 0 auto;">miniApiHabi</h1>
  <h5 align="center" style="margin: 0 auto 0 auto;">A mini API in python without framework</h5>
</p>

<p align="center">
  <img src="https://img.shields.io/github/last-commit/dmtzs/miniApiHabi?logo=Conventional Commits">
  <img src="https://img.shields.io/github/contributors/dmtzs/miniApiHabi?logo=Handshake">
  <img src="https://img.shields.io/github/issues/dmtzs/miniApiHabi?label=issues&logo=Eclipse Mosquitto">
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/dmtzs/miniApiHabi?logo=python">
</p>

<p align="center">
  <img src="https://img.shields.io/github/languages/code-size/dmtzs/miniApiHabi">
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/dmtzs/miniApiHabi">
  <img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/dmtzs/miniApiHabi?label=total%20lines%20in%20repo">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/dmtzs/miniApiHabi">
</p>

- [Ejercicio 1](#Ejercicio-1)
  - [Explicacion de lo que se realizara](#Explicación-de-lo-que-se-realizará)
  - [Estructura del proyecto](#Estructura-del-proyecto)
  - [Propuesta teórica con framework](#Propuesta-teórica-con-framework)
  - [Aditamentos](#Aditamentos)
  - [Ejecutar el código](#Ejecutar-el-código)
  - [Ejecucion local](#Ejecucion-local)
  - [Ejecucion usando dockerfile](#Ejecucion-usando-dockerfile)
  - [Instrucciones de uso del api](#Instrucciones-de-uso-del-api)
- [Ejercicio 2 de usuario pueda dar me gusta a propiedades](#Ejercicio-2-de-usuario-pueda-dar-me-gusta-a-propiedades)
- [Ejercicio 3 optimizar queries](#Ejercicio-3-optimizar-queries)

# NOTA
He notado que a veces la conexión a la bd se tarda de más y se da un timeout, no se a que se deba eso pero de igual manera me pasaba si intentaba conectarme con dbeaver cuando estaba analizando las tablas que hay creadas.

# Ejercicio 1
## Explicación de lo que se realizará
Una prueba que debe ser realizada con la creación de una pequeña API sin usar un framework de python o algún otro, de igual manera sin usar ORMs por lo que se deberán usar bibliotecas en las que se pueda crear el query escrito.
Esto es con el propósito de conocer la manera en la que genero los queries en la notación de SQL.

La manera en la que me aproximaré será a través del uso de bibliotecas que son parte del core de python esto por las limitaciones de que no se puede utilizar algún framework. Las bibliotecas a usar son:
* json
* http.server
* socketserver

También para hacer los queries para interactuar con la base de datos y la ceración de logs usaremos:
* PyMySQL
* ecs-logging

Aquí por las limitaciones decidí ser mas efectivo que eficiente, por qué?. Necesitamos tomar en consideración que las limitaciones de no usar framework, por lo que el desarrollo será más pequeño y en algunos aspectos inseguro para un ambiente productivo, por lo que es mejor utilizar frameworks como flask por solo mencionar un ejemplo que el overhead agregado por los mismos no es demasiado al momento de operar en producción con estos frameworks. Como recomendación considero debe mencionarse en el ejercicio dentro del mismo PDF que no se use framework para que así el aplicante lo tenga siempre presente.

De igual manera agregaré un método de autenticación al API que será usando basic auth solo por agregar una capa más de seguridad usando como base usuarios de la tabla de `auth_user`.

NOTA: De igual manera como he optado por ser mas eficaz, cabe mencionar que en la parte de cargar las credenciales para poder conectarnos de manera exitosa a la base de datos debe de ser tal vez obteniendolas de un secrets manager, pero en este caso las pondremos un archivo codificadas en base 64.

De igual manera tal vez se pueda notar que no se sigue un patrón como tal definido por algún estándar, esto porque me concentré más en ver cómo usar la biblioteca built in de python que me ayudó a realizar este ejercicio.
Sin embargo tengan por seguro que me puedo adaptar sin ningún problema a patrones en específico como ha sucedido en los trabajos que he tenido.

LOGS: A su vez haré usao de la biblioteca de `ecs-logging` para poder hacer logs locales aunque herramientas como elastic search podría ser uina mejor opción al respecto.

## Estructura del proyecto
Debido a que no se especifica que se deba de construir de alguna manera en concreto y teniendo en cuenta el tamaño del ejercicio considero que la manera en la que está construido el presente ejercicio está bien de esta manera aunque claro, en ambientes productivos se pueden tomar en cuenta otras prácticas teniendo en cuenta temas como escalabilidad, redundancia, etc.

Por lo que para el objetivo en concreto de este ejercicio tendrá una estructura más sencilla. Por favor, consideren mi adaptabilidad si se requiere algún patrón en concreto, forma en concreta en que se deben guardar las credenciales, etc en específico. Sin mebargo más adelante les hare una propuesta de cómo lo hubiera hecho con un framework.

Tenemos Nuestro proyecto y una carpeta que se llama src en la cual estará dentro el código, algo como esto:
```
src/
    app/
        controller/
            __init__.py
            api.py
            auth.py
        queries/
            __init__.py
            database.py
        __init__.py
    main.py
    requirements.txt
```

* `main.py`: En este archivo tenemos la ejecución de nuestro servidor http en la que estará al escucha de recibir peticiones desde postman por ejemplo para así poder de manera exitosa concentrar la ejecución de nuestra API de forma centralizada y de igual manera este archivo será el de ejecución para empezar a escuchar las peticiones http hacia nuestro servidor.
* `requirements.txt`: Las bibliotecas externas usadas para con el proyecto, en este caso la biblioteca que nos ayuda en la parte de crear un archivo de logs y pra ejecutar queries de SQL en la bd.
* `app`: Carpeta donde estará la lógica completa de la aplicación.
* `__init__.py`: Inicialización de objeto de logs para usarse en todo el proyecto así como para la carpeta de app y de igual manera para inicializar la variable de db_credentials para así poder usar las credenciales de la bd en otras partes del código que la requieran.
  * `controller`: Carpeta donde está la lógica para poder procesar y validar si se llamó al endpoint correcto, si se recibió los parámetros que se deben de estar recibiendo o no, etc. Básicamente es el core del proyecto debido a la manera en la que se debe de desarrollar el API usando la biblioteca built in que opte por usar.
    * `__init__.py`: Archivo de inicialización del modulo.
    * `api.py`: Archivo donde está el core del proyecto como definición del método http a usar, endpoint, etc
    * `auth.py`: Archivo donde se concentra la parte de validar credenciales y obtener los usuarios que tienen acceso a la API, incluyendo la parte de obtener las credenciales enviadas en la petición como de igual manera obtener los usuarios para comparar si si pueden interactuar con la bd o no.
  * `queries`: Sería lo proporcional a una carpeta repositories pero es la carpeta donde está la lógica para hacer los queries que se necesitan para poder traer la información necesaria al usuario incluyendo los filtros de ser el caso.
    * `__init__.py`: Archivo de inicialización del modulo.
    * `database.py`: Archivo que contiene la manera de crear las conexiones a la bd y de igual manera para poder ejecutar los queries que son necesarios para obtener las propiedades que se necesitan.

## Propuesta teórica con framework
Claramente la estructura anterior tiene sus defectos y un framework suele ayudar un poco más al momento de desarrollar un API. A continuación explicaré como mencioné con anterioridad solo la propuesta de cómo realizaría el proyecto con su estructura y el por qué de esa manera la cual considero se adapta mejor a una arquitectura de microservicios si pudiese usar un framework en este caso flask.

Para este caso consideremos la siguiente distribución de los archivos:
```
app/
    __init__.py
    admin_routes.py
    routes.py
    error_handlers.py
    repositories/
        __init__.py
        repo.py
main.py
requirements.txt
```

Con la forma anterior tenemos que:
* `some_project_library`: En caso de que se quiera crear bilbiotecas especificas del proyecto deben de estar a esta altura.
* `app/`: 
  * `__init__.py`: Archivo de inicialización del proyecto mismo que nos ayudaría a definir nuestros objetos de conexiones a bases de datos etc para poder realizar en otra parte queries. En este caso aquí se definirían los objetos para crear el objeto de conexión a la bd, el objeto para obtener las credenciales de un secret manager, archivo, el objeto de flask, el de la conexión a la bd, etc. Básicamente crear todos los objetos que necesitan ser creados una sola vez para que se puedan importar a través de todo el proyecto sin necesidad de crear un nuevo objeto cada vez que se necesite y así se pueda importar y usar en otros módulos/archivos del API.
  * `admin_routes.py`: Aquí se podrían definir los endpoints que solo sean accesibles por el administrador y que a través de roles por ejemplo se puedan definir incluso niveles de administrador y así definir mejor si se tiene acceso o no a un endpoint en específico a pesar de ser administrador.
  * `routes.py`: Algo similar al de administración solo que aquí estarán los endpoints expuestos para consumirse al usuario final o al front end por ende ya que serían los endpoints que el aplicativo del front consumirá para poder mostrar el resultado final al respecto.
  * `error_handlers.py`: Si queremos personalizar por ejemplo los errores de http enviados y sus mensajes aquí se concentran por ejemplo si queremos mandar un body en concreto cuando sale un authorized, forbidden, etc.
  * `__init__.py`: Archivo de inicialización del modulo.
  * `repo.py`: Aquí pondría la lógica para hacer el query a una bd importando el objeto de conexión desde donde se inicializa la app como tal, peticiones a API u otros microservicios, etc. Claramente no se limitaría a tener todo eso de ser necesario en un mismo archivo pero quiero dejar claro que podría estar dentro de la misma carpeta separado por archivos.
* `main.py`: Archivo que se encarga de traer todo dentro de la carpeta app como punto principal de ejecución para mandar las peticiones a la app y de igual manera sea el punto de inicio de ejecución del API para que sea levantada correctamente. Aquí se podrñia usar WSGI, gunicorn, etc para poder servir la API y hacer las peticiones HTTP a nuestro API con todo lo definido dentro de la carpeta app.
* `requirements.txt`: Las bibliotecas externas usadas para con el proyecto, en este caso la biblioteca que nos ayuda en la parte de crear un archivo de logs y pra ejecutar queries de SQL en la bd.

Ahora bien por ejemplo esto considerando que se pueda utilizar un ORM sería la misma lógica de arriba pero por ejemplo agregando una carpeta de `models/` a la altura de repositories. En models iría la definición de los modelos a usar con el ORM para poder ejecutar los queries de esa manera importandose dentro de `repositories` en los archivos que requieran del modelo definido con ayuda del ORM para la ejecución de nuestros queries, ejemplo de la estructura con eso a continuación.

```
app/
    __init__.py
    admin_routes.py
    routes.py
    error_handlers.py
    repositories/
        __init__.py
        repo.py
    models/
        __init__.py
        model.py
main.py
requirements.txt
```

## Aditamentos
Esto es para explicar lo que agregué que no se pedía en el PDF:
* `github action`: Para ejecutar un pylint en cada push para así apegarnos a pylint y crear código más estandarizado, por favor revisen la pestaña de actions una vez en el repositorio para que vean cuando me esquivoque y cuando lo corregí.
* `dockerfile`: Para ejecutar el API como si fuera un microservicio.
* `basic auth`: Se agregó basic auth al API usando un usuario de la tabla de auth_user.
* `logs`: Se agregó una forma de crear logs a través de un archivo.

## Ejecutar el código
El proyecto no necesita correrse desde un contenedor pero deje la opción en caso de que se desee hacer de esa manera.
Se necesita instalar las bibliotecas pertinentes, use el archivo `requirements.txt` para instalar las bibliotecas externas a través del siguiente comando:
```
pip install -r requirements.txt
```

### Ejecucion local
Se debe ir hasta la carpeta src dentro del presente proyecto y una vez dentro del proyecto se ejecuta lo siguiente:
```
python main.py
```
Y está todo listo para ser consumido, las instrucciones de uso puede encontrarlas [aqui](#Instrucciones-de-uso-del-api)
### Ejecucion usando dockerfile
1. Primero se crea la imagen con el siguiente comando y claramente estando en el directorio donde está el mismo Dockerfile:
```
docker build -t tuhabi:v1 -f Dockerfile .
```

2. Después de que termine la ejecución de ese comando aparecerá algo como esto:
```terminal
CONTAINER ID   IMAGE       COMMAND                  CREATED         STATUS         PORTS      NAMES
3525c4sdf1   tuhabi:v1   "python3 ./main.py"   3 seconds ago   Up 2 seconds   5000/tcp   recursing_engelbart
```

3. Se toma el ID de la imagen para ejecutar el siguiente comando:
```
docker run 3525c4sdf1
```

Y esto levantará el contenedor con la imagen designada desde el Dockerfile


## Instrucciones de uso del api
A continuación la forma de hacer el request al API:
* Método HTTP: `GET`
* URL: `{base_url}/properties`
* Request: Se debe hacer a través de params, un ejemplo a continuación: `{base_url}/properties?year=2019&city=pereira&status=vendido`
Así mismo se puede filtrar por cualquiera de esos parámetros de forma individual, es decir que solo se mande uno o dos o los tres parámetros juntos que era los criterios de filtración por parte del usuario según el problema a resolver. De igual manera tome en cuenta la opción en caso de que enviara sin filtros el request en el cual si lo hace de esa manera le mostrará todos los registros siempre y cuando estén en el status de `pre_venta`, `en_venta` o `vendido` acorde a las limitaciones mismas del problema planteado.
* Params: Los params a enviar deben tener el nombre designado debajo y el valor que haya en la base de datos, de lo contrario si no hay ningún registro con esas especificaciones respondera al API con un status de error y como mensaje `No records found`. De igual manera como se solicitaba en el ejercicio hay un archivo llamado `params.json` ya que se pedía en json cómo se haría el request, en este caso como menciono en este presente enunciado y como aparece en la colección de postman serían parámetros pero lo dejo en formato json en ese archivo de igual manera como solicita el ejercicio, puedes ir a el dando clic [aquí](./params.json)
    * `year`: Nombre del campo debe ser igual y se debe mandar los 4 dígitos del año.
    * `city`: Nombre del campo debe ser igual y se debe mandar el nombre de la ciudad.
    * `status`: Nombre del campo debe ser igual y se debe mandar el status.
* `Authorization`: Este es un header que se debe de mandar con las reglas del basic auth de la forma: `Basic username:passwd` y la cadena anterior despues de Basic debe ir codificado en base 64.

Finalmente como parte de este ejercicio si desean probar por ejemplo usando postman les dejo el archivo json para que puedan importar la colección que usé para probar mi API: [click aqui](./tuhabi.postman_collection.json)

NOTA: La colección de postman incluye las respuestas que recibí con los filtros aplicados a través de los ejemplos que salen una vez importada la colección.


# Ejercicio 2 de usuario pueda dar me gusta a propiedades
Considero que para hacer esto posible lo que se debe de hacer es crear una tabla con un nombre descriptivo como podría ser `liked_properties` tal vez, en donde se deben guardar 2 llaves foraneas que serían el `id` de la tabla `auth_user` que se guardaría como `id_user` dentro de la nueva tabla, el `id` de la tabla `property` que serçia guardado en la nueva tabla tal vez como `id_property` y un timestamp como para saber en caso de que sea necesario cuando el usuario le dio `like` a esa tabla. Debido a que veo que en algunos campos de fecha se pone por ejemplo en la tabla de `auth_user` un campo como `date_joined` yo creare mi campo de date para la tabla de propiedades con me gusta un campo llamado `date_liked`. Para ver cómo sería el esquema puede verlo dando click [aquí](./db_esquemas/esquema.png)

Los comandos para crear esa tabla sería:

Primero insertamos la tabla, los int 11 es porque veo que el id de las tablas de la bd de tuhabi dicen que son int 11 y por eso los coloco de igual manera así:
```sql
CREATE TABLE liked_properties (id_user int(11) NOT NULL, id_property int(11) NOT NULL,
  date_liked datetime,
  FOREIGN KEY (id_user) REFERENCES auth_user (id),
  FOREIGN KEY (id_property) REFERENCES property (id)
);
```

Con el comando anterior quedaría la tabla completa y lista para usarse y expandir el modelo actual para ahora si soportar esta funcionalidad.
Ahora bien como en el ejercicio se dice por el lado práctico que no se use ORM para ver la sintaxis de SQL colocaré a continuación cómo se harían nuevas inserciones en esta nueva tabla:

Primero el insert sería:
```sql
INSERT INTO liked_properties (id_user, id_property, date_liked) VALUES (<id_user>, <id_property>, NOW());
```

Ahora para obtener las propiedades con me gusta por un usuario en específico:
```sql
SELECT id_property FROM liked_properties WHERE id_user = <id_user>
```

Para obtener el nombre completo de los usuarios que le dieron like a algo:
```sql
SELECT Au.firstname, Au.last_name FROM auth_user Au LEFT JOIN liked_properties LP ON Au.id=LP.id_user;
```

# Ejercicio 3 optimizar queries
Ejercicio opcional.

Para esta parte la verdad creo que con cambiar la manera en la que se guarda el status sería una buena idea debido a que se hacen por lo menos dos JOIN así como lo hice yo para la resolución del ejercicio práctico.
Por lo que considero que la manera más sencilla es simplemente que el `status` pase a ser parte de la tabla property y de esta manera se hace más sencillo asignar `status` a las propiedades. Por lo que básicamente creo que la manera más sencilla es quitar la tabla de `status_history` y `status` y poner directamente el status en la tabla de `property`.