model MassRight
  Modelica.Mechanics.Translational.Components.Fixed fixed annotation(
    Placement(visible = true, transformation(origin = {80, 0}, extent = {{10, -10}, {-10, 10}}, rotation = 90)));
  Modelica.Mechanics.Translational.Components.Spring spring2(c = 4*3.1416*3.1416, s_rel(fixed = false), s_rel0 = 0) annotation(
    Placement(visible = true, transformation(origin = {56, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Mass mass2(L = 0, m = 1, s(fixed = true, start = 1), v(displayUnit = "Gm/s", fixed = true, start = 0)) annotation(
    Placement(visible = true, transformation(origin = {26, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Components.Spring spring12(c = 16*3.1316*3.1416) annotation(
    Placement(visible = true, transformation(origin = {-6, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Translational.Sources.Position position(exact = false, v(fixed = true, start = 0))  annotation(
    Placement(visible = true, transformation(origin = {-46, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput u annotation(
    Placement(visible = true, transformation(origin = {-86, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-86, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
equation
  connect(spring2.flange_b, fixed.flange) annotation(
    Line(points = {{66, 0}, {80, 0}}, color = {0, 127, 0}));
  connect(mass2.flange_b, spring2.flange_a) annotation(
    Line(points = {{36, 0}, {46, 0}}, color = {0, 127, 0}));
  connect(spring12.flange_b, mass2.flange_a) annotation(
    Line(points = {{4, 0}, {16, 0}}, color = {0, 127, 0}));
  connect(u, position.s_ref) annotation(
    Line(points = {{-86, 0}, {-58, 0}}, color = {0, 0, 127}));
  connect(position.flange, spring12.flange_a) annotation(
    Line(points = {{-36, 0}, {-16, 0}}, color = {0, 127, 0}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end MassRight;