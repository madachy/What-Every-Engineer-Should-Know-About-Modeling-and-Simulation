def Runge_Kutta(x, v, a, dt):
    """Runge-Kutta integration function returns final (position, velocity) tuple after
    time dt has passed.  Implements fourth order Runge-Kutta method.

    x: initial position
    v: initial velocity 
    a: acceleration function a(x,v,dt)
    dt: timestep"""
    x1 = x
    v1 = v
    a1 = a(x1, v1, 0)

    x2 = x + 0.5*v1*dt
    v2 = v + 0.5*a1*dt
    a2 = a(x2, v2, dt/2.0)

    x3 = x + 0.5*v2*dt
    v3 = v + 0.5*a2*dt
    a3 = a(x3, v3, dt/2.0)

    x4 = x + v3*dt
    v4 = v + a3*dt
    a4 = a(x4, v4, dt)

    xf = x + (dt/6.0)*(v1 + 2*v2 + 2*v3 + v4)
    vf = v + (dt/6.0)*(a1 + 2*a2 + 2*a3 + a4)
    return xf, vf

def accel(x, v, dt):
    """Determines acceleration from current position,
    velocity, and timestep. This acceleration
    function models a spring."""
    stiffness = 1
    damping = -0.005
    return -stiffness*x - damping*v

t = 0
dt = 1.25 # Timestep in seconds
state = 50, 5 # Position, velocity

print ("Initial position: %6.2f, Velocity: %6.2f" % state)

# label for time loop output
print ("  time  position velocity")

# Run for 10 seconds
while t < 10:
    t += dt
    state = Runge_Kutta(state[0], state[1], accel, dt)

    #print (t, state[0], state[1])
    print ("%6.2f %6.2f %6.2f" % (t, state[0], state[1]))

print ("Final position: %6.2f, velocity: %6.2f" % state)
