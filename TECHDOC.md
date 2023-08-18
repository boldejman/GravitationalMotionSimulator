# Technical documentation
Hello world! This is my python semester project for MFF UK. This is the gravitational motion simulator that use numerical methods to calculate the trajectory in gravitation field. 

## Architecture
The whole project was separated into four modules: UI, mode, simulation and units. Each module is tightly connected to each other (unfortunately), but performs its own function.
### UI
User Interface module contains main functionality logic of the simulator. 
#### Attrs:
1. screen: pygame display
2. clock: pygame attr. uses for settinf fps.
3. mouse: pygame attr. has position and type of click.
4. event: pygame attr. contains all events of each frame.
5. running: if True, then simulator is running.
6. planets: list of current planet on the playing screen.
7. planetDispositionCheck: If true, then a new planet is planned to be added.
8. ship: ship.
9. shipDispositionCheck: same as the 7. for the ship.
10. shipVelocityCheck: similar to the previous point.
11. velCoef: needs to regulate the velocity of the ship.
12. backgroundImage: background image.
13. menu: Menu class object.
14. simulation: Simulation class object.
15. simulationManager: SimulationManager class object.
16. currentMode: current mode.
17. currentUnit: current unit for Drag-n-Drop alg.
18. units: list of units for Drag-n-Drop.

#### Methods:
1. run: main loop.
2. update: updates mouse and events.
3. processInput: handles events.
4. checkPlanet: Checks if a new planet can be added. Need to set a mass of new unit.
5. checkShip: same as the 4. for ship.
6. launchSimulator: sets all units, accuracy and tMax and launch the simulator.
7. simulationCanBeStarted: checks if the simulation can be started(obviously)
8. setSettingMode: setter for currentMode attr.
9. reset: handles the reset button on the menu.
10. stopPlaying: handles the stop button on the menu.
11. quit: quits from the app.
12. setSimulationMode: setter for currentMode attr.

### mode
Mode is file, that contains 2 submodules: menu and simulationManager.
Menu is module that render handle all menu buttons, text input plates and notifying window.
#### Menu attrs:
1. ui: UI class object.
2. running: same as running in UI.
3. notifyingWindow: Notifying window class object. Displays all notifications.
4. menuButtons: list, that contains all buttons.
5. menuTextInput: list, that contains all text input plates.
6. mouse: same as in UI.
7. font: font for all text.
8. events: same as in UI.
9. currentTextInput: index of current text input plate.
10. planetMassIsChosen: bool, that needs to Drag-n-Drop.
11. shipMassIsChosen: same as the 10.

#### Menu methods:
1. update: synchronize mouse and events attributes with UI and do some else.
2. processInput: handles events
3. render: renders all plates, buttons atc.

#### Button attrs:
1. leftUp: upper left corner.
2. title: name of the button.
3. action: function.
4. font: font.

#### Button methods:
1. contains: dunder method.
2. render: renders button.

#### NotifyingWindow attrs:
1. lu: upper left corner.
2. text: text on the plate.
3. font: font.

#### NotifyingWindow methods:
1. render: renders notifying window.

#### TextInputPlate attrs:
1. hasDefaultValue: bool for accuracy anb tMax.
2. name: name of the plate.
3. leftUp: upper left corner of the button.
4. digitCounter: -||-
5. textFont: -||-
6. fontObject: TextInputVisualizer attr.
7. isCurrent: -||-

#### TextInputPlate methods:
1. contains: dunder method.
2. render: renders text input plate.

SimulatorManger is module, that renders units and trace dots on playing window.

#### SimulatorManger attrs:
1. ui: UI class object.
2. simulation: Simulation class object.
3. positions: list of coordinates pairs.
4. playingProgress: index of the positions attribute.
5. ship: ship.
6. planets: planets.
7. dotTraceImage: trace dot image.
8. trace: list of trace dots positions.
9. mouse: pygame attribute.
10. currentUnit: attribute, that needs to drag-n-Drop.

#### SimulatorManger methods:
1. runSimulating: checks if acc. and tMax are comform.
2. getShipPos: getter for ship positions and angles. if simulation ends, then return the last position and angle.
3. update: updates mouse atc.
4. render: renders all units at setting and simulation/stop modes.

### Simulation
This is the main simulation module. Moving of the ship is perform by numerical calculations of 2. order ODE for Newton`s gravitation law mx'' = G*m_ship*(SUM(mass_planet)/R_ship_planet^2). Here I`m using the Runge-Kutta Algorithm for this calculations.

#### Simulation attrs:
1. ship: ship.
2. tmax: playing time.
3. planets: list of planets.
4. gravConst: Gravitaion constant for the formula.
5. accuracy: accuracy.

#### Simulation methods:
1. rightSide: calculates for given parameters the right side of ode. here the main ode separated into 4 1. order odes.
2. rungeKutta: numerical method.
3. getPositions: getter for positions of the ship. activates Runge-Kutta method.

### Units
This module contains two types of units: Ship and Planet.

#### Ship attrs:
1. x, y: coordinates.
2. coord: pair of coordinates.
3. mass: mass of the ship.
4. vel: coordinate pair of velosity vector.
5. dragging: needs to Drag-n-Drop alg.
6. offsetX, offsetY: needs to Drag-n-Drop alg.
7. shipImage: ship image.
8. size: image size.
9. dragged: needs to Drag-n-Drop alg.

#### Ship methods:
1. contains: dunder method.
2. setMass: setter for ship mass.
3. setOffset: setter for Drag-n-Drop.
4. drag: -||-
5. render: renders ship.

#### Planet attrs:
1. name: name of the planet.
2. x, y: coordinates.
3. coord: pair of coordinates.
4. mass: mass of the planet.
5. dragging: same as 5. in Ship attrs.
6. offsetX, offsetY: -||-
7. planetImage: planet image.
8. size: image size.
9. dragged: -||-

#### Planet methods:
1. repr: dunder method.
2. contains: dunder method:
3. setMass: setter for planet mass.
4. setOffset, drag: -||-
5. render: renders planet.

#### Static functions:
1. blitRotate: needs to rotate ship sprite.

