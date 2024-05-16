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
int j = 0;
int max_base_speed = 100000;
int previous_base_pos = 0;



void setup(){

  Serial.begin(9600);

  base.setMaxSpeed(max_base_speed);
  base.setAcceleration(50000);

  extruder.setMaxSpeed(100);
  extruder.setAcceleration(50000);
  
}

void loop() {
  j++;
  //read input and maybe attach it to the stack of commands
  read_input();

  //if currently not processing any command 
  if(mode == 0){
    
    //Serial.println("mode is 0");
    //if command stack is not empty -> process command and set mode to 1
    if(commands[0] != "None"){
      Serial.println("command in the queue");
      mode = 1;
      process_command(commands[0]);
    }
  }
  
  //if currently procesing command only concerns base
  if(mode == 2) {
    if(abs(base.distanceToGo()) >= 1){
      base.runSpeed();
    }else{
      mode = 0;
      Serial.println("mode set to 0 again");
      base.setSpeed(0);
      base.setMaxSpeed(max_base_speed);
      base.runSpeed();
      Serial.println("done:i" + String(current_index));
      //base.setCurrentPosition(0);
    }
  }

  //if(mode == 3 ){ base.run(); extruder.run();}

  if(mode == 4){
    base.runSpeed();
    //Serial.println("currently running base in mode 4");
    //if command stack is not empty -> process command and set mode to 0
    if(commands[0] != "None"){
      mode = 0;
      Serial.println("speed only overriden by different command");
    }
  }

}


//read input that is called every loop iteration
void read_input(){
  
  //read icoming text and transform it
  char buffer[32]; // Buffer to hold incoming data
  Serial.setTimeout(10);
  int length = Serial.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
  buffer[length] = '\0'; // Null-terminate the String
  String input = String(buffer);

  if(input.startsWith("print")){
    print_stack();
    return;
  }
  
  if(input != "" && input != previous_input){
    Serial.println("read: " + input);
    push_back(input);
    previous_input = input;
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
  if(commands[4] != "None"){
    Serial.println("Stack Full");
    return;
  }

  for(int i = 0; i < 5; i++){

    if(commands[i] == "None"){
      commands[i] = input;
      return;
    }
  }
}


//process any possible command
void process_command(String command){

  if(command.startsWith("init"))
    {init_motors();}
  else if(command.startsWith("b"))
    { turn_base(command);}
  else if(command.startsWith("e"))
    { turn_extruder(command);}
  else if(command.startsWith("sb"))
    { speed_base(command);}
  else if(command.startsWith("reset_base"))
    { reset_base();}
  else
  {Serial.println("Invalid command");
    mode = 0;
     }

  shift_entries();
  timeout_begin = millis();

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

  if(position-previous_base_pos <= 0){
    speed = speed *(-1);
  }
  // calculate the number of steps required to move the specified distance
  float distanceInDeg = position;
  float degPerStep = 1.8/16; // Adjust this value based on your stepper motor specifications
  int steps = distanceInDeg / degPerStep;

  //set mode
  mode = 2;

  base.moveTo(steps);
  base.setMaxSpeed(max_base_speed);
  base.setSpeed(speed);
  current_index = index;
  previous_base_pos = position;

}

//command that the extruder is turned
bool turn_extruder(String command){
  Serial.println("theoretical turning of extruder");
  mode = 0;
}


void print_stack(){

  String output = "";
  for(int i = 0; i< 5; i++){
    output += commands[i] + " ; ";
  }
  Serial.println("previous position: " + String(previous_base_pos));
  Serial.println(output);

}

// only let the base turn with speed
bool speed_base(String command){

  Serial.println("\n-Acknowleged: base turning at speed");

  // Extract the position and speed from the command String
  int speed = command.substring(2).toInt();
  Serial.println("speed is" + String(speed));
  base.setMaxSpeed(max_base_speed);
  base.setSpeed(speed);
  base.runSpeed();
  mode = 4;
  
}


bool timeout_check(){}


bool reset_base(){

  for(int i = 0; i < 5; i++){
    commands[i] = "None";

  }
  base.setCurrentPosition(0);
  Serial.println("position reset");
  mode = 0;
}

bool init_motors(){

    Serial.println("\n-Ackknowleged: Motor initialization");
    base.setMaxSpeed(100000);
    base.setSpeed(600);
    unsigned long startTime = millis();
    unsigned long duration = 1000; // 3 seconds
    while (millis() - startTime < duration) {
        base.runSpeed();
    }
    base.setSpeed(-600);
    startTime = millis();
    duration = 1000; // 3 seconds
    while (millis() - startTime < duration) {
        base.runSpeed();
    }
    base.setSpeed(0);
    Serial.println("Stepper initialized");
    Serial.println("done");

    reset_base();

    mode = 0;
}