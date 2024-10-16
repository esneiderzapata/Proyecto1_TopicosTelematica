# Proyecto1_TopicosTelematica

## Integrantes
- Esneider Zapata Arias
- Miguel Angel Escudero

## Marco Teórico: Algoritmos de Consenso y Elección de Líder en Sistemas Distribuidos
Los algoritmos de consenso en sistemas distribuidos permiten que un grupo de nodos independientes acuerden un valor común o estado, garantizando consistencia a pesar de posibles fallos en los nodos o la red. Son esenciales en sistemas como bases de datos distribuidas, redes de blockchain y almacenamiento distribuido. Por otro lado, la elección de líder es una variante dentro de los algoritmos de consenso, donde un nodo es seleccionado como líder, responsable de coordinar y dirigir las acciones del sistema. El líder actúa como un punto de referencia centralizado para garantizar el consenso y evitar la fragmentación o conflicto entre los nodos.

### Algoritmos de Consenso
En un sistema distribuido, varios nodos pueden realizar tareas simultáneamente, pero la falta de un estado compartido puede causar inconsistencias. Aquí es donde los algoritmos de consenso juegan un papel crucial, permitiendo que todos los nodos lleguen a un acuerdo a pesar de los fallos. Algunos de los más reconocidos algoritmos de consenso incluyen:

Paxos: Un algoritmo de consenso teórico propuesto por Leslie Lamport. Paxos está diseñado para garantizar seguridad (consenso válido) a pesar de la presencia de fallos. Paxos es robusto, pero puede ser complejo de implementar y difícil de entender debido a su formalización.
Raft: Es una alternativa a Paxos que ofrece una implementación más simple. Raft se basa en un líder, donde este nodo gestiona todas las peticiones de los clientes, sincronizando a los nodos seguidores (followers) con el mismo estado a través de registros de comandos.

### Elección de Líder
La elección de líder asegura que en un grupo de nodos, uno sea elegido como líder para coordinar las operaciones. En sistemas distribuidos, tener un líder facilita el control y la resolución de conflictos, evitando condiciones de carrera y proporcionando un nodo central encargado de tomar decisiones importantes. Si el líder falla, se requiere un mecanismo para elegir un nuevo líder .

### Raft: Elección de Líder y Consenso
Raft es un algoritmo de consenso que está dividido en tres componentes principales: la elección de líder, la replicación de registros y la seguridad . En un clúster de nodos Raft, uno de ellos es seleccionado como líder. El líder maneja las peticiones de los clientes y asegura que los cambios se repliquen de manera consistente a todos los seguidores .

Si el líder falla, los seguidores pueden iniciar una nueva elección de líder. Cada nodo en el sistema tiene un "término de mandato", y el nodo con el término de mandato más alto tiene mayor probabilidad de ser elegido como líder . En cada ciclo de elección, los nodos votan por su candidato preferido, y si un nodo obtiene la mayoría de los votos, es elegido líder .

La simplicidad de Raft lo hace más entendible en comparación con Paxos, lo cual ha fomentado su adopción en proyectos de bases de datos distribuidas, como el sistema de archivos distribuido Etcd y Consul .

### Paxos: Consenso Tolerante a Fallos
Paxos es uno de los algoritmos de consenso más antiguos y teóricamente completos. A diferencia de Raft, Paxos no tiene una estructura de líder definida, sino que se basa en una serie de fases para proponer y aceptar valores. Un nodo propone un valor, y los nodos que actúan como aceptadores pueden decidir aceptar o rechazar el valor propuesto . Paxos asegura que incluso en presencia de fallos parciales, el sistema puede llegar a un acuerdo .

Si bien Paxos ofrece garantías fuertes de seguridad y tolerancia a fallos, es conocido por ser difícil de implementar correctamente debido a su complejidad y falta de claridad en algunos detalles . Variantes como Multi-Paxos introducen la figura de un líder para mejorar la eficiencia, similar a Raft, pero su implementación sigue siendo más complicada .

### Aplicación en el Proyecto: Base de Datos Simulada con Elección de Líder
En este proyecto de un sistema de base de datos simulado, se implementará un esquema de consenso utilizando la elección de líder basado en el algoritmo Raft. El sistema constará de tres procesos: un líder y dos seguidores, donde el líder será responsable de recibir las solicitudes de escritura, mientras que las lecturas serán atendidas por los seguidores. Este enfoque permite replicar los datos entre los nodos y garantiza la consistencia entre ellos .

El sistema debe también manejar la tolerancia a fallos, simulando caídas de nodos. Por ejemplo, si el líder falla, los seguidores deben ser capaces de elegir un nuevo líder a través de una nueva elección. Esto proporciona resiliencia y asegura que el sistema continúe funcionando a pesar de fallos temporales .

### Conclusión
Los algoritmos de consenso y la elección de líder son esenciales para garantizar consistencia y disponibilidad en sistemas distribuidos . Raft, con su enfoque claro y más comprensible, ha ganado terreno frente a Paxos, que, aunque más formalmente completo, es más difícil de implementar. Ambos enfoques ofrecen soluciones robustas para sistemas distribuidos con tolerancia a fallos, lo que los hace adecuados para proyectos que requieren alta disponibilidad y consistencia, como bases de datos distribuidas. Ya que Raft tiene una implementación más sencilla, utilizaremos dicho algoritmo para nuestro proyecto.

## Bibliografia marco teorico: 

### Algoritmos de consenso y eleccion de lider:

https://www.techtarget.com/whatis/definition/consensus-algorithm

https://www.geeksforgeeks.org/consensus-algorithms-in-distributed-system/

https://aws.amazon.com/es/builders-library/leader-election-in-distributed-systems/

https://www.geeksforgeeks.org/leader-election-vs-consensus-algorithm/

https://www.baeldung.com/cs/consensus-algorithms-distributed-systems

https://www.enjoyalgorithms.com/blog/leader-election-system-design

### Raft:

https://raft.github.io

https://thesecretlivesofdata.com/raft/

https://raft.github.io/raft.pdf

https://en.wikipedia.org/wiki/Raft_(algorithm)

https://www.geeksforgeeks.org/raft-consensus-algorithm/

### Paxos:


https://lamport.azurewebsites.net/pubs/paxos-simple.pdf

https://en.wikipedia.org/wiki/Paxos_(computer_science)

https://www.geeksforgeeks.org/paxos-consensus-algorithm/

https://www.geeksforgeeks.org/paxos-algorithm-in-distributed-system/

https://www.cs.yale.edu/homes/aspnes/pinewiki/Paxos.html

## Especificaciones de comunicación: 

![WhatsApp Image 2024-10-15 at 21 01 40](https://github.com/user-attachments/assets/648a0bd7-d14c-4304-8fd9-63e511d43710)

## Diseño del sistema: 

![WhatsApp Image 2024-10-14 at 18 34 24](https://github.com/user-attachments/assets/81eab16f-4173-43af-aff9-6a1ae6b563a1)


## Informe final: 
Veremos las pruebas realizadas al algoritmo y sus resultados (la evidencia de estas pruebas se puede encontrar en el video adjunto en la sección **Informe de pruebas** de este mismo documento):

### Se inician los nodos sin un lider inicial:
Resultado: Los nodos se ponen de acuerdo y se elige un único líder.

### Se envía una solicitud "write(message) al proxy"
Resultado: El proxy encuentra al nodo lider y reenvía la solictud a dicho nodo, la solictud se replica tanto en el log como en la base de datos de todos los nodos.

### Se envía una solicitud "read" al proxy
Resultado: El proxy crea una lista con solamente los nodos followers, y envia la solictud read a cualquier nodo en la lista, dicho nodo responde con todos los datos de su base de datos.

### Se cae el líder actual
Resultado: Los nodos se ponen de acuerdo y se elige a un nuevo líder.

### Se cae un follower
Resultado: El lider sigue intentando envíar mensajes a este nodo sin éxito, pero los nodos que siguen disponibles siguen funcionando con total normalidad.

### Un nodo se intenta reconectar a la red
Resultado: El nodo siempre entra como follower sin importar su estado antes de caerse, si se enviaron mensajes "write(message)" mientras el nodo estaba caido, dicho nodo es capaz de sincronizar estos mensajes que inicialmente no pudo recibir, sincronizando su log y base de datos con todos los demás nodos.

## Documentación técnica: 
A continuación explicaremos paso por paso como funciona el algoritmo Raft que implementamos:

### Paso 1 - Elección inicial del lider
Todos los nodos empiezan con el estado "Follower", y a cada nodo se le asigna una cantidad de tiempo aleatoria entre 3 y 5 segundos (ejemplo: 3.56789s). La función de este tiempo es iniciar un cronometro que una vez llegue a 0, el nodo asumirá que el lider actual ha dejado de estar disponible, este cronometro se vuelve a empezar cada vez que se recibe un heartbeat del lider, impidiendo que llegue a 0 si el lider no se ha caído.

Como todos los nodos empiezan como "Follower", ningúno recibe hearbeats, lo que pasa a continuación es que el el primer nodo cuyo cronometro llegue a 0 iniciará una "elección" en la que se determinará un nuevo lider, dicho nodo se postula como candidato y vota por si mismo, a la vez que solicita votos a los demás nodos.

Los demás nodos reciben la solicitud de voto y votarán por dicho nodo si y solo si el nodo candidato cuenta con un "term" mayor o igual al del nodo votante (Term es una variable que determina la cantidad de votaciones realizadas hasta el momento).

Cuando el nodo candidato recibe la mayoría de votos (en este caso 2: el suyo propio y el de cualquier otro nodo), este se vuelve el lider, y empieza a enviar hearbeats a los demás nodos para notificarles.

Si un candidato no recibe la mayoría de votos, este vuelve a ser un follower y el siguiente nodo cuyo contador llegue a 0 se convertirá en el nuevo candidato, hasta que se elija un lider.

### Paso 2 - Replicación del log y Consistencia de la base de datos

Una vez se ha elegido un nodo lider, este será quien reciba los solicitudes "write", cuando el nodo lider recibe una de estas solicitudes, la anota en su propio log (el log es un archivo persistente .json) y le informa a los followers para que estos repliquen dicha entrada tambien, sin embargo, no modifica la base de datos (que es tambien un archivo persistente .json) aún.

Cuando la mayoría de followers le informan al lider que sus logs han sido actualizados, el lider procede a escribir en su base de datos el mensaje que estaba adjunto a la solicitud "write", e informa a los followers de que hagan lo mismo, de esta manera nos aseguramos de que solo se actualice la base de datos si la mayoría de los nodos tienen su log sincronizado.

### Paso 3 - Re-elección del Lider

Supongamos que el lider por cualquier razón deja de estar disponible, es decir, se cae, lo que sucede a continuación es que el cronometro de los followers empezará a correr ya que dejaron de recibir heartbeats, el primer follower cuyo contador llegue a 0 pasará a ser un candidato, y repetira el proceso de elección de lider, lo que incluye solicitar y recibir los votos necesarios. Una vez recibidos, se convertirá en el nuevo lider y procederá con normalidad.

### Paso 4 - Re-conexión de nodos

Supongamos que el lider original vuelva a estar disponible, este iniciará nuevamente como un follower ya que detectará que el lider actual le está enviando hearbeats

### Paso 5 - Sincronización de log después de una caída

Supongamos que ahora se cae un follower, que mientras está caido llegan una serie de mensajes "write" y que luego se reconecta a la red. Para asegurar la sincronización del log, cada nodo al iniciar verifica si actualmente hay un lider, en caso de que lo haya, el nodo que se ha reconectado solicita al lider que le pase su log, el nodo reconectado verifica las diferencias entre su log y el del lider y hace los cambios pertinentes, una vez actualiza su log, procede a ejecutar las acciones en la base de datos, asegurando así la consistencia entre todos los nodos incluso si se llegaron a desconectar de la red.

## Informe de pruebas: 
Video de evidencia de las pruebas realizadas: https://youtu.be/DK1f0jX8xow

