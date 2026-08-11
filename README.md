*This project has been created as part of the 42 curriculum by jabuleje*

# Fly-in


Para resolver este escenario complejo, donde múltiples repartidores deben ir de A a B compitiendo por rutas, esquivando bloqueos y gestionando penalizaciones de tiempo (reducción de turnos), el algoritmo A* simple se queda corto. Necesitas un enfoque de Búsqueda de Caminos Multi-Agente (MAPF) o un modelo de Flujo de Costo Mínimo.

La solución óptima combina Pesos Dinámicos para las penalizaciones y Reserva de Espacio-Tiempo para evitar que los repartidores colisionen o se saturen entre sí.

## Los Algoritmos Idóneos

Dependiendo de si los repartidores se mueven de forma simultánea o planifican de manera centralizada, debes aplicar uno de los siguientes enfoques:

* Enfoque A: A* con Búsqueda Cooperativa (CBS / Cooperative A*)
  Cada repartidor calcula su ruta uno por uno utilizando una tabla de reservas de espacio-tiempo.
  * El Repartidor 1 calcula su ruta óptima de A a B. El sistema reserva los nodos y turnos exactos que va a pisar.
  * El Repartidor 2 calcula su ruta, pero el algoritmo trata los nodos reservados por el Repartidor 1 en turnos específicos como obstáculos temporales.
  * Resultado: Ningún repartidor se bloquea con otro en el mismo punto y se distribuyen por las rutas alternativas de forma natural.

* Enfoque B: Flujo de Costo Mínimo (Min-Cost Max-Flow)
  Si necesitas optimizar a todo el grupo de repartidores a la vez en un solo cálculo, tratas a los repartidores como "unidades de flujo".
  * El grafo define capacidades máximas (cuántos repartidores caben a la vez en una ruta).
  * El algoritmo (como Busacker-Gowen o Simplex de Redes) encuentra la distribución perfecta de rutas de A a B que minimiza el consumo total de turnos de toda la flota, enviando un porcentaje de trabajadores por la ruta principal y derivando al resto por rutas secundarias antes de que las primeras se saturen.

----

https://www.youtube.com/watch?v=hQa9JTtq4Ok

## Métodos Heurísticos y Metaheurísticos
Cuando el grafo es masivo o el problema es de tipo NP-duro (como el Traveling Salesperson Problem o TSP), los algoritmos exactos tardan demasiado. Se recurre a aproximaciones inteligentes:


* Algoritmos Genéticos (GA): Evolucionan una población de rutas posibles combinándolas y mutándolas para encontrar soluciones casi óptimas en problemas de optimización de rutas (como logística urbana).

* Búsqueda Tabú (Tabu Search): Explora el espacio de soluciones saltando de una ruta a otra vecina, bloqueando temporalmente (lista tabú) los movimientos recientes para evitar quedar atrapada en óptimos locales.