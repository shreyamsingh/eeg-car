/*
 * 
 Created 8/1/20016
 by Abdel-Razzak Merheb
 Controls a remote control car via serial port

 Pins 10, 11, 12, and 13 are used to control the car


 The circuit:
 * The remote controller is connected to pins 10, 11, 12, and 13
 * Arduino UNO is used
 * The remote takes its vcc and GND from the Arduino board
 * Note: on most Arduinos there is already an LED on the board
 attached to pin 13.
 */

// constants won't change. They're used here to
// set pin numbers:
const int UpPin =  11;      // The pin used to control the forward move
const int DwnPin =  10;      // The pin used to control the backward move
const int RghtPin =  13;      // The pin used to control the right move
const int LftPin =  12;      // The pin used to control the left move
bool forward = false;
bool backward = false;
bool left = false;
bool right = false;

int CommandByte = 0;   // Command received via serial port

// Initialize pins
void setup() {
// sets the digital pins as output  
pinMode(UpPin, OUTPUT); 
pinMode(DwnPin, OUTPUT); 
pinMode(RghtPin, OUTPUT); 
pinMode(LftPin, OUTPUT);      

// Initialize serial port
Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

// Repeat
void loop() {
// Whenever a byte is received via serial port
if (Serial.available() > 0) 
    {
      // Read the incoming byte:
      long clocktime = millis();
      CommandByte = Serial.read();
      // Perform the commands

      // Forward command is received
      if (CommandByte == 'f') 
        {
          // First be sure that Down button (go back) is unpressed, then send forward command
          digitalWrite(DwnPin, LOW);  // Stop backward
          backward = false;
          // Don't turn
          digitalWrite(LftPin, LOW); // stop left
          digitalWrite(RghtPin, LOW); // stop right
          left = false;
          right = false;
          // Move forward
          digitalWrite(UpPin, HIGH); // Go forward
          forward = true;
          Serial.print('f' + clocktime);
        }

          // Backward command is received
            if (CommandByte == 'b') 
        {
          // First be sure that Up button (go forward) is unpressed, then send backward command
          digitalWrite(UpPin, LOW); // Stop forward
          forward = false;
          // Don't turn
          digitalWrite(LftPin, LOW); // stop left
          digitalWrite(RghtPin, LOW); // stop right
          left = false;
          right = false;
          // Move backward
          digitalWrite(DwnPin, HIGH); // Go backward
          backward = true;
        }

         // Go right command is received
            if (CommandByte == 'r') 
        {
          // Stop left
          digitalWrite(LftPin, LOW);
          left = false;
          // If not already moving, go forward & right
          if (!backward && !forward){
            digitalWrite(UpPin, HIGH);
            digitalWrite(RghtPin, HIGH);
            forward = true;
            right = true;
          }
          // If already moving, turn wheels right
          else{
            digitalWrite(RghtPin, HIGH);
            right = true;
          }
        }

        // Go left command is received
            if (CommandByte == 'l') 
        {
          // Stop right
          digitalWrite(RghtPin, LOW);
          right = false;
          // If not already moving, go forward and left
          if (!backward && !forward){
            digitalWrite(UpPin, HIGH);
            digitalWrite(LftPin, HIGH);
            forward = true;
            left = true;
          }
          // If already moving, turn wheels left
          else{
            digitalWrite(LftPin, HIGH);
            left = true;
          }
        }


        // Stop command is received
            if (CommandByte == 's') 
        {
          // Stop everything
          digitalWrite(UpPin, LOW); // Stop forward
          digitalWrite(DwnPin, LOW); // Stop backward
          digitalWrite(RghtPin, LOW); // Stop turning right
          digitalWrite(LftPin, LOW); // Stop turning left
          forward = false;
          backward = false;
          left = false;
          right = false;
          
        }        

       delay(1000);                  // waits for a second
    }
}
