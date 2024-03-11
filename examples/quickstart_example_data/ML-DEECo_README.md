# ML-DEECo

ML-DEECo is a machine-learning-enabled component model for adaptive component architectures. It is based on DEECo component model, which features autonomic *components* and dynamic component coalitions (called *ensembles*). ML-DEECo allows exploiting machine learning in decisions about adapting component coalitions at runtime.

The framework provides abstractions for getting predictions (estimates) about the future state of the system. It uses machine learning models trained in a supervised manner to obtain these predictions. A simulation of the system is run to collect data used for training the ML model. The simulation can then be run again with the trained model to see the impact of the learned model on the system.

## Short summary of ensemble-based component systems

ML-DEECo is based on the DEECo component model ([Bures et al.](https://dl.acm.org/doi/10.1145/2465449.2465462)). We want to very briefly introduce the concepts of *components* and *ensembles* before describing the details of ML-DEECo usage.

### Component

Components are autonomous agents in the system. Based on the knowledge they have, they can independently operate in the environment. In ML-DEECo, the components have an `actuate` method which is executed in every step of the simulation, and it thus comprises the behavior of the component.

### Ensemble

An ensemble is a group of components created to express that the components are bound with the same objective (i.e., behavior). The ensembles are used for knowledge exchange among the member components and their coordination. The ensembles are formed and dismantled dynamically at runtime as the objectives emerge in the system and are completed. The member components of the ensemble are also selected dynamically at every step of the simulation.

## Usage

The ML-DEECo framework provides abstractions for creating components and ensembles and assigning machine learning estimates to them. A simulation can then be run with the components and ensembles to observe behavior of the system and collect data for training the estimates. The trained estimate can then be used in the next run of the simulation.

The configuration of the simulation (lists of components and ensembles, number of steps of the simulation, etc.) is managed by a class derived from the `Experiment` class. See section [Running the simulation](#running-the-simulation) for more details.

A typical ML experiment in ML-DEECo consists of several *iterations*. In each iteration, the simulation is run multiple times to collect data, and then the training of the ML model is performed. Each run of the simulation consists of *steps* -- in each step, the ensembles are reformed and the components are actuated.

### Specifying components

The `ml_deeco.simulation` module offers a base class `Component` for defining components. Furthermore, we provide
 `StationaryComponent2D` and `MovingComponent2D` (both derived from `Component`) to represent components on a 2D map. These have a `location` in a 2D space defined by an instance of `ml_deeco.simulation.Point2D` class.

Each component has an `actuate` method which is executed in every step of the simulation and should be implemented by the user.

The `MovingComponent2D` offers the `move` method which will move the component in a direction towards a target defined in the parameter. If the agent arrives at the target, the `move` method will return `True`.

```py
from ml_deeco.simulation import StationaryComponent2D, MovingComponent2D

# Example of a stationary component -- a charging station
class Charger(StationaryComponent2D):

    def __init__(self, location):
        super().__init__(location)
        self.charging_drones = []

    # a drone at the location of the charger can start charging
    def startCharging(self, drone):
        if drone.location == self.location:
            self.charging_drones.append(drone)

    def actuate(self):
        # we charge the drones
        for drone in self.charging_drones:
            drone.battery += 0.01
            if drone.battery == 1:
                # fully charged
                drone.station = None

# Example of a moving component -- a flying drone
class Drone(MovingComponent2D):

    def __init__(self, location, speed):
        super().__init__(location, speed)
        self.battery = 1
        self.charger = None

    def actuate(self):
        # if the drone has an assigned charger
        if self.charger:
            # fly towards it
            if self.move(self.charger.location):
                # drone arrived at the location of the charger
                self.charger.startCharging(self)

```

### Specifying ensembles

Ensembles are meant for coordination of the components. The base class for ensembles is `ml_deeco.simulation.Ensemble`. Each ensemble has a priority specified by overriding the `priority` method. Furthermore, ensemble can contain components in static and dynamic roles. Static roles are represented simply as variables of the ensemble.

The declaration of a dynamic role is done via the `someOf` (meaning a list of components) or `oneOf` (single component) function with the component type as an argument. The components are assigned and re-assigned to the dynamic roles (we say that a component becomes a member of the ensemble) by the framework in every step of the simulation. To select the members for the role, several conditions can be specified using decorators:

* `select` is a predicate, which the component must pass to be picked;
* `utility` orders the components;
* `cardinality` sets the maximum (or both minimum and maximum) allowed number of components to be picked.

The member selection works by first finding all components of the correct type that pass the `select` predicate, then ordering them by the `utility` (higher utility is better) and using the `cardinality` to limit the number of selected members. The `cardinality` can also be used to limit the minimal number of member components &ndash; if there are not enough components passing the selection, the ensemble cannot be active at the time.

```py
from ml_deeco.simulation import Ensemble, someOf

class ChargingAssignment(Ensemble):
    # static role
    charger: Charger

    # dynamic role
    drones: List[Drone] = someOf(Drone)

    # we select those drones which need charging
    @drones.select
    def need_charging(self, drone, otherEnsembles):
        return drone.needs_charging

    # order them by the missing battery (so the drones with less battery are selected first)
    @drones.utility
    def missing_battery(self, drone):
        return 1 - drone.battery

    # and limit the cardinality to the number of free slots on the charger
    @drones.cardinality
    def free_slots(self):
        return 0, self.charger.free_slots

    def __init__(self, charger):
        super().__init__()
        self.charger = charger

    def actuate(self):
        # assign the charger to each drone -- it will start flying towards it to charge
        for drone in self.drones:
            drone.station = self.charger
```

The framework performs ensemble materialization (selection of the ensembles which should be active at this time) in every step of the simulation. The ensembles are materialized in a greedy fashion, ordered by their priority (descending). Only those ensembles for which all roles were assigned appropriate number of members (conforming to the cardinality) can be materialized. For all materialized ensembles, the `actuate` method is called.
