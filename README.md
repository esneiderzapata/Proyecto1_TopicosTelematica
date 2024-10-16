# Proyecto1_TopicosTelematica



## Marco Teórico: Algoritmos de Consenso y Elección de Líder en Sistemas Distribuidos
Los algoritmos de consenso en sistemas distribuidos permiten que un grupo de nodos independientes acuerden un valor común o estado, garantizando consistencia a pesar de posibles fallos en los nodos o la red. Son esenciales en sistemas como bases de datos distribuidas, redes de blockchain y almacenamiento distribuido. Por otro lado, la elección de líder es una variante dentro de los algoritmos de consenso, donde un nodo es seleccionado como líder, responsable de coordinar y dirigir las acciones del sistema. El líder actúa como un punto de referencia centralizado para garantizar el consenso y evitar la fragmentación o conflicto entre los nodos.

### Algoritmos de Consenso
En un sistema distribuido, varios nodos pueden realizar tareas simultáneamente, pero la falta de un estado compartido puede causar inconsistencias. Aquí es donde los algoritmos de consenso juegan un papel crucial, permitiendo que todos los nodos lleguen a un acuerdo a pesar de los fallos .

Algunos de los más reconocidos algoritmos de consenso incluyen:

Paxos: Un algoritmo de consenso teórico propuesto por Leslie Lamport. Paxos está diseñado para garantizar seguridad (consenso válido) a pesar de la presencia de fallos. Paxos es robusto, pero puede ser complejo de implementar y difícil de entender debido a su formalización.
Raft: Es una alternativa a Paxos que ofrece una implementación más simple. Raft se basa en un líder, donde este nodo gestiona todas las peticiones de los clientes, sincronizando a los nodos seguidores (followers) con el mismo estado a través de registros de comandos.

## Elección de Líder
La elección de líder asegura que en un grupo de nodos, uno sea elegido como líder para coordinar las operaciones. En sistemas distribuidos, tener un líder facilita el control y la resolución de conflictos, evitando condiciones de carrera y proporcionando un nodo central encargado de tomar decisiones importantes. Si el líder falla, se requiere un mecanismo para elegir un nuevo líder .

## Raft: Elección de Líder y Consenso
Raft es un algoritmo de consenso que está dividido en tres componentes principales: la elección de líder, la replicación de registros y la seguridad . En un clúster de nodos Raft, uno de ellos es seleccionado como líder. El líder maneja las peticiones de los clientes y asegura que los cambios se repliquen de manera consistente a todos los seguidores .

Si el líder falla, los seguidores pueden iniciar una nueva elección de líder. Cada nodo en el sistema tiene un "término de mandato", y el nodo con el término de mandato más alto tiene mayor probabilidad de ser elegido como líder . En cada ciclo de elección, los nodos votan por su candidato preferido, y si un nodo obtiene la mayoría de los votos, es elegido líder .

La simplicidad de Raft lo hace más entendible en comparación con Paxos, lo cual ha fomentado su adopción en proyectos de bases de datos distribuidas, como el sistema de archivos distribuido Etcd y Consul .

## Paxos: Consenso Tolerante a Fallos
Paxos es uno de los algoritmos de consenso más antiguos y teóricamente completos. A diferencia de Raft, Paxos no tiene una estructura de líder definida, sino que se basa en una serie de fases para proponer y aceptar valores. Un nodo propone un valor, y los nodos que actúan como aceptadores pueden decidir aceptar o rechazar el valor propuesto . Paxos asegura que incluso en presencia de fallos parciales, el sistema puede llegar a un acuerdo .

Si bien Paxos ofrece garantías fuertes de seguridad y tolerancia a fallos, es conocido por ser difícil de implementar correctamente debido a su complejidad y falta de claridad en algunos detalles . Variantes como Multi-Paxos introducen la figura de un líder para mejorar la eficiencia, similar a Raft, pero su implementación sigue siendo más complicada .

## Aplicación en el Proyecto: Base de Datos Simulada con Elección de Líder
En este proyecto de un sistema de base de datos simulado, se implementará un esquema de consenso utilizando la elección de líder basado en el algoritmo Raft o Paxos. El sistema constará de tres procesos: un líder y dos seguidores, donde el líder será responsable de recibir las solicitudes de escritura, mientras que las lecturas serán atendidas por los seguidores. Este enfoque permite replicar los datos entre los nodos y garantiza la consistencia entre ellos .

El sistema debe también manejar la tolerancia a fallos, simulando caídas de nodos. Por ejemplo, si el líder falla, los seguidores deben ser capaces de elegir un nuevo líder a través de una nueva elección. Esto proporciona resiliencia y asegura que el sistema continúe funcionando a pesar de fallos temporales .

## Conclusión
Los algoritmos de consenso y la elección de líder son esenciales para garantizar consistencia y disponibilidad en sistemas distribuidos . Raft, con su enfoque claro y más comprensible, ha ganado terreno frente a Paxos, que, aunque más formalmente completo, es más difícil de implementar. Ambos enfoques ofrecen soluciones robustas para sistemas distribuidos con tolerancia a fallos, lo que los hace adecuados para proyectos que requieren alta disponibilidad y consistencia, como bases de datos distribuidas .
## Marco teorico: 
Presentacion del marco teorico sobre algoritmos de consenso
y la elecci ́on de l ́ıder en sistemas distribuidos, incluyendo Raft y Paxos.

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

## Especificaciones de comunicaci ́on: 
Definici ́on final de la arquitectura del
sistema, los protocolos y APIs para la comunicaci ́on entre los diferentes pro-
cesos, incluyendo la separaci ́on entre el plano de datos y el plano de control.

## Diseño del sistema: 

![WhatsApp Image 2024-10-14 at 18 34 24](https://github.com/user-attachments/assets/81eab16f-4173-43af-aff9-6a1ae6b563a1)


## Informe final: 
Incluir un an ́alisis detallado de las pruebas realizadas, simu-
laci ́on de fallos y resultados.

## Documentaci ́on t ́ecnica: 
Explicaci ́on detallada del algoritmo elegido (Raft,
Paxos o soluci ́on propia), incluyendo los desaf ́ıos enfrentados y c ́omo se ga-
rantiza la consistencia y la disponibilidad en el sistema.
## Informe de pruebas: 
Evidencia de las pruebas realizadas que demuestren
la funcionalidad del sistema ante la falla del l ́ıder y la correcta elecci ́on de un
nuevo l ́ıder. El informe debe incluir la simulaci ́on de fallos y c ́omo el sistema
se comporta en estas situaciones.

Video de evidencia de las pruebas realizadas: https://youtu.be/DK1f0jX8xow

