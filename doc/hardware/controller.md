
## Controller Frequency
The communications frequency between the ehterCAT master - i.e. your PC - and the joint controller is 1 kHz. That is the EtherCAT update rate with which you can call the setJointData - functions.

The Timmings/Control Loop Performance - i.e. the frequency with which the controller calculates the next value for the PID regulator is as follows

- for position control: 1 kHz
- for velocity control: 1 kHz
- for current control:  10 kHz
