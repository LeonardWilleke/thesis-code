model MassLeft
  Modelica.Mechanics.Translational.Components.Spring spring1(c = 4*3.1416*3.1416, s_rel(fixed = false))  annotation(
    Placement(visible = true, transformation(origin = {-50, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Mass mass1(L = 0, m = 1, s(fixed = true, start = 1), v(fixed = true, start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-10, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Fixed fixed annotation(
    Placement(visible = true, transformation(origin = {-80, 0}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Blocks.Sources.Sine sine annotation(
    Placement(visible = true, transformation(origin = {0, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Sources.Force force annotation(
    Placement(visible = true, transformation(origin = {54, -28}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(mass1.flange_a, spring1.flange_b) annotation(
    Line(points = {{-20, 0}, {-40, 0}}, color = {0, 127, 0}));
  connect(fixed.flange, spring1.flange_a) annotation(
    Line(points = {{-80, 0}, {-60, 0}}, color = {0, 127, 0}));
  connect(force.flange, mass1.flange_b) annotation(
    Line(points = {{64, -28}, {30, -28}, {30, 0}, {0, 0}}, color = {0, 127, 0}));
  connect(sine.y, force.f) annotation(
    Line(points = {{12, -40}, {42, -40}, {42, -28}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end MassLeft;