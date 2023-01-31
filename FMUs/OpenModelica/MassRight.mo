model MassRight
  Modelica.Mechanics.Translational.Components.Fixed fixed annotation(
    Placement(visible = true, transformation(origin = {80, 0}, extent = {{10, -10}, {-10, 10}}, rotation = 90)));
  Modelica.Mechanics.Translational.Components.Spring spring2(c = 4*3.1416*3.1416, s_rel(fixed = false), s_rel0 = 0) annotation(
    Placement(visible = true, transformation(origin = {62, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Mass mass2(L = 0, m = 1, s(fixed = true, start = 1), v(displayUnit = "Gm/s", fixed = true, start = 0)) annotation(
    Placement(visible = true, transformation(origin = {32, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Spring spring12(c = 16*3.1316*3.1416, s_rel0 = 0) annotation(
    Placement(visible = true, transformation(origin = {-2, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.GeneralPositionToForceAdaptor positionToForceAdaptor(use_pder = false, use_pder2 = false)  annotation(
    Placement(visible = true, transformation(origin = {-36, 0}, extent = {{32, -16}, {-32, 16}}, rotation = 180)));
  Modelica.Blocks.Interfaces.RealInput displacement annotation(
    Placement(visible = true, transformation(origin = {-90, -12}, extent = {{-14, -14}, {14, 14}}, rotation = 0), iconTransformation(origin = {-62, -48}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput force annotation(
    Placement(visible = true, transformation(origin = {-93, 13}, extent = {{13, -13}, {-13, 13}}, rotation = 0), iconTransformation(origin = {-64, 32}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(spring2.flange_b, fixed.flange) annotation(
    Line(points = {{72, 0}, {80, 0}}, color = {0, 127, 0}));
  connect(mass2.flange_b, spring2.flange_a) annotation(
    Line(points = {{42, 0}, {52, 0}}, color = {0, 127, 0}));
  connect(spring12.flange_b, mass2.flange_a) annotation(
    Line(points = {{8, 0}, {22, 0}}, color = {0, 127, 0}));
  connect(positionToForceAdaptor.flange, spring12.flange_a) annotation(
    Line(points = {{-30, 0}, {-12, 0}}, color = {0, 127, 0}));
  connect(force, positionToForceAdaptor.f) annotation(
    Line(points = {{-93, 13}, {-46, 13}, {-46, 12}}, color = {0, 0, 127}));
  connect(displacement, positionToForceAdaptor.p) annotation(
    Line(points = {{-90, -12}, {-46, -12}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")),
    experiment(StartTime = 0, StopTime = 1, Tolerance = 1e-6, Interval = 0.002),
    __OpenModelica_simulationFlags(lv = "LOG_STATS", s = "trapezoid"));
end MassRight;