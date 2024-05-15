#include "AccelStepper.h"
#include "Vector.h"
AccelStepper base = AccelStepper(1,3,6);
AccelStepper extruder = AccelStepper(1,2,5);
int timeout_begin = 0;
// Array for stored commands
String commands[5] = {"None", "None", "None", "None", "None"};
int mode = 0; // 0 = waiting, 1 = fulfilling, 2 = base.runtoposition, 3 = base + extruder run, 4 = only speedmode for base
int current_index = 0;
String previous_input = "None";




void setup(){

  Serial.begin(9600);

  base.setMaxSpeed(100);
  base.setAcceleration(100);

  extruder.setMaxSpeed(100);
  extruder.setAcceleration(100);
  
}

void loop() {

  //read input and maybe attach it to the stack of commands
  read_input();


  //if currently not processing any command 
  if(mode == 0){

    //if command stack is not empty -> process command and set mode to 1
    if(commands[0] != "None"){
      mode = 1;
      process_command(commands[0]);
    }

  }

  
  //if currently procesing command only concerns base
  if(mode == 2) {
    
    if(base.distanceToGo() != 0){
      base.run();
      
    }else{
      mode = 0;
      base.setSpeed(0);
      base.setMaxSpeed(0);
      base.run();
      Serial.println("done:i" + String(current_index));
      shift_entries();
    }
    //timeout
    if(millis() - timeout_begin >= 15000)
      mode = 0;
      Serial.println("timeout");
  }

  //if(mode == 3 ){ base.run(); extruder.run();}

  if(mode == 4){
    base.run();

    //if command stack is not empty -> process command and set mode to 1
    if(commands[0] != "None"){
      mode = 1;
      process_command(commands[0]);
    }
  }

}

//shift entries to one in front
void shift_entries(){

  for(int i = 0; i<5-1; i++){
    commands[i] = commands[i+1];
  }
  commands[5] = "None";
}

//put new input at first entry that is not 'None'
void push_back(String input){

  for(int i = 0; i < 5; i++){

    if(commands[i] != "None"){
      commands[i] = input;
      return;
    }
    Serial.println("Stack Full!");
  }

}


//process any possible command
void process_command(String command){

  if(command.startsWith("init")) init_motors();

  if(command.startsWith("b")) turn_base(command);

  if(command.startsWith("e")) turn_extruder(command);

  if(command.startsWith("sb")) speed_base(command);
  
  if(command.startsWith("reset_base")) reset_base();

  if(command.startsWith("print")) print_stack();

  timeout_begin = millis();

}

//read input that is called every loop iteration
void read_input(){

  //read icoming text and transform it
  char buffer[32]; // Buffer to hold incoming data
  Serial.setTimeout(10);
  int length = Serial.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
  buffer[length] = '\0'; // Null-terminate the String
  String input = String(buffer);
  
  if(input != "" && input != previous_input){
    Serial.println("read: " + input);
    push_back(input);
    previous_input = input;
  }
}

// command that the base is turned
bool turn_base(String command){

  Serial.println("\n-Ackknowleged: base turning to position");

  int pIndex = command.indexOf('b');
  int sIndex = command.indexOf('s');
  int iIndex = command.indexOf('i');

  // Extract the position and speed from the command String
  String positionString = command.substring(pIndex + 1, sIndex);
  String speedString = command.substring(sIndex + 1,iIndex);
  String indexString = command.substring(iIndex + 1);

  // Convert the position and speed to integers
  int position = positionString.toInt();
  int speed = speedString.toInt();
  int index = indexString.toInt();

 

  // calculate the number of steps required to move the specified distance
  float distanceInDeg = position;
  float degPerStep = 1.8; // Adjust this value based on your stepper motor specifications
  int steps = distanceInDeg / degPerStep;

  //set mode
  mode = 2;

  base.moveTo(steps);
  base.setMaxSpeed(speed);
  base.setSpeed(speed);
  current_index = index;

}

//command that the extruder is turned
bool turn_extruder(String command){}


void print_stack(){

  String output = "";
  for(int i = 0; i< 5; i++){
    output += commands[i] + " ; ";
  }

  Serial.println(output);

}
// only let the base turn with speed
bool speed_base(String command){

  Serial.println("\n-Ackknowleged: base turning at speed");
  int sIndex = command.indexOf('s');
  

  // Extract the position and speed from the command String
  
  String speedString = command.substring(sIndex + 1);
 

  // Convert the position and speed to integers
  
  int speed = speedString.toInt();
  

  Serial.println("ack_s");
  base.setMaxSpeed(1000);
  base.setSpeed(speed);
  base.run();
  mode = 4;
  
}


bool timeout_check(){}


bool reset_base(){


  base.setCurrentPosition(0);
  Serial.println("position reset");
}

bool init_motors(){

    Serial.println("\n-Ackknowleged: Motor initialization");
    base.setMaxSpeed(100);
    base.setSpeed(500);
    unsigned long startTime = millis();
    unsigned long duration = 1000; // 3 seconds
    while (millis() - startTime < duration) {
        base.runSpeed();
    }
    base.setSpeed(-1000);
    startTime = millis();
    duration = 1000; // 3 seconds
    while (millis() - startTime < duration) {
        base.runSpeed();
    }
    base.setSpeed(0);
    Serial.println("Stepper initialized");
    Serial.println("done");

    reset_base();

}