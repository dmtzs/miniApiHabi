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

# NOTA
He notado que a veces la conexión a la bd se tarda de más y se da un timeout, no se a que se deba eso pero de igual manera me pasaba si intentaba conectarme con dbeaver cuando estaba analizando las tablas que hay creadas.

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

NOTA: De igual manera como he optado por ser mas eficaz, cabe mencionar que en la parte de cargar las credenciales para poder conectarnos de manera exitosa a la base de datos debe de ser tal vez obteniendolas de un archivo con las credenciales o en mi muy personal opinión desde secrets manager de AWS por mencionar un ejemplo aunque hay varias formas de guardar las credenciales de base de datos de manera segura. Por el momento para cumplir con el objetivo principal del ejercicio he optado por ponerlas en el código para poder hacer la conexión a la bd. Sin embargo esto NO debe ser así en ambientes reales y mucho menos en producción.

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
* `__init__.py`: Inicialización de objeto de logs para usarse en todo el proyecto así como para la carpeta de app.
  * `controller`: Carpeta donde está la lógica para poder procesar y validar si se llamó al endpoint correcto, si se recibió los parámetros que se deben de estar recibiendo o no, etc. Básicamente es el core del proyecto debido a la manera en la que se debe de desarrollar el API usando la biblioteca built in que opte por usar.
    * `__init__.py`: Archivo de inicialización del modulo.
    * `api.py`: Archivo donde está el core del proyecto como definición del método http a usar, endpoint, etc
    * `auth.py`: Archivo donde se concentra la parte de validar credenciales y obtener los usuarios que tienen acceso a la API, incluyendo la parte de obtener las credenciales enviadas en la petición como de igual manera obtener los usuarios para comparar si si pueden interactuar con la bd o no.
  * `queries`: Es la carpeta donde está la lógica para hacer los queries que se necesitan para poder traer la información necesaria al usuario incluyendo los filtros de ser el caso.
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
* `some_project_library`: 
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
* `github action`: Para ejecutar un pylint en cada push para así apegarnos a pylint y crear código más estandarizado.
* `dockerfile`: Para ejecutar el API como si fuera un microservicio, estas instrucciones vendrán más adelante.
* `basic auth`: Se agregó basic auth al API.
* `Logs`: Se agregó una forma de crear logs a través de un archivo.

### Uso del dockerfile

## Requisito opcional de usuario pueda dar me gusta a propiedades