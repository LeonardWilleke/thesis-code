model MassLeft
  Modelica.Mechanics.Translational.Components.Spring spring1(c = 4*3.1416*3.1416, s_rel(fixed = false))  annotation(
    Placement(visible = true, transformation(origin = {-58, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Mass mass1(L = 0, m = 1, s(fixed = true, start = 1), v(fixed = true, start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-22, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Fixed fixed annotation(
    Placement(visible = true, transformation(origin = {-80, 0}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Interfaces.RealOutput y annotation(
    Placement(visible = true, transformation(origin = {58, 10}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {72, 44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.GeneralForceToPositionAdaptor forceToPositionAdaptor(use_pder = false, use_pder2 = false)  annotation(
    Placement(visible = true, transformation(origin = {9, 7.10543e-15}, extent = {{-25, -12}, {25, 12}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput u annotation(
    Placement(visible = true, transformation(origin = {62, -10}, extent = {{16, -16}, {-16, 16}}, rotation = 0), iconTransformation(origin = {54, -8}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
equation
  connect(mass1.flange_a, spring1.flange_b) annotation(
    Line(points = {{-32, 0}, {-48, 0}}, color = {0, 127, 0}));
  connect(fixed.flange, spring1.flange_a) annotation(
    Line(points = {{-80, 0}, {-68, 0}}, color = {0, 127, 0}));
  connect(forceToPositionAdaptor.flange, mass1.flange_b) annotation(
    Line(points = {{4, 0}, {-12, 0}}, color = {0, 127, 0}));
  connect(forceToPositionAdaptor.p, y) annotation(
    Line(points = {{16, 10}, {58, 10}}, color = {0, 0, 127}));
  connect(u, forceToPositionAdaptor.f) annotation(
    Line(points = {{62, -10}, {16, -10}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end MassLeft;