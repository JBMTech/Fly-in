*This project has been created as part of the 42 curriculum by jabuleje*

# Fly-in


Para resolver este escenario complejo, donde múltiples repartidores deben ir de A a B compitiendo por rutas, esquivando bloqueos y gestionando penalizaciones de tiempo (reducción de turnos), el algoritmo A* simple se queda corto. Necesitas un enfoque de Búsqueda de Caminos Multi-Agente (MAPF) o un modelo de Flujo de Costo Mínimo.

La solución óptima combina Pesos Dinámicos para las penalizaciones y Reserva de Espacio-Tiempo para evitar que los repartidores colisionen o se saturen entre sí.


Cooperative A*

  A*
   ↓
  genera varios caminos mediante penalizaciones
    ↓
  Simulation distribuye los drones y evita conflictos

https://www.youtube.com/watch?v=hQa9JTtq4Ok
https://www.datacamp.com/tutorial/a-star-algorithm
