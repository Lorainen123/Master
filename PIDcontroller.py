from simple_pid import PID

pid = PID(1, 0.1, 0.05, setpoint=1)
pid.sample_time = 0.01 
pid.setpoint = 10
pid.tunings = (1.0, 0.2, 0.4) #ki,Ti,Td
pid.output_limits = (0, 10)

while True:

  control = pid(9) # The PID class implements __call__(), which means that to compute a new output value
