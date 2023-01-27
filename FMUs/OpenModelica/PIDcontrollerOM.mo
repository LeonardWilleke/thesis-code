model PIDcontrollerOM
  Modelica.Blocks.Continuous.PID pid( Ti = 10, k = 10)  annotation(
    Placement(visible = true, transformation(origin = {0, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput u annotation(
    Placement(visible = true, transformation(origin = {-50, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-50, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput y annotation(
    Placement(visible = true, transformation(origin = {56, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {56, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(pid.u, u) annotation(
    Line(points = {{-12, 0}, {-50, 0}}, color = {0, 0, 127}));
  connect(pid.y, y) annotation(
    Line(points = {{12, 0}, {56, 0}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")));
end PIDcontrollerOM;