model MassLeft
  Modelica.Mechanics.Translational.Components.Spring spring1(c = 4*3.1416*3.1416, s_rel(fixed = false))  annotation(
    Placement(visible = true, transformation(origin = {-58, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Mass mass1(L = 0, m = 1, s(fixed = true, start = 1), v(fixed = true, start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-22, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Fixed fixed annotation(
    Placement(visible = true, transformation(origin = {-80, 0}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Mechanics.Translational.Components.GeneralForceToPositionAdaptor forceToPositionAdaptor(use_pder = false, use_pder2 = false)  annotation(
    Placement(visible = true, transformation(origin = {10, 1}, extent = {{-26, -11}, {26, 11}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput displacement annotation(
    Placement(visible = true, transformation(origin = {62, 10}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {62, 12}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput force annotation(
    Placement(visible = true, transformation(origin = {62, -8}, extent = {{12, -12}, {-12, 12}}, rotation = 0), iconTransformation(origin = {56, -32}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
equation
  connect(mass1.flange_a, spring1.flange_b) annotation(
    Line(points = {{-32, 0}, {-48, 0}}, color = {0, 127, 0}));
  connect(fixed.flange, spring1.flange_a) annotation(
    Line(points = {{-80, 0}, {-68, 0}}, color = {0, 127, 0}));
  connect(forceToPositionAdaptor.flange, mass1.flange_b) annotation(
    Line(points = {{5, 1}, {-3.5, 1}, {-3.5, 0}, {-12, 0}}, color = {0, 127, 0}));
  connect(forceToPositionAdaptor.p, displacement) annotation(
    Line(points = {{18, 10}, {62, 10}}, color = {0, 0, 127}));
  connect(forceToPositionAdaptor.f, force) annotation(
    Line(points = {{18, -8}, {62, -8}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")),
    experiment(StartTime = 0, StopTime = 1, Tolerance = 1e-6, Interval = 0.002),
    __OpenModelica_simulationFlags(lv = "LOG_STATS", s = "trapezoid"));
end MassLeft;