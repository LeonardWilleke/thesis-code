model MassLeft
  Modelica.Mechanics.Translational.Components.Spring spring1(c = 4*3.1416*3.1416, s_rel(fixed = false))  annotation(
    Placement(visible = true, transformation(origin = {-50, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Mass mass1(L = 0, m = 1, s(fixed = true, start = 1), v(fixed = true, start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-10, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Fixed fixed annotation(
    Placement(visible = true, transformation(origin = {-80, 0}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Mechanics.Translational.Components.Spring spring12(c = 16*3.1316*3.1416) annotation(
    Placement(visible = true, transformation(origin = {28, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(mass1.flange_a, spring1.flange_b) annotation(
    Line(points = {{-20, 0}, {-40, 0}}, color = {0, 127, 0}));
  connect(fixed.flange, spring1.flange_a) annotation(
    Line(points = {{-80, 0}, {-60, 0}}, color = {0, 127, 0}));
  connect(spring12.flange_a, mass1.flange_b) annotation(
    Line(points = {{18, 0}, {0, 0}}, color = {0, 127, 0}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end MassLeft;