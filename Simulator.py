"""
Simulation assumptions:
No tire deformation
Fixed Diameter wheel (OutsideDimater)
Constant forward velocity - if someone decides to relate Vx to the rebound time it should be able to be subbed in for Vx
"""
import sys, math
import matplotlib.pyplot as plt

def shaftFromAngleY(angle,Y): # Return the shaft property from the headtube angle and the Vertical property
    if angle > 1.5:
        angle=math.radians(angle)
        print(angle)
    shaft = Y/math.sin(angle)
    return shaft
def pythagA(one,two): #return A from A^2+B^2=C^2
    if one > two:
        C=one
        B=two
    elif two > one:
        C=two
        B=one
    A=math.sqrt(C**2-B**2)
    return A
def pythagC(A,B): #return C from A^2+B^2=C^2
    C=math.sqrt(A**2+B**2)
    return C
def inchesToM(inches): #convert inches to meters
    meters=inches*.0254
    return meters

def main():
    Vs = 0 #ShaftVelocity in m/s
    Aht = math.radians(70) #head tube angle in degrees converted to radians
    Dw = 29+2.2 #radius of wheel in inches
    Hb = 3 #Height of bump in inches
    Vx = 5 #forward velocity in m/s
    ThetaDot = 0 #degrees per second the wheel center travels to get over the bump
    As = 0 #Acceleration of the shaft

    Hb = inchesToM(Hb)
    Dw = inchesToM(Dw) #convert to meters
    Rw=Dw/2 #radius from diameter

    #find the distance required to clear the disturbance given a wheel diameter (only factor)
    disturbanceX=pythagA(Rw,Rw-Hb)

    VsData=[]
    AsData=[]
    x_data=[]

    X=disturbanceX
    xOld=X+.001
    VsOld=0
    while X > 0:
        #where in the arc of rolling over the disturbance as a function of X distance
        theta=math.radians(90)-math.acos(X/Rw)

        #Vertical component of wheel velocity from a given angle
        #Here we assume Vx is constant but should probably relate it to X
        Vy=math.tan(theta)*Vx

        # Given a position and forward velocity this gives Shaft Velocity
        Vs = shaftFromAngleY(Aht,Vy)

        #saving velocity and position in travel
        VsData.append(Vs)
        x_data.append(X)

        #Find the time traveled in last iteration based on Vx
        dT=(xOld-X)/Vx

        #change in velocity
        dV=VsOld-Vs

        #acceleration between this point and last
        As=dV/dT

        #saing acceleration data
        AsData.append(As)

        #Save points for change calcs and move forward 1mm
        VsOld=Vs
        xOld=X
        X-=.001

    plt.figure(1)
    plt.subplot(211)
    plt.plot(x_data,AsData[::-1])
    plt.axis([0, disturbanceX+.001, 0, 140])

    plt.subplot(212)
    plt.plot(x_data,VsData[::-1])
    plt.show()

    #As = (math.tan(ThetaDot)Vx)/math.sin(Aht)
    # Given a velocity you should get a acceleration?

    #As = (math.tan((math.acos((Rw-Hb)/Rw)Vx)/(math.sqrt(Rw^2-(Rw-Hb)^2)))Vx)/math.sin(Aht)
    # Relate ThetaDot to the current location in the bump travel and you get shaft acceleration @ a point, this goes from the height of the bump to zero

    #Vs = (math.tan(math.acos((Rw-Hb)/Rw))Vx)/math.sin(Aht)
    #Graph Hb from Hb inital to 0 and you can get a Shaft velocity graph

main()
