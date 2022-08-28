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

## Explicación de lo que se realizará
Una prueba que debe ser realizada con la creación de una pequeña API sin usar un framework de python o algún otro, de igual manera sin usar ORMs por lo que se deberán usar bibliotecas en las que se pueda crear el query escrito.
Esto es con el propósito de conocer la manera en la que genero los queries en la notación de SQL.

La manera en la que me aproximaré será a través del uso de bibliotecas que son parte del core de python esto por las limitaciones de que no se puede utilizar algún framework. Las bibliotecas a usar son:
* json
* http.server
* socketserver

También para hacer los queries para interactuar con la base de datos usaremos:
* PyMySQL

Aquí por las limitaciones decidí ser mas efectivo que eficiente, por qué?. Necesitamos tomar en consideración que las limitaciones de no usar framework, por lo que el desarrollo será más pequeño y en algunos aspectos inseguro para un ambiente productivo, por lo que es mejor utilizar frameworks como flask por solo mencionar un ejemplo que el overhead agregado por los mismos no es demasiado al momento de operar en producción con estos frameworks. Como recomendación considero debe mencionarse en el ejercicio dentro del mismo PDF que no se use framework para que así el aplicante lo tenga siempre presente.

De igual manera agregaré un método de autenticación al API que será usando basic auth solo por agregar una capa más de seguridad usando como base usuarios de la tabla de `auth_user`.

NOTA: De igual manera como he optado por ser mas eficaz, cabe mencionar que en la parte de cargar las credenciales para poder conectarnos de manera exitosa a la base de datos debe de ser tal vez obteniendolas de un archivo con las credenciales o en mi muy personal opinión desde secrets manager de AWS por mencionar un ejemplo aunque hay varias formas de guardar las credenciales de base de datos de manera segura. Por el momento para cumplir con el objetivo principal del ejercicio he optado por ponerlas en el código para poder hacer la conexión a la bd. Sin embargo esto NO debe ser así en ambientes reales y mucho menos en producción.

De igual manera tal vez se pueda notar que no se sigue un patrón como tal definido por algún estándar, esto porque me concentré más en ver cómo usar la biblioteca built in de python que me ayudó a realizar este ejercicio.
Sin embargo tengan por seguro que me puedo adaptar sin ningún problema a patrones en específico como ha sucedido en los trabajos que he tenido.

## Structure of the project
Debido a que no se especifica que se deba de construir de alguna manera en concreto y teniendo en cuenta el tamaño del ejercicio considero que la manera en la que está construido el presente ejercicio está bien de esta manera aunque claro, en ambientes productivos se pueden tomar en cuenta otras prácticas teniendo en cuenta temas como escalabilidad, redundancia, etc.

Por lo que para el objetivo en concreto de este ejercicio tendrá una estructura más sencilla. Por favor, consideren mi adaptabilidad si se requiere algún patrón en concreto, forma en concreta en que se deben guardar las credenciales, etc en específico.