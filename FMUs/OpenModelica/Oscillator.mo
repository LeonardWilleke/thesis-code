model Oscillator
  Modelica.Mechanics.Translational.Components.Fixed fixed annotation(
    Placement(visible = true, transformation(origin = {-76, 0}, extent = {{-10, -10}, {10, 10}}, rotation = -90)));
  Modelica.Mechanics.Translational.Components.Spring spring(c = 4*3.1416*3.1416, s_rel(fixed = false), s_rel0 = 0)  annotation(
    Placement(visible = true, transformation(origin = {-54, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Mass mass( L(displayUnit = "km"),a(start = 0), m = 1, s(fixed = true, start = 1), v(fixed = true, start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-22, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Spring spring1(c = 16*3.1416*3.1416, s_rel(fixed = false), s_rel0 = 0)  annotation(
    Placement(visible = true, transformation(origin = {8, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Mass mass1( m = 1, s(fixed = true, start = 0), v(fixed = true, start = 0))  annotation(
    Placement(visible = true, transformation(origin = {34, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Spring spring2(c = 4*3.1416*3.1416, s_rel(fixed = false), s_rel0 = 0)  annotation(
    Placement(visible = true, transformation(origin = {62, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Fixed fixed1 annotation(
    Placement(visible = true, transformation(origin = {82, 0}, extent = {{10, -10}, {-10, 10}}, rotation = 90)));
equation
  connect(fixed.flange, spring.flange_a) annotation(
    Line(points = {{-76, 0}, {-64, 0}}, color = {0, 127, 0}));
  connect(spring.flange_b, mass.flange_a) annotation(
    Line(points = {{-44, 0}, {-32, 0}}, color = {0, 127, 0}));
  connect(spring1.flange_a, mass.flange_b) annotation(
    Line(points = {{-2, 0}, {-12, 0}}, color = {0, 127, 0}));
  connect(mass1.flange_a, spring1.flange_b) annotation(
    Line(points = {{24, 0}, {18, 0}}, color = {0, 127, 0}));
  connect(mass1.flange_b, spring2.flange_a) annotation(
    Line(points = {{44, 0}, {52, 0}}, color = {0, 127, 0}));
  connect(spring2.flange_b, fixed1.flange) annotation(
    Line(points = {{72, 0}, {82, 0}}, color = {0, 127, 0}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end Oscillator;