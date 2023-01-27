model FeedBack
  Modelica.Blocks.Continuous.PID pid(Td = 0, Ti = 10, k = 1)  annotation(
    Placement(visible = true, transformation(origin = {8, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.SecondOrder secondOrder(D = 0.7, k = 2, w = 1)  annotation(
    Placement(visible = true, transformation(origin = {60, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.Feedback feedback annotation(
    Placement(visible = true, transformation(origin = {-28, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Step step(height = 1)  annotation(
    Placement(visible = true, transformation(origin = {-74, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput y annotation(
    Placement(visible = true, transformation(origin = {104, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {100, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(secondOrder.u, pid.y) annotation(
    Line(points = {{48, 0}, {20, 0}}, color = {0, 0, 127}));
  connect(pid.u, feedback.y) annotation(
    Line(points = {{-4, 0}, {-18, 0}}, color = {0, 0, 127}));
  connect(step.y, feedback.u1) annotation(
    Line(points = {{-62, 0}, {-36, 0}}, color = {0, 0, 127}));
  connect(secondOrder.y, feedback.u2) annotation(
    Line(points = {{72, 0}, {-28, 0}, {-28, -8}}, color = {0, 0, 127}));
  connect(secondOrder.y, feedback.u2) annotation(
    Line(points = {{72, 0}, {82, 0}, {82, -50}, {-28, -50}, {-28, -8}}, color = {0, 0, 127}));
  connect(secondOrder.y, y) annotation(
    Line(points = {{72, 0}, {104, 0}}, color = {0, 0, 127}));

annotation(
    uses(Modelica(version = "4.0.0")),
    experiment(StartTime = 0, StopTime = 50, Tolerance = 1e-6, Interval = 0.1));
end FeedBack;